# Validation report

**Overall status: Share with caveats**  
**Validated scope:** reconstructed analysis and surviving 328-authority reference outputs  
**Not validated:** independent end-to-end regeneration of all six raw components and reported Monte Carlo frequencies

## Verified checks

| Area | Check | Result |
| --- | --- | --- |
| Data shape | 328 local-authority rows loaded | Pass |
| Entity integrity | Authority names are populated and unique | Pass |
| Percentage bounds | Online and paper-first values are within 0–100 | Pass |
| OLS regression | Intercept 94.552, slope −0.546, R² 0.964, n=328 | Pass |
| Residual reconciliation | Maximum absolute difference from workbook <0.001 percentage points | Pass |
| Fixed-scheme weights | Each scheme is non-negative and sums to 1 | Pass |
| Cross-scheme result | Recalculated top-12 intersection equals the reported six-authority set | Pass |
| Monte Carlo reference | Frequencies are numeric and bounded 0–1 | Pass as a retained output |
| Automated tests | 12 unit, edge-case and reference-data checks | Pass |

## Reconciliation caveat

Only 300 of 328 displayed ranks for scheme A, 301 for B and 297 for C exactly reproduce from the three-decimal score columns. The workbook ranks were calculated from higher-precision values. This is expected rounding behaviour: adjacent positions can tie or swap, while the decision-relevant top-12 intersection remains unchanged.

## Blocking evidence gaps

- The surviving workbook does not contain the raw age 65–74, age 75+, deprivation and limited-English columns for all authorities.
- The exact z-score matrix and 1,000-draw Monte Carlo frequencies cannot therefore be independently regenerated from the preserved files.
- The five-location research set comes from the group report's combined quantitative and qualitative reasoning; only the surviving quantitative components are represented here.

## Interpretation risks

- The strong allocation relationship is descriptive, not causal.
- Composite weights encode judgement; sensitivity frequencies show robustness to alternate weights but do not establish “true” risk.
- Local-authority averages can conceal within-area variation.
- Area risk must not be used to label individuals or determine eligibility without additional evidence.

## Release recommendation

The repository is suitable for methodology review and exploratory prioritisation **if the limitations remain prominent**. Before operational use, restore and refresh the official raw inputs, rerun the full pipeline, reconcile geographic boundaries, obtain subject-matter review and document stakeholder acceptance criteria.
