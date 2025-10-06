import logging

import pytest

from src.logging_agent import LoggingAgent


@pytest.fixture
def logging_agent(tmp_path):
    return LoggingAgent(
        log_dir=str(tmp_path / "logs"),
        log_level=logging.INFO,
        log_to_file=True,
        log_to_console=False,
    )


def test_logging_agent_initialization(logging_agent):
    assert logging_agent.logger.name == "VisionTrack"
    assert logging_agent.log_level == logging.INFO
    assert logging_agent.metrics == {}


def test_log_directory_creation(tmp_path):
    log_dir = tmp_path / "test_logs"
    LoggingAgent(log_dir=str(log_dir), log_to_console=False)

    assert log_dir.exists()


def test_log_file_creation(tmp_path):
    log_dir = tmp_path / "logs"
    LoggingAgent(log_dir=str(log_dir), log_to_console=False, log_to_file=True)

    log_files = list(log_dir.glob("visiontrack_*.log"))
    assert len(log_files) == 1


def test_console_only_logging():
    agent = LoggingAgent(log_to_file=False, log_to_console=True)
    assert len(agent.logger.handlers) == 1
    assert isinstance(agent.logger.handlers[0], logging.StreamHandler)


def test_log_detection(logging_agent):
    detections = [
        {"bbox": [100, 100, 200, 200], "class_name": "person", "confidence": 0.9}
    ]
    logging_agent.log_detection(1, detections)


def test_log_tracking(logging_agent):
    tracks = [{"track_id": 0, "bbox": [100, 100, 200, 200], "class_name": "person"}]
    logging_agent.log_tracking(1, tracks)


def test_log_model_load(logging_agent):
    logging_agent.log_model_load("yolov8n.pt", 1.5)


def test_log_error(logging_agent):
    error = ValueError("Test error")
    logging_agent.log_error(error, "test context")


def test_log_warning(logging_agent):
    logging_agent.log_warning("Test warning")


def test_log_info(logging_agent):
    logging_agent.log_info("Test info")


def test_update_metrics(logging_agent):
    logging_agent.update_metrics("test_metric", 100)
    assert logging_agent.get_metric("test_metric") == 100


def test_increment_metric(logging_agent):
    logging_agent.increment_metric("counter")
    assert logging_agent.get_metric("counter") == 1

    logging_agent.increment_metric("counter", 5)
    assert logging_agent.get_metric("counter") == 6


def test_get_metric_nonexistent(logging_agent):
    assert logging_agent.get_metric("nonexistent") is None


def test_get_all_metrics(logging_agent):
    logging_agent.update_metrics("metric1", 10)
    logging_agent.update_metrics("metric2", 20)

    all_metrics = logging_agent.get_all_metrics()
    assert all_metrics == {"metric1": 10, "metric2": 20}


def test_reset_metrics(logging_agent):
    logging_agent.update_metrics("metric1", 10)
    logging_agent.update_metrics("metric2", 20)

    logging_agent.reset_metrics()
    assert logging_agent.metrics == {}


def test_log_metrics_summary(logging_agent):
    logging_agent.update_metrics("detections", 100)
    logging_agent.update_metrics("tracks", 50)

    logging_agent.log_metrics_summary()


def test_log_fps(logging_agent):
    logging_agent.log_fps(30.5)
    assert logging_agent.get_metric("fps") == 30.5


def test_multiple_metric_operations(logging_agent):
    logging_agent.increment_metric("frame_count")
    logging_agent.increment_metric("frame_count")
    logging_agent.update_metrics("fps", 30.0)
    logging_agent.increment_metric("detection_count", 5)

    assert logging_agent.get_metric("frame_count") == 2
    assert logging_agent.get_metric("fps") == 30.0
    assert logging_agent.get_metric("detection_count") == 5
