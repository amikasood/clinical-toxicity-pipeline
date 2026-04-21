from clinical_toxicity_pipeline import build_status_message


def test_build_status_message_contains_dataset() -> None:
    message = build_status_message("tox21")
    assert "tox21" in message
