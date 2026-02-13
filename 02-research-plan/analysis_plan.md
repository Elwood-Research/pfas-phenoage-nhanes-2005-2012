# Analysis Plan: PFAS Exposure and PhenoAge Biological Aging

## Overview

This document details the analytic approach for investigating associations between serum PFAS concentrations and biological aging as measured by PhenoAge in NHANES participants. All analyses will be conducted using Python within the NHANES Analysis Vault Docker environment, following STROBE guidelines for observational studies.

---

## Sample Inclusion and Exclusion Criteria

### Inclusion Criteria

| Criterion | Definition | Rationale |
|-----------|------------|-----------|
| Age | ≥18 years at examination | Adult population focus; PhenoAge validated in adults |
| PFAS measurement | At least one PFAS compound measured in serum | Exposure assessment requirement |
| PhenoAge components | Complete data for ≥8 of 9 PhenoAge biomarkers | Outcome calculation requirement |
| Survey weights | Valid subsample weight (WTSA2YR) | Population inference requirement |

### Exclusion Criteria

| Criterion | Definition | Rationale | Expected Exclusions |
|-----------|------------|-----------|---------------------|
| Pregnancy | Self-reported pregnancy or positive pregnancy test | Physiological changes affect biomarkers | ~300-400 |
| Missing demographics | Missing age, sex, or race/ethnicity | Essential covariates | ~50-100 |
| Extreme outliers | |z| > 4 for continuous key variables | Data quality | ~100-200 |
| Missing confounders | Missing >2 key confounders | Model completeness | ~200-300 |

### STROBE Flow Diagram

```
Initial NHANES Participants (1999-2000, 2005-2012)
    │
    ├── Total participants with PFAS measurement: ~7,500
    │
    ├── Exclusions:
    │   ├── Age <18 years: ~2,000
    │   ├── Pregnant: ~400
    │   ├── Missing PhenoAge components: ~500
    │   ├── Missing critical covariates: ~300
    │   └── Extreme outliers: ~200
    │
    └── Final Analytic Sample: ~4,000-5,000
```

---

## PhenoAge Calculation Method

### Algorithm Implementation

PhenoAge will be calculated following the validated method of Levine et al. (2018) using the following steps:

#### Step 1: Calculate Mortality Score

```python
# Linear predictor (x) calculation
x = (-19.9067 + 
     0.0237 * albumin_gL +          # Albumin (g/L)
     0.0229 * creatinine_umolL +     # Creatinine (μmol/L)
     0.1274 * glucose_mmolL +        # Glucose (mmol/L)
     0.1705 * ln_crp_mgL +           # ln(CRP) (mg/L)
     0.0441 * lymphocyte_pct +       # Lymphocyte %
     0.0681 * mcv_fL +               # MCV (fL)
     0.0754 * rdw_pct +              # RDW (%)
     0.0392 * alp_UL +               # Alkaline phosphatase (U/L)
     0.1434 * wbc_10e9L)             # WBC (10^9/L)

# Mortality score
mort_score = 1 - exp(-exp(x / 0.09165))
```

#### Step 2: Calculate PhenoAge

```python
import numpy as np

phenoage = 141.50 + (np.log(-0.00553 * np.log(1 - mort_score)) / 0.09165)
```

#### Step 3: Calculate PhenoAge Acceleration

```python
# Residual method
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(chronological_age.reshape(-1, 1), phenoage)
predicted_phenoage = model.predict(chronological_age.reshape(-1, 1))
phenoage_acceleration = phenoage - predicted_phenoage
```

### Variable Transformations

| Component | NHANES Variable | Unit Conversion | Notes |
|-----------|-----------------|-----------------|-------|
| Albumin | LBDSALSI | g/L (use as-is) | If g/dL: multiply by 10 |
| Creatinine | LBDSCRSI | μmol/L (use as-is) | If mg/dL: multiply by 88.4 |
| Glucose | LBDGLUSI | mmol/L (use as-is) | If mg/dL: multiply by 0.0555 |
| CRP | LBXCRP | mg/L (use as-is) | Natural log transform |
| Lymphocyte % | LBXLYPCT | % (use as-is) | Calculate from diff count |
| MCV | LBXMCVSI | fL (use as-is) | Standard CBC parameter |
| RDW | LBXRDW | % (use as-is) | Standard CBC parameter |
| ALP | LBXSAPSI | U/L (use as-is) | Standard chemistry |
| WBC | LBXWBCSI | 10⁹/L (use as-is) | Standard CBC parameter |

### Handling Missing Components

- **Complete case analysis**: Require all 9 components (reduces sample size)
- **Imputation approach**: Multiple imputation by chained equations (MICE) for ≤1 missing component
- **Sensitivity analysis**: Compare results between complete-case and imputed datasets

---

## PFAS Exposure Assessment

### Individual PFAS Compounds

| Compound | NHANES Variable | Detection Limit Handling |
|----------|-----------------|-------------------------|
| PFOA | LBXPFOA | <LOD: LOD/√2 |
| PFOS | LBXPFOS | <LOD: LOD/√2 |
| PFHxS | LBXPFHS | <LOD: LOD/√2 |
| PFNA | LBXPFNA | <LOD: LOD/√2 (cycles D-G only) |

### Exposure Metrics

1. **Continuous (log-transformed)**:
   ```python
   ln_pfas = np.log(pfas_concentration + 0.01)  # Small offset for zeros
   ```

2. **Standardized (z-scores)**:
   ```python
   pfas_zscore = (pfas - mean(pfas)) / sd(pfas)
   ```

3. **Categorical (tertiles/quartiles)**:
   ```python
   pfas_tertile = pd.qcut(pfas, q=3, labels=['T1', 'T2', 'T3'])
   ```

### PFAS Mixture Assessment

#### 1. Summed Concentrations

```python
# Sum of detected compounds (molar basis preferable)
pfas_sum = pfoa + pfos + pfhxs + pfna  # Only for cycles with all 4
```

#### 2. Principal Component Analysis

```python
from sklearn.decomposition import PCA

pfas_matrix = np.column_stack([ln_pfoa, ln_pfos, ln_pfhxs, ln_pfna])
pca = PCA(n_components=2)
pfas_pc1 = pca.fit_transform(pfas_matrix)[:, 0]
```

#### 3. Weighted Quantile Sum (WQS) Regression

```python
# Using WQS package or custom implementation
# Requires bootstrap validation (1000 iterations)
```

---

## Descriptive Statistics Plan

### Table 1: Population Characteristics

| Variable | Categories/Units | Statistic |
|----------|-----------------|-----------|
| **Demographics** | | |
| Age | Years | Mean ± SD, Median (IQR) |
| Sex | Male/Female | n (%) |
| Race/Ethnicity | 5 categories | n (%) |
| Education | 4 categories | n (%) |
| PIR | Ratio | Mean ± SD, Median (IQR) |
| **Health Behaviors** | | |
| Smoking | 3 categories | n (%) |
| BMI | kg/m² | Mean ± SD |
| Physical Activity | MET-min/week | Median (IQR) |
| **Health Conditions** | | |
| Diabetes | Yes/No | n (%) |
| Hypertension | Yes/No | n (%) |
| CVD | Yes/No | n (%) |
| eGFR | mL/min/1.73m² | Mean ± SD |
| **PhenoAge** | | |
| Chronological Age | Years | Mean ± SD |
| PhenoAge | Years | Mean ± SD |
| PhenoAge Acceleration | Years | Mean ± SD |

### PFAS Exposure Distribution

| PFAS | Geometric Mean | 95th Percentile | % >LOD |
|------|----------------|-----------------|--------|
| PFOA | XX ng/mL | XX ng/mL | XX% |
| PFOS | XX ng/mL | XX ng/mL | XX% |
| PFHxS | XX ng/mL | XX ng/mL | XX% |
| PFNA | XX ng/mL | XX ng/mL | XX% |

*Weighted using WTSA2YR for population representativeness*

### Correlation Matrix

Pearson correlations between:
- PFAS compounds (ln-transformed)
- PhenoAge acceleration
- Key covariates

---

## Main Analysis: Regression Models

### Model Specification

#### Model 1: Minimally Adjusted

```python
# Survey-weighted linear regression
# Outcome: PhenoAge acceleration
# Exposure: ln(PFAS)

import statsmodels.api as sm
from statsmodels.stats.weightstats import DescrStatsW

# Survey design setup
from statsmodels.stats.survey import SurveyDesign

design = SurveyDesign(
    strata=data['SDMVSTRA'],
    psu=data['SDMVPSU'],
    weights=data['WTSA2YR']
)

# Model formula
formula_m1 = """
    phenoage_accel ~ ln_pfas + 
                     age + age_squared + 
                     C(sex) + 
                     C(race_ethnicity) +
                     C(survey_cycle)
"""
```

#### Model 2: Fully Adjusted

```python
formula_m2 = """
    phenoage_accel ~ ln_pfas + 
                     age + age_squared + 
                     C(sex) + 
                     C(race_ethnicity) +
                     C(education) +
                     pir +
                     C(smoking) +
                     alcohol_drinks_per_week +
                     physical_activity_met +
                     bmi +
                     egfr +
                     C(survey_cycle)
"""
```

#### Model 3: Disease-Excluded Sensitivity

```python
# Exclude diabetes, CVD, CKD (eGFR <60)
data_sensitivity = data[
    (data['diabetes'] == 0) & 
    (data['cvd'] == 0) & 
    (data['egfr'] >= 60)
]
```

### Output Presentation

For each PFAS compound, report:

| Metric | Value | 95% CI | p-value |
|--------|-------|--------|---------|
| β coefficient | X.XX | (X.XX, X.XX) | 0.XXX |
| Interpretation | Years acceleration per ln-unit increase | | |
| Standardized β | X.XX | (X.XX, X.XX) | 0.XXX |

### Multiple Testing Correction

```python
from statsmodels.stats.multitest import multipletests

# Benjamini-Hochberg FDR correction
pvalues = [p_pfoa, p_pfos, p_pfhxs, p_pfna]
reject, pvals_corrected, _, _ = multipletests(pvalues, method='fdr_bh')
```

---

## Dose-Response Analysis (H2)

### Categorical Analysis

```python
# Tertile analysis with trend test
pfas_tertiles = pd.qcut(data['pfas'], q=3, labels=['T1', 'T2', 'T3'])

# T1 as reference
model = smf.ols('phenoage_accel ~ C(pfas_tertiles, Treatment(reference="T1")) + covariates', 
                data=data).fit()

# Trend test (ordinal coding)
model_trend = smf.ols('phenoage_accel ~ pfas_tertile_numeric + covariates', 
                      data=data).fit()
```

### Spline Analysis

```python
from patsy import cr  # Cubic regression splines

# Restricted cubic splines with 3 knots at tertiles
formula_spline = """
    phenoage_accel ~ cr(ln_pfas, df=3) + 
                     age + C(sex) + covariates
"""

# Likelihood ratio test for nonlinearity
model_linear = smf.ols('phenoage_accel ~ ln_pfas + covariates', data=data).fit()
model_spline = smf.ols(formula_spline, data=data).fit()

lrt_stat = 2 * (model_spline.llf - model_linear.llf)
lrt_pvalue = 1 - chi2.cdf(lrt_stat, df=2)  # df = difference in parameters
```

### Visualization

Generate exposure-response curves with 95% confidence intervals using:
- GAM (Generalized Additive Models) via pyGAM
- Predicted margins from spline models

---

## Sex-Specific Analysis (H3)

### Interaction Testing

```python
# Add interaction term
formula_interaction = """
    phenoage_accel ~ ln_pfas * C(sex) + 
                     age + C(race_ethnicity) + covariates
"""

model = smf.ols(formula_interaction, data=data).fit()
interaction_pvalue = model.pvalues['ln_pfas:C(sex)[T.Female]']
```

### Stratified Models

```python
# Separate models by sex
for sex_group in ['Male', 'Female']:
    subset = data[data['sex'] == sex_group]
    model = smf.ols('phenoage_accel ~ ln_pfas + covariates', data=subset).fit()
    print(f"{sex_group}: β = {model.params['ln_pfas']:.3f}")
```

### Menopausal Subgroup (Females only)

```python
# Restrict to females ≥45 years
menopause_analysis = data[
    (data['sex'] == 'Female') & 
    (data['age'] >= 45)
]

# Compare pre vs post-menopausal if variable available
```

---

## Mixture Analysis (H4)

### Weighted Quantile Sum (WQS) Regression

```python
# WQS implementation
"""
WQS models the mixture as a weighted sum of quantiles:
WQS = Σ(w_i × q_i) where Σw_i = 1, w_i ≥ 0

Optimization uses bootstrap sampling to:
1. Split data into training/validation
2. Estimate weights in training set
3. Test mixture effect in validation set
4. Repeat 1000 times
"""

# Key outputs:
# - Mixture effect (β_WQS)
# - Component weights (w_i for each PFAS)
# - 95% CI from bootstrap distribution
```

### Bayesian Kernel Machine Regression (BKMR)

```python
# BKMR using R via rpy2 or standalone Python implementation
"""
BKMR estimates:
h(Σx_i) ~ GP(0, K(x, x'))

where h is the exposure-response function
and K is a kernel function capturing correlation structure
"""

# Key outputs:
# - Overall mixture effect
# - Single-exposure effects (holding others at percentiles)
# - Interaction effects
# - Variable inclusion probabilities
```

### Quantile G-Computation

```python
# Estimate effect of simultaneous increase in all PFAS
"""
QGC estimates the marginal effect of shifting all exposures
from a reference quantile (e.g., 25th) to a higher quantile (e.g., 75th)
"""

# Key output: Intervention effect with 95% CI
```

---

## Subgroup and Sensitivity Analyses (H5)

### Subgroup Analyses

| Subgroup | Definition | Sample Size Target |
|----------|------------|-------------------|
| Age groups | 18-39, 40-59, ≥60 | ≥500 per group |
| Sex | Male, Female | ≥1500 each |
| Race/Ethnicity | NHW, NHB, MA | ≥500 each |
| SES | PIR <1.0, 1.0-3.9, ≥4.0 | ≥500 per group |
| BMI | <25, 25-30, ≥30 | ≥500 per group |
| Smoking | Never, Former, Current | ≥500 per group |

### Sensitivity Analyses

| Analysis | Description | Purpose |
|----------|-------------|---------|
| Complete cases | No missing data imputation | Robustness to missingness |
| LOD substitution | LOD/2 vs LOD/√2 | Robustness to detection limit |
| Outlier exclusion | |z| > 3 instead of |z| > 4 | Robustness to outliers |
| Cycle restriction | Exclude 1999-2000 | Consistent PFNA measurement |
| Disease exclusion | Exclude diabetes/CVD/CKD | Reverse causation |
| Additional confounders | Include diet quality if available | Residual confounding |

### Interaction Testing

For each subgroup modifier:
```python
formula = 'phenoage_accel ~ ln_pfas * C(subgroup) + covariates'
model = smf.ols(formula, data=data).fit()
# Report: interaction p-value, stratified β estimates
```

---

## Software and Packages

### Primary Software

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.10+ | Primary analysis language |
| NumPy | 1.24+ | Numerical computations |
| Pandas | 2.0+ | Data manipulation |
| SciPy | 1.10+ | Statistical functions |
| Statsmodels | 0.14+ | Regression modeling |
| Scikit-learn | 1.3+ | Machine learning/PCA |

### Survey Analysis

| Package | Purpose |
|---------|---------|
| `samplics` | Survey-weighted estimation |
| `statsmodels.survey` | Survey design specification |

### Visualization

| Package | Purpose |
|---------|---------|
| Matplotlib | Base plotting |
| Seaborn | Statistical visualization |
| Plotly | Interactive plots |

### Specialized Methods

| Package/Method | Purpose |
|----------------|---------|
| `pyGAM` | Generalized Additive Models |
| `scikit-learn` | WQS implementation |
| `rpy2` + R `bkmr` | BKMR if Python unavailable |
| `statsmodels` MICE | Multiple imputation |

### Docker Environment

All analyses will run in the `nhanes-analysis-vault` container with:
- Read-only access to `/data` (NHANES data)
- Read-write access to `/study` (study files)
- `--network none` for data isolation

---

## Output Specifications

### Tables

| Table | Content | Format |
|-------|---------|--------|
| Table 1 | Population characteristics | LaTeX/PDF |
| Table 2 | PFAS exposure distribution | LaTeX/PDF |
| Table 3 | Main regression results | LaTeX/PDF |
| Table 4 | Dose-response analysis | LaTeX/PDF |
| Table 5 | Subgroup analyses | LaTeX/PDF |
| Table 6 | Sensitivity analyses | LaTeX/PDF |

### Figures

| Figure | Content | Format |
|--------|---------|--------|
| Figure 1 | STROBE flow diagram | PNG/PDF (300 DPI) |
| Figure 2 | PFAS exposure distributions | PNG/PDF (300 DPI) |
| Figure 3 | Exposure-response curves | PNG/PDF (300 DPI) |
| Figure 4 | Forest plot of associations | PNG/PDF (300 DPI) |
| Figure 5 | Mixture analysis results | PNG/PDF (300 DPI) |
| Figure 6 | Subgroup analysis results | PNG/PDF (300 DPI) |

### Reproducibility

- All code version-controlled in GitHub repository
- Random seeds set for stochastic processes
- Complete package environment documented in requirements.txt
- Analysis log with timestamp and parameters

---

## Quality Control

### Data Validation Checks

| Check | Description | Threshold |
|-------|-------------|-----------|
| Range checks | Values within biological plausibility | Flag if outside |
| Missing patterns | Assess missing data mechanism | Document MAR/MCAR |
| Outlier detection | |z-score| > 4 | Exclude or winsorize |
| Logical consistency | Age > PhenoAge (usually) | Flag for review |
| Survey weights | Sum to population | Validate against NHANES |

### Analysis Validation

| Check | Description |
|-------|-------------|
| Compare unweighted vs weighted | Ensure survey adjustment matters |
| Compare raw vs transformed | Verify transformation appropriateness |
| Replication of published results | Validate against Yan et al. (2025) |
| Bootstrap CI coverage | Check 95% CI coverage in simulations |

---

## Timeline

| Week | Activity |
|------|----------|
| 1 | Data extraction and merging |
| 2 | PhenoAge calculation and QC |
| 3 | Descriptive statistics |
| 4 | Main regression analyses |
| 5 | Dose-response analyses |
| 6 | Subgroup and sensitivity analyses |
| 7 | Mixture analyses |
| 8 | Table and figure generation |
| 9 | Manuscript writing |
| 10 | Internal review and revision |

---

## References

1. Levine et al. (2018). An epigenetic biomarker of aging for lifespan and healthspan. *Aging*, 10(4), 573-591. DOI: 10.18632/aging.101414

2. Yan et al. (2025). Associations of per- and polyfluoroalkyl substances exposure with biological aging. *Ecotoxicology and Environmental Safety*, 293, 118819. DOI: 10.1016/j.ecoenv.2025.118819

3. von Elm et al. (2007). The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) Statement. *Annals of Internal Medicine*, 147(8), 573-577.

4. Gibson et al. (2019). An overview of methods for constructing mixture exposure indices. *Current Environmental Health Reports*, 6(2), 53-65.

5. Bose et al. (2022). Bayesian kernel machine regression: A review. *Environmental Health Perspectives*, 130(8), 085001.

---

*Document Version*: 1.0  
*Last Updated*: February 13, 2026  
*Study ID*: pfas-phenoage-2026-02-13
