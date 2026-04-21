"""CLI entry point for the clinical toxicity pipeline."""

from __future__ import annotations

import argparse

from clinical_toxicity_pipeline import build_status_message


def run() -> None:
    """Run a minimal CLI for project sanity checks."""
    parser = argparse.ArgumentParser(
        description="Clinical toxicity pipeline starter CLI."
    )
    parser.add_argument(
        "--dataset",
        default="not-set",
        help="Dataset label or path used for the current run.",
    )
    args = parser.parse_args()
    print(build_status_message(args.dataset))


if __name__ == "__main__":
    run()
