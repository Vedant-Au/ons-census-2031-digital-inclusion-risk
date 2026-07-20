# Reference-output data

`reference_scores.csv` is a machine-readable extraction of the surviving Excel
reference sheet. It contains the 328 local-authority outputs used to verify the
regression, residuals, rankings and reported Monte Carlo frequencies.

It does **not** contain the four underlying demographic component columns.
Consequently, the repository can independently reproduce all quantities based
on the surviving columns, while the full six-component Monte Carlo simulation
requires the public raw inputs described in `data/raw/README.md`.
