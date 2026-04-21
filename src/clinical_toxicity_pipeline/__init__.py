"""Clinical toxicity pipeline package."""

__all__ = ["build_status_message"]


def build_status_message(dataset: str = "not-set") -> str:
    """Return a small status message for the pipeline."""
    return f"Clinical toxicity pipeline ready. Dataset: {dataset}"
