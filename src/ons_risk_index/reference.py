"""Load and validate the surviving reference-output dataset."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .analysis import RegressionResult, fit_online_share_model


REFERENCE_COLUMN_MAP = {
    "Local Authority": "local_authority",
    "Online %": "online_pct",
    "Paper first %": "paper_first_pct",
    "Under-performance": "underperformance_reported",
    "Score A": "score_a",
    "Score B": "score_b",
    "Score C": "score_c",
    "Rank A": "rank_a",
    "Rank B": "rank_b",
    "Rank C": "rank_c",
    "Top 12 all 3": "top_12_all_three",
    "Monte Carlo freq": "monte_carlo_frequency_reported",
}


def load_reference_scores(path: str | Path) -> pd.DataFrame:
    """Load the derived CSV or the original reference workbook."""

    path = Path(path)
    if path.suffix.lower() == ".csv":
        frame = pd.read_csv(path)
    elif path.suffix.lower() in {".xlsx", ".xlsm"}:
        frame = pd.read_excel(path, sheet_name="Full LA scores (328)")
        frame = frame.rename(columns=REFERENCE_COLUMN_MAP)
    else:
        raise ValueError("Reference input must be .csv, .xlsx or .xlsm")

    required = [
        "local_authority",
        "online_pct",
        "paper_first_pct",
        "underperformance_reported",
        "score_a",
        "score_b",
        "score_c",
        "rank_a",
        "rank_b",
        "rank_c",
        "monte_carlo_frequency_reported",
    ]
    frame = frame.dropna(subset=["online_pct", "paper_first_pct"]).copy()
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"Reference file is missing columns: {missing}")
    if len(frame) != 328:
        raise ValueError(f"Expected 328 local authorities; found {len(frame)}")
    for column in ["rank_a", "rank_b", "rank_c"]:
        frame[column] = frame[column].astype(int)
    return frame


def validate_reference(frame: pd.DataFrame) -> tuple[dict[str, object], RegressionResult]:
    """Recalculate the reproducible quantities and compare to the report."""

    regression = fit_online_share_model(frame)
    predicted = regression.intercept + regression.slope * frame["paper_first_pct"]
    residual = predicted - frame["online_pct"]

    rank_matches: dict[str, int] = {}
    for scheme in ("a", "b", "c"):
        recalculated = frame[f"score_{scheme}"].rank(ascending=False, method="min").astype(int)
        rank_matches[scheme.upper()] = int((recalculated == frame[f"rank_{scheme}"]).sum())

    reported_intersection = set(
        frame.loc[frame["top_12_all_three"].eq("Yes"), "local_authority"]
    )
    calculated_intersection = set.intersection(
        *(set(frame.nlargest(12, f"score_{scheme}")["local_authority"]) for scheme in ("a", "b", "c"))
    )

    checks: dict[str, object] = {
        "authority_count": int(len(frame)),
        "regression_intercept": regression.intercept,
        "regression_slope": regression.slope,
        "regression_r_squared": regression.r_squared,
        "max_absolute_residual_difference": float(
            np.max(np.abs(residual - frame["underperformance_reported"]))
        ),
        "rank_matches_out_of_328": rank_matches,
        "rank_reproduction_note": (
            "Displayed composite scores are rounded to three decimals; the workbook ranks "
            "were calculated from higher-precision values, so some exact rank positions tie "
            "or swap when recalculated from the displayed scores."
        ),
        "top_12_all_three_reported": sorted(reported_intersection),
        "top_12_all_three_recalculated": sorted(calculated_intersection),
        "top_12_intersection_matches": reported_intersection == calculated_intersection,
    }
    return checks, regression
