from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ons_risk_index.analysis import (
    WEIGHT_SCHEMES,
    add_underperformance_residual,
    build_risk_index,
    monte_carlo_top_k_frequency,
    z_standardise,
)
from ons_risk_index.reference import load_reference_scores, validate_reference


class AnalysisTests(unittest.TestCase):
    def test_all_weight_schemes_sum_to_one(self) -> None:
        for weights in WEIGHT_SCHEMES.values():
            self.assertAlmostEqual(float(weights.sum()), 1.0)

    def test_population_z_scores(self) -> None:
        frame = pd.DataFrame({"x": [1.0, 2.0, 3.0], "y": [2.0, 4.0, 8.0]})
        result = z_standardise(frame, ["x", "y"])
        np.testing.assert_allclose(result.mean().to_numpy(), [0.0, 0.0], atol=1e-12)
        np.testing.assert_allclose(result.std(ddof=0).to_numpy(), [1.0, 1.0], atol=1e-12)

    def test_underperformance_is_expected_minus_actual(self) -> None:
        frame = pd.DataFrame(
            {"paper_first_pct": [0.0, 10.0, 20.0], "online_pct": [95.0, 90.0, 85.0]}
        )
        output, model = add_underperformance_residual(frame)
        self.assertAlmostEqual(model.intercept, 95.0)
        self.assertAlmostEqual(model.slope, -0.5)
        np.testing.assert_allclose(output["underperformance"], [0.0, 0.0, 0.0], atol=1e-12)

    def test_monte_carlo_is_deterministic(self) -> None:
        z = pd.DataFrame(np.arange(60, dtype=float).reshape(10, 6))
        first = monte_carlo_top_k_frequency(z, draws=100, top_k=3, seed=42)
        second = monte_carlo_top_k_frequency(z, draws=100, top_k=3, seed=42)
        np.testing.assert_array_equal(first, second)
        self.assertAlmostEqual(float(first.sum()), 3.0)

    def test_reference_results_match_report(self) -> None:
        frame = load_reference_scores(ROOT / "data/reference/reference_scores.csv")
        checks, regression = validate_reference(frame)
        self.assertEqual(checks["authority_count"], 328)
        self.assertAlmostEqual(regression.intercept, 94.552, places=3)
        self.assertAlmostEqual(regression.slope, -0.546, places=3)
        self.assertAlmostEqual(regression.r_squared, 0.964, places=3)
        self.assertLess(checks["max_absolute_residual_difference"], 0.001)
        self.assertTrue(checks["top_12_intersection_matches"])
        for matches in checks["rank_matches_out_of_328"].values():
            self.assertGreaterEqual(matches, 290)


if __name__ == "__main__":
    unittest.main()
