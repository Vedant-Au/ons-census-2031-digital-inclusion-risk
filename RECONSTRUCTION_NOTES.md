# Reconstruction notes

## Provenance

This repository was recreated after the original Python files were lost. It is
based on:

- the submitted ONS Census 2031 group case report;
- the surviving `Analysis ReferenceSheet` workbook;
- the methodology and core code fragment printed in Appendix C.

The underlying case was assigned to the MSc group by Hippo and addressed an
ONS Census 2031 digital-inclusion challenge. It was a group academic exercise,
not personal employment by ONS or Hippo.

The repository intentionally separates reproducible code, surviving derived
outputs and unrecovered raw inputs. The original report and workbook are not
published here.

## What has been independently reproduced

- OLS regression of online share on paper-first share;
- expected-minus-actual underperformance residual;
- rankings under the three reported composite scores;
- intersection of the top 12 under all three schemes;
- figures based on the surviving reference outputs;
- reusable population z-score, weighted-index and Monte Carlo functions.

## What still requires the original public raw inputs

The surviving workbook does not include the raw age, deprivation and English-
proficiency columns for every authority. Therefore the exact six-component
z-score matrix and the reported 1,000-draw Monte Carlo frequencies cannot be
independently regenerated from the two surviving files alone.

The workbook also displays composite scores rounded to three decimal places,
while its rank columns were produced from higher-precision values. Re-ranking
the displayed scores therefore creates some tied or adjacent rank differences.
The decision-relevant top-12 intersection remains unchanged.

The reported frequencies are retained as reference outputs. Once the public
raw inputs are restored, `scripts/run_full_analysis.py` regenerates the full
pipeline with Dirichlet weights and seed 42.

## Methodological fidelity

- Population standard deviation: `ddof=0`.
- Underperformance: predicted online share minus actual online share.
- Three component-weight schemes match Table 1 of the report.
- Monte Carlo: 1,000 `Dirichlet(1, ..., 1)` draws, top 12 per draw, seed 42.
