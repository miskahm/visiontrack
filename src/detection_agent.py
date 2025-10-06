from pathlib import Path
from typing import Any

import numpy as np
from ultralytics import YOLO


class DetectionAgent:
    def __init__(
        self, model_path: str, confidence_threshold: float = 0.5, device: str = "cpu"
    ):
        self.model_path = Path(model_path)
        self.confidence_threshold = confidence_threshold
        self.device = device
        self.model: YOLO | None = None

    def load_model(self) -> None:
        if not self.model_path.exists():
            self.model = YOLO(self.model_path.name)
        else:
            self.model = YOLO(str(self.model_path))

    def detect(
        self, frame: np.ndarray, class_filter: list[str] | None = None
    ) -> list[dict[str, Any]]:
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        # Convert class filter to class IDs for faster filtering
        class_ids_filter = None
        if class_filter:
            class_ids_filter = [
                cls_id
                for cls_id, cls_name in self.model.names.items()
                if cls_name in class_filter
            ]

        results = self.model(
            frame,
            conf=self.confidence_threshold,
            device=self.device,
            verbose=False,
            imgsz=640,
            half=False,
            max_det=50,
            agnostic_nms=True,
            classes=class_ids_filter,
        )

        detections = []
        for result in results:
            boxes = result.boxes
            if len(boxes) == 0:
                continue

            # Batch process boxes for better performance
            class_ids = boxes.cls.cpu().numpy().astype(int)
            confidences = boxes.conf.cpu().numpy()
            xyxy = boxes.xyxy.cpu().numpy()

            for i in range(len(boxes)):
                class_id = int(class_ids[i])
                class_name = self.model.names[class_id]
                confidence = float(confidences[i])
                x1, y1, x2, y2 = xyxy[i]

                detections.append(
                    {
                        "bbox": [float(x1), float(y1), float(x2), float(y2)],
                        "confidence": confidence,
                        "class_id": class_id,
                        "class_name": class_name,
                    }
                )

        return detections

    def get_class_names(self) -> dict[int, str]:
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        return self.model.names
