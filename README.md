# Census 2031 Digital Inclusion Risk

**A decision model for prioritising where a digital-first Census could require the most careful research and assisted-digital support.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Quality checks](https://github.com/Vedant-Au/ons-census-2031-digital-inclusion-risk/actions/workflows/quality.yml/badge.svg)](https://github.com/Vedant-Au/ons-census-2031-digital-inclusion-risk/actions/workflows/quality.yml)
[![Licence: MIT](https://img.shields.io/badge/Code-MIT-green.svg)](LICENSE)

**Role:** Team Lead for a six-person MSc consulting team  
**Scope:** 328 local authorities in England and Wales  
**Client brief:** ONS Census 2031 case assigned by Hippo

## The finding that changed the analysis

Raw online completion looked like an obvious proxy for digital exclusion. It was not.

The reproduced regression shows that 2021 paper-first mode allocation explains **96.4% of the variation** in online completion across 328 authorities. Treating the observed completion rate as an independent measure would therefore largely reproduce an operational allocation decision rather than isolate inclusion risk.

![Online completion share vs paper-first allocation](outputs/figures/online_vs_paper_first.png)

I used the regression residual as one component of a broader framework, then combined three decision lenses:

1. **Intensity** - six standardised risk components.
2. **Scale** - the size of the potentially paper-dependent population.
3. **Underperformance** - online completion below the level predicted by mode allocation.

## Recommendation

Prioritise a deliberately varied five-location research set from the group report: **Boston, Blaenau Gwent, Kingston upon Hull, Conwy and North Norfolk**. Together they cover different combinations of intensity, population scale and underperformance, reducing the risk of testing the same failure mode repeatedly.

The first intervention point should be **initial contact**. Later form or digital-skills support cannot help residents who never engage, so research should first test automatic fallbacks, trusted messengers and contact-channel resilience.

## Robustness

Six authorities remain high-risk under all three fixed weighting schemes: Boston, Blaenau Gwent, Denbighshire, Conwy, Carmarthenshire and Ceredigion.

![Evidence-led top 12](outputs/figures/evidence_led_top12.png)

The implementation also tests 1,000 alternative criterion-weight combinations. Conwy appears in the top 12 in **76.8%** of the reported draws; the ordering changes enough to show that the model should guide investigation, not create false precision.

![Monte Carlo robustness](outputs/figures/monte_carlo_robustness.png)

## What I led

I structured the decision, coordinated the six-person analysis, challenged the interpretation of the response metric and translated the quantitative ranking into intervention choices. The published implementation adds reproducible code, a guided notebook, validation checks, deterministic sensitivity testing and 12 automated tests.

Start with the [executive brief](docs/EXECUTIVE_BRIEF.md), then review the [methodology](docs/METHODOLOGY.md) and [validation report](docs/VALIDATION_REPORT.md).

## Reproduce

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/reproduce_reference_outputs.py
python -m unittest discover -s tests -v
```

To run the full six-component pipeline after restoring the public raw inputs:

```bash
python scripts/run_full_analysis.py data/raw/ons_la_components.csv
```

```text
notebooks/                 Guided analytical walkthrough
docs/                      Executive brief, methodology, dictionary and QA
data/reference/            Surviving 328-authority derived outputs
data/raw/                  Expected raw-data schema and source guidance
outputs/                   Recreated figures, tables and validation record
scripts/                   Reproduction entry points
src/ons_risk_index/        Tested analysis and visualisation package
tests/                     Unit, edge-case and data-quality checks
```

## Evidence boundary

The original Python files were lost, so this repository is a disclosed reconstruction rather than the submitted code or official ONS analysis. The surviving workbook preserves final scores, ranks and sensitivity frequencies but not every raw demographic component. The regression, residuals, ranking intersection and figures are independently reproducible; the exact six-component sensitivity result requires restored public inputs. Results are area-level investigation signals and must not be used to infer individual characteristics.

Official sources and licensing are documented in [DATA_LICENSE.md](DATA_LICENSE.md).
