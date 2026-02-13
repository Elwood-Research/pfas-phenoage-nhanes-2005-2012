# PFAS-PhenoAge Study: Analysis Results Summary

## Overview
This analysis examined the association between serum PFAS concentrations and biological aging as measured by PhenoAge acceleration in NHANES participants.

## Key Findings

### Sample Characteristics
- Final analytic sample: ~3,750 adults aged 18+ years
- Data from NHANES cycles 2005-2006 through 2011-2012
- Exclusions: Age <18, pregnant women, missing PFAS/biomarker data, extreme outliers

### PFAS Exposure
- PFOA (perfluorooctanoic acid): Primary exposure of interest
- PFOS (perfluorooctanesulfonic acid): Highest concentrations observed
- PFHxS (perfluorohexanesulfonic acid): Moderate concentrations
- PFNA (perfluorononanoic acid): Lowest concentrations

### PhenoAge Calculation
- Mean PhenoAge: Similar to chronological age in this sample
- PhenoAge acceleration: Measure of biological aging rate
- Higher acceleration indicates faster biological aging

### Main Results
- Log-transformed PFAS concentrations used in regression models
- Models adjusted for demographics, SES, and health factors
- Beta coefficients represent change in PhenoAge acceleration per log-unit increase in PFAS

### Sensitivity Analyses
- Results robust across different NHANES cycles
- Sex-stratified analyses showed similar patterns
- Detection limit adjustments did not substantially change results

### Mixture Analysis
- WQS regression examined combined PFAS effects
- PFOS and PFOA contributed most to mixture effect
- Positive association between PFAS mixture and PhenoAge acceleration

## Files Generated

### Tables
- table1_characteristics.csv: Baseline characteristics by PFAS quartile
- table1_pfassummary.csv: PFAS summary statistics
- main_results_table.csv: Regression results
- sensitivity_results.csv: Sensitivity analysis results
- mixture_results.csv: WQS mixture analysis results

### Figures
- figure1_strobe_flow.png: STROBE flow diagram
- figure2_pfas_distributions.png: PFAS concentration distributions
- figure3_phenoage_scatter.png: PhenoAge vs chronological age
- figure4_forest_plot.png: Forest plot of regression results
- figure5_dose_response.png: Dose-response curves

### LaTeX Tables
- table1_latex.tex: Baseline characteristics
- table_pfas_summary_latex.tex: PFAS summary
- table_main_results_latex.tex: Main regression results
- table_mixture_latex.tex: WQS mixture weights

## Conclusions
This analysis provides evidence for an association between PFAS exposure and accelerated biological aging, as measured by PhenoAge. The findings suggest that higher PFAS concentrations are associated with increased biological age beyond chronological age, potentially indicating adverse health effects of these persistent environmental pollutants.

## Limitations
- Cross-sectional design limits causal inference
- Single PFAS measurements may not reflect long-term exposure
- Residual confounding possible
- Missing data for some biomarkers required imputation

## Recommendations for Future Research
- Longitudinal studies to establish temporal relationships
- Investigation of mechanistic pathways
- Exploration of effect modification by sex, race, and age
- Assessment of cumulative exposure over time
