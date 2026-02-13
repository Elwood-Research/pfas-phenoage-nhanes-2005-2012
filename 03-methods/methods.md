# PFAS and PhenoAge Study: Methods Documentation

## Study Design

### Overview
This cross-sectional analysis examines associations between serum concentrations of per- and polyfluoroalkyl substances (PFAS) and biological aging measured by PhenoAge in the National Health and Nutrition Examination Survey (NHANES). The study uses data from multiple NHANES cycles spanning 2005-2018, representing the most recent nationally representative data with both PFAS measurements and complete biomarker panels for PhenoAge calculation.

### Study Design Characteristics
- **Design Type**: Cross-sectional analysis of nationally representative survey data
- **Data Source**: National Health and Nutrition Examination Survey (NHANES)
- **Study Period**: 2005-2018 (combined across 7 survey cycles)
- **Geographic Coverage**: United States (nationally representative)
- **Sampling Method**: Complex multistage probability sampling with oversampling of specific demographic groups

### NHANES Cycles Included

| Cycle Code | Years        | Primary PFAS Dataset | Notes                                  |
|------------|--------------|----------------------|----------------------------------------|
| D          | 2005-2006    | PFC_D                | Limited PFAS panel (4 main compounds)  |
| E          | 2007-2008    | PFC_E                | Limited PFAS panel                     |
| F          | 2009-2010    | PFC_F                | Limited PFAS panel                     |
| G          | 2011-2012    | PFC_G                | Limited PFAS panel                     |
| H          | 2013-2014    | PFAS_H               | Expanded PFAS panel (12 compounds)     |
| I          | 2015-2016    | PFAS_I               | Expanded PFAS panel                    |
| J          | 2017-2018    | PFAS_J               | Expanded PFAS panel                    |

**Note**: The dataset naming convention changed from "PFC" (Polyfluoroalkyl Chemicals) to "PFAS" (Per- and Polyfluoroalkyl Substances) starting with the 2013-2014 cycle. The expanded panel in cycles H-J includes additional compounds beyond the four legacy PFAS (PFOA, PFOS, PFHxS, PFNA).

### Rationale for Cycle Selection
- PFAS measured in a random one-third subsample of participants aged 12+ years
- Complete biomarker data required for PhenoAge calculation available across these cycles
- Weight variables appropriate for subsample analysis available
- Consistent laboratory methods and quality control procedures

---

## Data Sources and Integration

### Primary Datasets

| Dataset Prefix | Description                              | Years Available | Key Variables                        |
|----------------|------------------------------------------|-----------------|--------------------------------------|
| DEMO           | Demographics                             | All cycles      | Age, sex, race, education, income    |
| PFC/PFAS       | PFAS measurements                        | D-J             | Serum PFAS concentrations            |
| BIOPRO         | Standard biochemistry profile            | D, F-J          | Albumin, creatinine, glucose, ALP    |
| CBC            | Complete blood count                     | D-J             | Lymphocyte %, MCV, RDW, WBC          |
| CRP            | C-reactive protein                       | D-F             | High-sensitivity CRP                 |
| GLU            | Plasma glucose                           | D-J             | Fasting glucose (supplemental)       |

### Dataset Integration Strategy
1. **Primary Key**: SEQN (Respondent sequence number) used for all merges
2. **Merge Type**: Inner join to retain only participants with complete data
3. **Cycle Consistency**: Variables harmonized across cycles accounting for measurement changes

---

## Study Population and Eligibility Criteria

### Inclusion Criteria
1. **Age**: Adults aged 18 years and older at examination
2. **PFAS Data**: Complete serum PFAS measurements for at least PFOA, PFOS, PFHxS, and PFNA
3. **PhenoAge Components**: All 9 biomarkers required for PhenoAge calculation:
   - Albumin (LBXSAL)
   - Creatinine (LBXSCR)
   - Glucose (LBXSGL from BIOPRO or LBXGLU from GLU)
   - C-reactive protein (LBXCRP)
   - Lymphocyte percentage (LBXLYPCT)
   - Mean corpuscular volume (LBXMCVSI)
   - Red cell distribution width (LBXRDW)
   - Alkaline phosphatase (LBXSAPSI)
   - White blood cell count (LBXWBCSI)
4. **Survey Weights**: Valid subsample weights available (WTSA2YR or WTSB2YR)

### Exclusion Criteria
1. **Missing Data**: Any missing value in required PhenoAge biomarkers
2. **Pregnancy**: Pregnant women excluded (RIDEXPRG = 1)
3. **Extreme Outliers**: Observations with |z-score| > 4 on continuous variables
4. **Inadequate Sample Weight**: Missing or zero survey weights
5. **PFAS Below Detection**: Handled via substitution (see Exposure Assessment section)

### STROBE Compliance

This study adheres to the STROBE (Strengthening the Reporting of Observational Studies in Epidemiology) guidelines for cross-sectional studies.

#### STROBE Checklist Completion

| Item | Description                              | Location in Manuscript |
|------|------------------------------------------|------------------------|
| 1a   | Title and abstract indicating design     | Title, Abstract        |
| 2    | Background/rationale                     | Introduction           |
| 3    | Study objectives                         | Introduction           |
| 4    | Study design                             | Methods (this section) |
| 5    | Setting, location, timing                | Methods                |
| 6a   | Eligibility criteria                     | Methods                |
| 6b   | Matching criteria (N/A)                  | N/A                    |
| 6c   | Treatment/exposure details               | Methods                |
| 7a   | Outcome definitions                      | Methods                |
| 7b   | Diagnostic criteria (N/A)                | N/A                    |
| 8    | Data sources, measurement methods        | Methods                |
| 9    | Bias assessment                          | Methods/Discussion     |
| 10a| Quantitative variables, categories       | Methods/Tables         |
| 10b| Outlier handling, cutpoints              | Methods                |
| 11   | Missing data handling                    | Methods                |
| 12a| Participants, flow diagram               | Results/Figure         |
| 12b| Reasons for non-participation            | Results                |
| 12c| Follow-up (N/A for cross-sectional)      | N/A                    |
| 13a| Participants, descriptive data           | Results/Table 1        |
| 13b| Missing data for each variable           | Results/Tables         |
| 14   | Descriptive outcome data                 | Results                |
| 15   | Main results, associations               | Results                |
| 16a| Sensitivity analyses                     | Results/Appendix       |
| 16b| Analytical methods for subgroups         | Methods                |
| 17   | Other analyses performed                 | Results/Appendix       |
| 18   | Key results, interpretation              | Discussion             |
| 19   | Limitations                              | Discussion             |
| 20   | Generalizability                         | Discussion             |
| 21   | Other information, funding               | Acknowledgments        |
| 22   | Data availability                        | Data Availability      |

### Sample Flow Diagram (STROBE Figure)

A detailed flow diagram will be constructed showing:
1. Total NHANES participants per cycle
2. Number aged 18+ years
3. Number with PFAS measurements
4. Number with complete PhenoAge biomarkers
5. Exclusions for pregnancy, outliers, missing weights
6. Final analytic sample size

---

## Exposure Assessment: PFAS Measurement

### Laboratory Methods

#### Specimen Collection and Processing
- **Sample Type**: Serum from whole blood collected via venipuncture
- **Collection Tubes**: Red-top, serum separator tubes (SST)
- **Processing**: Centrifugation within 2 hours of collection
- **Storage**: Frozen at -70°C until analysis
- **Shipping**: Shipped on dry ice to analytical laboratories

#### Analytical Methodology
- **Primary Method**: Solid-phase extraction (SPE) coupled with high-performance liquid chromatography-tandem mass spectrometry (HPLC-MS/MS)
- **Detection**: Electrospray ionization in negative ion mode
- **Quality Control**: 
  - Calibration curves with isotope-labeled internal standards
  - Quality control samples in each analytical batch
  - Inter-laboratory proficiency testing
  - Blank samples to assess contamination

### PFAS Compounds Measured

#### Core PFAS (All Cycles D-J)

| Compound | Abbreviation | NHANES Variable | CAS Number   | Molecular Formula |
|----------|--------------|-----------------|--------------|-------------------|
| Perfluorooctanoic acid | PFOA | LBXPFOA | 335-67-1 | C8HF15O2 |
| Perfluorooctane sulfonic acid | PFOS | LBXPFOS | 1763-23-1 | C8HF17O3S |
| Perfluorohexane sulfonic acid | PFHxS | LBXPFHS | 355-46-4 | C6HF13O3S |
| Perfluorononanoic acid | PFNA | LBXPFNA | 375-95-1 | C9HF17O2 |

#### Additional PFAS (Cycles H-J Only)

| Compound | Abbreviation | NHANES Variable |
|----------|--------------|-----------------|
| Perfluorodecanoic acid | PFDA | LBXPFDE |
| Perfluoroundecanoic acid | PFUnDA | LBXPFUA |
| Perfluorododecanoic acid | PFDoDA | LBXPFDO |
| Perfluorobutane sulfonic acid | PFBS | LBXPFBS |
| Perfluoroheptanoic acid | PFHpA | LBXPFHP |
| 2-(N-ethyl-PFOSA) acetate | EtFOSAA | LBXEPAH |
| 2-(N-methyl-PFOSA) acetate | MeFOSAA | LBXMPAH |
| Perfluorooctane sulfonamide | FOSA | LBXPFOSA |

### Detection Limits and Handling

#### Detection Limit Values by Cycle

| Compound | Cycle D (ng/mL) | Cycle E (ng/mL) | Cycle F (ng/mL) | Cycle G (ng/mL) | Cycles H-J (ng/mL) |
|----------|-----------------|-----------------|-----------------|-----------------|--------------------|
| PFOA | 0.1 | 0.1 | 0.1 | 0.1 | 0.07 |
| PFOS | 0.2 | 0.2 | 0.2 | 0.2 | 0.14 |
| PFHxS | 0.1 | 0.1 | 0.1 | 0.1 | 0.07 |
| PFNA | 0.1 | 0.1 | 0.1 | 0.1 | 0.07 |

#### Values Below Detection Limit
- **Indicator Variables**: Each PFAS has a comment code variable (e.g., LBDPFOAL) indicating detection status
  - 0 = At or above detection limit
  - 1 = Below lower detection limit
- **Substitution Method**: Values below detection limit are substituted with LOD/√2 (detection limit divided by square root of 2)
- **Alternative Approaches**: Sensitivity analyses will compare:
  - LOD/√2 substitution
  - LOD/2 substitution
  - Multiple imputation
  - Maximum likelihood estimation

### Units and Transformations
- **Primary Units**: ng/mL (nanograms per milliliter), equivalent to μg/L
- **Log Transformation**: Natural log transformation applied for regression analyses due to right-skewed distributions
- **Standardization**: z-scores calculated for mixture analyses

---

## Outcome Assessment: PhenoAge Calculation

### Overview
PhenoAge (Levine et al., 2018) is a DNA methylation-based measure of biological aging that captures system-level dysregulation across multiple organ systems. The clinical version of PhenoAge can be calculated from routine blood chemistry markers.

### Biomarker Components

| Biomarker | NHANES Variable(s) | Units Required | NHANES Units | Conversion Factor |
|-----------|-------------------|----------------|--------------|-------------------|
| Albumin | LBXSAL, LBDSALSI | g/dL | g/dL | None needed |
| Creatinine | LBXSCR, LBDSCRSI | mg/dL | mg/dL | None needed |
| Glucose | LBXSGL, LBDSGLSI | mg/dL | mg/dL | None needed |
| C-reactive protein | LBXCRP | mg/L | mg/dL | × 10 |
| Lymphocyte percentage | LBXLYPCT | % | % | None needed |
| Mean cell volume | LBXMCVSI | fL | fL | None needed |
| Red cell distribution width | LBXRDW | % | % | None needed |
| Alkaline phosphatase | LBXSAPSI | U/L | IU/L | None needed |
| White blood cell count | LBXWBCSI | 1000 cells/μL | 1000 cells/μL | None needed |
| Chronological age | RIDAGEYR | years | years | None needed |

**Note**: CRP requires unit conversion from mg/dL to mg/L (multiply by 10).

### PhenoAge Algorithm

#### Step 1: Calculate Mortality Score (M)

```
M = 1 - exp(-exp(-11.99 + 
    (0.0296 * Albumin_gdL) +
    (-0.0189 * Creatinine_mgdL) +
    (0.00133 * Glucose_mgdL) +
    (0.000878 * CRP_mgL) +
    (-0.0375 * Lymphocyte_pct) +
    (0.00887 * MCV_fL) +
    (0.0228 * RDW_pct) +
    (0.00199 * ALP_UL) +
    (0.0554 * WBC_1000uL) +
    (0.0804 * Age_years)))
```

#### Step 2: Calculate PhenoAge

```
PhenoAge = 141.5 + (log(-0.00553 * log(1 - M)) / 0.09165)
```

#### Step 3: Calculate PhenoAge Acceleration (PhenoAgeAccel)

```
PhenoAgeAccel = PhenoAge - Chronological_Age
```

**Positive PhenoAgeAccel** indicates accelerated biological aging (biological age > chronological age).
**Negative PhenoAgeAccel** indicates decelerated biological aging (biological age < chronological age).

### Detailed Calculation Procedure

See separate document `phenoage_calculation.md` for complete step-by-step calculation with unit conversions and Python implementation.

---

## Covariate Definitions

### Demographic Variables

| Variable | NHANES Code | Categories/Description | Data Type |
|----------|-------------|------------------------|-----------|
| Age | RIDAGEYR | Continuous, 18+ years | Continuous |
| Sex | RIAGENDR | 1=Male, 2=Female | Binary |
| Race/Ethnicity | RIDRETH1 | 1=Mexican American, 2=Other Hispanic, 3=Non-Hispanic White, 4=Non-Hispanic Black, 5=Other/Multi-racial | Categorical |
| Education | DMDEDUC2 | 1=<9th grade, 2=9-11th, 3=High school, 4=Some college, 5=College graduate | Ordinal |
| Family Income | INDFMPIR | Ratio of family income to poverty threshold | Continuous |

### Health Behavior Variables

| Variable | NHANES Code/Source | Categories | Data Type |
|----------|-------------------|------------|-----------|
| Smoking Status | SMQ020/SMQ040 | Never, Former, Current | Categorical |
| Physical Activity | PAQ series | MET-minutes/week | Continuous |
| Alcohol Use | ALQ series | Drinks/day | Continuous |

### Health Status Variables

| Variable | NHANES Code | Categories/Description | Data Type |
|----------|-------------|------------------------|-----------|
| BMI | BMXBMI | kg/m² | Continuous |
| Hypertension | BPQ020/BPQ050A | Yes/No | Binary |
| Diabetes | DIQ010 | Yes/No | Binary |
| Cardiovascular Disease | MCQ160 series | Yes/No | Binary |
| eGFR | Calculated from LBXSCR | mL/min/1.73m² | Continuous |

### Handling of Categorical Variables
- **Level Exclusion**: Categories with <5% membership collapsed into "Other" or adjacent category
- **Reference Categories**: 
  - Sex: Female
  - Race/Ethnicity: Non-Hispanic White
  - Education: College graduate
  - Smoking: Never smokers

---

## Statistical Analysis Plan

### Primary Analysis

#### Main Exposures
- Individual PFAS: PFOA, PFOS, PFHxS, PFNA (continuous, ln-transformed)
- PFAS as mixtures: WQS and BKMR models

#### Primary Outcome
- PhenoAge acceleration (continuous)

#### Statistical Models

**Model 1 (Crude)**
- Survey-weighted linear regression
- Single PFAS predictor
- Adjusted for chronological age and sex

**Model 2 (Adjusted)**
- Survey-weighted linear regression
- Single PFAS predictor
- Adjusted for: age, sex, race/ethnicity, education, income, BMI, smoking

**Model 3 (Fully Adjusted)**
- Survey-weighted linear regression
- All four PFAS simultaneously
- Adjusted for all covariates in Model 2 plus health conditions (diabetes, hypertension, CVD)

### Survey Design and Weighting

#### Weight Selection
- **Primary Weight**: Subsample weights (WTSA2YR for cycles D-G, WTSB2YR for cycles H-J)
- **Weight Adjustment**: Weights divided by number of cycles combined (divide by 7)

#### Variance Estimation
- **Strata**: SDMVSTRA (masked variance unit stratum)
- **PSU**: SDMVPSU (masked variance unit primary sampling unit)
- **Method**: Taylor series linearization

#### Survey Design Specification (Python)
```python
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.weightstats import DescrStatsW

# Survey design for variance estimation
def get_survey_design(df):
    """Configure survey design for NHANES analysis"""
    design = {
        'weights': df['WTSA2YR'] / 7,  # Divide by number of cycles
        'strata': df['SDMVSTRA'],
        'psu': df['SDMVPSU'],
        'nest': True
    }
    return design
```

### Missing Data Handling

#### Missing Data Patterns
- **Complete Case Analysis**: Primary analysis restricted to complete cases
- **Missingness Assessment**: Patterns assessed by demographic characteristics
- **Sensitivity Analysis**: Multiple imputation by chained equations (MICE) for comparison

#### Imputation Strategy (if needed)
- **Method**: Multiple imputation using chained equations (MICE)
- **Imputations**: 20 imputed datasets
- **Variables Included**: All analysis variables and auxiliary variables
- **Pool Method**: Rubin's rules for parameter combination

### Outlier Handling

#### Continuous Variables
- **Screening Rule**: Remove observations with |z-score| > 4
- **Variables Screened**: All continuous exposure, outcome, and covariate variables
- **Timing**: Outlier removal performed before modeling
- **Documentation**: Number and characteristics of outliers removed reported

#### Categorical Variables
- **Level Exclusion**: Categories with <5% membership collapsed
- **Method**: Merge into adjacent category or "Other" category
- **Rationale**: Ensure stable model estimates

### Sensitivity Analyses

1. **Detection Limit Handling**
   - Compare LOD/√2 vs LOD/2 substitution
   - Multiple imputation for non-detects
   
2. **Cycle-Specific Analyses**
   - Separate analysis for cycles D-G (PFC datasets)
   - Separate analysis for cycles H-J (PFAS datasets)
   - Test for cycle-effect modification

3. **Sex-Stratified Analyses**
   - Separate models for males and females
   - Test for sex-PFAS interactions

4. **Age-Stratified Analyses**
   - Younger adults (18-50 years)
   - Older adults (50+ years)

5. **Exclusion Analyses**
   - Exclude participants with chronic diseases
   - Exclude extreme BMI values

### Mixture Analysis Approaches

#### Weighted Quantile Sum Regression (WQS)
- **Purpose**: Estimate joint effect of PFAS mixture
- **Software**: wqs package or custom implementation
- **Parameters**: 100 bootstrap samples, 40 quantiles
- **Constraints**: Non-negative weights sum to 1
- **Output**: Overall mixture effect, variable importance weights

#### Bayesian Kernel Machine Regression (BKMR)
- **Purpose**: Model complex exposure-response relationships
- **Software**: bkmr package
- **Parameters**: 
  - MCMC iterations: 50,000
  - Burn-in: 10,000
  - Thinning: 5
- **Output**: Exposure-response curves, variable importance, interactions

---

## Multiple Testing Correction

### Correction Methods
- **Primary**: False Discovery Rate (FDR) control using Benjamini-Hochberg procedure
- **Threshold**: FDR-adjusted p-value < 0.05 considered significant
- **Family**: Each PFAS-outcome combination treated as separate family

### Secondary Approach
- **Bonferroni Correction**: Applied for sensitivity analyses
- **Threshold**: p < 0.05/4 = 0.0125 for four PFAS compounds

---

## Software and Package Versions

### Primary Analysis Platform
- **Language**: Python 3.11+
- **Environment**: nhanes-analysis-vault Docker container

### Key Python Packages

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | 2.0+ | Data manipulation |
| numpy | 1.24+ | Numerical operations |
| scipy | 1.10+ | Statistical functions |
| statsmodels | 0.14+ | Survey-weighted regression |
| scikit-learn | 1.3+ | Machine learning, preprocessing |
| matplotlib | 3.7+ | Visualization |
| seaborn | 0.12+ | Statistical visualization |
| pingouin | 0.5+ | Additional statistics |

### Survey Analysis
- **sampling**: For survey weight calculations
- **survey**: Custom implementation for NHANES design

### Mixture Analysis
- **WQS**: Custom implementation (if not available in Python)
- **BKMR**: Interface to R bkmr package using rpy2

### Version Control
- All package versions documented in `vault_requirements.txt`
- Environment reproducible via Docker image
- Analysis code version controlled via git

---

## References

1. Levine, M. E., et al. (2018). An epigenetic biomarker of aging for lifespan and healthspan. Aging, 10(4), 573-591.
2. NHANES Laboratory Procedures Manual (various years). Centers for Disease Control and Prevention.
3. von Elm, E., et al. (2007). The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement. PLoS Medicine, 4(10), e296.
4. Johnson, C. L., et al. (2014). National Health and Nutrition Examination Survey: sample design, 2011-2014. National Center for Health Statistics.

---

## Document History

| Version | Date       | Changes                    |
|---------|------------|----------------------------|
| 1.0     | 2026-02-13 | Initial documentation      |
