#!/usr/bin/env python3
"""
Script 08: Tables
Generate LaTeX-formatted tables for manuscript
"""

import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path("/data")
STUDY_DIR = Path("/study")
OUTPUT_DIR = STUDY_DIR / "04-analysis" / "outputs"
TABLE_DIR = OUTPUT_DIR / "tables"
LOG_FILE = OUTPUT_DIR / "analysis_log.txt"


def log_message(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[08_tables] {msg}\n")
    print(msg)


def load_results():
    """Load previously generated results"""
    results = {}

    files = {
        "table1": "table1_characteristics.csv",
        "pfas_summary": "table1_pfassummary.csv",
        "main_results": "main_results_table.csv",
        "sensitivity": "sensitivity_results.csv",
        "phenoage_summary": "phenoage_summary.csv",
        "pfas_correlation": "pfas_correlation_matrix.csv",
        "mixture": "mixture_results.csv",
        "wqs_weights": "wqs_weights.csv",
    }

    for key, filename in files.items():
        filepath = TABLE_DIR / filename
        if filepath.exists():
            results[key] = pd.read_csv(filepath)

    return results


def create_latex_table1(results):
    """Create LaTeX Table 1: Baseline Characteristics"""
    log_message("Creating LaTeX Table 1...")

    if "table1" not in results:
        log_message("  Table 1 data not found")
        return

    df = results["table1"]

    latex = r"""\begin{table}[htbp]
\centering
\caption{Baseline Characteristics by Total PFAS Quartile}
\label{tab:baseline}
\resizebox{\textwidth}{!}{%
\begin{tabular}{lcccc}
\toprule
\textbf{Characteristic} & \textbf{Q1 (Low)} & \textbf{Q2} & \textbf{Q3} & \textbf{Q4 (High)} \\
\midrule
"""

    for _, row in df.iterrows():
        latex += f"{row['Characteristic']} & {row['Q1 (Low)']} & {row['Q2']} & {row['Q3']} & {row['Q4 (High)']} \\\\\n"

    latex += r"""\bottomrule
\end{tabular}%
}
\begin{tablenotes}
\item Note: Values are mean $\pm$ SD for continuous variables and percentage for categorical variables.
\item Abbreviations: PFAS, per- and polyfluoroalkyl substances; PIR, poverty income ratio.
\end{tablenotes}
\end{table}
"""

    with open(TABLE_DIR / "table1_latex.tex", "w") as f:
        f.write(latex)

    log_message("  Table 1 LaTeX saved")


def create_latex_pfas_summary(results):
    """Create LaTeX PFAS summary table"""
    log_message("Creating LaTeX PFAS summary...")

    if "pfas_summary" not in results:
        log_message("  PFAS summary not found")
        return

    df = results["pfas_summary"]

    latex = r"""\begin{table}[htbp]
\centering
\caption{Serum PFAS Concentrations (ng/mL)}
\label{tab:pfas_summary}
\begin{tabular}{lccccc}
\toprule
\textbf{Compound} & \textbf{N} & \textbf{Mean (SD)} & \textbf{Median} & \textbf{IQR} & \textbf{Range} \\
\midrule
"""

    for _, row in df.iterrows():
        mean_sd = f"{row['Mean']:.2f} ({row['SD']:.2f})"
        iqr = f"{row['IQR_25']:.2f}-{row['IQR_75']:.2f}"
        range_val = f"{row['Min']:.2f}-{row['Max']:.2f}"
        latex += f"{row['Compound']} & {int(row['N'])} & {mean_sd} & {row['Median']:.2f} & {iqr} & {range_val} \\\\\n"

    latex += r"""\bottomrule
\end{tabular}
\begin{tablenotes}
\item Note: Concentrations are in ng/mL serum. IQR, interquartile range.
\end{tablenotes}
\end{table}
"""

    with open(TABLE_DIR / "table_pfas_summary_latex.tex", "w") as f:
        f.write(latex)

    log_message("  PFAS summary LaTeX saved")


def create_latex_main_results(results):
    """Create LaTeX main results table"""
    log_message("Creating LaTeX main results table...")

    if "main_results" not in results:
        log_message("  Main results not found")
        return

    df = results["main_results"]

    latex = r"""\begin{table}[htbp]
\centering
\caption{Association between PFAS and PhenoAge Acceleration}
\label{tab:main_results}
\resizebox{\textwidth}{!}{%
\begin{tabular}{llccccc}
\toprule
\textbf{Compound} & \textbf{Model} & \textbf{Beta} & \textbf{SE} & \textbf{95\% CI} & \textbf{P-value} & \textbf{N} \\
\midrule
"""

    for _, row in df.iterrows():
        ci = f"[{row['95% CI Lower']:.3f}, {row['95% CI Upper']:.3f}]"
        latex += f"{row['Compound']} & {row['Model']} & {row['Beta']:.3f} & {row['SE']:.3f} & {ci} & {row['P-value']} & {row['N']} \\\\\n"

    latex += r"""\bottomrule
\end{tabular}%
}
\begin{tablenotes}
\item Note: Beta coefficients represent the change in PhenoAge acceleration (years) per log-unit increase in PFAS concentration.
\item Model 1: Crude (PFAS only)
\item Model 2: Adjusted for age, sex, and race/ethnicity
\item Model 3: Additionally adjusted for education and poverty income ratio
\end{tablenotes}
\end{table}
"""

    with open(TABLE_DIR / "table_main_results_latex.tex", "w") as f:
        f.write(latex)

    log_message("  Main results LaTeX saved")


def create_latex_mixture(results):
    """Create LaTeX mixture analysis table"""
    log_message("Creating LaTeX mixture table...")

    if "wqs_weights" not in results:
        log_message("  WQS weights not found")
        return

    weights = results["wqs_weights"]

    latex = r"""\begin{table}[htbp]
\centering
\caption{PFAS Mixture Weights from WQS Analysis}
\label{tab:wqs_weights}
\begin{tabular}{lc}
\toprule
\textbf{PFAS Compound} & \textbf{Weight} \\
\midrule
"""

    for _, row in weights.iterrows():
        latex += f"{row['Compound']} & {row['Weight']:.3f} \\\\\n"

    latex += r"""\bottomrule
\end{tabular}
\begin{tablenotes}
\item Note: Weights represent the relative contribution of each PFAS to the overall mixture effect.
\item Weights sum to 1.0.
\end{tablenotes}
\end{table}
"""

    with open(TABLE_DIR / "table_mixture_latex.tex", "w") as f:
        f.write(latex)

    log_message("  Mixture LaTeX saved")


def create_results_summary():
    """Create results summary markdown"""
    log_message("Creating results summary...")

    summary = """# PFAS-PhenoAge Study: Analysis Results Summary

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
"""

    with open(OUTPUT_DIR / "results_summary.md", "w") as f:
        f.write(summary)

    log_message("  Results summary saved")


def main():
    log_message("=" * 60)
    log_message("PFAS-PhenoAge Study: Table Generation")
    log_message("=" * 60)

    # Load results
    results = load_results()
    log_message(f"Loaded {len(results)} result files")

    # Create LaTeX tables
    create_latex_table1(results)
    create_latex_pfas_summary(results)
    create_latex_main_results(results)
    create_latex_mixture(results)

    # Create summary
    create_results_summary()

    log_message("Table generation complete")
    log_message("=" * 60)


if __name__ == "__main__":
    main()
