# PFAS-PhenoAge Study Presentation

## Overview
This presentation summarizes the research study examining associations between Per- and Polyfluoroalkyl Substances (PFAS) and biological aging (PhenoAge) in U.S. adults using NHANES 2005-2012 data.

**Updated**: February 13, 2026  
**Status**: FINALIZED with comprehensive content

## Presentation Formats

### Primary Format: LaTeX Beamer PDF
- **File**: `presentation.pdf` (21 slides, 384 KB)
- **Theme**: Madrid (professional academic theme)
- **Status**: ✅ Compiled and ready
- **Use**: Academic conferences, seminars, formal presentations

### Secondary Format: Markdown
- **File**: `presentation.md`
- **Status**: ✅ Updated with comprehensive content
- **Use**: Web viewing, conversion to other formats

### Source Format: LaTeX Beamer
- **File**: `presentation.tex`
- **Status**: ✅ Compiled successfully
- **Compilation**: `pdflatex presentation.tex` (via TinyTeX)

## Contents (21 Slides)

### 1. Title Slide
PFAS and Biological Aging: NHANES 2005-2012 Analysis

### 2. Background: PFAS Contamination
- "Forever chemicals" and health effects
- Study rationale

### 3. PhenoAge Biomarker
- Levine et al. (2018) algorithm
- 9 biomarkers + chronological age
- Validated predictor of mortality and morbidity

### 4. Study Objectives
- Primary aim
- Research questions (4 specific questions)

### 5. Methods: Study Design
- NHANES 2005-2012
- Inclusion criteria
- Final sample: N = 3,198

### 6. Methods: PFAS Exposure
- Four legacy compounds (PFOA, PFOS, PFHxS, PFNA)
- CDC laboratory measurements
- Log-transformation

### 7. Methods: Statistical Analysis
- Progressive regression models (Models 1-3)
- Subgroup analyses
- Mixture analysis

### 8. Results: Sample Characteristics
- Demographics table
- PFAS exposure levels

### 9. Results: Main Findings
- Regression results table
- All PFAS showed inverse associations

### 10. Results: Forest Plot
- Figure 4: Visual display of associations
- Consistent inverse patterns

### 11. Results: STROBE Flow Diagram
- Figure 1: Sample exclusions
- Final analytic sample derivation

### 12. Discussion: Paradoxical Findings
- Unexpected inverse associations
- Critical interpretation warnings
- NOT evidence of safety

### 13. Discussion: Potential Explanations
1. Survival bias (most likely)
2. Reverse causation
3. Residual confounding

### 14. Discussion: Biological Context
- Established PFAS toxicity mechanisms
- Expected vs. observed findings
- Cross-sectional design limitations

### 15. Study Strengths
- Methodological rigor
- Novel contributions
- Large representative sample

### 16. Study Limitations
- Cross-sectional design
- Single timepoint measurement
- Survival bias
- Unmeasured confounding

### 17. Public Health Implications
- DO NOT interpret as evidence of safety
- Recommendations unchanged
- Continued PFAS reduction warranted

### 18. Future Research Priorities
1. Longitudinal cohort studies
2. Mechanistic & multi-omics research
3. Vulnerable populations
4. Advanced causal inference

### 19. Conclusions
- Six key takeaways
- Paradoxical findings
- Methodological lessons

### 20. Final Thoughts
- Association ≠ Causation
- Importance of study design
- Path forward

### 21. Acknowledgments & Contact
- Data sources
- Transparency statements
- Contact information

## Viewing the Presentation

### View PDF (Recommended)
```bash
# Open the compiled PDF
xdg-open presentation.pdf   # Linux
open presentation.pdf       # macOS
start presentation.pdf      # Windows
```

### Recompile LaTeX (if needed)
```bash
# Using TinyTeX pdflatex
~/.TinyTeX/bin/x86_64-linux/pdflatex presentation.tex
```

### Convert Markdown to Other Formats
```bash
# Option 1: Reveal.js HTML slides
reveal-md presentation.md

# Option 2: Marp PowerPoint
marp presentation.md -o presentation.pptx

# Option 3: Pandoc Beamer
pandoc presentation.md -t beamer -o presentation_alt.pdf
```

## Key Messages

### Main Findings
- **All four PFAS compounds** (PFOA, PFOS, PFHxS, PFNA) showed significant **inverse associations** with PhenoAge acceleration
- **Effect sizes** (Model 3):
  - PFOA: β = -1.90 years (95% CI: -2.14 to -1.67)
  - PFOS: β = -1.32 years (95% CI: -1.52 to -1.13)
  - PFHxS: β = -1.29 years (95% CI: -1.47 to -1.11)
  - PFNA: β = -1.26 years (95% CI: -1.51 to -1.02)
- **All p-values < 0.001**

### Critical Interpretation

⚠️ **These paradoxical findings likely reflect**:
1. **Survival bias**: Most susceptible individuals died before study enrollment
2. **Reverse causation**: Biological aging influences PFAS metabolism/retention
3. **Residual confounding**: Unmeasured dietary, socioeconomic, lifestyle factors
4. **Cross-sectional limitations**: Cannot establish temporal relationships

⚠️ **NOT evidence that PFAS is safe or prevents aging**

### Public Health Message
- ✅ Continued PFAS regulation **warranted**
- ✅ Precautionary principle **applies**
- ✅ Longitudinal research **critically needed**
- ✅ Exposure reduction efforts **should continue**

## Figures Referenced

All figures are linked from `../04-analysis/outputs/figures/`:
- ✅ `figure1_strobe_flow.png` - STROBE flow diagram
- ✅ `figure2_pfas_distributions.png` - PFAS distributions by compound
- ✅ `figure3_phenoage_scatter.png` - PhenoAge vs. chronological age
- ✅ `figure4_forest_plot.png` - Forest plot of main associations
- ✅ `figure5_dose_response.png` - Dose-response curves

## Presentation Tips

### Timing Suggestions (Total: ~25 minutes)
- **Title + Background**: 5 minutes (slides 1-3)
- **Objectives + Methods**: 5 minutes (slides 4-7)
- **Results**: 5 minutes (slides 8-11)
- **Discussion**: 8 minutes (slides 12-17)
- **Future Research + Conclusions**: 4 minutes (slides 18-20)
- **Wrap-up**: 1 minute (slide 21)
- **Q&A**: 5-10 minutes

### Key Points to Emphasize

1. **Paradoxical Nature of Findings**
   - Results opposite of biological expectations
   - Contradicts toxicological evidence
   - Requires careful interpretation

2. **Methodological Limitations**
   - Cross-sectional design is fundamentally limited
   - Survival bias cannot be addressed in this design
   - Reverse causation possible

3. **Public Health Implications**
   - DO NOT interpret as evidence of safety
   - Precautionary approach maintained
   - Exposure reduction remains essential

4. **Need for Longitudinal Research**
   - Repeated measurements needed
   - Temporal relationships must be established
   - Within-person changes should be assessed

### Anticipated Questions & Suggested Responses

**Q: "Do PFAS prevent aging?"**
- **A**: **No.** The inverse associations we observed do NOT indicate that PFAS prevents aging or is protective. These paradoxical findings most likely result from survival bias (healthiest individuals remain in study), reverse causation, and limitations of cross-sectional design. Extensive toxicological evidence shows PFAS causes oxidative stress, inflammation, and organ damage—processes that should accelerate, not decelerate, aging.

**Q: "Should PFAS regulations be changed based on this study?"**
- **A**: **No.** Our findings should not change PFAS regulations or reduce exposure reduction efforts. The cross-sectional design cannot establish causality, and our results contradict extensive experimental and mechanistic evidence. The precautionary principle applies to persistent environmental contaminants like PFAS. Regulations should remain in place or be strengthened.

**Q: "What would be the ideal study design to resolve this question?"**
- **A**: A prospective cohort study with:
  - Repeated PFAS measurements over 10-20 years
  - Repeated biological aging assessments (PhenoAge and other markers)
  - Comprehensive covariate data on diet, occupation, co-exposures
  - Within-person change analysis
  - Adequate follow-up to minimize survival bias
  - Integration with mechanistic biomarkers (epigenetics, metabolomics)

**Q: "Could the inverse associations be real?"**
- **A**: While we cannot completely rule out complex non-monotonic dose-response relationships or hormetic effects, this explanation is unlikely given:
  - Consistent toxicological evidence of harm
  - Monotonic inverse dose-response in our data (not U-shaped)
  - Similar findings in other cross-sectional studies showing paradoxes
  - Biological implausibility (mechanisms should accelerate aging)
  - The more parsimonious explanation is methodological bias

**Q: "How does this compare to Yan et al. (2025)?"**
- **A**: Yan et al. found **positive** associations between PFAS and biological aging in a larger NHANES sample (1999-2018) and in UK Biobank longitudinal data. The key differences:
  - Different time periods (declining PFAS exposure over time)
  - Different analytic samples and exclusion criteria
  - Longitudinal vs. cross-sectional design
  - Our paradoxical findings reinforce the importance of study design
  - Longitudinal evidence (Yan et al.) should be weighted more heavily

**Q: "What are the clinical implications?"**
- **A**: Clinically, healthcare providers should:
  - Continue to counsel patients on PFAS exposure reduction
  - Focus on vulnerable populations (pregnant women, children)
  - Recommend practical strategies (water filtration, dietary choices, avoiding PFAS-containing products)
  - These findings do NOT change clinical recommendations
  - The weight of evidence supports minimizing PFAS exposure

## Files in This Directory

```
presentation/
├── presentation.pdf          ← PRIMARY DELIVERABLE (21 slides, 384 KB)
├── presentation.tex          ← LaTeX Beamer source
├── presentation.md           ← Markdown version (comprehensive)
├── presentation.log          ← Compilation log
├── presentation.aux          ← LaTeX auxiliary file
├── presentation.nav          ← Beamer navigation
├── presentation.out          ← PDF outline/bookmarks
├── presentation.snm          ← Beamer snm file
├── presentation.toc          ← Table of contents
└── README.md                 ← This file
```

## Quality Verification

✅ **Content Completeness**
- All 21 slides present and render correctly
- All key findings included
- Discussion of limitations comprehensive
- Public health framing clear

✅ **Figure Integration**
- Figure 4 (forest plot) displays correctly
- Figure 1 (STROBE) displays correctly
- All figure paths correct

✅ **Professional Formatting**
- Madrid theme applied consistently
- Tables formatted with booktabs
- Text readable and well-sized
- Color scheme professional

✅ **Scientific Accuracy**
- Results match analysis outputs
- Interpretations consistent with manuscript
- Limitations honestly presented
- Public health messages appropriate

## Contact

**Elwood Research Team**  
elwoodresearch@gmail.com

Full study materials available upon request:
- Complete manuscript (17 pages)
- Analysis code and scripts
- All figures and tables
- Supplementary materials

## License

Educational and academic use permitted with attribution.

---

**Last Updated**: February 13, 2026  
**Status**: ✅ FINALIZED AND READY FOR PRESENTATION
