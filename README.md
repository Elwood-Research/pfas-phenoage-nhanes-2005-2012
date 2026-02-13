# Paradoxical Inverse Associations Between Serum PFAS and Biological Aging in U.S. Adults

**NHANES 2005-2012 Cross-Sectional Analysis**

## Author
**Elwood Research**  
📧 elwoodresearch@gmail.com  
📅 February 13, 2026

---

## Abstract

**Background:** Per- and polyfluoroalkyl substances (PFAS) are persistent environmental pollutants with known toxicological effects. Recent evidence suggests associations with accelerated biological aging, but findings remain inconsistent.

**Objective:** We examined associations between serum PFAS concentrations and biological aging measured by PhenoAge in a nationally representative sample of U.S. adults.

**Methods:** Cross-sectional analysis of 3,198 adults aged ≥18 years from NHANES 2005-2012. Serum concentrations of four legacy PFAS (PFOA, PFOS, PFHxS, PFNA) were measured. PhenoAge, a validated biomarker-based measure of biological aging, was calculated using the Levine et al. (2018) algorithm. Survey-weighted linear regression models examined associations between log-transformed PFAS concentrations and PhenoAge acceleration, adjusting for demographics and socioeconomic factors.

**Results:** Median serum concentrations were: PFOA 3.30 ng/mL, PFOS 12.30 ng/mL, PFHxS 1.60 ng/mL, and PFNA 1.10 ng/mL. Mean PhenoAge acceleration was -1.80 ± 6.00 years. In fully adjusted models, all four PFAS showed significant *inverse* associations with PhenoAge acceleration:
- PFOA: β = -0.850 (95% CI: -1.202 to -0.498), p < 0.001
- PFOS: β = -0.420 (95% CI: -0.722 to -0.117), p = 0.007
- PFHxS: β = -0.605 (95% CI: -0.860 to -0.350), p < 0.001
- PFNA: β = -0.560 (95% CI: -0.924 to -0.196), p = 0.003

**Conclusions:** Contrary to hypotheses, higher PFAS exposure was associated with *lower* PhenoAge acceleration, suggesting paradoxically slower biological aging. These unexpected findings likely reflect survival bias, reverse causation, and limitations of cross-sectional designs rather than protective effects. The discrepancy with prior longitudinal evidence (Yan et al. 2025) underscores the need for careful interpretation of cross-sectional PFAS-aging associations and highlights potential methodological pitfalls in biological aging research.

**Keywords:** PFAS, PhenoAge, biological aging, NHANES, cross-sectional bias, survival bias

---

## Key Findings

### 🔴 Paradoxical Inverse Associations
All four legacy PFAS compounds showed **significant inverse associations** with PhenoAge acceleration:
- Higher PFAS → Lower biological aging (opposite of expected!)
- Robust across all three adjustment models
- Monotonic dose-response relationships

### ⚠️ Important Interpretation
**These findings DO NOT suggest PFAS are protective.**

Likely explanations for paradoxical results:
1. **Survival bias**: Individuals with both high PFAS and poor health may die before study enrollment
2. **Reverse causation**: Better kidney function → higher PFAS retention
3. **Unmeasured confounding**: Socioeconomic status, lifestyle, healthcare access
4. **Sample selection bias**: Complete-case analysis selecting healthier participants
5. **Cross-sectional limitations**: Cannot establish temporal sequence

### 📊 Comparison to Literature
- **Yan et al. (2025)**: Longitudinal UK Biobank study found *positive* associations
- **This study**: Cross-sectional NHANES found *inverse* associations
- **Implication**: Study design profoundly affects PFAS-aging associations

### 🔬 Methodological Contribution
- Identified and corrected critical bug in PhenoAge calculation (RDW variable)
- Demonstrates importance of cross-sectional vs. longitudinal designs
- Highlights need for cautious interpretation of biological aging biomarkers

---

## Repository Structure

```
pfas-phenoage-2026-02-13/
├── README.md                          # This file
├── PROJECT.md                         # Research question and objectives
├── STATE.md                           # Study state tracker
├── 01-literature/                     # Literature review
│   ├── references.bib                 # Bibliography (60+ references)
│   └── literature-review.md           # Synthesis of prior evidence
├── 02-variables/                      # Variable selection
│   ├── variable-selection.md          # PFAS and biomarker variables
│   └── final-variables.json           # Machine-readable variable list
├── 03-methods/                        # Methods documentation
│   └── methods.md                     # Detailed statistical methods
├── 04-analysis/                       # Analysis scripts and outputs
│   ├── scripts/
│   │   └── complete_analysis.py       # Unified analysis pipeline
│   └── outputs/
│       ├── figures/                   # 5 figures (STROBE, distributions, etc.)
│       ├── tables/                    # Summary tables
│       └── results_summary.md         # Key numerical results
├── 05-conclusion/                     # Synthesis and interpretation
│   └── synthesis.md                   # Detailed discussion of findings
├── manuscript/                        # Publication-ready manuscript
│   └── manuscript.pdf                 # 21-page PDF (figures, tables, references)
└── presentation/                      # Conference presentation
    └── presentation.pdf               # 10-slide Beamer presentation
```

---

## How to Reproduce

### Prerequisites
- Docker (for isolated analysis execution)
- Python 3.9+ (in Docker container)
- LaTeX distribution (TinyTeX or TeX Live)
- NHANES processed data (2005-2012 cycles)

### Data Requirements
This study uses locally processed NHANES data:
- **Demographics**: DEMO_D, DEMO_E, DEMO_F, DEMO_G
- **PFAS**: PFC_D, PFC_E, PFC_F, PFC_G
- **Biomarkers**: BIOPRO_D-G, CRP_D-G, CBC_D-G, GLU_D-G

### Step 1: Run Analysis (Docker Vault)
```bash
# Navigate to study directory
cd studies/pfas-phenoage-2026-02-13

# Run analysis in isolated Docker container (no network access)
docker run --rm \
  --network none \
  -v "/path/to/NHANES_BOT_ORIGINAL/Processed Data/Data:/data:ro" \
  -v "$(pwd):/study" \
  nhanes-analysis-vault \
  python3 /study/04-analysis/scripts/complete_analysis.py

# Outputs saved to: 04-analysis/outputs/
```

### Step 2: Compile Manuscript
```bash
cd manuscript
pdflatex manuscript.tex
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex

# Output: manuscript.pdf (21 pages)
```

### Step 3: Compile Presentation
```bash
cd presentation
pdflatex presentation.tex
pdflatex presentation.tex

# Output: presentation.pdf (10 slides)
```

---

## Files and Outputs

### Analysis Outputs (`04-analysis/outputs/`)

#### Figures
1. **figure1_strobe_flow.png**: STROBE diagram showing sample selection
2. **figure2_pfas_distributions.png**: Log-transformed PFAS concentration distributions
3. **figure3_phenoage_scatter.png**: PhenoAge vs. chronological age
4. **figure4_forest_plot.png**: Forest plot of main regression results
5. **figure5_dose_response.png**: Dose-response curves for all PFAS

#### Tables
- **table_exclusion_flow.csv**: Sample exclusion criteria and N
- **table_characteristics_by_pfas.csv**: Baseline characteristics by PFAS quartile
- **table_pfas_summary.csv**: PFAS concentration descriptive statistics
- **table_main_results.csv**: Main regression results (3 models × 4 PFAS)
- **table_sensitivity_results.csv**: Sensitivity analyses (sex-stratified, BMI-adjusted, continuous age)
- **table_mixture_weights.csv**: WQS mixture analysis component weights

#### Results Summary
- **results_summary.md**: Comprehensive numerical results with interpretation

### Manuscript (`manuscript/`)
- **manuscript.pdf**: 21-page publication-ready manuscript
  - Title, abstract, keywords
  - Introduction (background, biological aging, PFAS toxicology)
  - Methods (data source, sample, variables, statistical analysis)
  - Results (sample characteristics, main findings, sensitivity analyses)
  - Discussion (interpretation, comparison to literature, limitations, implications)
  - References (60+ citations)
  - Figures and tables embedded

### Presentation (`presentation/`)
- **presentation.pdf**: 10-slide Beamer presentation
  - Background and motivation
  - Research question and hypothesis
  - Methods overview
  - Sample characteristics
  - Main results (forest plot, dose-response)
  - Discussion of paradoxical findings
  - Conclusions and future directions

---

## Study Limitations

1. **Cross-sectional design**: Cannot establish temporal sequence or causality
2. **Survival bias**: Healthiest individuals with high PFAS exposure may be overrepresented
3. **Reverse causation**: Kidney function may affect both PFAS retention and PhenoAge
4. **Complete-case analysis**: Excludes participants with missing data (may select healthier subsample)
5. **Residual confounding**: Unmeasured lifestyle, dietary, and healthcare factors
6. **PhenoAge limitations**: Single biomarker composite; may not capture all aging dimensions
7. **Legacy PFAS only**: Does not include newer PFAS replacements
8. **U.S. population**: May not generalize to other populations with different PFAS exposure profiles

---

## Future Research Directions

1. **Longitudinal studies** with repeated PFAS and aging biomarker measurements
2. **Multi-biomarker approaches** integrating epigenetic clocks (DNAmAge, GrimAge), telomere length
3. **Life-course perspective** examining early-life PFAS exposure effects on later-life aging
4. **Mediation analysis** to identify biological pathways (oxidative stress, inflammation, kidney function)
5. **Non-linear modeling** to detect threshold effects or U-shaped relationships
6. **Mixture analysis** of legacy + replacement PFAS compounds
7. **Prospective cohorts** minimizing survival and selection biases
8. **Replication** in diverse populations with varying PFAS exposure levels

---

## Citation

If you use this analysis or code, please cite:

```
Elwood Research. (2026). Paradoxical Inverse Associations Between Serum PFAS 
Concentrations and Biological Aging in U.S. Adults: A Cross-Sectional Analysis 
of NHANES 2005-2012. GitHub: Elwood-Research/pfas-phenoage-nhanes-2005-2012
```

---

## License

This work is released under the MIT License. See LICENSE file for details.

---

## Contact

For questions, collaborations, or feedback:

📧 **Email**: elwoodresearch@gmail.com  
🐙 **GitHub**: [Elwood-Research](https://github.com/Elwood-Research)

---

## Acknowledgments

- **Data Source**: CDC National Health and Nutrition Examination Survey (NHANES)
- **PhenoAge Algorithm**: Levine et al. (2018), *Aging*
- **Inspiration**: Yan et al. (2025) PFAS-epigenetic aging study in UK Biobank
- **Infrastructure**: Docker-based analysis vault for data privacy and reproducibility

---

**⚠️ IMPORTANT DISCLAIMER**: This study found inverse associations between PFAS and biological aging that contradict toxicological evidence and longitudinal studies. These findings likely reflect methodological limitations (survival bias, reverse causation, cross-sectional design) rather than true protective effects. PFAS remain harmful environmental pollutants with established adverse health effects. This study serves as a cautionary example of potential biases in cross-sectional biological aging research.
