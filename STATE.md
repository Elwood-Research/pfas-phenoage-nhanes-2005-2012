# Study State

## Current Phase
✅ **STUDY COMPLETE - Ready for Publication**

## Phase Status
| Phase | Status | Iteration | Complete |
|-------|--------|-----------|----------|
| Literature Review | Completed | 1 | Yes |
| Research Plan | Completed | 1 | Yes |
| Methods Definition | Completed | 1 | Yes |
| Analysis Execution | Completed | 1 | Yes |
| Synthesis | Completed | 1 | Yes |
| Manuscript | Completed | 1 | Yes |
| Presentation | Completed | 1 | Yes |
| GitHub Publication | Pending | 0 | No |

## Data Sources Used
- [x] PFAS datasets: PFC_D, PFC_E, PFC_F, PFC_G (2005-2012)
- [x] Demographics: DEMO_D, DEMO_E, DEMO_F, DEMO_G
- [x] Biomarkers: BIOPRO_D-G, CRP_D-G, CBC_D-G, GLU_D-G
- [x] Sample size: N = 3,198 adults

## Key Variables Confirmed
- **PFAS exposures**: PFOA (LBXPFOA), PFOS (LBXPFOS), PFHxS (LBXPFHS), PFNA (LBXPFNA)
- **PhenoAge components**: 
  - Albumin (LBXSAL), Creatinine (LBXSCR), Glucose (LBXGLU)
  - CRP (LBXCRP), Lymphocyte % (LBXLYPCT), MCV (LBXMCVSI)
  - **RDW (LBXRDW)** ← Corrected from incorrect LBXRBWSI in prior scripts
  - Alkaline Phosphatase (LBXSAPSI), WBC (LBXWBCSI)

## Critical Bug Fixed
**Problem**: Scripts 02-08 used wrong RDW variable (`LBXRBWSI` instead of `LBXRDW`)
**Impact**: PhenoAge calculations were invalid (mean 0.00, acceleration -47.91 years)
**Solution**: Created `complete_analysis.py` with correct variable names
**Result**: Realistic PhenoAge (mean 45.6 years, acceleration -1.80 years)

## Key Findings
⚠️ **PARADOXICAL INVERSE ASSOCIATIONS** (opposite of hypothesis):
- All four PFAS showed significant **inverse** associations with PhenoAge acceleration
- Higher PFAS → Lower biological aging (contrary to toxicological evidence)
- Fully adjusted Model 3 results:
  - PFOA: β = -0.850 (p < 0.001)
  - PFOS: β = -0.420 (p = 0.007)
  - PFHxS: β = -0.605 (p < 0.001)
  - PFNA: β = -0.560 (p = 0.003)

## Interpretation
**These findings DO NOT suggest PFAS are protective!**

Likely explanations:
1. **Survival bias**: Individuals with high PFAS + poor health die before enrollment
2. **Reverse causation**: Better kidney function → higher PFAS retention
3. **Cross-sectional limitations**: Cannot establish temporal sequence
4. **Sample selection bias**: Complete-case analysis selects healthier participants
5. **Unmeasured confounding**: SES, lifestyle, healthcare access

Contrasts with **Yan et al. (2025)** longitudinal UK Biobank study (found positive associations).

## Deliverables Completed
- [x] Literature review (60+ references, BibTeX verified)
- [x] Variable selection and data dictionary
- [x] Methods documentation (detailed statistical plan)
- [x] Complete analysis script (`complete_analysis.py`)
- [x] 5 figures (STROBE flow, PFAS distributions, scatter, forest plot, dose-response)
- [x] Summary tables (characteristics, PFAS summary, main results, sensitivity)
- [x] Results summary markdown
- [x] Synthesis document (detailed interpretation)
- [x] Full manuscript (21 pages, LaTeX PDF with references)
- [x] Presentation (10 slides, Beamer PDF)
- [x] README.md (comprehensive documentation)

## Files Ready for Publication
```
pfas-phenoage-2026-02-13/
├── README.md ✅
├── PROJECT.md ✅
├── STATE.md ✅ (this file)
├── 01-literature/ ✅
├── 02-variables/ ✅
├── 03-methods/ ✅
├── 04-analysis/scripts/complete_analysis.py ✅
├── 04-analysis/outputs/ ✅ (figures, tables, results)
├── 05-conclusion/synthesis.md ✅
├── manuscript/manuscript.pdf ✅ (21 pages)
└── presentation/presentation.pdf ✅ (10 slides)
```

## Next Step
📤 **Publish to GitHub** (Elwood-Research organization)

## Notes
- Study initiated: 2026-02-13
- Study completed: 2026-02-13
- Analysis executed in Docker vault with `--network none`
- All outputs reproducible and documented
- **Methodological contribution**: Identified critical PhenoAge calculation bug
- **Scientific contribution**: Demonstrates importance of study design in PFAS-aging research

