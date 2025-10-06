import pytest

from src.tracking_agent import TrackingAgent


@pytest.fixture
def tracking_agent():
    return TrackingAgent(max_age=30, min_hits=3, iou_threshold=0.3)


@pytest.fixture
def sample_detection():
    return {
        "bbox": [100.0, 100.0, 200.0, 200.0],
        "confidence": 0.9,
        "class_id": 0,
        "class_name": "person",
    }


def test_tracking_agent_initialization():
    agent = TrackingAgent(max_age=30, min_hits=3, iou_threshold=0.3)
    assert agent.max_age == 30
    assert agent.min_hits == 3
    assert agent.iou_threshold == 0.3
    assert agent.tracks == []
    assert agent.track_id_counter == 0


def test_update_with_empty_detections(tracking_agent):
    active_tracks = tracking_agent.update([])
    assert active_tracks == []


def test_create_new_track(tracking_agent, sample_detection):
    tracking_agent.update([sample_detection])
    assert len(tracking_agent.tracks) == 1
    assert tracking_agent.tracks[0]["track_id"] == 0
    assert tracking_agent.tracks[0]["class_name"] == "person"


def test_track_requires_min_hits(tracking_agent, sample_detection):
    active_tracks = tracking_agent.update([sample_detection])
    assert len(active_tracks) == 0

    active_tracks = tracking_agent.update([sample_detection])
    assert len(active_tracks) == 0

    active_tracks = tracking_agent.update([sample_detection])
    assert len(active_tracks) == 1
    assert active_tracks[0]["track_id"] == 0


def test_track_matching_with_iou(tracking_agent, sample_detection):
    for _ in range(3):
        tracking_agent.update([sample_detection])

    similar_detection = {
        "bbox": [105.0, 105.0, 205.0, 205.0],
        "confidence": 0.85,
        "class_id": 0,
        "class_name": "person",
    }

    active_tracks = tracking_agent.update([similar_detection])
    assert len(active_tracks) == 1
    assert active_tracks[0]["track_id"] == 0
    assert len(tracking_agent.tracks) == 1


def test_new_track_creation_for_different_position(tracking_agent, sample_detection):
    for _ in range(3):
        tracking_agent.update([sample_detection])

    different_detection = {
        "bbox": [400.0, 400.0, 500.0, 500.0],
        "confidence": 0.8,
        "class_id": 0,
        "class_name": "person",
    }

    tracking_agent.update([different_detection])
    assert len(tracking_agent.tracks) == 2


def test_track_aging(tracking_agent, sample_detection):
    for _ in range(3):
        tracking_agent.update([sample_detection])

    active_tracks = tracking_agent.update([sample_detection])
    assert len(active_tracks) == 1

    for _ in range(30):
        active_tracks = tracking_agent.update([])

    assert len(tracking_agent.tracks) == 0


def test_calculate_iou(tracking_agent):
    bbox1 = [0.0, 0.0, 100.0, 100.0]
    bbox2 = [50.0, 50.0, 150.0, 150.0]

    iou = tracking_agent._calculate_iou(bbox1, bbox2)
    assert 0 < iou < 1

    bbox_same = [0.0, 0.0, 100.0, 100.0]
    iou_same = tracking_agent._calculate_iou(bbox1, bbox_same)
    assert iou_same == 1.0

    bbox_no_overlap = [200.0, 200.0, 300.0, 300.0]
    iou_no_overlap = tracking_agent._calculate_iou(bbox1, bbox_no_overlap)
    assert iou_no_overlap == 0.0


def test_class_name_filtering(tracking_agent):
    person_detection = {
        "bbox": [100.0, 100.0, 200.0, 200.0],
        "confidence": 0.9,
        "class_id": 0,
        "class_name": "person",
    }

    car_detection = {
        "bbox": [105.0, 105.0, 205.0, 205.0],
        "confidence": 0.85,
        "class_id": 2,
        "class_name": "car",
    }

    for _ in range(3):
        tracking_agent.update([person_detection])

    tracking_agent.update([car_detection])

    assert len(tracking_agent.tracks) == 2


def test_reset(tracking_agent, sample_detection):
    for _ in range(3):
        tracking_agent.update([sample_detection])

    tracking_agent.reset()

    assert tracking_agent.tracks == []
    assert tracking_agent.track_id_counter == 0


def test_multiple_detections_same_frame(tracking_agent):
    detection1 = {
        "bbox": [100.0, 100.0, 200.0, 200.0],
        "confidence": 0.9,
        "class_id": 0,
        "class_name": "person",
    }

    detection2 = {
        "bbox": [300.0, 300.0, 400.0, 400.0],
        "confidence": 0.85,
        "class_id": 0,
        "class_name": "person",
    }

    for _ in range(3):
        tracking_agent.update([detection1, detection2])

    active_tracks = tracking_agent.update([detection1, detection2])
    assert len(active_tracks) == 2
    assert active_tracks[0]["track_id"] != active_tracks[1]["track_id"]
