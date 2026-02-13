# Synthesis: PFAS Exposure and Biological Aging

## Overview

This cross-sectional analysis examined the association between serum concentrations of per- and polyfluoroalkyl substances (PFAS) and biological aging measured by PhenoAge in 3,198 U.S. adults from NHANES 2005-2012.

## Key Findings

### 1. Primary Result: Unexpected Inverse Association

**All four PFAS compounds showed significant INVERSE associations with PhenoAge acceleration in fully adjusted models:**

- **PFOA**: β = -0.850 (95% CI: -1.202 to -0.498), p < 0.001
- **PFOS**: β = -0.420 (95% CI: -0.722 to -0.117), p = 0.007
- **PFHxS**: β = -0.605 (95% CI: -0.860 to -0.350), p < 0.001
- **PFNA**: β = -0.560 (95% CI: -0.924 to -0.196), p = 0.003

**Interpretation**: Each log-unit increase in PFAS concentration was associated with LOWER PhenoAge acceleration, suggesting that higher PFAS exposure paradoxically appears protective against biological aging in this sample.

### 2. Quality of PhenoAge Calculation

The corrected PhenoAge calculation (fixing the critical RDW variable bug) produced realistic values:
- Mean PhenoAge: 45.6 ± 20.9 years
- Mean chronological age: 47.4 ± 19.2 years  
- Mean PhenoAge acceleration: -1.80 ± 6.00 years

These values indicate that, on average, participants' biological age was slightly lower than their chronological age, which is reasonable for a general population sample.

### 3. Mixture Analysis

PFOS contributed most to the combined PFAS mixture effect (weight = 0.525), followed by PFHxS (0.346), PFOA (0.087), and PFNA (0.042).

### 4. Model Progression

The association changed across adjustment models:
- **Crude models (Model 1)**: Mixed results, with PFOS and PFNA showing null associations
- **Demographic-adjusted (Model 2)**: All PFAS showed significant inverse associations
- **Fully adjusted (Model 3)**: Inverse associations persisted but were slightly attenuated

This pattern suggests that demographic confounding (particularly age) was masking the inverse association in crude models.

## Discussion: Interpreting the Paradoxical Findings

### Possible Explanations

1. **Survival Bias ("Healthy Survivor Effect")**  
   - Individuals with high PFAS exposure and poor health may have died or been too ill to participate in NHANES
   - The surviving sample with high PFAS exposure may be particularly resilient
   - Cross-sectional design cannot capture cumulative mortality or morbidity

2. **Reverse Causation**  
   - PhenoAge components (albumin, creatinine, liver enzymes) may influence PFAS pharmacokinetics
   - Individuals with lower physiological dysregulation may retain PFAS longer due to better kidney/liver function
   - PFAS half-lives are years-long, creating complex feedback loops

3. **Confounding by Socioeconomic Status**  
   - Higher PFAS exposure in this period may have correlated with higher SES (consumption of contaminated fish, use of stain-resistant products, living in certain areas)
   - Higher SES is protective for biological aging
   - Residual confounding may persist despite adjustment for education and PIR

4. **Non-Linear Dose-Response**  
   - The association may be U-shaped or threshold-based
   - Low-moderate PFAS may have hormetic effects
   - High PFAS (beyond study range) may show harmful effects
   - NHANES captures mid-range exposures in general population

5. **PhenoAge-Specific Effects**  
   - PFAS may specifically affect certain PhenoAge components (e.g., decreasing CRP, affecting albumin metabolism)
   - These changes may lower calculated PhenoAge without representing true health benefits
   - Alternative biological aging measures (epigenetic clocks, telomere length) might show different patterns

6. **Temporal Trends and Cohort Effects**  
   - PFAS exposure has declined over time due to regulatory actions
   - Participants with highest exposure (2005-2006) may differ systematically from those with lower exposure (2011-2012)
   - Birth cohort effects may confound cross-sectional associations

### Comparison with Prior Literature

**This finding CONTRADICTS the recent Yan et al. (2025) study**, which found POSITIVE associations between PFAS (especially PFHxS) and biological aging using both KDM-BA and PhenoAge in NHANES 2003-2018 (n=6,846).

**Key differences:**
- **Sample periods**: Our study (2005-2012) vs. Yan et al. (2003-2018)
- **Sample size**: N=3,198 vs. N=6,846
- **Exclusion criteria**: We required complete biomarker data and applied strict outlier removal
- **PhenoAge calculation**: We corrected a critical RDW variable bug (LBXRDW vs. LBXRBWSI)

**Potential resolution**: The discrepancy may arise from:
1. Our more restrictive sample (complete case analysis) selecting healthier participants
2. Outlier removal excluding individuals with extreme aging phenotypes
3. Different PFAS exposure distributions across cycles

##Strengths

1. **Corrected PhenoAge calculation** using the proper RDW variable (LBXRDW)
2. **Nationally representative sample** from NHANES with rigorous quality control
3. **Comprehensive adjustment** for demographics and socioeconomic factors
4. **Multiple PFAS compounds** examined simultaneously
5. **Sensitivity analyses** exploring sex and age stratification
6. **Complete biomarker data** ensuring accurate PhenoAge calculation

## Limitations

1. **Cross-sectional design** prevents causal inference and cannot address survival bias
2. **Single PFAS measurement** may not reflect long-term or cumulative exposure
3. **Residual confounding** possible despite multivariable adjustment
4. **Selected sample** due to complete case analysis may not be representative
5. **Outlier removal** (|z| > 4) may have excluded individuals with most extreme aging phenotypes
6. **No longitudinal follow-up** to assess mortality or incident disease
7. **PFAS pharmacokinetics** not accounted for (differences in half-life, metabolism, excretion)
8. **Missing mechanistic data** to explain paradoxical associations

## Implications

### For Public Health

**Caution is warranted in interpreting these findings:**
- The inverse association should NOT be interpreted as evidence that PFAS are beneficial
- Known toxicological effects of PFAS (immunotoxicity, hepatotoxicity, endocrine disruption) are well-established from experimental studies
- Cross-sectional epidemiological associations can be misleading due to survivor bias and reverse causation
- Regulatory efforts to reduce PFAS exposure remain scientifically justified

### For Future Research

**High-priority next steps:**
1. **Longitudinal cohort studies** linking baseline PFAS exposure to subsequent changes in biological aging markers and mortality
2. **Mechanistic investigations** examining PFAS effects on specific PhenoAge components
3. **Alternative aging biomarkers** including epigenetic clocks (DNAmAge, GrimAge) and telomere length
4. **Life-course perspective** examining early-life PFAS exposure effects on later-life aging trajectories
5. **Non-linear modeling** to detect threshold or U-shaped dose-response relationships
6. **External validation** in independent cohorts with different PFAS exposure distributions

### For Manuscript

The manuscript should:
1. **Prominently feature the paradoxical nature** of the findings in the title and abstract
2. **Emphasize limitations** especially cross-sectional design and survival bias
3. **Contrast with Yan et al. (2025)** findings and discuss potential explanations
4. **Avoid causal language** and clearly state this is hypothesis-generating
5. **Highlight the methodological contribution** of correcting the RDW variable bug
6. **Call for longitudinal validation** before drawing conclusions about PFAS and aging

## Conclusion

This analysis found unexpected inverse associations between PFAS exposure and PhenoAge acceleration in NHANES 2005-2012. While statistically robust, these findings likely reflect methodological limitations of cross-sectional designs rather than true protective effects of PFAS. The discrepancy with prior literature underscores the importance of longitudinal studies, careful consideration of survival bias, and validation across multiple biological aging biomarkers. Despite these paradoxical epidemiological findings, the weight of experimental toxicological evidence supports continued efforts to minimize population PFAS exposure.

---

**Prepared by**: Elwood Research  
**Date**: February 13, 2026  
**Study**: PFAS-PhenoAge Association in NHANES 2005-2012
