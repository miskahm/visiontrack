from typing import Any


class TrackingAgent:
    def __init__(
        self, max_age: int = 30, min_hits: int = 3, iou_threshold: float = 0.3
    ):
        self.max_age = max_age
        self.min_hits = min_hits
        self.iou_threshold = iou_threshold
        self.tracks: list[dict[str, Any]] = []
        self.track_id_counter = 0

    def update(self, detections: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not detections:
            self._age_tracks()
            return self._get_active_tracks()

        matched_tracks, unmatched_detections = self._match_detections_to_tracks(
            detections
        )

        for track_idx, detection in matched_tracks:
            self.tracks[track_idx]["bbox"] = detection["bbox"]
            self.tracks[track_idx]["confidence"] = detection["confidence"]
            self.tracks[track_idx]["class_name"] = detection["class_name"]
            self.tracks[track_idx]["hits"] += 1
            self.tracks[track_idx]["age"] = 0

        for detection in unmatched_detections:
            self._create_new_track(detection)

        self._age_tracks()

        return self._get_active_tracks()

    def _match_detections_to_tracks(
        self, detections: list[dict[str, Any]]
    ) -> tuple[list[tuple[int, dict[str, Any]]], list[dict[str, Any]]]:
        if not self.tracks:
            return [], detections

        matched = []
        unmatched_detections = []
        used_tracks = set()

        for detection in detections:
            best_iou = 0
            best_track_idx = -1

            for track_idx, track in enumerate(self.tracks):
                if track_idx in used_tracks:
                    continue

                if track["class_name"] != detection["class_name"]:
                    continue

                iou = self._calculate_iou(detection["bbox"], track["bbox"])

                if iou > self.iou_threshold and iou > best_iou:
                    best_iou = iou
                    best_track_idx = track_idx

            if best_track_idx >= 0:
                matched.append((best_track_idx, detection))
                used_tracks.add(best_track_idx)
            else:
                unmatched_detections.append(detection)

        return matched, unmatched_detections

    def _calculate_iou(self, bbox1: list[float], bbox2: list[float]) -> float:
        x1_min, y1_min, x1_max, y1_max = bbox1
        x2_min, y2_min, x2_max, y2_max = bbox2

        inter_x_min = max(x1_min, x2_min)
        inter_y_min = max(y1_min, y2_min)
        inter_x_max = min(x1_max, x2_max)
        inter_y_max = min(y1_max, y2_max)

        if inter_x_max <= inter_x_min or inter_y_max <= inter_y_min:
            return 0.0

        inter_area = (inter_x_max - inter_x_min) * (inter_y_max - inter_y_min)

        bbox1_area = (x1_max - x1_min) * (y1_max - y1_min)
        bbox2_area = (x2_max - x2_min) * (y2_max - y2_min)

        union_area = bbox1_area + bbox2_area - inter_area

        if union_area == 0:
            return 0.0

        return inter_area / union_area

    def _create_new_track(self, detection: dict[str, Any]) -> None:
        track = {
            "track_id": self.track_id_counter,
            "bbox": detection["bbox"],
            "confidence": detection["confidence"],
            "class_id": detection["class_id"],
            "class_name": detection["class_name"],
            "hits": 1,
            "age": 0,
        }
        self.tracks.append(track)
        self.track_id_counter += 1

    def _age_tracks(self) -> None:
        self.tracks = [track for track in self.tracks if track["age"] < self.max_age]

        for track in self.tracks:
            track["age"] += 1

    def _get_active_tracks(self) -> list[dict[str, Any]]:
        return [track for track in self.tracks if track["hits"] >= self.min_hits]

    def reset(self) -> None:
        self.tracks = []
        self.track_id_counter = 0
