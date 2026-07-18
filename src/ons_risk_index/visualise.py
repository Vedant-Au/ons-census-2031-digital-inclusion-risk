"""Publication-ready figures for the reconstructed analysis."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .analysis import RegressionResult


NAVY = "#17324D"
BLUE = "#2F75B5"
GOLD = "#E5A823"
LIGHT = "#EAF1F8"


def _finish(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close()


def _title(main: str, subtitle: str) -> None:
    ax = plt.gca()
    ax.set_title(main, loc="left", weight="bold", color=NAVY, pad=38)
    ax.text(
        0,
        1.025,
        subtitle,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=10,
        color="#526577",
    )


def plot_online_vs_paper_first(
    frame: pd.DataFrame, model: RegressionResult, output_path: str | Path
) -> None:
    """Scatter plot and fitted OLS line for all 328 authorities."""

    x = frame["paper_first_pct"].to_numpy(dtype=float)
    y = frame["online_pct"].to_numpy(dtype=float)
    line_x = np.linspace(x.min(), x.max(), 200)
    line_y = model.intercept + model.slope * line_x

    plt.figure(figsize=(9, 5.8))
    plt.scatter(x, y, s=26, alpha=0.62, color=BLUE, edgecolors="white", linewidths=0.4)
    plt.plot(line_x, line_y, color=GOLD, linewidth=2.6, label="OLS fitted line")
    _title(
        "Online completion share vs paper-first allocation",
        f"328 local authorities | slope {model.slope:.3f} | R² {model.r_squared:.3f}",
    )
    plt.xlabel("Local authority LSOAs allocated paper-first (%)")
    plt.ylabel("Completed household returns submitted online (%)")
    plt.grid(axis="both", alpha=0.18)
    plt.legend(frameon=False)
    _finish(Path(output_path))


def plot_monte_carlo_robustness(frame: pd.DataFrame, output_path: str | Path) -> None:
    """Top 12 reported Monte Carlo frequencies from the surviving workbook."""

    top = frame.nlargest(12, "monte_carlo_frequency_reported").sort_values(
        "monte_carlo_frequency_reported"
    )
    colors = [GOLD if value == "Yes" else BLUE for value in top["top_12_all_three"]]

    plt.figure(figsize=(9, 6.2))
    bars = plt.barh(
        top["local_authority"], top["monte_carlo_frequency_reported"] * 100, color=colors
    )
    for bar, value in zip(bars, top["monte_carlo_frequency_reported"], strict=True):
        plt.text(
            bar.get_width() + 1,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.1%}",
            va="center",
            fontsize=9,
        )
    _title(
        "Monte Carlo robustness of the intensity ranking",
        "Share of 1,000 Dirichlet weightings placing an authority in the top 12 | Gold = top 12 in all fixed schemes",
    )
    plt.xlabel("Top-12 frequency (%)")
    plt.xlim(0, max(85, top["monte_carlo_frequency_reported"].max() * 110))
    plt.grid(axis="x", alpha=0.18)
    _finish(Path(output_path))


def plot_evidence_led_ranking(frame: pd.DataFrame, output_path: str | Path) -> None:
    """Top 12 authorities under evidence-led scheme B."""

    top = frame.nsmallest(12, "rank_b").sort_values("score_b")
    colors = [GOLD if value == "Yes" else NAVY for value in top["top_12_all_three"]]
    plt.figure(figsize=(9, 6.2))
    bars = plt.barh(top["local_authority"], top["score_b"], color=colors)
    for bar, value in zip(bars, top["score_b"], strict=True):
        plt.text(
            bar.get_width() + 0.025,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.3f}",
            va="center",
            fontsize=9,
        )
    _title(
        "Evidence-led composite risk ranking",
        "Scheme B | weighted sum of six population z-scores | Gold = top 12 in all three schemes",
    )
    plt.xlabel("Composite risk score")
    plt.xlim(0, top["score_b"].max() * 1.12)
    plt.grid(axis="x", alpha=0.18)
    _finish(Path(output_path))
