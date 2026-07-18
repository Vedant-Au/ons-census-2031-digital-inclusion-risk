# Data dictionary and lineage

## Surviving reference dataset

File: `data/reference/reference_scores.csv`  
Grain: one row per local authority in England and Wales  
Rows: 328  
Purpose: preserve the derived outputs that can be checked against the submitted group report

| Field | Type | Unit / allowed values | Meaning | Lineage |
| --- | --- | --- | --- | --- |
| `local_authority` | text | unique authority name | Analytical entity | Surviving workbook |
| `online_pct` | number | 0–100 percentage points | Completed household returns submitted online | ONS-derived reference input |
| `paper_first_pct` | number | 0–100 percentage points | Share of an authority's LSOAs allocated paper-first | ONS-derived reference input |
| `underperformance_reported` | number | percentage-point residual | Predicted online share minus actual online share | Reported derived output |
| `score_a` | number | weighted z-score | Balanced composite score | Reported derived output, displayed to 3 decimals |
| `score_b` | number | weighted z-score | Evidence-led composite score | Reported derived output, displayed to 3 decimals |
| `score_c` | number | weighted z-score | Underperformance stress-test score | Reported derived output, displayed to 3 decimals |
| `rank_a` | integer | 1–328 | Descending rank under scheme A | Workbook calculation using higher precision |
| `rank_b` | integer | 1–328 | Descending rank under scheme B | Workbook calculation using higher precision |
| `rank_c` | integer | 1–328 | Descending rank under scheme C | Workbook calculation using higher precision |
| `top_12_all_three` | category | `Yes` or blank | Top 12 under every fixed scheme | Reported derived output |
| `monte_carlo_frequency_reported` | number | 0–1 proportion | Share of 1,000 random weightings in the top 12 | Reported derived output |

## Expected full raw schema

The full pipeline in `scripts/run_full_analysis.py` expects one row per authority with these fields:

| Field | Unit | Direction in risk index |
| --- | --- | --- |
| `local_authority` | name | identifier |
| `online_pct` | percentage points | used to calculate residual |
| `paper_first_pct` | percentage points | higher = greater risk |
| `aged_65_74_pct` | percentage points | higher = greater risk proxy |
| `aged_75_plus_pct` | percentage points | higher = greater risk proxy |
| `deprived_2plus_pct` | percentage points | higher = greater risk proxy |
| `limited_english_pct` | percentage points | higher = greater risk proxy |

`underperformance` is then calculated by the pipeline. Percentages must be numeric, finite and use a consistent 0–100 scale.

## Data-quality rules

- Exactly 328 unique, non-empty local-authority names in the reference frame.
- `online_pct` and `paper_first_pct` must be within 0–100.
- Ranks must be integers within 1–328.
- Monte Carlo frequency must be within 0–1.
- Regression inputs must be finite and have at least three observations.
- Any production refresh should reconcile authority codes and boundary changes, not names alone.

## Known limitations

The reference CSV is a derived artefact, not a substitute for the original raw public tables. Four demographic component columns are not present, and composite scores have been rounded. The submitted report and original workbook are excluded from the repository.
