import numpy as np
import pytest

from src.detection_agent import DetectionAgent


@pytest.fixture
def detection_agent():
    agent = DetectionAgent(
        model_path="yolov8n.pt", confidence_threshold=0.5, device="cpu"
    )
    agent.load_model()
    return agent


@pytest.fixture
def sample_frame():
    return np.zeros((640, 640, 3), dtype=np.uint8)


def test_detection_agent_initialization():
    agent = DetectionAgent(
        model_path="yolov8n.pt", confidence_threshold=0.5, device="cpu"
    )
    assert agent.model_path.name == "yolov8n.pt"
    assert agent.confidence_threshold == 0.5
    assert agent.device == "cpu"
    assert agent.model is None


def test_model_loading(detection_agent):
    assert detection_agent.model is not None


def test_detect_without_loaded_model(sample_frame):
    agent = DetectionAgent(model_path="yolov8n.pt")
    with pytest.raises(RuntimeError, match="Model not loaded"):
        agent.detect(sample_frame)


def test_detect_returns_list(detection_agent, sample_frame):
    detections = detection_agent.detect(sample_frame)
    assert isinstance(detections, list)


def test_detection_structure(detection_agent, sample_frame):
    detections = detection_agent.detect(sample_frame)

    if detections:
        detection = detections[0]
        assert "bbox" in detection
        assert "confidence" in detection
        assert "class_id" in detection
        assert "class_name" in detection
        assert len(detection["bbox"]) == 4
        assert isinstance(detection["confidence"], float)
        assert isinstance(detection["class_id"], int)
        assert isinstance(detection["class_name"], str)


def test_class_filter(detection_agent, sample_frame):
    detection_agent.detect(sample_frame)
    detections_filtered = detection_agent.detect(sample_frame, class_filter=["person"])

    for detection in detections_filtered:
        assert detection["class_name"] == "person"


def test_get_class_names(detection_agent):
    class_names = detection_agent.get_class_names()
    assert isinstance(class_names, dict)
    assert len(class_names) > 0
    assert 0 in class_names


def test_get_class_names_without_model():
    agent = DetectionAgent(model_path="yolov8n.pt")
    with pytest.raises(RuntimeError, match="Model not loaded"):
        agent.get_class_names()
