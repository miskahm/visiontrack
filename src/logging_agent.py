import logging
from datetime import datetime
from pathlib import Path
from typing import Any


class LoggingAgent:
    def __init__(
        self,
        log_dir: str = "logs",
        log_level: int = logging.INFO,
        log_to_file: bool = True,
        log_to_console: bool = True,
    ):
        self.log_dir = Path(log_dir)
        self.log_level = log_level
        self.log_to_file = log_to_file
        self.log_to_console = log_to_console
        self.logger = logging.getLogger("VisionTrack")
        self.metrics: dict[str, Any] = {}
        self._setup_logger()

    def _setup_logger(self) -> None:
        self.logger.setLevel(self.log_level)
        self.logger.handlers.clear()

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        if self.log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.log_level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        if self.log_to_file:
            self.log_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = self.log_dir / f"visiontrack_{timestamp}.log"

            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(self.log_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def log_detection(self, frame_count: int, detections: list[dict[str, Any]]) -> None:
        self.logger.debug(
            f"Frame {frame_count}: {len(detections)} detections",
            extra={"detections": detections},
        )

    def log_tracking(self, frame_count: int, tracks: list[dict[str, Any]]) -> None:
        self.logger.debug(
            f"Frame {frame_count}: {len(tracks)} active tracks",
            extra={"tracks": tracks},
        )

    def log_model_load(self, model_name: str, load_time: float) -> None:
        self.logger.info(f"Loaded model '{model_name}' in {load_time:.2f}s")

    def log_error(self, error: Exception, context: str = "") -> None:
        error_msg = f"Error in {context}: {str(error)}" if context else str(error)
        self.logger.error(error_msg, exc_info=True)

    def log_warning(self, message: str) -> None:
        self.logger.warning(message)

    def log_info(self, message: str) -> None:
        self.logger.info(message)

    def update_metrics(self, key: str, value: Any) -> None:
        self.metrics[key] = value

    def increment_metric(self, key: str, amount: int = 1) -> None:
        if key not in self.metrics:
            self.metrics[key] = 0
        self.metrics[key] += amount

    def get_metric(self, key: str) -> Any:
        return self.metrics.get(key)

    def get_all_metrics(self) -> dict[str, Any]:
        return self.metrics.copy()

    def reset_metrics(self) -> None:
        self.metrics = {}

    def log_metrics_summary(self) -> None:
        self.logger.info("Metrics Summary:")
        for key, value in self.metrics.items():
            self.logger.info(f"  {key}: {value}")

    def log_fps(self, fps: float) -> None:
        self.logger.info(f"FPS: {fps:.2f}")
        self.update_metrics("fps", fps)
