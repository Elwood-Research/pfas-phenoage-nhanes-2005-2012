# Statistical Methods: Detailed Technical Specifications

## Survey Design and Weighting

### NHANES Complex Survey Design

NHANES employs a complex, multistage probability sampling design that requires special statistical methods for valid inference.

#### Sampling Design Components

| Component | Description | NHANES Variable |
|-----------|-------------|-----------------|
| **Primary Sampling Units (PSU)** | Geographic areas (counties or groups of counties) | SDMVPSU |
| **Strata** | Geographic divisions within each PSU | SDMVSTRA |
| **Weights** | Survey weights accounting for unequal selection probability | WTSB2YR or WTSA2YR |

#### Weighting Strategy

##### Subsample Weights for PFAS Analysis
- PFAS measurements were collected in a **random one-third subsample** of participants
- Special subsample weights required: **WTSA2YR** (cycles D-G) or **WTSB2YR** (cycles H-J)
- These weights account for:
  - Unequal probability of selection
  - Non-response adjustment
  - Post-stratification to match Census population totals

##### Weight Adjustment for Combined Cycles

When combining data across multiple 2-year cycles:

```python
def adjust_weights_for_combined_cycles(df, n_cycles=7):
    """
    Adjust survey weights for combined cycle analysis.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        NHANES data with weights
    n_cycles : int
        Number of 2-year cycles combined (default: 7)
    
    Returns:
    --------
    pandas.DataFrame
        Data with adjusted weights
    """
    df = df.copy()
    
    # Use appropriate weight variable
    if 'WTSB2YR' in df.columns:
        weight_col = 'WTSB2YR'
    elif 'WTSA2YR' in df.columns:
        weight_col = 'WTSA2YR'
    else:
        raise ValueError("No valid weight column found")
    
    # Divide by number of cycles to maintain population totals
    df['weight_adjusted'] = df[weight_col] / n_cycles
    
    return df
```

**Rationale**: Dividing by the number of cycles ensures that weighted estimates reflect the average annual population rather than summing to the total across all years.

### Variance Estimation

#### Taylor Series Linearization

The primary method for variance estimation in NHANES is Taylor series linearization, which accounts for:
- Stratification
- Clustering within PSUs
- Unequal weights

#### Survey Design Specification

```python
import numpy as np
import pandas as pd
from scipy import stats

class NHANESSurveyDesign:
    """
    NHANES complex survey design for variance estimation.
    """
    
    def __init__(self, df, weight_col='weight_adjusted', 
                 strata_col='SDMVSTRA', psu_col='SDMVPSU'):
        """
        Initialize survey design.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            NHANES data
        weight_col : str
            Column name for survey weights
        strata_col : str
            Column name for strata
        psu_col : str
            Column name for PSU
        """
        self.df = df.copy()
        self.weight_col = weight_col
        self.strata_col = strata_col
        self.psu_col = psu_col
        
        # Get unique strata-PSU combinations
        self.design = df[[strata_col, psu_col, weight_col]].copy()
        
    def get_degrees_of_freedom(self):
        """Calculate degrees of freedom for survey design."""
        # Degrees of freedom = number of PSUs - number of strata
        n_psu = self.df[self.psu_col].nunique()
        n_strata = self.df[self.strata_col].nunique()
        return n_psu - n_strata
    
    def weighted_mean(self, var):
        """Calculate survey-weighted mean."""
        weights = self.df[self.weight_col]
        values = self.df[var]
        
        # Weighted mean
        weighted_mean = np.average(values, weights=weights)
        
        # Calculate standard error using stratified design
        se = self._calculate_se(var, weighted_mean)
        
        return {
            'mean': weighted_mean,
            'se': se,
            'ci_lower': weighted_mean - 1.96 * se,
            'ci_upper': weighted_mean + 1.96 * se
        }
    
    def _calculate_se(self, var, mean):
        """Calculate standard error accounting for survey design."""
        
        # Calculate variance using stratified approach
        strata_var = []
        
        for stratum in self.df[self.strata_col].unique():
            stratum_data = self.df[self.df[self.strata_col] == stratum]
            
            # For each stratum, calculate variance between PSUs
            psu_means = []
            psu_weights = []
            
            for psu in stratum_data[self.psu_col].unique():
                psu_data = stratum_data[stratum_data[self.psu_col] == psu]
                
                # PSU-level weighted mean
                w = psu_data[self.weight_col]
                v = psu_data[var]
                psu_mean = np.average(v, weights=w)
                psu_total_weight = w.sum()
                
                psu_means.append(psu_mean)
                psu_weights.append(psu_total_weight)
            
            # Variance between PSUs within stratum
            if len(psu_means) > 1:
                # Weighted variance
                psu_weights = np.array(psu_weights)
                psu_means = np.array(psu_means)
                stratum_mean = np.average(psu_means, weights=psu_weights)
                
                # Sum of squared deviations weighted by PSU size
                ssq = np.sum(psu_weights * (psu_means - stratum_mean) ** 2)
                stratum_var.append(ssq)
        
        # Total variance = sum of stratum variances
        total_var = np.sum(stratum_var)
        
        # Standard error
        se = np.sqrt(total_var / (self.df[self.weight_col].sum() ** 2))
        
        return se


def create_survey_design(df):
    """
    Create survey design object for NHANES analysis.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        NHANES data with required columns
    
    Returns:
    --------
    NHANESSurveyDesign
        Survey design object
    """
    # Ensure required columns exist
    required = ['SDMVSTRA', 'SDMVPSU', 'weight_adjusted']
    missing = [col for col in required if col not in df.columns]
    
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    return NHANESSurveyDesign(df)
```

#### Degrees of Freedom

```python
def calculate_df_for_survey(df, strata_col='SDMVSTRA', psu_col='SDMVPSU'):
    """
    Calculate degrees of freedom for survey-based analyses.
    
    Formula: df = number of PSUs - number of strata
    """
    n_psu = df[psu_col].nunique()
    n_strata = df[strata_col].nunique()
    
    df_survey = n_psu - n_strata
    
    print(f"Survey Design Degrees of Freedom:")
    print(f"  Number of PSUs: {n_psu}")
    print(f"  Number of strata: {n_strata}")
    print(f"  Degrees of freedom: {df_survey}")
    
    return df_survey
```

### Design Effects

The design effect (DEFF) quantifies the increase in variance due to the complex survey design:

```python
def calculate_design_effect(df, var, weight_col='weight_adjusted'):
    """
    Calculate design effect for a variable.
    
    DEFF = Var_complex / Var_srs
    
    where Var_srs is the variance under simple random sampling
    """
    # Complex survey variance
    design = create_survey_design(df)
    complex_var = design.weighted_mean(var)['se'] ** 2
    
    # Simple random sampling variance
    weights = df[weight_col]
    values = df[var]
    
    # Weighted variance
    weighted_var = np.average((values - np.average(values, weights=weights)) ** 2, 
                               weights=weights)
    
    # SRS variance (accounting for finite population)
    n_eff = (weights.sum() ** 2) / (weights ** 2).sum()  # Effective sample size
    srs_var = weighted_var / n_eff
    
    deff = complex_var / srs_var
    
    return {
        'design_effect': deff,
        'complex_var': complex_var,
        'srs_var': srs_var,
        'effective_sample_size': n_eff
    }
```

---

## Regression Model Specifications

### Survey-Weighted Linear Regression

#### Primary Model Specification

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf

def fit_survey_weighted_model(df, formula, weight_col='weight_adjusted'):
    """
    Fit survey-weighted linear regression model.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Analysis dataset
    formula : str
        R-style formula (e.g., 'PhenoAgeAccel ~ log_pfoa + age + sex')
    weight_col : str
        Column with survey weights
    
    Returns:
    --------
    RegressionResults
        Fitted model results
    """
    # Use WLS (Weighted Least Squares) with survey weights
    model = smf.wls(formula=formula, data=df, weights=df[weight_col])
    results = model.fit()
    
    return results


# Example model specifications
model_formulas = {
    'model_1_crude': 'PhenoAgeAccel ~ log_pfoa + RIDAGEYR + RIAGENDR',
    'model_2_adjusted': 'PhenoAgeAccel ~ log_pfoa + RIDAGEYR + RIAGENDR + RIDRETH1 + DMDEDUC2 + INDFMPIR + BMXBMI + smoking_status',
    'model_3_full': 'PhenoAgeAccel ~ log_pfoa + log_pfos + log_pfhxs + log_pfna + RIDAGEYR + RIAGENDR + RIDRETH1 + DMDEDUC2 + INDFMPIR + BMXBMI + smoking_status + diabetes + hypertension'
}
```

#### Robust Standard Errors

To account for survey design in regression standard errors:

```python
def fit_survey_weighted_model_with_robust_se(df, formula, 
                                              weight_col='weight_adjusted',
                                              strata_col='SDMVSTRA',
                                              psu_col='SDMVPSU'):
    """
    Fit survey-weighted model with robust standard errors.
    
    Uses Huber-White sandwich estimator adjusted for clustering.
    """
    import statsmodels.formula.api as smf
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    
    # Fit weighted model
    model = smf.wls(formula=formula, data=df, weights=df[weight_col])
    results = model.fit(
        cov_type='cluster', 
        cov_kwds={'groups': df[psu_col]}
    )
    
    return results
```

### Interpretation of Regression Coefficients

For log-transformed PFAS:

```
Coefficient interpretation:
- Beta represents change in PhenoAgeAccel per unit change in ln(PFAS)
- Approximately: Beta/ln(2) = change per doubling of PFAS
- Or: (exp(Beta) - 1) × 100 = percent change in outcome per unit change in ln(PFAS)

Example:
Beta = 0.5 for ln(PFOA)
- A doubling of PFOA (ln(2) ≈ 0.693 increase) is associated with:
  0.5 × 0.693 = 0.35 years increase in PhenoAgeAccel
```

### Model Diagnostics

#### Residual Analysis

```python
def diagnose_regression_model(results, df):
    """
    Comprehensive model diagnostics for survey-weighted regression.
    
    Parameters:
    -----------
    results : RegressionResults
        Fitted model results
    df : pandas.DataFrame
        Analysis data
    
    Returns:
    --------
    dict
        Diagnostic statistics and flags
    """
    diagnostics = {}
    
    # 1. Residual analysis
    residuals = results.resid
    fitted = results.fittedvalues
    
    diagnostics['residuals'] = {
        'mean': residuals.mean(),
        'std': residuals.std(),
        'min': residuals.min(),
        'max': residuals.max(),
        'shapiro_pvalue': stats.shapiro(residuals.sample(min(5000, len(residuals))))[1]
    }
    
    # 2. Heteroscedasticity test (Breusch-Pagan)
    from statsmodels.stats.diagnostic import het_breuschpagan
    bp_test = het_breuschpagan(residuals, results.model.exog)
    diagnostics['heteroscedasticity'] = {
        'lagrange_multiplier': bp_test[0],
        'p_value': bp_test[1],
        'f_pvalue': bp_test[3]
    }
    
    # 3. Influential observations
    influence = results.get_influence()
    diagnostics['influential'] = {
        'n_high_cooks_d': (influence.cooks_d[0] > 4/len(df)).sum(),
        'max_cooks_d': influence.cooks_d[0].max()
    }
    
    # 4. Multicollinearity (VIF)
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    exog = results.model.exog
    vif_data = pd.DataFrame()
    vif_data['Variable'] = results.model.exog_names
    vif_data['VIF'] = [variance_inflation_factor(exog, i) 
                       for i in range(exog.shape[1])]
    diagnostics['multicollinearity'] = vif_data.to_dict()
    
    # 5. Model fit
    diagnostics['fit'] = {
        'r_squared': results.rsquared,
        'adj_r_squared': results.rsquared_adj,
        'f_statistic': results.fvalue,
        'f_pvalue': results.f_pvalue,
        'aic': results.aic,
        'bic': results.bic
    }
    
    return diagnostics
```

#### Variance Inflation Factor (VIF)

```python
def check_multicollinearity(df, predictors, threshold=5.0):
    """
    Check for multicollinearity among predictors.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Data containing predictors
    predictors : list
        List of predictor variable names
    threshold : float
        VIF threshold for concern (default: 5.0)
    
    Returns:
    --------
    pandas.DataFrame
        VIF values for each predictor
    """
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    
    X = df[predictors].dropna()
    X = sm.add_constant(X)
    
    vif_data = pd.DataFrame()
    vif_data['Variable'] = X.columns
    vif_data['VIF'] = [variance_inflation_factor(X.values, i) 
                       for i in range(X.shape[1])]
    
    # Flag high VIF
    vif_data['High_VIF'] = vif_data['VIF'] > threshold
    
    return vif_data
```

---

## Sensitivity Analyses

### Detection Limit Handling

```python
def sensitivity_detection_limit(df, pfas_vars, lod_values):
    """
    Sensitivity analysis for different detection limit substitutions.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        NHANES data with PFAS and detection indicators
    pfas_vars : list
        List of PFAS variable names
    lod_values : dict
        LOD values by cycle and compound
    
    Returns:
    --------
    dict
        Results from different substitution methods
    """
    results = {}
    
    # Method 1: LOD/√2 (standard)
    df_1 = df.copy()
    for var in pfas_vars:
        lod = lod_values[var]
        comment_var = var.replace('LBX', 'LBD') + 'L'
        df_1.loc[df_1[comment_var] == 1, var] = lod / np.sqrt(2)
    results['LOD_sqrt2'] = df_1
    
    # Method 2: LOD/2
    df_2 = df.copy()
    for var in pfas_vars:
        lod = lod_values[var]
        comment_var = var.replace('LBX', 'LBD') + 'L'
        df_2.loc[df_2[comment_var] == 1, var] = lod / 2
    results['LOD_2'] = df_2
    
    # Method 3: Multiple imputation
    results['MI'] = impute_pfas_nondetects(df, pfas_vars, lod_values)
    
    return results


def impute_pfas_nondetects(df, pfas_vars, lod_values, n_imputations=20):
    """
    Multiple imputation for non-detect PFAS values.
    
    Uses log-normal distribution assumption.
    """
    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import IterativeImputer
    
    imputed_datasets = []
    
    for _ in range(n_imputations):
        df_imp = df.copy()
        
        for var in pfas_vars:
            # Detected values
            detected = df_imp[var] >= lod_values[var]
            
            if detected.sum() > 0:
                # Fit log-normal to detected values
                log_values = np.log(df_imp.loc[detected, var])
                mu = log_values.mean()
                sigma = log_values.std()
                
                # Impute from truncated log-normal
                comment_var = var.replace('LBX', 'LBD') + 'L'
                nondetect = df_imp[comment_var] == 1
                
                # Sample from uniform(0, LOD) then fit distribution
                n_nondetect = nondetect.sum()
                imputed = np.exp(np.random.normal(mu - sigma**2, sigma, n_nondetect))
                imputed = np.clip(imputed, 0.001, lod_values[var])
                
                df_imp.loc[nondetect, var] = imputed
        
        imputed_datasets.append(df_imp)
    
    return imputed_datasets
```

### Cycle-Specific Analyses

```python
def sensitivity_by_cycle(df, formula, cycle_col='cycle'):
    """
    Run analyses stratified by NHANES cycle.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Analysis data
    formula : str
        Regression formula
    cycle_col : str
        Column indicating NHANES cycle
    
    Returns:
    --------
    dict
        Results by cycle
    """
    results = {}
    
    for cycle in df[cycle_col].unique():
        cycle_data = df[df[cycle_col] == cycle]
        
        if len(cycle_data) > 100:  # Minimum sample size
            model = fit_survey_weighted_model(cycle_data, formula)
            results[cycle] = {
                'n': len(cycle_data),
                'params': model.params.to_dict(),
                'pvalues': model.pvalues.to_dict(),
                'r_squared': model.rsquared
            }
    
    return results
```

### Sex-Stratified Analyses

```python
def sensitivity_sex_stratified(df, formula):
    """
    Run sex-stratified analyses.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Analysis data
    formula : str
        Regression formula (without sex term)
    
    Returns:
    --------
    dict
        Results for males and females
    """
    results = {}
    
    # Males (RIAGENDR = 1)
    male_data = df[df['RIAGENDR'] == 1]
    male_model = fit_survey_weighted_model(male_data, formula)
    results['male'] = {
        'n': len(male_data),
        'params': male_model.params.to_dict(),
        'pvalues': male_model.pvalues.to_dict()
    }
    
    # Females (RIAGENDR = 2)
    female_data = df[df['RIAGENDR'] == 2]
    female_model = fit_survey_weighted_model(female_data, formula)
    results['female'] = {
        'n': len(female_data),
        'params': female_model.params.to_dict(),
        'pvalues': female_model.pvalues.to_dict()
    }
    
    # Test for interaction
    interaction_formula = formula + ' + log_pfoa * C(RIAGENDR)'
    interaction_model = fit_survey_weighted_model(df, interaction_formula)
    results['interaction_pvalue'] = interaction_model.pvalues.get('log_pfoa:C(RIAGENDR)[T.2]', np.nan)
    
    return results
```

### Exclusion Analyses

```python
def sensitivity_exclusion_analyses(df, base_formula):
    """
    Run analyses with various exclusion criteria.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Full analysis data
    base_formula : str
        Base regression formula
    
    Returns:
    --------
    dict
        Results from different exclusion scenarios
    """
    results = {}
    
    # 1. Exclude chronic diseases
    healthy = df[(df['diabetes'] == 0) & 
                  (df['hypertension'] == 0) & 
                  (df['cvd'] == 0)]
    results['exclude_chronic_disease'] = fit_survey_weighted_model(
        healthy, base_formula
    ).params.to_dict()
    
    # 2. Exclude extreme BMI
    normal_bmi = df[(df['BMXBMI'] >= 18.5) & (df['BMXBMI'] <= 35)]
    results['exclude_extreme_bmi'] = fit_survey_weighted_model(
        normal_bmi, base_formula
    ).params.to_dict()
    
    # 3. Exclude current smokers
    non_smokers = df[df['smoking_status'] != 'Current']
    results['exclude_smokers'] = fit_survey_weighted_model(
        non_smokers, base_formula
    ).params.to_dict()
    
    # 4. Age restriction
    middle_age = df[(df['RIDAGEYR'] >= 30) & (df['RIDAGEYR'] <= 65)]
    results['middle_age_only'] = fit_survey_weighted_model(
        middle_age, base_formula
    ).params.to_dict()
    
    return results
```

---

## Mixture Analysis Approaches

### Weighted Quantile Sum Regression (WQS)

WQS estimates the joint effect of a mixture of correlated exposures.

```python
def weighted_quantile_sum(df, exposures, outcome, covariates, 
                          n_quantiles=4, n_boot=100, seed=42):
    """
    Weighted Quantile Sum (WQS) regression for PFAS mixtures.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Analysis data
    exposures : list
        List of exposure variable names
    outcome : str
        Outcome variable name
    covariates : list
        List of covariate names
    n_quantiles : int
        Number of quantiles for exposure categorization
    n_boot : int
        Number of bootstrap samples
    seed : int
        Random seed
    
    Returns:
    --------
    dict
        WQS results including mixture effect and weights
    """
    np.random.seed(seed)
    
    # Create quantile scores for each exposure
    quantile_df = df.copy()
    for exp in exposures:
        quantile_df[f'{exp}_q'] = pd.qcut(df[exp], n_quantiles, 
                                          labels=False, duplicates='drop')
    
    # Bootstrap to estimate weights
    weights_list = []
    
    for b in range(n_boot):
        # Bootstrap sample
        boot_idx = np.random.choice(len(df), size=len(df), replace=True)
        boot_df = quantile_df.iloc[boot_idx].copy()
        
        # Optimize weights using constrained regression
        # Weights sum to 1, all non-negative
        from scipy.optimize import minimize
        
        def neg_log_likelihood(weights):
            # Calculate WQS index
            wqs_index = np.zeros(len(boot_df))
            for i, exp in enumerate(exposures):
                wqs_index += weights[i] * boot_df[f'{exp}_q'].values
            
            # Fit regression model
            X = sm.add_constant(np.column_stack([
                wqs_index,
                boot_df[covariates].values
            ]))
            y = boot_df[outcome].values
            
            model = sm.OLS(y, X).fit()
            return -model.llf
        
        # Constrained optimization
        n_exp = len(exposures)
        constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
        bounds = [(0, 1) for _ in range(n_exp)]
        initial_weights = np.ones(n_exp) / n_exp
        
        result = minimize(neg_log_likelihood, initial_weights,
                          method='SLSQP', bounds=bounds,
                          constraints=constraints)
        
        weights_list.append(result.x)
    
    # Average weights across bootstrap samples
    mean_weights = np.mean(weights_list, axis=0)
    weight_se = np.std(weights_list, axis=0)
    
    # Calculate final WQS index with mean weights
    df['wqs_index'] = 0
    for i, exp in enumerate(exposures):
        df['wqs_index'] += mean_weights[i] * pd.qcut(df[exp], n_quantiles, 
                                                      labels=False, 
                                                      duplicates='drop')
    
    # Fit final model
    formula = f"{outcome} ~ wqs_index + {' + '.join(covariates)}"
    final_model = smf.ols(formula=formula, data=df).fit()
    
    results = {
        'mixture_effect': {
            'coef': final_model.params['wqs_index'],
            'se': final_model.bse['wqs_index'],
            'pvalue': final_model.pvalues['wqs_index'],
            'ci_95': final_model.conf_int().loc['wqs_index'].tolist()
        },
        'weights': {
            exp: {'mean': mean_weights[i], 'se': weight_se[i]}
            for i, exp in enumerate(exposures)
        },
        'model': final_model
    }
    
    return results
```

### Bayesian Kernel Machine Regression (BKMR)

BKMR models complex exposure-response relationships and interactions.

```python
def bayesian_kernel_machine_regression(df, exposures, outcome, covariates,
                                       n_iter=50000, burn_in=10000, thin=5):
    """
    Bayesian Kernel Machine Regression (BKMR) for PFAS mixtures.
    
    Note: This requires the bkmr R package. In Python, use rpy2 or
    implement simplified version.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Analysis data
    exposures : list
        List of exposure variable names
    outcome : str
        Outcome variable name
    covariates : list
        List of covariate names
    n_iter : int
        Number of MCMC iterations
    burn_in : int
        Number of burn-in iterations
    thin : int
        Thinning parameter
    
    Returns:
    --------
    dict
        BKMR results (requires R/bkmr package)
    """
    try:
        import rpy2.robjects as ro
        from rpy2.robjects import pandas2ri
        from rpy2.robjects.packages import importr
        
        # Activate pandas-to-R conversion
        pandas2ri.activate()
        
        # Import R packages
        bkmr = importr('bkmr')
        base = importr('base')
        
        # Prepare data
        y = df[outcome].values
        Z = df[exposures].values
        X = df[covariates].values
        
        # Pass to R
        ro.globalenv['y'] = y
        ro.globalenv['Z'] = Z
        ro.globalenv['X'] = X
        
        # Fit BKMR model
        ro.r('''
            fit <- kmbayes(y = y, Z = Z, X = X,
                           iter = %d, verbose = FALSE,
                           varsel = TRUE)
        ''' % n_iter)
        
        # Extract results
        ro.r('''
            # Variable selection posterior inclusion probabilities
            pip <- ExtractPIPs(fit)
            
            # Overall mixture effect
            risks.overall <- OverallRiskSummaries(
                fit = fit, y = y, Z = Z, X = X,
                qs = seq(0.25, 0.75, by = 0.05),
                q.fixed = 0.5, method = 'approx'
            )
            
            # Single variable effects
            risks.singvar <- SingVarRiskSummaries(
                fit = fit, y = y, Z = Z, X = X,
                qs.diff = c(0.25, 0.75),
                q.fixed = c(0.25, 0.50, 0.75)
            )
        ''' % locals())
        
        # Convert back to Python
        pip = pandas2ri.ri2py(ro.r('pip'))
        risks_overall = pandas2ri.ri2py(ro.r('risks.overall'))
        risks_singvar = pandas2ri.ri2py(ro.r('risks.singvar'))
        
        results = {
            'posterior_inclusion_probs': pip,
            'overall_risks': risks_overall,
            'single_variable_risks': risks_singvar
        }
        
        return results
        
    except ImportError:
        print("R and bkmr package required for BKMR analysis")
        print("Please install R and run: install.packages('bkmr')")
        return None
```

### Simplified Mixture Approach: Summation

```python
def pfas_sum_score(df, pfas_vars, weight_by_toxicity=False):
    """
    Calculate simple PFAS sum score.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Data with PFAS variables
    pfas_vars : list
        List of PFAS variable names
    weight_by_toxicity : bool
        If True, weight by relative toxic potency
    
    Returns:
    --------
    pandas.Series
        PFAS sum score
    """
    # Standardize PFAS to z-scores
    z_scores = df[pfas_vars].apply(lambda x: (x - x.mean()) / x.std())
    
    if weight_by_toxicity:
        # Approximate toxic potency weights
        # Based on half-life and toxicity data
        toxicity_weights = {
            'LBXPFOA': 1.0,
            'LBXPFOS': 1.0,
            'LBXPFHS': 0.8,
            'LBXPFNA': 0.9
        }
        weights = [toxicity_weights.get(v, 1.0) for v in pfas_vars]
        sum_score = (z_scores * weights).sum(axis=1) / sum(weights)
    else:
        sum_score = z_scores.mean(axis=1)
    
    return sum_score
```

---

## Multiple Testing Correction

### False Discovery Rate (FDR) Control

```python
def fdr_correction(pvalues, method='benjamini_hochberg', alpha=0.05):
    """
    Apply FDR correction to p-values.
    
    Parameters:
    -----------
    pvalues : array-like
        Array of p-values
    method : str
        FDR method ('benjamini_hochberg' or 'benjamini_yekutieli')
    alpha : float
        Significance level
    
    Returns:
    --------
    dict
        Corrected p-values and significance flags
    """
    from statsmodels.stats.multitest import multipletests
    
    pvalues = np.array(pvalues)
    
    reject, pvals_corrected, _, _ = multipletests(
        pvalues, alpha=alpha, method=method
    )
    
    return {
        'pvalues_original': pvalues,
        'pvalues_corrected': pvals_corrected,
        'significant': reject,
        'method': method,
        'alpha': alpha
    }


def apply_fdr_to_results(results_dict, pvalue_key='pvalue'):
    """
    Apply FDR correction to a set of results.
    
    Parameters:
    -----------
    results_dict : dict
        Dictionary of results with p-values
    pvalue_key : str
        Key for p-value in each result
    
    Returns:
    --------
    dict
        Results with FDR-corrected p-values added
    """
    pvalues = [r[pvalue_key] for r in results_dict.values()]
    fdr_results = fdr_correction(pvalues)
    
    for i, (key, result) in enumerate(results_dict.items()):
        result['pvalue_fdr'] = fdr_results['pvalues_corrected'][i]
        result['significant_fdr'] = fdr_results['significant'][i]
    
    return results_dict
```

### Bonferroni Correction

```python
def bonferroni_correction(pvalues, n_tests=None, alpha=0.05):
    """
    Apply Bonferroni correction.
    
    Parameters:
    -----------
    pvalues : array-like
        Array of p-values
    n_tests : int
        Number of tests (if None, uses len(pvalues))
    alpha : float
        Significance level
    
    Returns:
    --------
    dict
        Corrected p-values and significance flags
    """
    pvalues = np.array(pvalues)
    
    if n_tests is None:
        n_tests = len(pvalues)
    
    pvals_corrected = np.minimum(pvalues * n_tests, 1.0)
    significant = pvals_corrected < alpha
    
    return {
        'pvalues_original': pvalues,
        'pvalues_corrected': pvals_corrected,
        'significant': significant,
        'threshold': alpha / n_tests,
        'n_tests': n_tests
    }
```

---

## Software and Package Versions

### Python Environment

| Package | Minimum Version | Recommended Version | Purpose |
|---------|----------------|---------------------|---------|
| Python | 3.9 | 3.11 | Base language |
| pandas | 1.5 | 2.0+ | Data manipulation |
| numpy | 1.21 | 1.24+ | Numerical computing |
| scipy | 1.9 | 1.10+ | Statistical functions |
| statsmodels | 0.13 | 0.14+ | Regression, survey methods |
| scikit-learn | 1.2 | 1.3+ | ML, preprocessing |
| matplotlib | 3.5 | 3.7+ | Plotting |
| seaborn | 0.11 | 0.12+ | Statistical plots |

### R Environment (for BKMR)

| Package | Version | Purpose |
|---------|---------|---------|
| bkmr | 0.2.2+ | Bayesian kernel machine regression |
| survey | 4.1+ | Survey-weighted analysis |

### Docker Environment

```dockerfile
# nhanes-analysis-vault Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    r-base \
    r-base-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install R packages
RUN R -e "install.packages(c('bkmr', 'survey'), repos='https://cloud.r-project.org/')"

# Install Python packages
COPY vault_requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/vault_requirements.txt

# Set working directory
WORKDIR /study
```

### vault_requirements.txt

```
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
statsmodels>=0.14.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
seaborn>=0.12.0
pingouin>=0.5.0
rpy2>=3.5.0
openpyxl>=3.1.0
xlrd>=2.0.0
```

### Version Documentation

```python
def log_software_versions():
    """Log all software versions for reproducibility."""
    import platform
    import pandas
    import numpy
    import scipy
    import statsmodels
    import sklearn
    
    versions = {
        'python': platform.python_version(),
        'pandas': pandas.__version__,
        'numpy': numpy.__version__,
        'scipy': scipy.__version__,
        'statsmodels': statsmodels.__version__,
        'sklearn': sklearn.__version__,
        'platform': platform.platform()
    }
    
    return versions
```

---

## References

1. Korn, E. L., & Graubard, B. I. (1999). Analysis of Health Surveys. John Wiley & Sons.
2. Lumley, T. (2010). Complex Surveys: A Guide to Analysis Using R. John Wiley & Sons.
3. Carriquiry, A. L., et al. (2003). Evaluation of the use of complex survey samples in National Health and Nutrition Examination Survey analyses. Journal of Official Statistics, 19(1), 21-32.
4. Keil, A. P., et al. (2020). A quantile-based g-computation approach to addressing the effects of exposure mixtures. Environmental Health Perspectives, 128(4), 047004.
5. Bobb, J. F., et al. (2015). Bayesian kernel machine regression for estimating the health effects of multi-pollutant mixtures. Biostatistics, 16(3), 493-508.
6. Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: a practical and powerful approach to multiple testing. Journal of the Royal Statistical Society, 57(1), 289-300.
