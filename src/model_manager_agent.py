from pathlib import Path
from typing import Any

import yaml
from ultralytics import YOLO


class ModelManagerAgent:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self.config: dict[str, Any] = {}
        self.current_model: YOLO | None = None
        self.model_name: str = ""
        self.load_config()

    def load_config(self) -> None:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def load_model(self, model_name: str | None = None) -> YOLO:
        if model_name is None:
            model_name = self.config.get("model", {}).get("name", "yolov8n.pt")

        if not isinstance(model_name, str):
            model_name = "yolov8n.pt"

        model_path = Path("models") / model_name

        if model_path.exists():
            self.current_model = YOLO(str(model_path))
        else:
            self.current_model = YOLO(model_name)

        self.model_name = model_name
        return self.current_model

    def get_model(self) -> YOLO:
        if self.current_model is None:
            raise RuntimeError("No model loaded. Call load_model() first.")
        return self.current_model

    def get_class_names(self) -> dict[int, str]:
        if self.current_model is None:
            raise RuntimeError("No model loaded. Call load_model() first.")
        return self.current_model.names

    def get_config_value(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def update_config(self, key: str, value: Any) -> None:
        keys = key.split(".")
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def save_config(self) -> None:
        with open(self.config_path, "w") as f:
            yaml.dump(self.config, f, default_flow_style=False)

    def get_available_models(self) -> list[str]:
        models_dir = Path("models")

        if not models_dir.exists():
            return []

        return [
            f.name for f in models_dir.iterdir() if f.suffix in [".pt", ".pth", ".onnx"]
        ]
