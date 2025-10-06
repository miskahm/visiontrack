import time
from pathlib import Path

import cv2
import numpy as np
import streamlit as st

from src.detection_agent import DetectionAgent
from src.label_agent import LabelAgent
from src.logging_agent import LoggingAgent
from src.model_manager_agent import ModelManagerAgent
from src.tracking_agent import TrackingAgent


@st.cache_resource
def load_model():
    model_manager = ModelManagerAgent()
    with st.spinner("Loading YOLO model... (this only happens once)"):
        model_manager.load_model()
    return model_manager


def initialize_agents():
    if "initialized" not in st.session_state:
        st.session_state.model_manager = load_model()

        st.session_state.detection_agent = DetectionAgent(
            model_path=st.session_state.model_manager.model_name,
            confidence_threshold=st.session_state.model_manager.get_config_value(
                "model.confidence_threshold", 0.5
            ),
        )
        st.session_state.detection_agent.model = (
            st.session_state.model_manager.get_model()
        )

        st.session_state.tracking_agent = TrackingAgent(
            max_age=st.session_state.model_manager.get_config_value(
                "tracking.max_age", 30
            ),
            min_hits=st.session_state.model_manager.get_config_value(
                "tracking.min_hits", 3
            ),
            iou_threshold=st.session_state.model_manager.get_config_value(
                "tracking.iou_threshold", 0.3
            ),
        )

        st.session_state.label_agent = LabelAgent(
            valid_classes=st.session_state.model_manager.get_class_names()
        )

        st.session_state.logging_agent = LoggingAgent(
            log_to_file=False, log_to_console=True
        )

        st.session_state.initialized = True


def draw_detections(frame, detections, tracks, show_confidence=True):
    annotated_frame = frame.copy()

    for track in tracks:
        x1, y1, x2, y2 = [int(coord) for coord in track["bbox"]]

        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        label = f"ID:{track['track_id']} {track['class_name']}"
        if show_confidence:
            label += f" {track['confidence']:.2f}"

        label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        cv2.rectangle(
            annotated_frame,
            (x1, y1 - label_size[1] - 10),
            (x1 + label_size[0], y1),
            (0, 255, 0),
            -1,
        )
        cv2.putText(
            annotated_frame,
            label,
            (x1, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            2,
        )

    return annotated_frame


def process_frame(frame, class_filter=None, show_confidence=True, frame_skip=0):
    if (
        frame_skip > 0
        and st.session_state.get("frame_count", 0) % (frame_skip + 1) != 0
    ):
        return frame, [], []

    detections = st.session_state.detection_agent.detect(frame, class_filter)

    tracks = st.session_state.tracking_agent.update(detections)

    annotated_frame = draw_detections(frame, detections, tracks, show_confidence)

    return annotated_frame, detections, tracks


def main():
    st.set_page_config(page_title="VisionTrack - YOLO Object Tracking", layout="wide")

    st.title("🎯 VisionTrack - Real-time Object Tracking")
    st.markdown("*Powered by Ultralytics YOLO*")

    initialize_agents()

    with st.sidebar:
        st.header("⚙️ Configuration")

        all_classes = st.session_state.label_agent.get_all_class_names()
        selected_classes = st.multiselect(
            "Select objects to track:",
            options=all_classes,
            default=["person"],
            help="Choose which objects you want to detect and track",
        )

        class_filter = selected_classes if selected_classes else None

        st.divider()

        st.subheader("Detection Settings")

        confidence_threshold = st.slider(
            "Confidence Threshold",
            min_value=0.1,
            max_value=1.0,
            value=0.5,
            step=0.05,
            help="Minimum confidence for detections",
        )
        st.session_state.detection_agent.confidence_threshold = confidence_threshold

        iou_threshold = st.slider(
            "IOU Threshold",
            min_value=0.1,
            max_value=0.9,
            value=0.3,
            step=0.05,
            help="Intersection over Union threshold for tracking",
        )
        st.session_state.tracking_agent.iou_threshold = iou_threshold

        frame_skip = st.slider(
            "Frame Skip",
            min_value=0,
            max_value=5,
            value=0,
            step=1,
            help="Skip frames to improve performance (0 = process every frame)",
        )

        show_confidence = st.checkbox("Show confidence scores", value=True)

        st.divider()

        input_source = st.radio(
            "Input Source:", ["Webcam", "Video File", "Image"], index=0
        )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("📹 Video Feed")
        video_placeholder = st.empty()

    with col2:
        st.header("📊 Statistics")
        stats_placeholder = st.empty()

    if input_source == "Webcam":
        if "webcam_running" not in st.session_state:
            st.session_state.webcam_running = False

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button(
                "▶️ Start Webcam",
                type="primary",
                use_container_width=True,
                disabled=st.session_state.webcam_running,
            ):
                with st.spinner("Opening webcam..."):
                    cap = cv2.VideoCapture(0)
                    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

                    if not cap.isOpened():
                        st.error("Cannot access webcam")
                    else:
                        st.session_state.webcam_cap = cap
                        st.session_state.webcam_running = True
                        st.session_state.tracking_agent.reset()
                        st.session_state.logging_agent.reset_metrics()
                        st.session_state.frame_count = 0
                        st.session_state.webcam_frame_count = 0
                        st.session_state.webcam_start_time = time.time()
                        st.rerun()

        with col_btn2:
            if st.button(
                "⏹️ Stop Webcam",
                type="secondary",
                use_container_width=True,
                disabled=not st.session_state.webcam_running,
            ):
                st.session_state.webcam_running = False
                if "webcam_cap" in st.session_state:
                    st.session_state.webcam_cap.release()
                    del st.session_state.webcam_cap
                st.rerun()

        if st.session_state.webcam_running:
            if "webcam_cap" not in st.session_state:
                st.error("Webcam not initialized")
                st.session_state.webcam_running = False
            else:
                ret, frame = st.session_state.webcam_cap.read()

                if ret:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    st.session_state.frame_count = st.session_state.webcam_frame_count

                    annotated_frame, detections, tracks = process_frame(
                        frame_rgb, class_filter, show_confidence, frame_skip
                    )

                    video_placeholder.image(
                        annotated_frame, channels="RGB", use_container_width=True
                    )

                    st.session_state.webcam_frame_count += 1
                    elapsed_time = time.time() - st.session_state.webcam_start_time
                    fps = (
                        st.session_state.webcam_frame_count / elapsed_time
                        if elapsed_time > 0
                        else 0
                    )

                    with stats_placeholder.container():
                        st.metric("FPS", f"{fps:.2f}")
                        st.metric("Frame", st.session_state.webcam_frame_count)
                        st.metric("Detections", len(detections))
                        st.metric("Active Tracks", len(tracks))

                    time.sleep(0.01)
                    st.rerun()
                else:
                    st.error("Failed to read from webcam")
                    st.session_state.webcam_running = False
                    if "webcam_cap" in st.session_state:
                        st.session_state.webcam_cap.release()
                        del st.session_state.webcam_cap

    elif input_source == "Video File":
        uploaded_file = st.file_uploader(
            "Upload a video file", type=["mp4", "avi", "mov"]
        )

        if uploaded_file is not None:
            tfile = Path("temp_video.mp4")
            tfile.write_bytes(uploaded_file.read())

            cap = cv2.VideoCapture(str(tfile))

            if not cap.isOpened():
                st.error("Cannot open video file")
                return

            st.session_state.tracking_agent.reset()
            st.session_state.logging_agent.reset_metrics()
            st.session_state.frame_count = 0

            frame_count = 0
            start_time = time.time()

            process_video = st.button("Process Video", type="primary")

            if process_video:
                progress_bar = st.progress(0)
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    st.session_state.frame_count = frame_count

                    annotated_frame, detections, tracks = process_frame(
                        frame_rgb, class_filter, show_confidence, frame_skip
                    )

                    video_placeholder.image(
                        annotated_frame, channels="RGB", use_container_width=True
                    )

                    frame_count += 1
                    elapsed_time = time.time() - start_time
                    fps = frame_count / elapsed_time if elapsed_time > 0 else 0

                    with stats_placeholder.container():
                        st.metric("FPS", f"{fps:.2f}")
                        st.metric("Frame", f"{frame_count}/{total_frames}")
                        st.metric("Detections", len(detections))
                        st.metric("Active Tracks", len(tracks))

                    progress_bar.progress(frame_count / total_frames)

                cap.release()
                tfile.unlink()
                st.success("Video processing complete!")

    elif input_source == "Image":
        uploaded_image = st.file_uploader(
            "Upload an image", type=["jpg", "jpeg", "png"]
        )

        if uploaded_image is not None:
            file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            st.session_state.tracking_agent.reset()
            st.session_state.frame_count = 0

            annotated_image, detections, tracks = process_frame(
                image_rgb, class_filter, show_confidence, 0
            )

            video_placeholder.image(
                annotated_image, channels="RGB", use_container_width=True
            )

            with stats_placeholder.container():
                st.metric("Detections", len(detections))
                st.metric("Active Tracks", len(tracks))

                if detections:
                    st.write("**Detected Objects:**")
                    for det in detections:
                        st.write(
                            f"- {det['class_name']} (confidence: {det['confidence']:.2f})"
                        )


if __name__ == "__main__":
    main()
