"""Recreate all outputs supported by the surviving reference workbook."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ons_risk_index.reference import load_reference_scores, validate_reference
from ons_risk_index.visualise import (
    plot_evidence_led_ranking,
    plot_monte_carlo_robustness,
    plot_online_vs_paper_first,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=ROOT / "data/reference/reference_scores.csv",
        help="Derived reference CSV or the original Analysis ReferenceSheet workbook.",
    )
    parser.add_argument("--output", type=Path, default=ROOT / "outputs")
    args = parser.parse_args()

    frame = load_reference_scores(args.input)
    checks, regression = validate_reference(frame)

    figures = args.output / "figures"
    tables = args.output / "tables"
    figures.mkdir(parents=True, exist_ok=True)
    tables.mkdir(parents=True, exist_ok=True)

    plot_online_vs_paper_first(frame, regression, figures / "online_vs_paper_first.png")
    plot_monte_carlo_robustness(frame, figures / "monte_carlo_robustness.png")
    plot_evidence_led_ranking(frame, figures / "evidence_led_top12.png")

    top_columns = [
        "local_authority",
        "online_pct",
        "paper_first_pct",
        "underperformance_reported",
        "score_b",
        "rank_b",
        "monte_carlo_frequency_reported",
    ]
    frame.nsmallest(12, "rank_b")[top_columns].to_csv(
        tables / "evidence_led_top12.csv", index=False
    )
    with (args.output / "validation_report.json").open("w", encoding="utf-8") as handle:
        json.dump(checks, handle, indent=2)

    print(json.dumps(checks, indent=2))


if __name__ == "__main__":
    main()

