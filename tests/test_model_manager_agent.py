from pathlib import Path

import pytest

from src.model_manager_agent import ModelManagerAgent


@pytest.fixture
def model_manager():
    return ModelManagerAgent(config_path="config.yaml")


def test_model_manager_initialization(model_manager):
    assert model_manager.config_path == Path("config.yaml")
    assert isinstance(model_manager.config, dict)
    assert model_manager.current_model is None


def test_load_config(model_manager):
    assert len(model_manager.config) > 0
    assert "model" in model_manager.config


def test_load_model_default(model_manager):
    model = model_manager.load_model()
    assert model is not None
    assert model_manager.current_model is not None
    assert model_manager.model_name != ""


def test_load_model_specific(model_manager):
    model = model_manager.load_model("yolov8n.pt")
    assert model is not None
    assert model_manager.model_name == "yolov8n.pt"


def test_get_model_without_loading():
    manager = ModelManagerAgent()
    with pytest.raises(RuntimeError, match="No model loaded"):
        manager.get_model()


def test_get_model_after_loading(model_manager):
    model_manager.load_model()
    model = model_manager.get_model()
    assert model is not None


def test_get_class_names(model_manager):
    model_manager.load_model()
    class_names = model_manager.get_class_names()
    assert isinstance(class_names, dict)
    assert len(class_names) > 0


def test_get_class_names_without_model():
    manager = ModelManagerAgent()
    with pytest.raises(RuntimeError, match="No model loaded"):
        manager.get_class_names()


def test_get_config_value(model_manager):
    value = model_manager.get_config_value("model.name")
    assert value is not None

    default_value = model_manager.get_config_value("nonexistent.key", default="default")
    assert default_value == "default"


def test_update_config(model_manager):
    original_value = model_manager.get_config_value("model.confidence_threshold")

    model_manager.update_config("model.confidence_threshold", 0.7)
    new_value = model_manager.get_config_value("model.confidence_threshold")

    assert new_value == 0.7
    assert new_value != original_value


def test_update_nested_config(model_manager):
    model_manager.update_config("new.nested.key", "test_value")
    value = model_manager.get_config_value("new.nested.key")
    assert value == "test_value"


def test_get_available_models():
    manager = ModelManagerAgent()
    models = manager.get_available_models()
    assert isinstance(models, list)
