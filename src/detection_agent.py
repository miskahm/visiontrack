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

        results = self.model(
            frame, conf=self.confidence_threshold, device=self.device, verbose=False
        )

        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]

                if class_filter and class_name not in class_filter:
                    continue

                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = float(box.conf[0])

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
