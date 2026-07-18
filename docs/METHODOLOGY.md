# Methodology

## Unit of analysis and outcome

The analytical grain is one row per local authority in England and Wales (**n = 328**). The outcome is the percentage of completed household returns submitted online in Census 2021. The allocation variable is the percentage of local-authority LSOAs designated paper-first.

## 1. Adjust for the 2021 contact strategy

A simple OLS model estimates the relationship between paper-first allocation and online completion:

$$
\widehat{Online}_i = \beta_0 + \beta_1 PaperFirst_i
$$

The risk-oriented residual is defined as:

$$
Underperformance_i = \widehat{Online}_i - Online_i
$$

Positive values mean online completion was below the level predicted by allocation. This sign convention makes a larger value consistently represent greater risk.

The reproduced model is:

$$
\widehat{Online}_i = 94.552 - 0.546 \times PaperFirst_i
$$

with $R^2 = 0.964$ across 328 authorities.

## 2. Standardise the six risk components

Each component is converted to a population z-score using `ddof=0`:

$$
z_{ij} = \frac{x_{ij}-\mu_j}{\sigma_j}
$$

The components are paper-first share, ages 65–74, ages 75+, deprivation on two or more dimensions, limited English proficiency, and underperformance.

## 3. Build composite scores

For scheme $s$, the composite score is:

$$
Score_{is} = \sum_{j=1}^{6} w_{js} z_{ij}, \qquad \sum_j w_{js}=1
$$

| Component | A: balanced | B: evidence-led | C: stress test |
| --- | ---: | ---: | ---: |
| Paper-first share | 0.20 | 0.30 | 0.15 |
| Age 65–74 | 0.10 | 0.10 | 0.05 |
| Age 75+ | 0.10 | 0.15 | 0.10 |
| Deprived on 2+ dimensions | 0.20 | 0.20 | 0.15 |
| Limited English proficiency | 0.20 | 0.15 | 0.15 |
| Underperformance | 0.20 | 0.10 | 0.40 |

Authorities are ranked in descending score order. Scheme B is used as the main evidence-led view; agreement across schemes is treated as stronger evidence than any exact rank.

## 4. Test weighting sensitivity

For each of 1,000 draws, six non-negative weights are sampled from a uniform simplex:

$$
\mathbf{w}^{(m)} \sim Dirichlet(1,1,1,1,1,1)
$$

Each authority's robustness is the proportion of draws in which it appears in the top 12. A fixed random seed of 42 makes the procedure deterministic once the component data are available.

## 5. Convert a ranking into a decision portfolio

The final selection uses three lenses:

- **Intensity:** the composite score and cross-scheme agreement.
- **Scale:** the number of residents potentially affected.
- **Underperformance:** outcome below the level expected from paper-first allocation.

The portfolio rule deliberately chooses distinct contexts and failure modes. It is a research-prioritisation heuristic, not a funding formula or prediction of individual behaviour.

## Assumptions

- Local-authority percentages are comparable at the stated 2021 reference period.
- Population standardisation is appropriate because the analysis covers the complete 328-authority frame used in the report.
- Equal-simplex Dirichlet draws are a sensitivity device, not a probabilistic statement about the true weights.
- The allocation relationship is descriptive and should not be interpreted causally.
- Area-level results cannot support individual-level inference.
