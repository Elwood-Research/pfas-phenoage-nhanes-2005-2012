# Analysis Plan: PFAS and PhenoAge Study

## Executive Summary

This document outlines the comprehensive analysis plan for the cross-sectional investigation of associations between serum PFAS concentrations and biological aging measured by PhenoAge in NHANES 2005-2018.

### Key Methodological Decisions

| Decision | Specification | Rationale |
|----------|--------------|-----------|
| **Study Design** | Cross-sectional | NHANES design; temporal ordering assumptions |
| **Population** | Adults 18+ | Age-related PhenoAge validity |
| **PFAS Compounds** | PFOA, PFOS, PFHxS, PFNA | Core legacy PFAS across all cycles |
| **Outcome** | PhenoAge acceleration | Continuous measure of biological aging |
| **Primary Analysis** | Survey-weighted linear regression | Account for complex design |
| **Mixture Analysis** | WQS and BKMR | Joint effects of PFAS mixture |
| **Missing Data** | Complete case analysis | <5% missing for key variables |
| **Multiple Testing** | FDR correction (Benjamini-Hochberg) | Balance Type I error and power |

---

## Analysis Workflow

### Phase 1: Data Preparation and Quality Control

#### 1.1 Data Integration
```
Step 1: Load and merge datasets by SEQN for each cycle
Step 2: Combine cycles using consistent variable naming
Step 3: Apply survey weight adjustment (divide by 7 cycles)
Step 4: Generate cycle indicator variable
```

#### 1.2 Inclusion/Exclusion Criteria Application
```
INCLUDE:
  - Age 18+ years (RIDAGEYR >= 18)
  - Complete PFAS measurements (≥4 compounds)
  - All 9 PhenoAge biomarkers available
  - Valid survey weights

EXCLUDE:
  - Pregnant women (RIDEXPRG = 1)
  - Missing critical covariates
  - Extreme outliers (|z| > 4 on continuous variables)
```

#### 1.3 Variable Derivation
```
DERIVE:
  1. PFAS log-transformations
  2. CRP unit conversion (mg/dL → mg/L)
  3. PhenoAge calculation
  4. PhenoAge acceleration (PhenoAge - chronological age)
  5. Categorical covariates (smoking status, diabetes, etc.)
  6. Combined PFAS variables (sum, mixture indices)
```

### Phase 2: Descriptive Analysis

#### 2.1 Sample Characteristics (Table 1)

| Variable | Statistic | Weighted |
|----------|-----------|----------|
| Age | Mean (SD), Median (IQR) | Yes |
| Sex | n (%) | Yes |
| Race/Ethnicity | n (%) | Yes |
| Education | n (%) | Yes |
| Income ratio | Mean (SD), Median (IQR) | Yes |
| BMI | Mean (SD), Median (IQR) | Yes |
| Smoking status | n (%) | Yes |
| Diabetes | n (%) | Yes |
| Hypertension | n (%) | Yes |
| CVD | n (%) | Yes |
| PhenoAgeAccel | Mean (SD), Median (IQR) | Yes |

#### 2.2 PFAS Distributions (Table 2)

| Compound | LOD | % Detect | GM (95% CI) | Percentiles (25th, 50th, 75th, 95th) |
|----------|-----|----------|-------------|--------------------------------------|
| PFOA | By cycle | | | |
| PFOS | By cycle | | | |
| PFHxS | By cycle | | | |
| PFNA | By cycle | | | |

#### 2.3 Correlation Analysis
- Pearson correlation matrix for PFAS (ln-transformed)
- Spearman correlation between PFAS and PhenoAgeAccel
- Weighted correlations accounting for survey design

#### 2.4 STROBE Flow Diagram
Construct flow diagram showing:
1. Initial NHANES participants per cycle
2. Exclusions by criterion
3. Final analytic sample
4. Missing data patterns

### Phase 3: Primary Analysis

#### 3.1 Individual PFAS Associations

**Model 1: Crude (Minimally Adjusted)**
```
PhenoAgeAccel ~ ln(PFAS) + RIDAGEYR + RIAGENDR
```

**Model 2: Demographically Adjusted**
```
PhenoAgeAccel ~ ln(PFAS) + RIDAGEYR + RIAGENDR + RIDRETH1 + 
                DMDEDUC2 + INDFMPIR
```

**Model 3: Fully Adjusted**
```
PhenoAgeAccel ~ ln(PFAS) + RIDAGEYR + RIAGENDR + RIDRETH1 + 
                DMDEDUC2 + INDFMPIR + BMXBMI + smoking_status +
                diabetes + hypertension + cvd
```

**Model 4: Multi-PFAS Model**
```
PhenoAgeAccel ~ ln(PFOA) + ln(PFOS) + ln(PFHxS) + ln(PFNA) +
                RIDAGEYR + RIAGENDR + RIDRETH1 + DMDEDUC2 + 
                INDFMPIR + BMXBMI + smoking_status + diabetes + 
                hypertension + cvd
```

**For each model, report:**
- β coefficient (95% CI)
- Standard error
- p-value (unadjusted)
- p-value (FDR-adjusted)

#### 3.2 Interactions

Test effect modification by:
- Sex (RIAGENDR)
- Age group (<50 vs ≥50 years)
- BMI category (normal vs overweight/obese)
- Race/ethnicity

**Interaction Model:**
```
PhenoAgeAccel ~ ln(PFAS) * modifier + covariates
```

#### 3.3 Multiple Testing Correction
- Apply Benjamini-Hochberg FDR correction within each model
- Family: 4 PFAS compounds × 1 outcome = 4 tests per model
- Report both unadjusted and FDR-adjusted p-values

### Phase 4: Mixture Analysis

#### 4.1 Weighted Quantile Sum (WQS) Regression

**Objective**: Estimate joint effect of PFAS mixture

**Specifications:**
- Quantiles: 4 categories (quartiles)
- Bootstrap samples: 100
- Direction: Unconstrained (allow negative weights if needed)
- Constraint: Weights sum to 1, non-negative

**Output:**
- Overall mixture effect (β, 95% CI, p-value)
- Variable importance weights for each PFAS
- Weight distribution across bootstrap samples

#### 4.2 Bayesian Kernel Machine Regression (BKMR)

**Objective**: Model exposure-response relationships and interactions

**Specifications:**
- MCMC iterations: 50,000
- Burn-in: 10,000
- Thinning: 5
- Variable selection: Enabled

**Outputs:**
1. **Posterior inclusion probabilities** for each PFAS
2. **Overall mixture effect**: Risk at 25th, 50th, 75th vs 25th percentile
3. **Single variable effects**: Independent effects holding others at median
4. **Interaction effects**: Pairwise interaction plots

### Phase 5: Sensitivity Analyses

#### 5.1 Detection Limit Handling

| Method | Description | Implementation |
|--------|-------------|----------------|
| Standard | LOD/√2 substitution | Primary analysis |
| Alternative | LOD/2 substitution | Sensitivity 1 |
| Imputation | Multiple imputation | Sensitivity 2 |

#### 5.2 Cycle-Specific Analyses

**Analysis 1: Early cycles (D-G, 2005-2012)**
- Smaller PFAS panel (4 compounds)
- Separate analysis

**Analysis 2: Recent cycles (H-J, 2013-2018)**
- Expanded PFAS panel
- Separate analysis

**Analysis 3: Test for cycle effect**
- Include cycle indicator in pooled model
- Test for cycle-PFAS interactions

#### 5.3 Exclusion Analyses

| Exclusion Criteria | Rationale |
|-------------------|-----------|
| Exclude chronic diseases | Remove confounding by disease |
| Exclude current smokers | Remove confounding by smoking |
| Exclude extreme BMI (<18.5 or >35) | Remove metabolic outliers |
| Age restriction (30-65 years) | Working-age adults |
| Exclude CRP >10 mg/L | Remove acute inflammation |

#### 5.4 Alternative PhenoAge Specifications

| Specification | Description |
|--------------|-------------|
| Standard | Primary calculation (LOD/√2 for missing components) |
| Exclude CRP | Calculate without CRP (if high missingness) |
| Alternative glucose | Use fasting glucose if available |

### Phase 6: Model Diagnostics

#### 6.1 Regression Diagnostics

For each model, assess:
- **Residual distribution**: Normality (Shapiro-Wilk), QQ plots
- **Heteroscedasticity**: Breusch-Pagan test
- **Influential observations**: Cook's distance, DFBETA
- **Multicollinearity**: VIF for all predictors

#### 6.2 Survey Design Diagnostics

- Design effects (DEFF) for key estimates
- Effective sample size calculation
- Strata with single PSU (collapsed variance)

---

## Analysis Outputs

### Tables

| Table | Content | Location |
|-------|---------|----------|
| Table 1 | Sample characteristics | `04-analysis/outputs/tables/` |
| Table 2 | PFAS distributions | `04-analysis/outputs/tables/` |
| Table 3 | Individual PFAS associations | `04-analysis/outputs/tables/` |
| Table 4 | Multi-PFAS model | `04-analysis/outputs/tables/` |
| Table 5 | WQS results | `04-analysis/outputs/tables/` |
| Table 6 | BKMR results | `04-analysis/outputs/tables/` |
| Table 7 | Sensitivity analyses | `04-analysis/outputs/tables/` |

### Figures

| Figure | Content | Location |
|--------|---------|----------|
| Figure 1 | STROBE flow diagram | `04-analysis/outputs/figures/` |
| Figure 2 | PFAS distributions by cycle | `04-analysis/outputs/figures/` |
| Figure 3 | PhenoAgeAccel vs chronological age | `04-analysis/outputs/figures/` |
| Figure 4 | PFAS-PhenoAgeAccel associations | `04-analysis/outputs/figures/` |
| Figure 5 | WQS weights | `04-analysis/outputs/figures/` |
| Figure 6 | BKMR exposure-response curves | `04-analysis/outputs/figures/` |
| Figure 7 | Sensitivity analysis forest plot | `04-analysis/outputs/figures/` |

### Supplementary Materials

- Full correlation matrices
- Cycle-specific results
- Detailed model diagnostics
- Codebook for derived variables

---

## Quality Control Checklist

### Data Preparation QC

| Check | Pass Criteria | Status |
|-------|--------------|--------|
| SEQN uniqueness | No duplicates | |
| Weight positivity | All weights > 0 | |
| Age range | 18-120 years | |
| PFAS non-negativity | All values ≥ 0 | |
| CRP conversion | Correct unit conversion verified | |
| PhenoAge range | 0-150 years | |
| Outlier screen | <2% excluded | |

### Analysis QC

| Check | Pass Criteria | Status |
|-------|--------------|--------|
| Sample size | ≥1000 complete cases | |
| Convergence | All models converge | |
| VIF | All < 5.0 | |
| Residual normality | Shapiro-Wilk p > 0.01 | |
| Design effect | DEFF < 5.0 for key estimates | |

---

## Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Data preparation | 1 week | Clean analytic dataset |
| Descriptive analysis | 1 week | Table 1, Table 2 |
| Primary analysis | 2 weeks | Tables 3-4, Figures 1-4 |
| Mixture analysis | 2 weeks | Tables 5-6, Figures 5-6 |
| Sensitivity analyses | 1 week | Table 7, Figure 7 |
| Documentation | 1 week | Complete results summary |
| Total | 8 weeks | Publication-ready outputs |

---

## References

1. Levine, M. E., et al. (2018). An epigenetic biomarker of aging for lifespan and healthspan. Aging, 10(4), 573-591.
2. Keil, A. P., et al. (2020). A quantile-based g-computation approach to addressing the effects of exposure mixtures. Environmental Health Perspectives, 128(4), 047004.
3. Bobb, J. F., et al. (2015). Bayesian kernel machine regression for estimating the health effects of multi-pollutant mixtures. Biostatistics, 16(3), 493-508.
4. NHANES Analytic Guidelines. National Center for Health Statistics.
