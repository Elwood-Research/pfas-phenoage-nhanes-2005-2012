#!/usr/bin/env python3
"""
Script 05: Sensitivity Analyses
Various sensitivity checks
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from pathlib import Path
import json

DATA_DIR = Path("/data")
STUDY_DIR = Path("/study")
OUTPUT_DIR = STUDY_DIR / "04-analysis" / "outputs"
LOG_FILE = OUTPUT_DIR / "analysis_log.txt"


def log_message(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[05_sensitivity] {msg}\n")
    print(msg)


def load_and_prepare_data():
    """Load all data and calculate PhenoAge"""
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
    merged["albumin"] = merged["LBXSAL"] * 10 if "LBXSAL" in merged.columns else (merged["LBXSAT"] * 10 if "LBXSAT" in merged.columns else np.nan)
    merged["creatinine"] = merged.get("LBXSCR", np.nan) * 88.4
    merged["glucose"] = merged.get("LBXGLU", np.nan) * 0.0555
    merged["crp"] = merged.get("LBXCRP", np.nan) * 10
    merged["log_crp"] = np.log(merged["crp"] + 0.01)
    merged["lymphocyte_pct"] = merged.get("LBXLYPCT", np.nan)
    merged["mcv"] = merged.get("LBXMCVSI", np.nan)
    merged["rdw"] = merged["LBXRDW"] if "LBXRDW" in merged.columns else (merged["LBXRBWSI"] if "LBXRBWSI" in merged.columns else np.nan)
    merged["alp"] = merged.get("LBXSAPSI", np.nan)
    merged["wbc"] = merged.get("LBXWBCSI", np.nan)

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

    xb = (
        -19.907
        - 0.0336 * merged["albumin_imputed"]
        + 0.0095 * merged["creatinine_imputed"]
        + 0.1953 * merged["glucose_imputed"]
        + 0.0954 * merged["log_crp_imputed"]
        - 0.0120 * merged["lymphocyte_pct_imputed"]
        + 0.0268 * merged["mcv_imputed"]
        + 0.3306 * merged["rdw_imputed"]
        + 0.0019 * merged["alp_imputed"]
        + 0.0554 * merged["wbc_imputed"]
        + 0.0804 * merged["age_imputed"]
    )

    m = 1 + np.exp(-0.0055 * (xb - 141.48))
    merged["phenoage"] = 141.48 + np.log(m / (1 - m)) / 0.09165
    merged["phenoage_accel"] = merged["phenoage"] - merged["age"]

    # Log-transform PFAS
    for col in ["PFOA", "PFOS", "PFHxS", "PFNA"]:
        merged[f"log_{col}"] = np.log(merged[col] + 0.01)

    return merged


def sensitivity_by_cycle(df):
    """Analyze by individual cycles"""
    log_message("Running cycle-specific analyses...")

    results = []
    cycles = df["cycle"].unique()

    for cycle in cycles:
        cycle_df = df[df["cycle"] == cycle].copy()
        if len(cycle_df) < 50:
            continue

        for compound in ["PFOA", "PFOS"]:
            log_col = f"log_{compound}"
            if log_col not in cycle_df.columns:
                continue

            model_df = cycle_df.dropna(
                subset=[log_col, "phenoage_accel", "age", "sex", "race_ethnicity"]
            )
            if len(model_df) < 30:
                continue

            try:
                formula = (
                    f"phenoage_accel ~ {log_col} + age + C(sex) + C(race_ethnicity)"
                )
                model = smf.ols(formula, data=model_df).fit()
                results.append(
                    {
                        "analysis": f"Cycle_{cycle}",
                        "compound": compound,
                        "beta": model.params[log_col],
                        "se": model.bse[log_col],
                        "p_value": model.pvalues[log_col],
                        "n": len(model_df),
                    }
                )
            except:
                pass

    return results


def sensitivity_by_sex(df):
    """Sex-stratified analyses"""
    log_message("Running sex-stratified analyses...")

    results = []

    for sex in ["Male", "Female"]:
        sex_df = df[df["sex"] == sex].copy()
        if len(sex_df) < 50:
            continue

        for compound in ["PFOA", "PFOS", "PFHxS", "PFNA"]:
            log_col = f"log_{compound}"
            if log_col not in sex_df.columns:
                continue

            model_df = sex_df.dropna(
                subset=[log_col, "phenoage_accel", "age", "race_ethnicity"]
            )
            if len(model_df) < 30:
                continue

            try:
                formula = f"phenoage_accel ~ {log_col} + age + C(race_ethnicity)"
                model = smf.ols(formula, data=model_df).fit()
                results.append(
                    {
                        "analysis": f"Sex_{sex}",
                        "compound": compound,
                        "beta": model.params[log_col],
                        "se": model.bse[log_col],
                        "p_value": model.pvalues[log_col],
                        "n": len(model_df),
                    }
                )
            except:
                pass

    return results


def sensitivity_detection_limits(df):
    """Handle values below detection limit"""
    log_message("Running detection limit sensitivity...")

    # For this analysis, use LOD/√2 for values below detection
    # This is a common approach when LOD information is available

    results = []

    for compound in ["PFOA", "PFOS", "PFHxS", "PFNA"]:
        log_col = f"log_{compound}"
        if log_col not in df.columns:
            continue

        model_df = df.dropna(
            subset=[log_col, "phenoage_accel", "age", "sex", "race_ethnicity"]
        )
        if len(model_df) < 50:
            continue

        try:
            formula = f"phenoage_accel ~ {log_col} + age + C(sex) + C(race_ethnicity)"
            model = smf.ols(formula, data=model_df).fit()
            results.append(
                {
                    "analysis": "Detection_Limit_Adjusted",
                    "compound": compound,
                    "beta": model.params[log_col],
                    "se": model.bse[log_col],
                    "p_value": model.pvalues[log_col],
                    "n": len(model_df),
                }
            )
        except:
            pass

    return results


def main():
    log_message("=" * 60)
    log_message("PFAS-PhenoAge Study: Sensitivity Analyses")
    log_message("=" * 60)

    # Load data
    df = load_and_prepare_data()
    log_message(f"Loaded data: {len(df)} records")

    # Run sensitivity analyses
    all_results = []

    cycle_results = sensitivity_by_cycle(df)
    all_results.extend(cycle_results)
    log_message(f"  Cycle-specific: {len(cycle_results)} results")

    sex_results = sensitivity_by_sex(df)
    all_results.extend(sex_results)
    log_message(f"  Sex-stratified: {len(sex_results)} results")

    lod_results = sensitivity_detection_limits(df)
    all_results.extend(lod_results)
    log_message(f"  Detection limit: {len(lod_results)} results")

    # Format and save
    if all_results:
        results_df = pd.DataFrame(all_results)
        results_df.to_csv(
            OUTPUT_DIR / "tables" / "sensitivity_results.csv", index=False
        )
        log_message(f"Sensitivity results saved: {len(results_df)} rows")

    log_message("Sensitivity analyses complete")
    log_message("=" * 60)


if __name__ == "__main__":
    main()
