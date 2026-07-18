"""Run the complete risk index when the six raw component columns are available."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ons_risk_index.analysis import analyse_raw_components


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/full_analysis")
    args = parser.parse_args()

    frame = pd.read_csv(args.input_csv)
    scored, regression = analyse_raw_components(frame)
    args.output.mkdir(parents=True, exist_ok=True)
    scored.to_csv(args.output / "all_authority_scores.csv", index=False)
    with (args.output / "regression.json").open("w", encoding="utf-8") as handle:
        json.dump(regression.to_dict(), handle, indent=2)
    print(json.dumps(regression.to_dict(), indent=2))


if __name__ == "__main__":
    main()

