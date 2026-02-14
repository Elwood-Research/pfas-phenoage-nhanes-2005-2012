# Data Requirements

## PhenoAge Biomarkers
- Age (RIDAGEYR from DEMO)
- Albumin (LBXSALSI from BIOPRO)
- Creatinine (LBXSCR from BIOPRO)
- Glucose (LBXGLU from GLU or BIOPRO)
- C-reactive protein (LBXCRP from CRP or BIOPRO)
- Lymphocyte % (LBXLYPCT from CBC)
- Mean cell volume (LBXMCVSI from CBC)
- Red cell distribution width (LBXRDW from CBC) **CRITICAL: Use LBXRDW**
- Alkaline phosphatase (LBXSAPSI from BIOPRO)
- White blood cell count (LBXWBCSI from CBC)

## PFAS Exposures
- PFOS (perfluorooctane sulfonate)
- PFOA (perfluorooctanoic acid)
- PFHxS (perfluorohexane sulfonate)
- PFNA (perfluorononanoic acid)
- Dataset prefix: PFC or PFAS (cycles D, E, F, G, H, I, J)

## Covariates
- Demographics: age, sex, race/ethnicity, education, income
- Lifestyle: smoking, alcohol, BMI, physical activity
- Health status: diabetes, hypertension, cardiovascular disease

## Sample Design Variables
- WTMEC2YR (MEC exam weight)
- SDMVPSU (masked variance pseudo-PSU)
- SDMVSTRA (masked variance pseudo-stratum)
