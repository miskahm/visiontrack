import pytest

from src.label_agent import LabelAgent


@pytest.fixture
def sample_classes():
    return {0: "person", 1: "bicycle", 2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}


@pytest.fixture
def label_agent(sample_classes):
    return LabelAgent(valid_classes=sample_classes)


def test_label_agent_initialization():
    agent = LabelAgent()
    assert agent.valid_classes == {}
    assert agent._class_name_to_id == {}


def test_label_agent_with_classes(label_agent):
    assert len(label_agent.valid_classes) == 6
    assert "person" in label_agent._class_name_to_id.keys()


def test_set_valid_classes(label_agent):
    new_classes = {0: "cat", 1: "dog"}
    label_agent.set_valid_classes(new_classes)

    assert label_agent.valid_classes == new_classes
    assert "cat" in label_agent._class_name_to_id.keys()


def test_validate_class_name_valid(label_agent):
    assert label_agent.validate_class_name("person") is True
    assert label_agent.validate_class_name("Person") is True
    assert label_agent.validate_class_name("PERSON") is True


def test_validate_class_name_invalid(label_agent):
    assert label_agent.validate_class_name("invalid") is False
    assert label_agent.validate_class_name("") is False


def test_validate_class_name_empty_agent():
    agent = LabelAgent()
    assert agent.validate_class_name("person") is False


def test_normalize_class_name(label_agent):
    assert label_agent.normalize_class_name("person") == "person"
    assert label_agent.normalize_class_name("Person") == "person"
    assert label_agent.normalize_class_name("PERSON") == "person"
    assert label_agent.normalize_class_name("  person  ") == "person"


def test_normalize_class_name_invalid(label_agent):
    assert label_agent.normalize_class_name("invalid") is None
    assert label_agent.normalize_class_name("") is None


def test_get_class_id(label_agent):
    assert label_agent.get_class_id("person") == 0
    assert label_agent.get_class_id("Person") == 0
    assert label_agent.get_class_id("car") == 2
    assert label_agent.get_class_id("  car  ") == 2


def test_get_class_id_invalid(label_agent):
    assert label_agent.get_class_id("invalid") is None


def test_suggest_similar_classes(label_agent):
    suggestions = label_agent.suggest_similar_classes("cycle")
    assert "bicycle" in suggestions
    assert "motorcycle" in suggestions


def test_suggest_similar_classes_no_match(label_agent):
    suggestions = label_agent.suggest_similar_classes("xyz")
    assert suggestions == []


def test_suggest_similar_classes_max_suggestions(label_agent):
    suggestions = label_agent.suggest_similar_classes("c", max_suggestions=2)
    assert len(suggestions) <= 2


def test_parse_class_filter_single(label_agent):
    result = label_agent.parse_class_filter("person")
    assert result == ["person"]


def test_parse_class_filter_multiple(label_agent):
    result = label_agent.parse_class_filter("person, car, bicycle")
    assert "person" in result
    assert "car" in result
    assert "bicycle" in result
    assert len(result) == 3


def test_parse_class_filter_case_insensitive(label_agent):
    result = label_agent.parse_class_filter("Person, CAR, BiCyCle")
    assert "person" in result
    assert "car" in result
    assert "bicycle" in result


def test_parse_class_filter_with_invalid(label_agent):
    result = label_agent.parse_class_filter("person, invalid, car")
    assert "person" in result
    assert "car" in result
    assert "invalid" not in result
    assert len(result) == 2


def test_parse_class_filter_empty(label_agent):
    result = label_agent.parse_class_filter("")
    assert result == []


def test_parse_class_filter_whitespace(label_agent):
    result = label_agent.parse_class_filter("   ")
    assert result == []


def test_get_all_class_names(label_agent):
    names = label_agent.get_all_class_names()
    assert len(names) == 6
    assert "person" in names
    assert "car" in names


def test_get_class_info(label_agent):
    info = label_agent.get_class_info()
    assert len(info) == 6
    assert info[0]["id"] == 0
    assert info[0]["name"] == "person"
    assert all("id" in item and "name" in item for item in info)


def test_get_class_info_sorted(label_agent):
    info = label_agent.get_class_info()
    ids = [item["id"] for item in info]
    assert ids == sorted(ids)
