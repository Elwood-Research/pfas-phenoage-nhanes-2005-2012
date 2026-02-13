# PhenoAge Calculation: Detailed Methodology

## Overview

PhenoAge is a DNA methylation-based measure of biological aging that was developed by Levine et al. (2018) to capture system-level dysregulation across multiple physiological systems. The clinical version of PhenoAge can be calculated using standard clinical chemistry markers available in routine blood work.

### Key References
- **Primary Citation**: Levine, M. E., et al. (2018). An epigenetic biomarker of aging for lifespan and healthspan. Aging, 10(4), 573-591.
- **Clinical Application**: Lu, A. T., et al. (2019). DNA methylation GrimAge strongly predicts lifespan and healthspan. Aging, 11(2), 303-327.

---

## Original Levine et al. (2018) Methodology

### Development Cohort
The original PhenoAge algorithm was developed using:
- Training data: NHANES III (n = 9,926)
- Validation: Multiple independent cohorts
- Mortality follow-up: Up to 23 years

### Clinical Biomarker Selection

The 9 biomarkers were selected through LASSO regression to predict DNA methylation age (mortality-associated DNAm age estimate):

| Biomarker | Biological System | Rationale for Inclusion |
|-----------|-------------------|------------------------|
| Albumin | Liver function, nutrition | Marker of liver synthetic function |
| Creatinine | Kidney function | Marker of renal filtration |
| Glucose | Metabolism | Indicator of metabolic dysregulation |
| C-reactive protein | Inflammation | Acute phase reactant, chronic inflammation marker |
| Lymphocyte % | Immune function | Adaptive immunity indicator |
| Mean cell volume | Blood cell production | Bone marrow function, nutrient status |
| Red cell distribution width | Erythrocyte size variability | Systemic inflammation, nutrient deficiency |
| Alkaline phosphatase | Liver/bone metabolism | Tissue damage marker |
| White blood cell count | Immune function/Inflammation | Innate immune activation |

### Model Formula

The original model uses a two-stage calculation:

**Stage 1**: Calculate mortality score (M) using a Gompertz distribution
**Stage 2**: Convert mortality score to biological age

---

## Required Biomarkers and Units

### NHANES Variable Mapping

| PhenoAge Component | NHANES Variable(s) | NHANES Units | Required Units | Conversion |
|-------------------|-------------------|--------------|----------------|------------|
| Albumin | LBXSAL | g/dL | g/dL | None |
| Creatinine | LBXSCR | mg/dL | mg/dL | None |
| Glucose | LBXSGL | mg/dL | mg/dL | None |
| C-reactive protein | LBXCRP | mg/dL | mg/L | × 10 |
| Lymphocyte percentage | LBXLYPCT | % | % | None |
| Mean cell volume | LBXMCVSI | fL | fL | None |
| Red cell distribution width | LBXRDW | % | % | None |
| Alkaline phosphatase | LBXSAPSI | IU/L | U/L | None |
| White blood cell count | LBXWBCSI | 1000 cells/μL | 1000 cells/μL | None |
| Chronological age | RIDAGEYR | years | years | None |

### Unit Conversion Details

#### C-reactive Protein (CRP)
**Critical Conversion Required**

NHANES reports CRP in **mg/dL**, but PhenoAge requires **mg/L**.

```python
# Conversion formula
crp_mg_L = crp_mg_dL * 10
```

**Example**:
- NHANES value: 0.21 mg/dL
- Converted: 2.1 mg/L

#### Other Variables
All other biomarkers in NHANES use the same units required by PhenoAge and require no conversion.

---

## Step-by-Step Calculation Procedure

### Step 1: Data Preparation

1. **Extract required variables** from merged NHANES dataset
2. **Convert CRP units** from mg/dL to mg/L
3. **Handle missing values** (exclude incomplete cases)
4. **Screen for outliers** (|z-score| > 4)

### Step 2: Calculate Mortality Score (M)

The mortality score represents the predicted cumulative hazard of mortality based on the biomarker profile.

#### Linear Predictor Calculation

```
linear_predictor = -11.99 
    + (0.0296 × Albumin_gdL)
    + (-0.0189 × Creatinine_mgdL)
    + (0.00133 × Glucose_mgdL)
    + (0.000878 × CRP_mgL)
    + (-0.0375 × Lymphocyte_pct)
    + (0.00887 × MCV_fL)
    + (0.0228 × RDW_pct)
    + (0.00199 × ALP_UL)
    + (0.0554 × WBC_1000uL)
    + (0.0804 × Age_years)
```

#### Gompertz Mortality Score

```
M = 1 - exp(-exp(linear_predictor))
```

**Interpretation**: 
- M ranges from 0 to 1
- Higher M indicates higher predicted mortality risk
- Represents the probability of mortality under Gompertz model assumptions

### Step 3: Calculate PhenoAge

Convert the mortality score to biological age using the inverse Gompertz transformation:

```
PhenoAge = 141.5 + (ln(-0.00553 × ln(1 - M)) / 0.09165)
```

**Interpretation**:
- PhenoAge in years
- Comparable to chronological age scale
- Represents biological age based on physiological dysregulation

### Step 4: Calculate PhenoAge Acceleration

```
PhenoAgeAccel = PhenoAge - Chronological_Age
```

**Interpretation**:
- **Positive values**: Accelerated aging (biologically older than chronological age)
- **Negative values**: Decelerated aging (biologically younger than chronological age)
- **Zero**: Biological age matches chronological age

---

## NHANES-Specific Adaptations

### Data Availability Across Cycles

| Component | Cycles D-F (2005-2010) | Cycles G-J (2011-2018) | Notes |
|-----------|------------------------|------------------------|-------|
| Albumin | BIOPRO | BIOPRO | Consistent |
| Creatinine | BIOPRO | BIOPRO | Consistent |
| Glucose | BIOPRO | BIOPRO | Consistent |
| CRP | CRP dataset | High-sensitivity CRP in different dataset | May need harmonization |
| Lymphocyte % | CBC | CBC | Consistent |
| MCV | CBC | CBC | Consistent |
| RDW | CBC | CBC | Consistent |
| ALP | BIOPRO | BIOPRO | Consistent |
| WBC | CBC | CBC | Consistent |

### Cycle-Specific Considerations

#### CRP Measurement Differences
- **Cycles D-F**: Separate CRP dataset, standard CRP assay
- **Cycles G-J**: High-sensitivity CRP may be in different datasets
- **Action**: Verify CRP variable availability and units across all cycles

#### Missing Data Patterns
- CRP has higher missingness than other biomarkers
- May need cycle-specific handling or multiple imputation

---

## Example Calculation with Hypothetical Values

### Example Participant

| Variable | Value (NHANES units) | Converted Value | Unit |
|----------|---------------------|-----------------|------|
| Albumin | 4.2 | 4.2 | g/dL |
| Creatinine | 0.9 | 0.9 | mg/dL |
| Glucose | 95 | 95 | mg/dL |
| CRP | 0.15 | 1.5 | mg/L (×10) |
| Lymphocyte % | 32 | 32 | % |
| MCV | 88 | 88 | fL |
| RDW | 13.2 | 13.2 | % |
| ALP | 65 | 65 | U/L |
| WBC | 6.5 | 6.5 | 1000/μL |
| Chronological age | 45 | 45 | years |

### Calculation Steps

**Step 1: Linear Predictor**
```
linear_predictor = -11.99
    + (0.0296 × 4.2)        = -11.99 + 0.1243
    + (-0.0189 × 0.9)       = + (-0.0170)
    + (0.00133 × 95)        = + 0.1264
    + (0.000878 × 1.5)      = + 0.0013
    + (-0.0375 × 32)        = + (-1.2000)
    + (0.00887 × 88)        = + 0.7806
    + (0.0228 × 13.2)       = + 0.3010
    + (0.00199 × 65)        = + 0.1294
    + (0.0554 × 6.5)        = + 0.3601
    + (0.0804 × 45)         = + 3.6180
    
linear_predictor = -7.7669
```

**Step 2: Mortality Score (M)**
```
M = 1 - exp(-exp(-7.7669))
M = 1 - exp(-0.000424)
M = 1 - 0.999576
M = 0.000424
```

**Step 3: PhenoAge**
```
PhenoAge = 141.5 + (ln(-0.00553 × ln(1 - 0.000424)) / 0.09165)
PhenoAge = 141.5 + (ln(-0.00553 × ln(0.999576)) / 0.09165)
PhenoAge = 141.5 + (ln(-0.00553 × -0.000424) / 0.09165)
PhenoAge = 141.5 + (ln(0.00000234) / 0.09165)
PhenoAge = 141.5 + (-12.96 / 0.09165)
PhenoAge = 141.5 + (-141.4)
PhenoAge ≈ 42.5 years
```

**Step 4: PhenoAge Acceleration**
```
PhenoAgeAccel = 42.5 - 45 = -2.5 years
```

**Interpretation**: This participant is biologically approximately 2.5 years younger than their chronological age.

---

## Python Code Template for Calculation

### Complete Implementation

```python
import numpy as np
import pandas as pd

def calculate_phenoage(df):
    """
    Calculate PhenoAge and PhenoAge acceleration for NHANES data.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing NHANES biomarker variables
        Required columns: LBXSAL, LBXSCR, LBXSGL, LBXCRP, LBXLYPCT,
                         LBXMCVSI, LBXRDW, LBXSAPSI, LBXWBCSI, RIDAGEYR
    
    Returns:
    --------
    pandas.DataFrame
        Original DataFrame with added PhenoAge and PhenoAgeAccel columns
    """
    
    # Create a copy to avoid modifying original
    data = df.copy()
    
    # Step 1: Unit conversions
    # Convert CRP from mg/dL to mg/L
    data['CRP_mgL'] = data['LBXCRP'] * 10
    
    # Step 2: Calculate linear predictor
    # Coefficients from Levine et al. (2018)
    data['linear_predictor'] = (
        -11.99 +
        (0.0296 * data['LBXSAL']) +           # Albumin (g/dL)
        (-0.0189 * data['LBXSCR']) +          # Creatinine (mg/dL)
        (0.00133 * data['LBXSGL']) +          # Glucose (mg/dL)
        (0.000878 * data['CRP_mgL']) +        # CRP (mg/L)
        (-0.0375 * data['LBXLYPCT']) +        # Lymphocyte %
        (0.00887 * data['LBXMCVSI']) +        # MCV (fL)
        (0.0228 * data['LBXRDW']) +           # RDW (%)
        (0.00199 * data['LBXSAPSI']) +        # ALP (U/L)
        (0.0554 * data['LBXWBCSI']) +         # WBC (1000 cells/μL)
        (0.0804 * data['RIDAGEYR'])           # Chronological age
    )
    
    # Step 3: Calculate mortality score (M)
    data['mortality_score'] = 1 - np.exp(-np.exp(data['linear_predictor']))
    
    # Step 4: Calculate PhenoAge
    data['PhenoAge'] = (
        141.5 +
        (np.log(-0.00553 * np.log(1 - data['mortality_score'])) / 0.09165)
    )
    
    # Step 5: Calculate PhenoAge acceleration
    data['PhenoAgeAccel'] = data['PhenoAge'] - data['RIDAGEYR']
    
    return data


def validate_phenoage_inputs(df):
    """
    Validate input data for PhenoAge calculation.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input data to validate
    
    Returns:
    --------
    dict
        Validation results with flags and summary statistics
    """
    
    required_cols = [
        'LBXSAL', 'LBXSCR', 'LBXSGL', 'LBXCRP', 'LBXLYPCT',
        'LBXMCVSI', 'LBXRDW', 'LBXSAPSI', 'LBXWBCSI', 'RIDAGEYR'
    ]
    
    results = {
        'has_required_columns': True,
        'missing_columns': [],
        'missing_values': {},
        'out_of_range': {},
        'valid_range': {}
    }
    
    # Check for required columns
    for col in required_cols:
        if col not in df.columns:
            results['has_required_columns'] = False
            results['missing_columns'].append(col)
    
    if not results['has_required_columns']:
        return results
    
    # Check for missing values
    for col in required_cols:
        n_missing = df[col].isna().sum()
        if n_missing > 0:
            results['missing_values'][col] = n_missing
    
    # Define valid ranges (based on physiological plausibility)
    valid_ranges = {
        'LBXSAL': (1.0, 6.0),       # g/dL
        'LBXSCR': (0.2, 20.0),      # mg/dL
        'LBXSGL': (50, 500),        # mg/dL
        'LBXCRP': (0.001, 50),      # mg/dL
        'LBXLYPCT': (1, 90),        # %
        'LBXMCVSI': (50, 130),      # fL
        'LBXRDW': (10, 35),         # %
        'LBXSAPSI': (10, 500),      # U/L
        'LBXWBCSI': (1, 50),        # 1000 cells/μL
        'RIDAGEYR': (18, 120)       # years
    }
    
    results['valid_range'] = valid_ranges
    
    # Check for values outside valid ranges
    for col, (min_val, max_val) in valid_ranges.items():
        out_of_range = df[(df[col] < min_val) | (df[col] > max_val)][col]
        if len(out_of_range) > 0:
            results['out_of_range'][col] = len(out_of_range)
    
    return results


def calculate_phenoage_with_diagnostics(df):
    """
    Calculate PhenoAge with comprehensive diagnostic output.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input NHANES data
    
    Returns:
    --------
    tuple
        (DataFrame with PhenoAge, diagnostics dictionary)
    """
    
    # Validate inputs
    validation = validate_phenoage_inputs(df)
    
    if not validation['has_required_columns']:
        raise ValueError(f"Missing required columns: {validation['missing_columns']}")
    
    # Calculate PhenoAge
    results_df = calculate_phenoage(df)
    
    # Compile diagnostics
    diagnostics = {
        'validation': validation,
        'n_complete_cases': len(results_df.dropna(subset=['PhenoAge'])),
        'phenoage_stats': results_df['PhenoAge'].describe().to_dict(),
        'phenoageaccel_stats': results_df['PhenoAgeAccel'].describe().to_dict(),
        'age_correlation': results_df[['RIDAGEYR', 'PhenoAge']].corr().iloc[0, 1]
    }
    
    return results_df, diagnostics


# Example usage
if __name__ == "__main__":
    # Create example data
    example_data = pd.DataFrame({
        'SEQN': [1, 2, 3],
        'RIDAGEYR': [45, 62, 38],
        'LBXSAL': [4.2, 3.8, 4.5],
        'LBXSCR': [0.9, 1.2, 0.8],
        'LBXSGL': [95, 110, 88],
        'LBXCRP': [0.15, 0.35, 0.08],  # mg/dL
        'LBXLYPCT': [32, 28, 35],
        'LBXMCVSI': [88, 92, 86],
        'LBXRDW': [13.2, 14.1, 12.8],
        'LBXSAPSI': [65, 78, 58],
        'LBXWBCSI': [6.5, 7.2, 5.8]
    })
    
    # Calculate PhenoAge
    results, diagnostics = calculate_phenoage_with_diagnostics(example_data)
    
    print("PhenoAge Results:")
    print(results[['SEQN', 'RIDAGEYR', 'PhenoAge', 'PhenoAgeAccel']])
    print("\nDiagnostics:")
    print(diagnostics)
```

### Integration with NHANES Analysis Pipeline

```python
def prepare_phenoage_data(nhanes_merged_df):
    """
    Prepare merged NHANES data for PhenoAge calculation.
    
    Parameters:
    -----------
    nhanes_merged_df : pandas.DataFrame
        Merged NHANES dataset with all required components
    
    Returns:
    --------
    pandas.DataFrame
        Dataset with PhenoAge calculated, ready for PFAS analysis
    """
    
    # Filter to complete cases only
    required_vars = [
        'LBXSAL', 'LBXSCR', 'LBXSGL', 'LBXCRP', 'LBXLYPCT',
        'LBXMCVSI', 'LBXRDW', 'LBXSAPSI', 'LBXWBCSI', 'RIDAGEYR'
    ]
    
    complete_df = nhanes_merged_df.dropna(subset=required_vars)
    
    # Screen for outliers
    for var in required_vars:
        z_scores = np.abs(stats.zscore(complete_df[var]))
        complete_df = complete_df[z_scores < 4]
    
    # Calculate PhenoAge
    results, diagnostics = calculate_phenoage_with_diagnostics(complete_df)
    
    # Log diagnostics
    print(f"PhenoAge calculation diagnostics:")
    print(f"  Complete cases: {diagnostics['n_complete_cases']}")
    print(f"  Age-PhenoAge correlation: {diagnostics['age_correlation']:.3f}")
    
    return results
```

---

## Interpretation Guidelines

### PhenoAge Distribution
- **Typical Range**: Approximately ±10 years around chronological age
- **Healthy Aging**: PhenoAge < Chronological age
- **Accelerated Aging**: PhenoAge > Chronological age

### Clinical Relevance
- **1-year increase in PhenoAge**: Associated with ~5-10% increase in all-cause mortality
- **5-year increase in PhenoAge**: Clinically meaningful acceleration
- **Comparison Groups**: Age-matched population norms

### Quality Control Checks

1. **Age Correlation**: PhenoAge should correlate with chronological age (r ≈ 0.7-0.8)
2. **Distribution**: PhenoAgeAccel should be approximately normal
3. **Outliers**: Investigate extreme PhenoAgeAccel values (>±20 years)
4. **Missing Patterns**: Check for systematic missingness by demographics

---

## Troubleshooting

### Common Issues

#### Issue 1: Extreme PhenoAge Values
**Symptom**: PhenoAge values < 0 or > 150
**Cause**: Extreme biomarker values or calculation errors
**Solution**: Check input ranges, validate linear predictor calculation

#### Issue 2: Missing CRP Data
**Symptom**: Many missing values for CRP
**Cause**: CRP measured in different subsamples across cycles
**Solution**: Use cycle-specific datasets or multiple imputation

#### Issue 3: Unit Confusion
**Symptom**: Systematically high/low PhenoAge values
**Cause**: CRP units not converted (mg/dL vs mg/L)
**Solution**: Verify CRP unit conversion is applied

---

## References

1. Levine, M. E., et al. (2018). An epigenetic biomarker of aging for lifespan and healthspan. Aging, 10(4), 573-591.
2. Levine, M. E. (2013). Modeling the rate of senescence: can estimated biological age predict mortality more accurately than chronological age? Journals of Gerontology Series A, 68(6), 667-674.
3. Lu, A. T., et al. (2019). DNA methylation GrimAge strongly predicts lifespan and healthspan. Aging, 11(2), 303-327.
