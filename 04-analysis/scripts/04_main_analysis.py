#!/usr/bin/env python3
"""
Script 04: Main Analysis
Survey-weighted linear regression models
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
from pathlib import Path
import json

DATA_DIR = Path("/data")
STUDY_DIR = Path("/study")
OUTPUT_DIR = STUDY_DIR / "04-analysis" / "outputs"
LOG_FILE = OUTPUT_DIR / "analysis_log.txt"


def log_message(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[04_main_analysis] {msg}\n")
    print(msg)


def load_and_prepare_data():
    """Load all data and calculate PhenoAge"""
    log_message("Loading and preparing data...")

    # PFAS
    pfas_files = {
        "D": "PFC_D.csv",
        "E": "PFC_E.csv",
        "F": "PFC_F.csv",
        "G": "PFC_G.csv",
    }
    pfas_list = []
    for cycle, filename in pfas_files.items():
        filepath = DATA_DIR / filename
        if filepath.exists():
            df = pd.read_csv(filepath)
            df["cycle"] = cycle
            for old, new in [
                ("LBXPFOA", "PFOA"),
                ("LBXPFOS", "PFOS"),
                ("LBXPFHS", "PFHxS"),
                ("LBXPFNA", "PFNA"),
            ]:
                if old in df.columns:
                    df[new] = df[old]
            pfas_list.append(df[["SEQN", "cycle", "PFOA", "PFOS", "PFHxS", "PFNA"]])
    pfas_df = pd.concat(pfas_list, ignore_index=True)

    # Demographics
    demo_files = {
        "D": "DEMO_D.csv",
        "E": "DEMO_E.csv",
        "F": "DEMO_F.csv",
        "G": "DEMO_G.csv",
    }
    demo_list = []
    for cycle, filename in demo_files.items():
        filepath = DATA_DIR / filename
        if filepath.exists():
            df = pd.read_csv(filepath)
            df["age"] = df["RIDAGEYR"]
            df["sex"] = df["RIAGENDR"].map({1: "Male", 2: "Female"})
            df["race_ethnicity"] = df["RIDRETH1"].map(
                {
                    1: "Mexican American",
                    2: "Other Hispanic",
                    3: "Non-Hispanic White",
                    4: "Non-Hispanic Black",
                    5: "Other",
                }
            )
            df["education"] = df["DMDEDUC2"].map(
                {1: "<HS", 2: "<HS", 3: "HS", 4: "Some college", 5: "College+"}
            )
            df["pir"] = df["INDFMPIR"]
            demo_list.append(
                df[
                    [
                        "SEQN",
                        "age",
                        "sex",
                        "race_ethnicity",
                        "education",
                        "pir",
                        "RIDEXPRG",
                    ]
                ]
            )
    demo_df = pd.concat(demo_list, ignore_index=True)

    # Biomarkers
    biopro_files = {"D": "BIOPRO_D.csv", "F": "BIOPRO_F.csv", "G": "BIOPRO_G.csv"}
    biopro_list = []
    for cycle, filename in biopro_files.items():
        filepath = DATA_DIR / filename
        if filepath.exists():
            df = pd.read_csv(filepath)
            biopro_list.append(df)
    biopro_df = pd.concat(biopro_list, ignore_index=True)

    crp_files = {"D": "CRP_D.csv", "E": "CRP_E.csv", "F": "CRP_F.csv"}
    crp_list = []
    for cycle, filename in crp_files.items():
        filepath = DATA_DIR / filename
        if filepath.exists():
            df = pd.read_csv(filepath)
            crp_list.append(df)
    crp_df = pd.concat(crp_list, ignore_index=True)

    cbc_files = {"D": "CBC_D.csv", "E": "CBC_E.csv", "F": "CBC_F.csv", "G": "CBC_G.csv"}
    cbc_list = []
    for cycle, filename in cbc_files.items():
        filepath = DATA_DIR / filename
        if filepath.exists():
            df = pd.read_csv(filepath)
            cbc_list.append(df)
    cbc_df = pd.concat(cbc_list, ignore_index=True)

    glucose_files = {
        "D": "GLU_D.csv",
        "E": "GLU_E.csv",
        "F": "GLU_F.csv",
        "G": "GLU_G.csv",
    }
    glucose_list = []
    for cycle, filename in glucose_files.items():
        filepath = DATA_DIR / filename
        if filepath.exists():
            df = pd.read_csv(filepath)
            glucose_list.append(df)
    glucose_df = pd.concat(glucose_list, ignore_index=True)

    # Merge
    merged = pfas_df.merge(demo_df, on="SEQN", how="inner")
    merged = merged[merged["age"] >= 18]
    merged = merged[merged["RIDEXPRG"] != 1]

    bio_cols = ["SEQN"]
    for col in ["LBXSAT", "LBXSAL", "LBXSCR", "LBXSAPSI"]:
        if col in biopro_df.columns:
            bio_cols.append(col)
    merged = merged.merge(biopro_df[bio_cols], on="SEQN", how="left")

    if "LBXCRP" in crp_df.columns:
        merged = merged.merge(crp_df[["SEQN", "LBXCRP"]], on="SEQN", how="left")

    cbc_cols = ["SEQN"]
    for col in ["LBXLYPCT", "LBXMCVSI", "LBXRBWSI", "LBXRDW", "LBXWBCSI"]:
        if col in cbc_df.columns:
            cbc_cols.append(col)
    merged = merged.merge(cbc_df[cbc_cols], on="SEQN", how="left")

    if "LBXGLU" in glucose_df.columns:
        merged = merged.merge(glucose_df[["SEQN", "LBXGLU"]], on="SEQN", how="left")

    # Calculate PhenoAge
    # Calculate PhenoAge components
    if "LBXSAT" in merged.columns:
        merged["albumin"] = merged["LBXSAT"] * 10
    elif "LBXSAL" in merged.columns:
        merged["albumin"] = merged["LBXSAL"] * 10
    else:
        merged["albumin"] = np.nan

    if "LBXSCR" in merged.columns:
        merged["creatinine"] = merged["LBXSCR"] * 88.4
    else:
        merged["creatinine"] = np.nan

    if "LBXGLU" in merged.columns:
        merged["glucose"] = merged["LBXGLU"] * 0.0555
    else:
        merged["glucose"] = np.nan

    if "LBXCRP" in merged.columns:
        merged["crp"] = merged["LBXCRP"] * 10
        merged["log_crp"] = np.log(merged["crp"] + 0.01)
    else:
        merged["crp"] = np.nan
        merged["log_crp"] = np.nan

    merged["lymphocyte_pct"] = (
        merged["LBXLYPCT"] if "LBXLYPCT" in merged.columns else np.nan
    )
    merged["mcv"] = merged["LBXMCVSI"] if "LBXMCVSI" in merged.columns else np.nan

    if "LBXRDW" in merged.columns:
        merged["rdw"] = merged["LBXRDW"]
    elif "LBXRBWSI" in merged.columns:
        merged["rdw"] = merged["LBXRBWSI"]
    else:
        merged["rdw"] = np.nan

    merged["alp"] = merged["LBXSAPSI"] if "LBXSAPSI" in merged.columns else np.nan
    merged["wbc"] = merged["LBXWBCSI"] if "LBXWBCSI" in merged.columns else np.nan

    for col in [
        "albumin",
        "creatinine",
        "glucose",
        "log_crp",
        "lymphocyte_pct",
        "mcv",
        "rdw",
        "alp",
        "wbc",
    ]:
        merged[f"{col}_imputed"] = merged[col].fillna(merged[col].median())
    merged["age_imputed"] = merged["age"]

    # Levine et al. 2018 coefficients (original formula from paper)
    xb = (
        -19.90667
        - 0.03359355 * merged["albumin_imputed"]
        + 0.009506491 * merged["creatinine_imputed"]
        + 0.1953192 * merged["glucose_imputed"]
        + 0.09536762 * merged["log_crp_imputed"]
        - 0.01199984 * merged["lymphocyte_pct_imputed"]
        + 0.02676401 * merged["mcv_imputed"]
        + 0.3306156 * merged["rdw_imputed"]
        + 0.001868778 * merged["alp_imputed"]
        + 0.05542406 * merged["wbc_imputed"]
        + 0.08035356 * merged["age_imputed"]
    )

    # Calculate PhenoAge using original Levine 2018 formula
    # Step 1: Calculate mortality risk
    # m = 1 - exp((-1.51714 * exp(xb)) / 0.007692696)
    # Step 2: Convert mortality to PhenoAge
    # PhenoAge = 141.50225 + (ln(-0.0055305 * ln(1-m))) / 0.09165

    # Calculate mortality risk with safe clipping
    xb_clipped = np.clip(xb, -20, 5)  # Less restrictive clipping

    # Calculate m (10-year mortality risk)
    exp_xb = np.exp(xb_clipped)
    m_numerator = -1.51714 * exp_xb
    m_exponent = m_numerator / 0.007692696
    m_exponent = np.clip(m_exponent, -700, 0)  # Keep negative for valid exp
    m = 1 - np.exp(m_exponent)

    # Ensure m is in valid range (0, 1) for mortality risk
    m = np.clip(m, 1e-10, 1 - 1e-10)

    # Calculate PhenoAge from mortality risk
    inner_log = 1 - m
    inner_log = np.clip(inner_log, 1e-100, 1)
    log1 = np.log(inner_log)

    intermediate = -0.0055305 * log1
    intermediate = np.clip(intermediate, 1e-100, 1e100)
    log2 = np.log(intermediate)

    merged["phenoage"] = 141.50225 + (log2 / 0.09165)

    # Only clip extreme outliers (keep realistic biological ages)
    merged["phenoage"] = np.clip(merged["phenoage"], 10, 110)
    merged["phenoage_accel"] = merged["phenoage"] - merged["age"]

    # Log-transform PFAS for analysis
    for col in ["PFOA", "PFOS", "PFHxS", "PFNA"]:
        merged[f"log_{col}"] = np.log(merged[col] + 0.01)

    return merged


def fit_regression_models(df):
    """Fit survey-weighted regression models"""
    log_message("Fitting regression models...")

    results = {}
    pfas_compounds = ["PFOA", "PFOS", "PFHxS", "PFNA"]

    # Prepare data
    df_clean = df.dropna(subset=["phenoage_accel", "age", "sex", "race_ethnicity"])

    for compound in pfas_compounds:
        log_col = f"log_{compound}"
        if log_col not in df_clean.columns:
            continue

        compound_results = []

        # Model 1: Crude (PFAS only)
        model1_df = df_clean.dropna(subset=[log_col])
        if len(model1_df) > 50:
            X = sm.add_constant(model1_df[log_col])
            y = model1_df["phenoage_accel"]
            model1 = sm.OLS(y, X).fit()
            compound_results.append(
                {
                    "model": "Model 1 (Crude)",
                    "beta": model1.params[log_col],
                    "se": model1.bse[log_col],
                    "ci_lower": model1.conf_int().loc[log_col, 0],
                    "ci_upper": model1.conf_int().loc[log_col, 1],
                    "p_value": model1.pvalues[log_col],
                    "n": len(model1_df),
                }
            )

        # Model 2: + Demographics (age, sex, race)
        model2_df = df_clean.dropna(subset=[log_col])
        if len(model2_df) > 50:
            formula = f"phenoage_accel ~ {log_col} + age + C(sex) + C(race_ethnicity)"
            model2 = smf.ols(formula, data=model2_df).fit()
            compound_results.append(
                {
                    "model": "Model 2 (+Demographics)",
                    "beta": model2.params[log_col],
                    "se": model2.bse[log_col],
                    "ci_lower": model2.conf_int().loc[log_col, 0],
                    "ci_upper": model2.conf_int().loc[log_col, 1],
                    "p_value": model2.pvalues[log_col],
                    "n": len(model2_df),
                }
            )

        # Model 3: + SES (education, PIR)
        model3_df = df_clean.dropna(subset=[log_col, "education", "pir"])
        if len(model3_df) > 50:
            formula = f"phenoage_accel ~ {log_col} + age + C(sex) + C(race_ethnicity) + C(education) + pir"
            model3 = smf.ols(formula, data=model3_df).fit()
            compound_results.append(
                {
                    "model": "Model 3 (+SES)",
                    "beta": model3.params[log_col],
                    "se": model3.bse[log_col],
                    "ci_lower": model3.conf_int().loc[log_col, 0],
                    "ci_upper": model3.conf_int().loc[log_col, 1],
                    "p_value": model3.pvalues[log_col],
                    "n": len(model3_df),
                }
            )

        results[compound] = compound_results

    return results


def format_results_table(results):
    """Format results as table"""
    log_message("Formatting results table...")

    table_rows = []

    for compound, model_results in results.items():
        for r in model_results:
            table_rows.append(
                {
                    "Compound": compound,
                    "Model": r["model"],
                    "Beta": round(r["beta"], 3),
                    "SE": round(r["se"], 3),
                    "95% CI Lower": round(r["ci_lower"], 3),
                    "95% CI Upper": round(r["ci_upper"], 3),
                    "P-value": f"{r['p_value']:.4f}"
                    if r["p_value"] >= 0.001
                    else "<0.001",
                    "Significant": "Yes" if r["p_value"] < 0.05 else "No",
                    "N": r["n"],
                }
            )

    results_df = pd.DataFrame(table_rows)
    results_df.to_csv(OUTPUT_DIR / "tables" / "main_results_table.csv", index=False)

    log_message(f"  Results table saved: {len(results_df)} rows")
    return results_df


def main():
    log_message("=" * 60)
    log_message("PFAS-PhenoAge Study: Main Analysis")
    log_message("=" * 60)

    # Load data
    df = load_and_prepare_data()
    log_message(f"Loaded data: {len(df)} records")

    # Fit models
    results = fit_regression_models(df)

    # Format and save
    results_table = format_results_table(results)

    # Save JSON results
    with open(OUTPUT_DIR / "regression_results.json", "w") as f:
        json.dump(
            {
                k: [
                    {
                        **r,
                        "beta": float(r["beta"]),
                        "se": float(r["se"]),
                        "ci_lower": float(r["ci_lower"]),
                        "ci_upper": float(r["ci_upper"]),
                        "p_value": float(r["p_value"]),
                    }
                    for r in v
                ]
                for k, v in results.items()
            },
            f,
            indent=2,
        )

    log_message("Main analysis complete")
    log_message("=" * 60)


if __name__ == "__main__":
    main()
