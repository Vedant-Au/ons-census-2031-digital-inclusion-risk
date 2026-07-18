from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ons_risk_index.analysis import (
    COMPONENT_COLUMNS,
    analyse_raw_components,
    build_risk_index,
    monte_carlo_top_k_frequency,
    z_standardise,
)
from ons_risk_index.reference import load_reference_scores


class EdgeCaseTests(unittest.TestCase):
    def test_missing_component_is_rejected(self) -> None:
        frame = pd.DataFrame({"local_authority": ["A"], "paper_first_pct": [10.0]})
        with self.assertRaisesRegex(ValueError, "Missing required columns"):
            build_risk_index(frame)

    def test_constant_component_is_rejected(self) -> None:
        frame = pd.DataFrame({"constant": [1.0, 1.0, 1.0]})
        with self.assertRaisesRegex(ValueError, "constant columns"):
            z_standardise(frame, ["constant"])

    def test_invalid_top_k_is_rejected(self) -> None:
        z_scores = pd.DataFrame(np.ones((5, 6)))
        for invalid in (0, 6):
            with self.subTest(top_k=invalid):
                with self.assertRaisesRegex(ValueError, "top_k"):
                    monte_carlo_top_k_frequency(z_scores, top_k=invalid)

    def test_synthetic_full_pipeline(self) -> None:
        rows = 20
        x = np.arange(rows, dtype=float)
        frame = pd.DataFrame(
            {
                "local_authority": [f"Authority {i}" for i in range(rows)],
                "online_pct": 94.0 - 0.5 * x + np.sin(x),
                "paper_first_pct": x,
                "aged_65_74_pct": 8.0 + 0.2 * x,
                "aged_75_plus_pct": 5.0 + 0.1 * x + np.cos(x),
                "deprived_2plus_pct": 10.0 + 0.3 * x + np.sin(x / 2),
                "limited_english_pct": 2.0 + np.sqrt(x + 1),
            }
        )
        scored, regression = analyse_raw_components(frame, draws=100, top_k=4)
        self.assertEqual(regression.n, rows)
        for column in ["underperformance", "score_a", "rank_b", "score_c"]:
            self.assertIn(column, scored.columns)
        self.assertAlmostEqual(float(scored["monte_carlo_frequency"].sum()), 4.0)
        self.assertTrue(set(COMPONENT_COLUMNS).issubset(scored.columns))


class ReferenceDataQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.frame = load_reference_scores(ROOT / "data/reference/reference_scores.csv")

    def test_authority_key_is_complete_and_unique(self) -> None:
        self.assertEqual(len(self.frame), 328)
        self.assertFalse(self.frame["local_authority"].isna().any())
        self.assertFalse(self.frame["local_authority"].duplicated().any())

    def test_percentages_and_frequencies_are_bounded(self) -> None:
        for column in ("online_pct", "paper_first_pct"):
            self.assertTrue(self.frame[column].between(0, 100).all())
        self.assertTrue(
            self.frame["monte_carlo_frequency_reported"].between(0, 1).all()
        )

    def test_ranks_are_valid(self) -> None:
        for column in ("rank_a", "rank_b", "rank_c"):
            self.assertTrue(self.frame[column].between(1, 328).all())
            self.assertTrue(np.issubdtype(self.frame[column].dtype, np.integer))


if __name__ == "__main__":
    unittest.main()
