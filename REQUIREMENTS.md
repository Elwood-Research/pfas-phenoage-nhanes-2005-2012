# Data Requirements

## Primary Exposure Variables

### PFAS Serum Concentrations
**Source Datasets**: PFC_D (2005-2006), PFC_E (2007-2008), PFC_F (2009-2010), PFC_G (2011-2012), SSPFC_A (1999-2000)

**Key Variables**:
- `LBXPFOA` - Perfluorooctanoic acid (ng/mL)
- `LBXPFOS` - Perfluorooctane sulfonic acid (ng/mL)  
- `LBXPFHS` - Perfluorohexane sulfonic acid (ng/mL)
- `LBXPFNA` - Perfluorononanoic acid (ng/mL)
- `LBXPFDE` - Perfluorodecanoic acid (ng/mL)

## Outcome Variables

### PhenoAge Components
PhenoAge is calculated from the following biomarkers available in NHANES:

**Clinical Chemistry** (BIOPRO, L40, LAB18 datasets):
- Albumin (g/L)
- Creatinine (μmol/L)
- Glucose (mmol/L)
- C-reactive protein (CRP, mg/L)
- Lymphocyte percentage (%)
- Mean corpuscular volume (MCV, fL)
- Red cell distribution width (RDW, %)
- Alkaline phosphatase (ALP, U/L)
- White blood cell count (WBC, 10^9/L)

## Covariates

### Demographics (DEMO datasets)
- Age (years)
- Sex (Male/Female)
- Race/Ethnicity
- Education level
- Poverty income ratio

### Health Behaviors
- Smoking status (SMQ datasets)
- Alcohol consumption (ALQ datasets)
- Physical activity (PAQ datasets)
- BMI (BMX datasets)

### Health Conditions
- Diabetes status (DIQ datasets)
- Hypertension (BPX datasets)
- Cardiovascular disease (MCQ datasets)

## Survey Design Variables
- `SDMVSTRA` - Stratum
- `SDMVPSU` - Primary sampling unit
- `WTMEC2YR` or `WTSA2YR` - Sample weights

## Data Integration Notes

- Merge using `SEQN` (Respondent sequence number)
- PFAS data uses subsample weights (`WTSA2YR`)
- Apply appropriate survey design variables for variance estimation
- Handle detection limits for PFAS variables (below LOD codes)
