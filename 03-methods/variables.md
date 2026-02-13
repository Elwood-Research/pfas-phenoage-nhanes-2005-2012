# Variables Documentation: PFAS Exposure and PhenoAge Study

## Overview

This document provides detailed documentation of all variables used in the study investigating associations between PFAS exposure and PhenoAge biological aging in NHANES participants.

---

## Dataset Mapping

### Primary Data Sources

| NHANES Cycle | Years | PFAS Dataset | Biochemistry | CBC | Demographics |
|--------------|-------|--------------|--------------|-----|--------------|
| A | 1999-2000 | SSPFC_A | LAB18 | L28 | DEMO_A |
| D | 2005-2006 | PFC_D | BIOPRO_D | CBC_D | DEMO_D |
| E | 2007-2008 | PFC_E | BIOPRO_E | CBC_E | DEMO_E |
| F | 2009-2010 | PFC_F | BIOPRO_F | CBC_F | DEMO_F |
| G | 2011-2012 | PFC_G | BIOPRO_G | CBC_G | DEMO_G |

### Merge Key

All datasets will be merged using `SEQN` (Respondent Sequence Number), the unique identifier for NHANES participants.

---

## Exposure Variables: PFAS

### Individual PFAS Compounds

#### PFOA (Perfluorooctanoic Acid)

| Attribute | Value |
|-----------|-------|
| **NHANES Variable** | `LBXPFOA` |
| **Description** | Perfluorooctanoic acid in serum |
| **Units** | ng/mL |
| **Detection Limit (typical)** | 0.1 ng/mL |
| **LOD Indicator** | `LBDPFOAL` (0=detected, 1=<LOD) |
| **Available Cycles** | A, D, E, F, G |
| **Study Variable Name** | `pfoa_ng_ml` |
| **Transformed** | `ln_pfoa` (natural log) |

**Imputation for <LOD**: LOD/√2

#### PFOS (Perfluorooctane Sulfonic Acid)

| Attribute | Value |
|-----------|-------|
| **NHANES Variable** | `LBXPFOS` |
| **Description** | Perfluorooctane sulfonic acid in serum |
| **Units** | ng/mL |
| **Detection Limit (typical)** | 0.2 ng/mL |
| **LOD Indicator** | `LBDPFOSL` (0=detected, 1=<LOD) |
| **Available Cycles** | A, D, E, F, G |
| **Study Variable Name** | `pfos_ng_ml` |
| **Transformed** | `ln_pfos` (natural log) |

**Imputation for <LOD**: LOD/√2

#### PFHxS (Perfluorohexane Sulfonic Acid)

| Attribute | Value |
|-----------|-------|
| **NHANES Variable** | `LBXPFHS` |
| **Description** | Perfluorohexane sulfonic acid in serum |
| **Units** | ng/mL |
| **Detection Limit (typical)** | 0.1 ng/mL |
| **LOD Indicator** | `LBDPFHSL` (0=detected, 1=<LOD) |
| **Available Cycles** | A, D, E, F, G |
| **Study Variable Name** | `pfhxs_ng_ml` |
| **Transformed** | `ln_pfhxs` (natural log) |

**Imputation for <LOD**: LOD/√2

#### PFNA (Perfluorononanoic Acid)

| Attribute | Value |
|-----------|-------|
| **NHANES Variable** | `LBXPFNA` |
| **Description** | Perfluorononanoic acid in serum |
| **Units** | ng/mL |
| **Detection Limit (typical)** | 0.1 ng/mL |
| **LOD Indicator** | `LBDPFNAL` (0=detected, 1=<LOD) |
| **Available Cycles** | D, E, F, G (NOT in 1999-2000) |
| **Study Variable Name** | `pfna_ng_ml` |
| **Transformed** | `ln_pfna` (natural log) |

**Imputation for <LOD**: LOD/√2

### Derived PFAS Variables

| Variable | Calculation | Description |
|----------|-------------|-------------|
| `ln_pfas_sum` | Sum of ln-transformed concentrations | Summed log-exposure |
| `pfas_pc1` | First principal component | PFAS mixture score |
| `pfas_tertile` | Tertile of summed PFAS | Categorical exposure |
| `pfos_quartile` | Quartile of PFOS | Categorical exposure |
| `pfoa_quartile` | Quartile of PFOA | Categorical exposure |
| `pfhxs_quartile` | Quartile of PFHxS | Categorical exposure |
| `pfna_quartile` | Quartile of PFNA | Categorical exposure |

### PFAS Availability by Cycle

| Cycle | PFOA | PFOS | PFHxS | PFNA |
|-------|------|------|-------|------|
| 1999-2000 (A) | ✓ | ✓ | ✓ | ✗ |
| 2005-2006 (D) | ✓ | ✓ | ✓ | ✓ |
| 2007-2008 (E) | ✓ | ✓ | ✓ | ✓ |
| 2009-2010 (F) | ✓ | ✓ | ✓ | ✓ |
| 2011-2012 (G) | ✓ | ✓ | ✓ | ✓ |

---

## Outcome Variables: PhenoAge

### PhenoAge Components

#### Albumin

| Attribute | Value |
|-----------|-------|
| **NHANES Variable** | `LBDSALSI` (preferred) or `LBXSAL` |
| **Description** | Serum albumin |
| **Original Units** | g/dL (`LBXSAL`) |
| **SI Units** | g/L (`LBDSALSI`) |
| **Required Units** | g/L |
| **Conversion** | If using `LBXSAL`: multiply by 10 |
| **Coefficient (Levine)** | 0.0237 |
| **Study Variable** | `albumin_gl` |

#### Creatinine

| Attribute | Value |
|-----------|-------|
| **NHANES Variable** | `LBDSCRSI` (preferred) or `LBXSCR` |
| **Description** | Serum creatinine |
| **Original Units** | mg/dL (`LBXSCR`) |
| **SI Units** | μmol/L (`LBDSCRSI`) |
| **Required Units** | μmol/L |
| **Conversion** | If using `LBXSCR`: multiply by 88.4 |
| **Coefficient (Levine)** | 0.0229 |
| **Study Variable** | `creatinine_umol_l` |

#### Glucose

| Attribute | Value |
|-----------|-------|
| **NHANES Variable** | `LBDGLUSI` (preferred) or `LBXGLU` |
| **Description** | Fasting plasma glucose |
| **Original Units** | mg/dL (`LBXGLU`) |
| **SI Units** | mmol/L (`LBDGLUSI`) |
| **Required Units** | mmol/L |
| **Conversion** | If using `LBXGLU`: multiply by 0.0555 |
| **Coefficient (Levine)** | 0.1274 |
| **Study Variable** | `glucose_mmol_l` |

#### C-Reactive Protein (CRP)

| Attribute | Value |
|-----------|-------|
| **NHANES Variable** | `LBXCRP` |
| **Description** | C-reactive protein |
| **Units** | mg/L |
| **Required Units** | mg/L (natural log) |
| **Transformation** | ln(CRP) |
| **Coefficient (Levine)** | 0.1705 |
| **Study Variable** | `ln_crp_mg_l` |

**Note**: Use `log(LBXCRP)` in calculation

#### Lymphocyte Percentage

| Attribute | Value |
|-----------|-------|
| **NHANES Variable** | `LBXLYPCT` |
| **Description** | Lymphocyte percentage |
| **Units** | % |
| **Coefficient (Levine)** | 0.0441 |
| **Study Variable** | `lymphocyte_pct` |

**Calculation**: If `LBXLYPCT` not available, calculate from:
- `LBXLYMNO` / `LBXWBCSI` × 100

#### Mean Corpuscular Volume (MCV)

| Attribute | Value |
|-----------|-------|
| **NHANES Variable** | `LBXMCVSI` |
| **Description** | Mean corpuscular volume |
| **Units** | fL |
| **Coefficient (Levine)** | 0.0681 |
| **Study Variable** | `mcv_fl` |

#### Red Cell Distribution Width (RDW)

| Attribute | Value |
|-----------|-------|
| **NHANES Variable** | `LBXRDW` |
| **Description** | Red cell distribution width |
| **Units** | % |
| **Coefficient (Levine)** | 0.0754 |
| **Study Variable** | `rdw_pct` |

#### Alkaline Phosphatase (ALP)

| Attribute | Value |
|-----------|-------|
| **NHANES Variable** | `LBXSAPSI` |
| **Description** | Alkaline phosphatase |
| **Units** | U/L |
| **Coefficient (Levine)** | 0.0392 |
| **Study Variable** | `alp_ul` |

#### White Blood Cell Count (WBC)

| Attribute | Value |
|-----------|-------|
| **NHANES Variable** | `LBXWBCSI` |
| **Description** | White blood cell count |
| **Units** | 10⁹/L (or 1000 cells/μL) |
| **Coefficient (Levine)** | 0.1434 |
| **Study Variable** | `wbc_10e9_l` |

### Derived Outcome Variables

| Variable | Calculation | Description |
|----------|-------------|-------------|
| `chronological_age` | `RIDAGEYR` | Age in years at examination |
| `phenoage` | Algorithm (see below) | Biological age estimate |
| `phenoage_acceleration` | `phenoage - predicted_phenoage` | Residual from age regression |
| `phenoage_acceleration_z` | Standardized residual | Z-score of acceleration |

### PhenoAge Calculation

```
Step 1: Calculate linear predictor (x)
x = -19.9067 + 
    0.0237 × albumin_gl +
    0.0229 × creatinine_umol_l +
    0.1274 × glucose_mmol_l +
    0.1705 × ln_crp_mg_l +
    0.0441 × lymphocyte_pct +
    0.0681 × mcv_fl +
    0.0754 × rdw_pct +
    0.0392 × alp_ul +
    0.1434 × wbc_10e9_l

Step 2: Calculate mortality score
mort_score = 1 - exp(-exp(x / 0.09165))

Step 3: Calculate PhenoAge
phenoage = 141.50 + (ln(-0.00553 × ln(1 - mort_score)) / 0.09165)

Step 4: Calculate PhenoAge acceleration
phenoage_acceleration = phenoage - (β₀ + β₁ × chronological_age)
```

---

## Covariates

### Demographic Variables

#### Age

| Attribute | Value |
|-----------|-------|
| **NHANES Variable** | `RIDAGEYR` |
| **Description** | Age at examination |
| **Units** | Years |
| **Study Variable** | `age_years` |
| **Transformed** | `age_centered`, `age_squared` |
| **Range** | 18-85+ (top-coded at 85) |

#### Sex

| Attribute | Value |
|-----------|-------|
| **NHANES Variable** | `RIAGENDR` |
| **Description** | Gender |
| **Codes** | 1=Male, 2=Female |
| **Study Variable** | `sex` (Male/Female) |

#### Race/Ethnicity

| Attribute | Value |
|-----------|-------|
| **NHANES Variable** | `RIDRETH1` or `RIDRETH3` (2011+) |
| **Description** | Race/Hispanic origin |
| **Codes** | 1=Mexican American, 2=Other Hispanic, 3=Non-Hispanic White, 4=Non-Hispanic Black, 6=Non-Hispanic Asian (2011+), 7=Other/Multi-racial |
| **Study Variable** | `race_ethnicity` |
| **Categories** | Mexican American, Other Hispanic, Non-Hispanic White, Non-Hispanic Black, Other |

#### Education

| Attribute | Value |
|-----------|-------|
| **NHANES Variable** | `DMDEDUC2` (adults) |
| **Description** | Education level |
| **Codes** | 1=<9th grade, 2=9-11th grade, 3=High school/GED, 4=Some college/AA, 5=College graduate or above |
| **Study Variable** | `education` |
| **Categories** | <High School, High School/GED, Some College, College Graduate |

#### Poverty Income Ratio (PIR)

| Attribute | Value |
|-----------|-------|
| **NHANES Variable** | `INDFMPIR` |
| **Description** | Ratio of family income to poverty threshold |
| **Units** | Ratio (0-5, with 5 representing ≥5.0) |
| **Study Variable** | `pir` |
| **Categories** | <1.0 (poor), 1.0-1.99 (near-poor), 2.0-3.99 (middle), ≥4.0 (high) |

### Health Behavior Variables

#### Smoking Status

| Attribute | Value |
|-----------|-------|
| **NHANES Variables** | `SMQ020`, `SMQ040` |
| **Description** | Smoking status |
| **Codes** | Derived from ever smoked (SMQ020) and current smoking (SMQ040) |
| **Study Variable** | `smoking_status` |
| **Categories** | Never, Former, Current |

**Derivation Logic**:
- Never: SMQ020 = 2 (No)
- Former: SMQ020 = 1 AND SMQ040 = 3 (No longer)
- Current: SMQ020 = 1 AND SMQ040 = 1 or 2 (Every day/Some days)

#### Alcohol Consumption

| Attribute | Value |
|-----------|-------|
| **NHANES Variable** | `ALQ130` or `ALQ120Q` |
| **Description** | Average drinks per day/week |
| **Study Variable** | `alcohol_drinks_per_week` |
| **Categories** | None, Light (≤3/week), Moderate (4-14/week), Heavy (>14/week) |

#### Physical Activity

| Attribute | Value |
|-----------|-------|
| **NHANES Variables** | `PAQ605`, `PAQ610`, `PAQ620`, `PAQ635`, `PAQ640`, `PAQ655`, `PAQ665` |
| **Description** | Vigorous/moderate recreational activity |
| **Study Variable** | `physical_activity_met` |
| **Categories** | Sedentary, Low, Moderate, High |

**MET-minute calculation**:
- Vigorous: 8.0 METs × minutes × days
- Moderate: 4.0 METs × minutes × days
- Total MET-minutes/week = sum of vigorous + moderate

#### Body Mass Index (BMI)

| Attribute | Value |
|-----------|-------|
| **NHANES Variable** | `BMXBMI` |
| **Description** | Body mass index |
| **Units** | kg/m² |
| **Study Variable** | `bmi` |
| **Categories** | <18.5, 18.5-24.9, 25-29.9, ≥30 |

### Health Condition Variables

#### Diabetes

| Attribute | Value |
|-----------|-------|
| **NHANES Variables** | `DIQ010`, `LBXGH`, `LBDGLUSI` |
| **Description** | Diabetes status |
| **Study Variable** | `diabetes` |
| **Categories** | Yes/No |

**Definition**: Yes if any of:
- Self-reported diagnosis (DIQ010 = 1)
- HbA1c ≥6.5% (`LBXGH` ≥6.5)
- Fasting glucose ≥126 mg/dL (`LBXGLU` ≥126 or `LBDGLUSI` ≥7.0)

#### Hypertension

| Attribute | Value |
|-----------|-------|
| **NHANES Variables** | `BPXSY1`, `BPXDI1`, `BPQ050A` |
| **Description** | Hypertension status |
| **Study Variable** | `hypertension` |
| **Categories** | Yes/No |

**Definition**: Yes if any of:
- Average SBP ≥140 mmHg (from `BPXSY1`, `BPXSY2`, `BPXSY3`, `BPXSY4`)
- Average DBP ≥90 mmHg (from `BPXDI1`, `BPXDI2`, `BPXDI3`, `BPXDI4`)
- Self-reported medication use (BPQ050A = 1)

#### Cardiovascular Disease

| Attribute | Value |
|-----------|-------|
| **NHANES Variables** | `MCQ160C`, `MCQ160D`, `MCQ160E`, `MCQ160F` |
| **Description** | History of CVD |
| **Study Variable** | `cvd_history` |
| **Categories** | Yes/No |

**Definition**: Yes if any:
- CHD (MCQ160C = 1)
- Angina (MCQ160D = 1)
- Heart attack (MCQ160E = 1)
- Stroke (MCQ160F = 1)

#### eGFR (Estimated Glomerular Filtration Rate)

| Attribute | Value |
|-----------|-------|
| **Calculation** | CKD-EPI equation |
| **Inputs** | `LBXSCR` (creatinine), `RIAGENDR` (sex), `RIDAGEYR` (age) |
| **Study Variable** | `egfr` |
| **Units** | mL/min/1.73m² |

**CKD-EPI Equation**:
```
eGFR = 141 × min(Scr/κ, 1)^α × max(Scr/κ, 1)^(-1.209) × 0.993^Age × [1.018 if female] × [1.159 if Black]

Where:
- Scr = serum creatinine (mg/dL)
- κ = 0.7 (females) or 0.9 (males)
- α = -0.329 (females) or -0.411 (males)
```

#### Chronic Kidney Disease

| Attribute | Value |
|-----------|-------|
| **Study Variable** | `ckd` |
| **Definition** | eGFR <60 mL/min/1.73m² |
| **Categories** | Yes/No |

---

## Survey Design Variables

| Variable | NHANES Name | Description | Usage |
|----------|-------------|-------------|-------|
| Stratum | `SDMVSTRA` | Masked variance unit stratum | Variance estimation |
| PSU | `SDMVPSU` | Masked variance unit PSU | Variance estimation |
| Subsample Weight | `WTSA2YR` | Two-year subsample weight | PFAS analyses |
| MEC Weight | `WTMEC2YR` | Two-year MEC exam weight | When PFAS unavailable |

**Weight Adjustment for Pooled Cycles**:
```python
# For 4 cycles (2005-2012)
weight_4yr = WTSA2YR / 2  # For analyses excluding 1999-2000

# For all 5 cycles
weight_5yr = WTSA2YR / 5
```

---

## Variable Recoding Summary

### Numeric Variables

| Variable | Original | Recoding | Notes |
|----------|----------|----------|-------|
| PFAS | ng/mL | ln(ng/mL + 0.01) | Log-transform |
| Age | Years | Center at mean | For regression stability |
| BMI | kg/m² | None | Use as continuous |
| PIR | Ratio | Set >5 to 5 | Cap extreme values |
| eGFR | mL/min | None | Use as continuous |
| Alcohol | Drinks | Winsorize at 99th percentile | Handle outliers |

### Categorical Variables

| Variable | Original Codes | Study Categories |
|----------|----------------|------------------|
| Sex | 1, 2 | Male, Female |
| Race/Ethnicity | 1-7 | 5 categories |
| Education | 1-5 | 4 categories |
| Smoking | Multiple | 3 categories |
| Diabetes | 1, 2, 3 | Yes/No/Unknown |
| Hypertension | Multiple | Yes/No |
| CVD | Multiple | Yes/No |

---

## Missing Data Handling

### Missing Data Patterns

| Variable Type | Strategy |
|---------------|----------|
| PFAS (<LOD) | LOD/√2 imputation |
| PFAS (missing) | Exclude from specific analysis |
| PhenoAge components | Multiple imputation if ≤1 missing |
| PhenoAge (>1 missing) | Complete case exclusion |
| Covariates | Complete case or single imputation |

### Imputation Methods

| Scenario | Method |
|----------|--------|
| Single missing PhenoAge component | Predictive mean matching |
| Missing covariates | Mode/median imputation or category for missing |
| Pattern missingness | Sensitivity analysis excluding cases |

---

## Variable Naming Convention

All study variables follow this naming convention:

```
{domain}_{specific}_{units}
```

Examples:
- `pfoa_ng_ml` - PFOA in ng/mL
- `ln_pfos` - Natural log of PFOS
- `phenoage_acceleration` - PhenoAge acceleration (years)
- `age_years` - Age in years
- `sex_female` - Indicator for female sex

---

## Data Validation Rules

### Range Checks

| Variable | Minimum | Maximum | Action if Outside |
|----------|---------|---------|-------------------|
| PFAS | 0 | 100 ng/mL | Flag for review |
| Albumin | 10 | 60 g/L | Flag for review |
| Creatinine | 20 | 1500 μmol/L | Flag for review |
| Glucose | 2 | 35 mmol/L | Flag for review |
| CRP | 0 | 100 mg/L | Winsorize at 99th %ile |
| PhenoAge | 5 | 110 years | Flag for review |
| Age | 18 | 85+ | Top-code at 85 |
| BMI | 10 | 80 | Winsorize at 99th %ile |

### Logical Consistsency

| Rule | Description |
|------|-------------|
| Age check | PhenoAge typically > Age (positive acceleration indicates biological age > chronological age) |
| Sex-specific ranges | Albumin, creatinine ranges differ by sex |
| Component correlation | PhenoAge components should correlate in expected directions |

---

## Output Variables for Analysis

### Primary Analysis Dataset

| Variable | Type | Description |
|----------|------|-------------|
| `seqn` | ID | NHANES respondent ID |
| `survey_cycle` | String | NHANES cycle (A, D, E, F, G) |
| `weight` | Float | Survey weight (adjusted) |
| `stratum` | Int | SDMVSTRA |
| `psu` | Int | SDMVPSU |
| `age_years` | Int | Age at examination |
| `sex` | Category | Male/Female |
| `race_ethnicity` | Category | 5-level race/ethnicity |
| `education` | Category | 4-level education |
| `pir` | Float | Poverty income ratio |
| `smoking_status` | Category | Never/Former/Current |
| `alcohol_drinks_per_week` | Float | Alcohol consumption |
| `physical_activity_met` | Float | MET-minutes per week |
| `bmi` | Float | Body mass index |
| `diabetes` | Binary | Diabetes status |
| `hypertension` | Binary | Hypertension status |
| `cvd_history` | Binary | CVD history |
| `egfr` | Float | eGFR |
| `ckd` | Binary | CKD status |
| `ln_pfoa` | Float | Log PFOA |
| `ln_pfos` | Float | Log PFOS |
| `ln_pfhxs` | Float | Log PFHxS |
| `ln_pfna` | Float | Log PFNA (may be NA for cycle A) |
| `phenoage` | Float | PhenoAge (years) |
| `phenoage_acceleration` | Float | PhenoAge acceleration (years) |

---

*Document Version*: 1.0  
*Last Updated*: February 13, 2026  
*Study ID*: pfas-phenoage-2026-02-13
