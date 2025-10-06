from typing import Any


class LabelAgent:
    def __init__(self, valid_classes: dict[int, str] | None = None):
        self.valid_classes = valid_classes or {}
        self._class_name_to_id: dict[str, int] = {}
        if self.valid_classes:
            self._build_name_to_id_mapping()

    def set_valid_classes(self, valid_classes: dict[int, str]) -> None:
        self.valid_classes = valid_classes
        self._build_name_to_id_mapping()

    def _build_name_to_id_mapping(self) -> None:
        self._class_name_to_id = {
            name.lower(): class_id for class_id, name in self.valid_classes.items()
        }

    def validate_class_name(self, class_name: str) -> bool:
        if not self.valid_classes:
            return False
        return class_name.lower() in self._class_name_to_id

    def normalize_class_name(self, user_input: str) -> str | None:
        normalized = user_input.lower().strip()

        if normalized in self._class_name_to_id:
            class_id = self._class_name_to_id[normalized]
            return self.valid_classes[class_id]

        return None

    def get_class_id(self, class_name: str) -> int | None:
        normalized = class_name.lower().strip()
        return self._class_name_to_id.get(normalized)

    def suggest_similar_classes(
        self, user_input: str, max_suggestions: int = 5
    ) -> list[str]:
        if not self.valid_classes:
            return []

        user_input_lower = user_input.lower().strip()
        suggestions = []

        for class_name in self.valid_classes.values():
            if user_input_lower in class_name.lower():
                suggestions.append(class_name)

        return suggestions[:max_suggestions]

    def parse_class_filter(self, user_input: str) -> list[str]:
        if not user_input.strip():
            return []

        raw_classes = [item.strip() for item in user_input.split(",")]

        valid_classes = []
        for raw_class in raw_classes:
            normalized = self.normalize_class_name(raw_class)
            if normalized:
                valid_classes.append(normalized)

        return valid_classes

    def get_all_class_names(self) -> list[str]:
        return list(self.valid_classes.values())

    def get_class_info(self) -> list[dict[str, Any]]:
        return [
            {"id": class_id, "name": name}
            for class_id, name in sorted(self.valid_classes.items())
        ]
