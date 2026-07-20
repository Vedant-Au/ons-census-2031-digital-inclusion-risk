# Census 2031: Finding the Risk Hidden by the Response Rate

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Quality checks](https://github.com/Vedant-Au/ons-census-2031-digital-inclusion-risk/actions/workflows/quality.yml/badge.svg)](https://github.com/Vedant-Au/ons-census-2031-digital-inclusion-risk/actions/workflows/quality.yml)
[![Licence: MIT](https://img.shields.io/badge/Code-MIT-green.svg)](LICENSE)

**328 local authorities · six-person MSc consulting team · team lead**

## The apparent signal was mostly an operating decision

Online completion initially looked like the obvious way to identify digital-exclusion risk. The data challenged that assumption.

![Online completion share vs paper-first allocation](outputs/figures/online_vs_paper_first.png)

The reproduced regression shows that 2021 paper-first mode allocation explains **96.4% of the variation** in online completion. Ranking authorities on the raw response measure would therefore largely reproduce how households were contacted rather than isolate who may struggle with a digital-first Census.

That finding changed the model.

## From a misleading measure to three decision lenses

| Lens | Question | Implementation |
| --- | --- | --- |
| Intensity | Where do several risk factors accumulate? | Six standardised components |
| Scale | Where could more people be affected? | Potentially paper-dependent population |
| Underperformance | Where is completion below the contact-mode expectation? | Regression residual |

The result is not one “true” ranking. It is a set of signals for choosing research locations and interventions.

## Where I would investigate first

The group recommendation selects **Boston, Blaenau Gwent, Kingston upon Hull, Conwy and North Norfolk**. The five locations deliberately cover different combinations of intensity, scale and underperformance so field research does not repeatedly test the same context.

The first service intervention should target **initial contact**: automatic fallbacks, trusted messengers and resilient contact channels. Later form support cannot help a resident who never engages.

![Evidence-led top 12](outputs/figures/evidence_led_top12.png)

## Does the conclusion survive different weights?

Six authorities remain high-risk under all three fixed schemes. A further 1,000 random weight combinations test how often each authority stays in the top 12; Conwy appears in **76.8%** of reported draws.

![Weight sensitivity](outputs/figures/monte_carlo_robustness.png)

Changing ranks are informative: they show where judgement about criteria materially affects the answer. The model is a research-prioritisation tool, not a funding formula or prediction about individuals.

## Reproduce the investigation

Start with the [executive brief](docs/EXECUTIVE_BRIEF.md). The [methodology](docs/METHODOLOGY.md) and [data dictionary](docs/DATA_DICTIONARY.md) provide the statistical and lineage detail.

```bash
pip install -r requirements.txt
python scripts/reproduce_reference_outputs.py
python -m unittest discover -s tests -v
```

The guided notebook is in [`notebooks/01_reference_analysis.ipynb`](notebooks/01_reference_analysis.ipynb). Restoring the documented public raw inputs enables the complete six-component pipeline:

```bash
python scripts/run_full_analysis.py data/raw/ons_la_components.csv
```

## Reconstruction status

The original Python files were lost. This repository transparently reconstructs the analysis from the surviving 328-authority workbook rather than presenting itself as the submitted code or official ONS work. Regression, residuals, ranking intersections and figures are independently reproducible; exact six-component sensitivity requires the restored public inputs. See [RECONSTRUCTION_NOTES.md](RECONSTRUCTION_NOTES.md) and [validation report](docs/VALIDATION_REPORT.md).

Area-level results must not be used to infer individual characteristics. Official sources and licensing are documented in [DATA_LICENSE.md](DATA_LICENSE.md).
