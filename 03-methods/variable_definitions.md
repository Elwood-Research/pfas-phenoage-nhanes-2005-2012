# Variable Definitions: Complete NHANES Variable Mapping

## Overview

This document provides comprehensive variable definitions for the PFAS and PhenoAge study, including all exposure variables (PFAS), outcome variables (PhenoAge components), covariates, and survey design variables.

---

## Variable Naming Conventions

### NHANES Variable Code Structure

NHANES variable codes follow standardized naming conventions:

| Prefix | Component Category |
|--------|-------------------|
| LBX | Laboratory result (numeric value) |
| LBD | Laboratory result (calculated/derived) |
| LBDPF | PFAS detection indicator (e.g., LBDPFOAL) |
| RID | Respondent identification/Demographics |
| RIAG | Respondent individual - gender |
| RIDRE | Respondent identification - race/ethnicity |
| DM | Demographics |
| SDMV | Survey design (masked variance) |
| WT | Survey weight |

### Year Suffix Mapping

| Suffix | Years | Notes |
|--------|-------|-------|
| D | 2005-2006 | |
| E | 2007-2008 | |
| F | 2009-2010 | |
| G | 2011-2012 | |
| H | 2013-2014 | PFAS panel expansion |
| I | 2015-2016 | PFAS panel expansion |
| J | 2017-2018 | PFAS panel expansion |

---

## Exposure Variables: PFAS

### Core PFAS Variables (All Cycles)

| Descriptive Name | NHANES Code | Dataset(s) | Data Type | Units | Missing Code | Detection Indicator |
|-----------------|-------------|------------|-----------|-------|--------------|---------------------|
| Perfluorooctanoic acid (PFOA) | LBXPFOA | PFC_D-J, PFAS_H-J | Continuous | ng/mL | . | LBDPFOAL |
| Perfluorooctane sulfonic acid (PFOS) | LBXPFOS | PFC_D-J, PFAS_H-J | Continuous | ng/mL | . | LBDPFOSL |
| Perfluorohexane sulfonic acid (PFHxS) | LBXPFHS | PFC_D-J, PFAS_H-J | Continuous | ng/mL | . | LBDPFHSL |
| Perfluorononanoic acid (PFNA) | LBXPFNA | PFC_D-J, PFAS_H-J | Continuous | ng/mL | . | LBDPFNAL |

### PFAS Detection Indicators

| Descriptive Name | NHANES Code | Dataset(s) | Data Type | Categories | Missing Code |
|-----------------|-------------|------------|-----------|------------|--------------|
| PFOA detection indicator | LBDPFOAL | PFC_D-J, PFAS_H-J | Categorical | 0=Detectable, 1=Below LOD | . |
| PFOS detection indicator | LBDPFOSL | PFC_D-J, PFAS_H-J | Categorical | 0=Detectable, 1=Below LOD | . |
| PFHxS detection indicator | LBDPFHSL | PFC_D-J, PFAS_H-J | Categorical | 0=Detectable, 1=Below LOD | . |
| PFNA detection indicator | LBDPFNAL | PFC_D-J, PFAS_H-J | Categorical | 0=Detectable, 1=Below LOD | . |

### Detection Limit Values by Cycle

| Compound | Cycle D (2005-2006) | Cycle E (2007-2008) | Cycle F (2009-2010) | Cycle G (2011-2012) | Cycles H-J (2013-2018) |
|----------|---------------------|---------------------|---------------------|---------------------|------------------------|
| PFOA | 0.1 ng/mL | 0.1 ng/mL | 0.1 ng/mL | 0.1 ng/mL | 0.07 ng/mL |
| PFOS | 0.2 ng/mL | 0.2 ng/mL | 0.2 ng/mL | 0.2 ng/mL | 0.14 ng/mL |
| PFHxS | 0.1 ng/mL | 0.1 ng/mL | 0.1 ng/mL | 0.1 ng/mL | 0.07 ng/mL |
| PFNA | 0.1 ng/mL | 0.1 ng/mL | 0.1 ng/mL | 0.1 ng/mL | 0.07 ng/mL |

### Expanded PFAS Panel (Cycles H-J Only)

| Descriptive Name | NHANES Code | Dataset | Data Type | Units | Missing Code |
|-----------------|-------------|---------|-----------|-------|--------------|
| Perfluorodecanoic acid (PFDA) | LBXPFDE | PFAS_H-J | Continuous | ng/mL | . |
| Perfluoroundecanoic acid (PFUnDA) | LBXPFUA | PFAS_H-J | Continuous | ng/mL | . |
| Perfluorododecanoic acid (PFDoDA) | LBXPFDO | PFAS_H-J | Continuous | ng/mL | . |
| Perfluorobutane sulfonic acid (PFBS) | LBXPFBS | PFAS_H-J | Continuous | ng/mL | . |
| Perfluoroheptanoic acid (PFHpA) | LBXPFHP | PFAS_H-J | Continuous | ng/mL | . |
| 2-(N-ethyl-PFOSA) acetate (EtFOSAA) | LBXEPAH | PFAS_H-J | Continuous | ng/mL | . |
| 2-(N-methyl-PFOSA) acetate (MeFOSAA) | LBXMPAH | PFAS_H-J | Continuous | ng/mL | . |
| Perfluorooctane sulfonamide (FOSA) | LBXPFOSA | PFAS_H-J | Continuous | ng/mL | . |
| n-methyl perfluorooctane sulfonamidoacetic acid (N-MeFOSAA) | LBXNMEF | PFAS_H-J | Continuous | ng/mL | . |

### PFAS Survey Weights

| Descriptive Name | NHANES Code | Dataset(s) | Data Type | Description | Missing Code |
|-----------------|-------------|------------|-----------|-------------|--------------|
| Two-year MEC weights - Subsample A | WTSA2YR | PFC_D, PFC_E, PFC_F, PFC_G | Continuous | Sampling weight for PFAS subsample | 0, . |
| Two-year Subsample B weights | WTSB2YR | PFAS_H, PFAS_I, PFAS_J | Continuous | Sampling weight for PFAS subsample | 0, . |

---

## Outcome Variables: PhenoAge Components

### Standard Biochemistry Profile (BIOPRO)

| Descriptive Name | NHANES Code | Dataset | Data Type | NHANES Units | PhenoAge Units | Conversion |
|-----------------|-------------|---------|-----------|--------------|----------------|------------|
| Albumin | LBXSAL | BIOPRO_D, F-J | Continuous | g/dL | g/dL | None |
| Albumin (SI) | LBDSALSI | BIOPRO_D, F-J | Continuous | g/L | - | Not used |
| Creatinine | LBXSCR | BIOPRO_D, F-J | Continuous | mg/dL | mg/dL | None |
| Creatinine (SI) | LBDSCRSI | BIOPRO_D, F-J | Continuous | umol/L | - | Not used |
| Glucose, refrigerated serum | LBXSGL | BIOPRO_D, F-J | Continuous | mg/dL | mg/dL | None |
| Glucose (SI) | LBDSGLSI | BIOPRO_D, F-J | Continuous | mmol/L | - | Not used |
| Alkaline phosphatase | LBXSAPSI | BIOPRO_D, F-J | Continuous | IU/L | U/L | None |

### C-Reactive Protein (CRP)

| Descriptive Name | NHANES Code | Dataset | Data Type | NHANES Units | PhenoAge Units | Conversion |
|-----------------|-------------|---------|-----------|--------------|----------------|------------|
| C-reactive protein | LBXCRP | CRP_D, E, F | Continuous | mg/dL | mg/L | × 10 |
| C-reactive protein | LBXCRP | High-sensitivity CRP in later cycles | Continuous | mg/L | mg/L | None |

**CRITICAL**: CRP requires unit conversion. Original NHANES CRP data is in mg/dL, but PhenoAge requires mg/L. Multiply by 10.

### Complete Blood Count (CBC)

| Descriptive Name | NHANES Code | Dataset | Data Type | Units | Missing Code |
|-----------------|-------------|---------|-----------|-------|--------------|
| White blood cell count | LBXWBCSI | CBC_D-J | Continuous | 1000 cells/μL | . |
| Lymphocyte percentage | LBXLYPCT | CBC_D-J | Continuous | % | . |
| Mean cell volume | LBXMCVSI | CBC_D-J | Continuous | fL | . |
| Red cell distribution width | LBXRDW | CBC_D-J | Continuous | % | . |
| Lymphocyte number | LBDLYMNO | CBC_D-J | Continuous | 1000 cells/μL | . |
| Monocyte percentage | LBXMOPCT | CBC_D-J | Continuous | % | . |
| Segmented neutrophils percent | LBXNEPCT | CBC_D-J | Continuous | % | . |
| Red blood cell count | LBXRBCSI | CBC_D-J | Continuous | million cells/μL | . |
| Hemoglobin | LBXHGB | CBC_D-J | Continuous | g/dL | . |
| Hematocrit | LBXHCT | CBC_D-J | Continuous | % | . |

### Alternative Glucose Source

| Descriptive Name | NHANES Code | Dataset | Data Type | Units | Missing Code | Notes |
|-----------------|-------------|---------|-----------|-------|--------------|-------|
| Fasting glucose | LBXGLU | GLU_D-J | Continuous | mg/dL | . | Fasting subsample only |
| Plasma glucose | LBXPLASI | GHB_D-J | Continuous | mmol/L | . | Convert to mg/dL |

---

## Covariates: Demographics

### Core Demographics (DEMO)

| Descriptive Name | NHANES Code | Dataset | Data Type | Categories | Missing Code |
|-----------------|-------------|---------|-----------|------------|--------------|
| Respondent sequence number | SEQN | All | Identifier | Unique identifier | None |
| Age in years at screening | RIDAGEYR | DEMO_B-J | Continuous | 0-120 years | . |
| Age in months at screening | RIDAGEMN | DEMO_B-J | Continuous | 0-1440 months | . |
| Gender | RIAGENDR | DEMO_B-J | Binary | 1=Male, 2=Female | . |
| Race/Hispanic origin | RIDRETH1 | DEMO_B-J | Categorical | 1=Mexican American, 2=Other Hispanic, 3=Non-Hispanic White, 4=Non-Hispanic Black, 5=Other/Multi-racial | . |
| Race/Hispanic origin w/ NH Asian | RIDRETH3 | DEMO_H-J | Categorical | 1=Mexican American, 2=Other Hispanic, 3=Non-Hispanic White, 4=Non-Hispanic Black, 6=Non-Hispanic Asian, 7=Other/Multi-racial | . |

### Education and Socioeconomic Status

| Descriptive Name | NHANES Code | Dataset | Data Type | Categories | Missing Code |
|-----------------|-------------|---------|-----------|------------|--------------|
| Education level - Adults 20+ | DMDEDUC2 | DEMO_B-J | Ordinal | 1=<9th grade, 2=9-11th grade, 3=High school graduate/GED, 4=Some college/AA degree, 5=College graduate or above, 7=Refused, 9=Don't know | 7, 9, . |
| Family income to poverty ratio | INDFMPIR | DEMO_B-J | Continuous | 0-5 (values >5 capped at 5) | . |
| Annual family income | INDFMINC/INDFMIN2 | DEMO_B-J | Categorical | Income categories | 77, 99, . |

### Pregnancy Status

| Descriptive Name | NHANES Code | Dataset | Data Type | Categories | Missing Code |
|-----------------|-------------|---------|-----------|------------|--------------|
| Pregnancy status | RIDEXPRG | DEMO_B-J | Categorical | 1=Yes, positive lab pregnancy test or self-reported pregnant, 2=No, not pregnant, 3=Cannot ascertain | . |

**Exclusion**: Participants with RIDEXPRG = 1 will be excluded from analysis.

---

## Covariates: Health Behaviors

### Smoking Status (SMQ)

| Descriptive Name | NHANES Code | Dataset | Data Type | Categories | Missing Code |
|-----------------|-------------|---------|-----------|------------|--------------|
| Smoked at least 100 cigarettes | SMQ020 | SMQ_B-J | Binary | 1=Yes, 2=No, 7=Refused, 9=Don't know | 7, 9, . |
| Do you now smoke cigarettes? | SMQ040 | SMQ_B-J | Categorical | 1=Every day, 2=Some days, 3=Not at all, 7=Refused, 9=Don't know | 7, 9, . |

**Derived Smoking Status Categories**:
- Never smoker: SMQ020 = 2
- Former smoker: SMQ020 = 1 AND SMQ040 = 3
- Current smoker: SMQ020 = 1 AND (SMQ040 = 1 OR SMQ040 = 2)

### Alcohol Use (ALQ)

| Descriptive Name | NHANES Code | Dataset | Data Type | Categories | Missing Code |
|-----------------|-------------|---------|-----------|------------|--------------|
| Had at least 12 alcohol drinks/year | ALQ110 | ALQ_B-J | Binary | 1=Yes, 2=No, 7=Refused, 9=Don't know | 7, 9, . |
| Avg # alcoholic drinks/day past 12 mo | ALQ130 | ALQ_B-J | Continuous | 1-99 drinks | 777, 999, . |

### Physical Activity (PAQ)

| Descriptive Name | NHANES Code | Dataset | Data Type | Categories | Missing Code |
|-----------------|-------------|---------|-----------|------------|--------------|
| Vigorous work activity | PAQ605 | PAQ_H-J | Binary | 1=Yes, 2=No | . |
| Moderate work activity | PAQ620 | PAQ_H-J | Binary | 1=Yes, 2=No | . |
| Vigorous recreational activities | PAQ650 | PAQ_H-J | Binary | 1=Yes, 2=No | . |
| Moderate recreational activities | PAQ665 | PAQ_H-J | Binary | 1=Yes, 2=No | . |

---

## Covariates: Health Status and Anthropometry

### Body Measurements (BMX)

| Descriptive Name | NHANES Code | Dataset | Data Type | Units | Missing Code |
|-----------------|-------------|---------|-----------|-------|--------------|
| Body mass index | BMXBMI | BMX_B-J | Continuous | kg/m² | . |
| Weight | BMXWT | BMX_B-J | Continuous | kg | . |
| Standing height | BMXHT | BMX_B-J | Continuous | cm | . |
| Waist circumference | BMXWAIST | BMX_B-J | Continuous | cm | . |

### Blood Pressure (BPX)

| Descriptive Name | NHANES Code | Dataset | Data Type | Units | Missing Code |
|-----------------|-------------|---------|-----------|-------|--------------|
| Systolic blood pressure - 1st reading | BPXSY1 | BPX_B-J | Continuous | mmHg | . |
| Diastolic blood pressure - 1st reading | BPXDI1 | BPX_B-J | Continuous | mmHg | . |

### Diabetes Questionnaire (DIQ)

| Descriptive Name | NHANES Code | Dataset | Data Type | Categories | Missing Code |
|-----------------|-------------|---------|-----------|------------|--------------|
| Doctor told you have diabetes | DIQ010 | DIQ_B-J | Categorical | 1=Yes, 2=No, 3=Borderline, 7=Refused, 9=Don't know | 7, 9, . |
| Taking insulin now | DIQ050 | DIQ_B-J | Binary | 1=Yes, 2=No, 7=Refused, 9=Don't know | 7, 9, . |
| Taking diabetic pills | DIQ070 | DIQ_B-J | Binary | 1=Yes, 2=No, 7=Refused, 9=Don't know | 7, 9, . |

**Derived Diabetes Status**: DIQ010 = 1 OR taking insulin OR taking diabetic pills

### Medical Conditions (MCQ)

| Descriptive Name | NHANES Code | Dataset | Data Type | Categories | Missing Code |
|-----------------|-------------|---------|-----------|------------|--------------|
| Ever told you had heart attack | MCQ160E | MCQ_B-J | Categorical | 1=Yes, 2=No, 7=Refused, 9=Don't know | 7, 9, . |
| Ever told you had stroke | MCQ160F | MCQ_B-J | Categorical | 1=Yes, 2=No, 7=Refused, 9=Don't know | 7, 9, . |
| Ever told you had coronary heart disease | MCQ160C | MCQ_B-J | Categorical | 1=Yes, 2=No, 7=Refused, 9=Don't know | 7, 9, . |
| Ever told you had heart failure | MCQ160B | MCQ_B-J | Categorical | 1=Yes, 2=No, 7=Refused, 9=Don't know | 7, 9, . |

**Derived CVD Status**: MCQ160E = 1 OR MCQ160F = 1 OR MCQ160C = 1 OR MCQ160B = 1

### Blood Pressure Questionnaire (BPQ)

| Descriptive Name | NHANES Code | Dataset | Data Type | Categories | Missing Code |
|-----------------|-------------|---------|-----------|------------|--------------|
| Ever told you had hypertension | BPQ020 | BPQ_B-J | Categorical | 1=Yes, 2=No, 7=Refused, 9=Don't know | 7, 9, . |
| Taking prescription for hypertension | BPQ050A | BPQ_B-J | Categorical | 1=Yes, 2=No, 7=Refused, 9=Don't know | 7, 9, . |

**Derived Hypertension Status**: BPQ020 = 1 OR taking BP medication OR average SBP ≥140 OR average DBP ≥90

---

## Survey Design Variables

### Masked Variance Units

| Descriptive Name | NHANES Code | Dataset | Data Type | Description | Missing Code |
|-----------------|-------------|---------|-----------|-------------|--------------|
| Masked variance pseudo-PSU | SDMVPSU | DEMO_B-J | Categorical | 1 or 2 | . |
| Masked variance pseudo-stratum | SDMVSTRA | DEMO_B-J | Categorical | 1-100+ | . |

### Usage in Analysis
- **SDMVPSU**: Primary sampling unit for variance estimation (clustering)
- **SDMVSTRA**: Stratum for variance estimation (stratification)
- Combine with survey weights for proper variance estimation

### Combined Cycle Weights

| Descriptive Name | Calculation | Purpose |
|-----------------|-------------|---------|
| Adjusted survey weight | WTSB2YR / 7 or WTSA2YR / 7 | Combined 2005-2018 analysis |
| 4-year weight | WTSB2YR / 2 | When combining 2 cycles |
| 2-year weight | WTSB2YR | Single cycle analysis |

---

## Derived Variables

### PhenoAge Variables

| Descriptive Name | Calculation | Data Type | Units |
|-----------------|-------------|-----------|-------|
| Linear predictor | Sum of biomarker × coefficient | Continuous | - |
| Mortality score (M) | 1 - exp(-exp(linear_predictor)) | Continuous | 0-1 |
| PhenoAge | 141.5 + (ln(-0.00553 × ln(1-M)) / 0.09165) | Continuous | years |
| PhenoAge acceleration | PhenoAge - RIDAGEYR | Continuous | years |
| Log-transformed PFAS | ln(PFAS + LOD/√2 for non-detects) | Continuous | ln(ng/mL) |

### Categorical Groupings

| Descriptive Name | Base Variables | Categories |
|-----------------|----------------|------------|
| Smoking status | SMQ020, SMQ040 | Never, Former, Current |
| Race/ethnicity (3-level) | RIDRETH1 | Hispanic, Non-Hispanic White, Non-Hispanic Black, Other |
| Education (2-level) | DMDEDUC2 | <College graduate, College graduate |
| Income (2-level) | INDFMPIR | <2.0 (poor/near-poor), ≥2.0 |
| BMI categories | BMXBMI | <25 (normal), 25-30 (overweight), ≥30 (obese) |
| Age groups | RIDAGEYR | 18-39, 40-59, 60+ years |

---

## Missing Value Handling Codes

### Standard NHANES Missing Codes

| Code | Meaning | Action |
|------|---------|--------|
| . | Missing | Exclude from analysis |
| 7 / 77 | Refused | Exclude from analysis |
| 9 / 99 | Don't know | Exclude from analysis |
| 0 | Zero value / Not applicable | Check context |
| .L | Below LOD | Substitute LOD/√2 |

### Laboratory Missing Indicators

| Dataset | Missing Code | Description |
|---------|--------------|-------------|
| PFAS | . | No laboratory result |
| PFAS comment codes | 0 | At or above detection limit |
| PFAS comment codes | 1 | Below lower detection limit |

---

## Variable Cross-Reference Table

### Analysis Variables Summary

| Role | Variable | NHANES Code | Dataset | Cycles |
|------|----------|-------------|---------|--------|
| **Exposures** | | | | |
| PFOA | LBXPFOA | PFC, PFAS | D-J | |
| PFOS | LBXPFOS | PFC, PFAS | D-J | |
| PFHxS | LBXPFHS | PFC, PFAS | D-J | |
| PFNA | LBXPFNA | PFC, PFAS | D-J | |
| **Outcome** | | | | |
| PhenoAgeAccel | Derived | - | - | D-J |
| **Covariates** | | | | |
| Age | RIDAGEYR | DEMO | B-J | |
| Sex | RIAGENDR | DEMO | B-J | |
| Race/ethnicity | RIDRETH1 | DEMO | B-J | |
| Education | DMDEDUC2 | DEMO | B-J | |
| Income ratio | INDFMPIR | DEMO | B-J | |
| BMI | BMXBMI | BMX | B-J | |
| Smoking | SMQ020, SMQ040 | SMQ | B-J | |
| Diabetes | DIQ010 | DIQ | B-J | |
| Hypertension | BPQ020, BPQ050A | BPQ | B-J | |
| CVD | MCQ160 series | MCQ | B-J | |
| **Survey Design** | | | | |
| PSU | SDMVPSU | DEMO | B-J | |
| Stratum | SDMVSTRA | DEMO | B-J | |
| Weight | WTSA2YR/WTSB2YR | PFC/PFAS | D-J | |

---

## Data Integration Requirements

### Merge Strategy

1. **Primary Key**: SEQN (Respondent sequence number)
2. **Merge Type**: Inner join to retain complete cases
3. **Order of Operations**:
   - Merge demographics with all datasets
   - Apply inclusion/exclusion criteria
   - Calculate derived variables
   - Handle missing values
   - Calculate PhenoAge
   - Merge with PFAS data
   - Final analytic dataset

### Required Datasets by Cycle

| Cycle | Datasets Required |
|-------|-------------------|
| D (2005-2006) | DEMO_D, PFC_D, BIOPRO_D, CBC_D, CRP_D, BMX_D, BPX_D, DIQ_D, BPQ_D, MCQ_D, SMQ_D |
| E (2007-2008) | DEMO_E, PFC_E, BIOPRO_E, CBC_E, CRP_E, BMX_E, BPX_E, DIQ_E, BPQ_E, MCQ_E, SMQ_E |
| F (2009-2010) | DEMO_F, PFC_F, BIOPRO_F, CBC_F, CRP_F, BMX_F, BPX_F, DIQ_F, BPQ_F, MCQ_F, SMQ_F |
| G (2011-2012) | DEMO_G, PFC_G, BIOPRO_G, CBC_G, BMX_G, BPX_G, DIQ_G, BPQ_G, MCQ_G, SMQ_G |
| H (2013-2014) | DEMO_H, PFAS_H, BIOPRO_H, CBC_H, BMX_H, BPX_H, DIQ_H, BPQ_H, MCQ_H, SMQ_H |
| I (2015-2016) | DEMO_I, PFAS_I, BIOPRO_I, CBC_I, BMX_I, BPX_I, DIQ_I, BPQ_I, MCQ_I, SMQ_I |
| J (2017-2018) | DEMO_J, PFAS_J, BIOPRO_J, CBC_J, BMX_J, BPX_J, DIQ_J, BPQ_J, MCQ_J, SMQ_J |

---

## References

1. NHANES Data Documentation (various cycles). Centers for Disease Control and Prevention.
2. Levine, M. E., et al. (2018). An epigenetic biomarker of aging for lifespan and healthspan. Aging, 10(4), 573-591.
3. NHANES Analytic Guidelines. National Center for Health Statistics.
4. NHANES Laboratory Procedures Manual (various years). Centers for Disease Control and Prevention.
