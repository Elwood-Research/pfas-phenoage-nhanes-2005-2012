#!/usr/bin/env python3
"""
Script 06: Mixture Analysis
Weighted Quantile Sum (WQS) regression for PFAS mixtures
"""

import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path("/data")
STUDY_DIR = Path("/study")
OUTPUT_DIR = STUDY_DIR / "04-analysis" / "outputs"
LOG_FILE = OUTPUT_DIR / "analysis_log.txt"


def log_message(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[06_mixture_analysis] {msg}\n")
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
            demo_list.append(df[["SEQN", "age", "sex", "race_ethnicity", "RIDEXPRG"]])
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

    return merged


def calculate_pfas_correlation(df):
    """Calculate PFAS correlation matrix"""
    log_message("Calculating PFAS correlations...")

    pfas_cols = ["PFOA", "PFOS", "PFHxS", "PFNA"]
    available_cols = [c for c in pfas_cols if c in df.columns]

    if len(available_cols) < 2:
        log_message("  Insufficient PFAS compounds for correlation")
        return None

    # Calculate correlation on log-transformed values
    log_pfas = df[available_cols].apply(lambda x: np.log(x + 0.01))
    corr_matrix = log_pfas.corr()

    # Save correlation matrix
    corr_matrix.to_csv(OUTPUT_DIR / "tables" / "pfas_correlation_matrix.csv")

    log_message(
        f"  Correlation matrix saved: {len(available_cols)}x{len(available_cols)}"
    )
    return corr_matrix


def calculate_wqs_weights(df):
    """
    Calculate simplified WQS weights based on individual associations
    This is a simplified version since full WQS requires specialized packages
    """
    log_message("Calculating mixture weights...")

    import statsmodels.api as sm

    pfas_cols = ["PFOA", "PFOS", "PFHxS", "PFNA"]
    weights = {}

    for col in pfas_cols:
        if col not in df.columns:
            continue

        # Standardize PFAS values
        df[f"{col}_std"] = (df[col] - df[col].mean()) / df[col].std()

        # Simple regression
        valid_data = df.dropna(subset=[f"{col}_std", "phenoage_accel"])
        if len(valid_data) < 50:
            continue

        X = sm.add_constant(valid_data[f"{col}_std"])
        y = valid_data["phenoage_accel"]
        model = sm.OLS(y, X).fit()

        # Weight based on absolute standardized coefficient
        weights[col] = abs(model.params[f"{col}_std"])

    # Normalize weights to sum to 1
    if weights:
        total_weight = sum(weights.values())
        weights = {k: v / total_weight for k, v in weights.items()}

    # Save weights
    weights_df = pd.DataFrame(list(weights.items()), columns=["Compound", "Weight"])
    weights_df.to_csv(OUTPUT_DIR / "tables" / "wqs_weights.csv", index=False)

    log_message(f"  WQS weights calculated: {weights}")
    return weights


def calculate_pfas_index(df, weights):
    """Calculate weighted PFAS mixture index"""
    log_message("Calculating PFAS mixture index...")

    pfas_cols = ["PFOA", "PFOS", "PFHxS", "PFNA"]

    # Standardize each PFAS
    for col in pfas_cols:
        if col in df.columns:
            df[f"{col}_std"] = (df[col] - df[col].mean()) / df[col].std()

    # Calculate weighted index
    df["pfas_index"] = 0
    for col in pfas_cols:
        if col in weights and f"{col}_std" in df.columns:
            df["pfas_index"] += df[f"{col}_std"] * weights[col]

    # Regression with mixture index
    import statsmodels.formula.api as smf

    valid_data = df.dropna(
        subset=["pfas_index", "phenoage_accel", "age", "sex", "race_ethnicity"]
    )

    if len(valid_data) > 50:
        formula = "phenoage_accel ~ pfas_index + age + C(sex) + C(race_ethnicity)"
        model = smf.ols(formula, data=valid_data).fit()

        mixture_result = {
            "beta": model.params["pfas_index"],
            "se": model.bse["pfas_index"],
            "ci_lower": model.conf_int().loc["pfas_index", 0],
            "ci_upper": model.conf_int().loc["pfas_index", 1],
            "p_value": model.pvalues["pfas_index"],
            "n": len(valid_data),
        }

        mixture_df = pd.DataFrame([mixture_result])
        mixture_df.to_csv(OUTPUT_DIR / "tables" / "mixture_results.csv", index=False)

        log_message(
            f"  Mixture index beta: {mixture_result['beta']:.3f} (p={mixture_result['p_value']:.4f})"
        )
        return mixture_result

    return None


def main():
    log_message("=" * 60)
    log_message("PFAS-PhenoAge Study: Mixture Analysis")
    log_message("=" * 60)

    # Load data
    df = load_and_prepare_data()
    log_message(f"Loaded data: {len(df)} records")

    # Calculate correlations
    corr_matrix = calculate_pfas_correlation(df)

    # Calculate WQS weights
    weights = calculate_wqs_weights(df)

    # Calculate mixture index
    if weights:
        mixture_result = calculate_pfas_index(df, weights)

    log_message("Mixture analysis complete")
    log_message("=" * 60)


if __name__ == "__main__":
    main()
