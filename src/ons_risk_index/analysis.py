"""Core analytical functions reconstructed from the submitted methodology.

The original Python files were unavailable. This implementation follows the
method documented in the group report: simple OLS, population z-scores,
three weighted composite scores, and 1,000 Dirichlet-weight Monte Carlo draws.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Mapping, Sequence

import numpy as np
import pandas as pd
from scipy import stats


COMPONENT_COLUMNS: tuple[str, ...] = (
    "paper_first_pct",
    "aged_65_74_pct",
    "aged_75_plus_pct",
    "deprived_2plus_pct",
    "limited_english_pct",
    "underperformance",
)

WEIGHT_SCHEMES: Mapping[str, np.ndarray] = {
    "A": np.array([0.20, 0.10, 0.10, 0.20, 0.20, 0.20]),
    "B": np.array([0.30, 0.10, 0.15, 0.20, 0.15, 0.10]),
    "C": np.array([0.15, 0.05, 0.10, 0.15, 0.15, 0.40]),
}


@dataclass(frozen=True)
class RegressionResult:
    """Summary of online share regressed on paper-first area share."""

    intercept: float
    slope: float
    r_squared: float
    p_value: float
    slope_std_error: float
    intercept_std_error: float
    n: int

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


def _require_columns(frame: pd.DataFrame, columns: Sequence[str]) -> None:
    missing = [column for column in columns if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")


def fit_online_share_model(
    frame: pd.DataFrame,
    *,
    online_col: str = "online_pct",
    paper_col: str = "paper_first_pct",
) -> RegressionResult:
    """Fit ordinary least squares for online share on paper-first share.

    With one predictor, scipy.stats.linregress is algebraically equivalent to
    an OLS model with an intercept. Population-level regression inputs must be
    complete and finite.
    """

    _require_columns(frame, [online_col, paper_col])
    clean = frame[[paper_col, online_col]].apply(pd.to_numeric, errors="coerce").dropna()
    if len(clean) < 3:
        raise ValueError("At least three complete observations are required for OLS.")
    if not np.isfinite(clean.to_numpy(dtype=float)).all():
        raise ValueError("Regression inputs must be finite.")

    result = stats.linregress(clean[paper_col], clean[online_col])
    return RegressionResult(
        intercept=float(result.intercept),
        slope=float(result.slope),
        r_squared=float(result.rvalue**2),
        p_value=float(result.pvalue),
        slope_std_error=float(result.stderr),
        intercept_std_error=float(result.intercept_stderr),
        n=int(len(clean)),
    )


def add_underperformance_residual(
    frame: pd.DataFrame,
    *,
    online_col: str = "online_pct",
    paper_col: str = "paper_first_pct",
    output_col: str = "underperformance",
) -> tuple[pd.DataFrame, RegressionResult]:
    """Add expected-minus-actual online share as the underperformance residual."""

    model = fit_online_share_model(frame, online_col=online_col, paper_col=paper_col)
    result = frame.copy()
    expected = model.intercept + model.slope * pd.to_numeric(result[paper_col])
    result[output_col] = expected - pd.to_numeric(result[online_col])
    return result, model


def z_standardise(frame: pd.DataFrame, columns: Sequence[str]) -> pd.DataFrame:
    """Return population z-scores using ddof=0, matching the report."""

    _require_columns(frame, columns)
    numeric = frame.loc[:, columns].apply(pd.to_numeric, errors="raise")
    means = numeric.mean(axis=0)
    std = numeric.std(axis=0, ddof=0)
    if (std == 0).any():
        constant = std.index[std == 0].tolist()
        raise ValueError(f"Cannot standardise constant columns: {constant}")
    return (numeric - means) / std


def _validate_weight_schemes(
    schemes: Mapping[str, np.ndarray], component_count: int
) -> None:
    for name, weights in schemes.items():
        values = np.asarray(weights, dtype=float)
        if values.shape != (component_count,):
            raise ValueError(f"Scheme {name} must contain {component_count} weights.")
        if (values < 0).any() or not np.isclose(values.sum(), 1.0):
            raise ValueError(f"Scheme {name} weights must be non-negative and sum to 1.")


def build_risk_index(
    frame: pd.DataFrame,
    *,
    authority_col: str = "local_authority",
    component_columns: Sequence[str] = COMPONENT_COLUMNS,
    weight_schemes: Mapping[str, np.ndarray] = WEIGHT_SCHEMES,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create z-scores, composite scores and descending ranks for each scheme."""

    _require_columns(frame, [authority_col, *component_columns])
    _validate_weight_schemes(weight_schemes, len(component_columns))
    z_scores = z_standardise(frame, component_columns)
    output = frame.copy()
    for scheme_name, weights in weight_schemes.items():
        output[f"score_{scheme_name.lower()}"] = z_scores.to_numpy() @ weights
        output[f"rank_{scheme_name.lower()}"] = (
            output[f"score_{scheme_name.lower()}"]
            .rank(ascending=False, method="min")
            .astype(int)
        )
    return output, z_scores


def monte_carlo_top_k_frequency(
    z_scores: pd.DataFrame,
    *,
    draws: int = 1_000,
    top_k: int = 12,
    seed: int = 42,
) -> np.ndarray:
    """Return each authority's share of Dirichlet draws in the top k.

    Random weights are sampled uniformly on the simplex using Dirichlet(1).
    The fixed seed reproduces the design documented in the report.
    """

    if draws <= 0:
        raise ValueError("draws must be positive")
    if top_k <= 0 or top_k > len(z_scores):
        raise ValueError("top_k must be between 1 and the number of authorities")
    values = z_scores.to_numpy(dtype=float)
    if not np.isfinite(values).all():
        raise ValueError("z_scores must contain only finite values")

    rng = np.random.default_rng(seed)
    random_weights = rng.dirichlet(np.ones(values.shape[1]), size=draws)
    simulated_scores = values @ random_weights.T
    top_indices = np.argpartition(simulated_scores, -top_k, axis=0)[-top_k:, :]
    counts = np.bincount(top_indices.ravel(), minlength=len(z_scores))
    return counts / draws


def analyse_raw_components(
    frame: pd.DataFrame,
    *,
    authority_col: str = "local_authority",
    draws: int = 1_000,
    top_k: int = 12,
    seed: int = 42,
) -> tuple[pd.DataFrame, RegressionResult]:
    """Run the full documented analytical pipeline on a complete raw dataset."""

    with_residual, regression = add_underperformance_residual(frame)
    scored, z_scores = build_risk_index(with_residual, authority_col=authority_col)
    scored["monte_carlo_frequency"] = monte_carlo_top_k_frequency(
        z_scores, draws=draws, top_k=top_k, seed=seed
    )
    return scored, regression

