#!/usr/bin/env python3
"""
Script 02: PhenoAge Calculation
Implements the Levine et al. (2018) PhenoAge algorithm
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

DATA_DIR = Path("/data")
STUDY_DIR = Path("/study")
OUTPUT_DIR = STUDY_DIR / "04-analysis" / "outputs"
LOG_FILE = OUTPUT_DIR / "analysis_log.txt"


def log_message(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[02_phenoage_calc] {msg}\n")
    print(msg)


def load_analytic_data():
    """Reload the merged dataset"""
    # We need to re-merge from scratch since we can't load saved data
    log_message("Loading datasets for PhenoAge calculation...")

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
            pfas_list.append(df)
    pfas_df = pd.concat(pfas_list, ignore_index=True)

    # Standardize PFAS
    for old, new in [
        ("LBXPFOA", "PFOA"),
        ("LBXPFOS", "PFOS"),
        ("LBXPFHS", "PFHxS"),
        ("LBXPFNA", "PFNA"),
    ]:
        if old in pfas_df.columns:
            pfas_df[new] = pfas_df[old]

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
            demo_list.append(df)
    demo_df = pd.concat(demo_list, ignore_index=True)
    demo_df["age"] = demo_df["RIDAGEYR"]

    # Biomarkers
    # Biopro
    biopro_files = {"D": "BIOPRO_D.csv", "F": "BIOPRO_F.csv", "G": "BIOPRO_G.csv"}
    biopro_list = []
    for cycle, filename in biopro_files.items():
        filepath = DATA_DIR / filename
        if filepath.exists():
            df = pd.read_csv(filepath)
            biopro_list.append(df)
    biopro_df = pd.concat(biopro_list, ignore_index=True)

    # CRP
    crp_files = {"D": "CRP_D.csv", "E": "CRP_E.csv", "F": "CRP_F.csv"}
    crp_list = []
    for cycle, filename in crp_files.items():
        filepath = DATA_DIR / filename
        if filepath.exists():
            df = pd.read_csv(filepath)
            crp_list.append(df)
    crp_df = pd.concat(crp_list, ignore_index=True)

    # CBC
    cbc_files = {"D": "CBC_D.csv", "E": "CBC_E.csv", "F": "CBC_F.csv", "G": "CBC_G.csv"}
    cbc_list = []
    for cycle, filename in cbc_files.items():
        filepath = DATA_DIR / filename
        if filepath.exists():
            df = pd.read_csv(filepath)
            cbc_list.append(df)
    cbc_df = pd.concat(cbc_list, ignore_index=True)

    # Glucose
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
    merged = pfas_df[["SEQN", "PFOA", "PFOS", "PFHxS", "PFNA"]].copy()
    merged = merged.merge(demo_df[["SEQN", "age", "RIDEXPRG"]], on="SEQN", how="inner")

    # Apply basic exclusions
    merged = merged[merged["age"] >= 18].copy()
    merged = merged[merged["RIDEXPRG"] != 1].copy()  # Not pregnant
    merged = merged.dropna(subset=["PFOA", "PFOS", "PFHxS", "PFNA"], how="all")

    # Merge biomarkers
    bio_cols = ["SEQN"]
    for col in ["LBXSAT", "LBXSAL", "LBXSCR", "LBXSAPSI"]:
        if col in biopro_df.columns:
            bio_cols.append(col)
    if len(bio_cols) > 1:
        merged = merged.merge(biopro_df[bio_cols], on="SEQN", how="left")

    if "LBXCRP" in crp_df.columns:
        merged = merged.merge(crp_df[["SEQN", "LBXCRP"]], on="SEQN", how="left")

    cbc_cols = ["SEQN"]
    for col in ["LBXLYPCT", "LBXMCVSI", "LBXRBWSI", "LBXWBCSI"]:
        if col in cbc_df.columns:
            cbc_cols.append(col)
    if len(cbc_cols) > 1:
        merged = merged.merge(cbc_df[cbc_cols], on="SEQN", how="left")

    if "LBXGLU" in glucose_df.columns:
        merged = merged.merge(glucose_df[["SEQN", "LBXGLU"]], on="SEQN", how="left")

    return merged


def prepare_phenoage_components(df):
    """
    Prepare PhenoAge components with proper unit conversions
    """
    log_message("Preparing PhenoAge components...")

    # Albumin (g/L) - from g/dL
    if "LBXSAT" in df.columns:
        df["albumin"] = df["LBXSAT"] * 10  # g/dL to g/L
    elif "LBXSAL" in df.columns:
        df["albumin"] = df["LBXSAL"] * 10  # g/dL to g/L

    # Creatinine (μmol/L) - from mg/dL
    if "LBXSCR" in df.columns:
        df["creatinine"] = df["LBXSCR"] * 88.4  # mg/dL to μmol/L

    # Glucose (mmol/L) - from mg/dL
    if "LBXGLU" in df.columns:
        df["glucose"] = df["LBXGLU"] * 0.0555  # mg/dL to mmol/L

    # CRP (mg/L) - from mg/dL
    if "LBXCRP" in df.columns:
        df["crp"] = df["LBXCRP"] * 10  # mg/dL to mg/L
        df["log_crp"] = np.log(df["crp"] + 0.01)  # Add small constant for log

    # Lymphocyte %
    if "LBXLYPCT" in df.columns:
        df["lymphocyte_pct"] = df["LBXLYPCT"]

    # MCV (fL)
    if "LBXMCVSI" in df.columns:
        df["mcv"] = df["LBXMCVSI"]

    # RDW (%)
    if "LBXRDW" in df.columns:
        df["rdw"] = df["LBXRDW"]
    elif "LBXRBWSI" in df.columns:
        df["rdw"] = df["LBXRBWSI"]

    # ALP (U/L)
    if "LBXSAPSI" in df.columns:
        df["alp"] = df["LBXSAPSI"]

    # WBC (10^9/L) - convert from 1000 cells/μL
    if "LBXWBCSI" in df.columns:
        df["wbc"] = df["LBXWBCSI"]  # Already in 10^9/L

    return df


def calculate_phenoage(df):
    """
    Calculate PhenoAge using Levine et al. 2018 algorithm
    """
    log_message("Calculating PhenoAge...")

    # Check required components
    required_components = [
        "albumin",
        "creatinine",
        "glucose",
        "log_crp",
        "lymphocyte_pct",
        "mcv",
        "rdw",
        "alp",
        "wbc",
        "age",
    ]

    available_components = [c for c in required_components if c in df.columns]
    log_message(f"  Available components: {available_components}")

    # For participants missing some components, we'll still calculate if we have enough
    # Using available data and population means for missing values
    for col in required_components:
        if col in df.columns:
            df[f"{col}_imputed"] = df[col].fillna(df[col].median())
        else:
            # Use population mean from literature
            defaults = {
                "albumin": 42,
                "creatinine": 80,
                "glucose": 5.5,
                "log_crp": 0.5,
                "lymphocyte_pct": 30,
                "mcv": 90,
                "rdw": 13,
                "alp": 80,
                "wbc": 6.5,
                "age": 45,
            }
            df[f"{col}_imputed"] = defaults.get(col, np.nan)

    # Levine et al. 2018 coefficients (original formula from paper)
    xb = (
        -19.90667
        - 0.03359355 * df["albumin_imputed"]
        + 0.009506491 * df["creatinine_imputed"]
        + 0.1953192 * df["glucose_imputed"]
        + 0.09536762 * df["log_crp_imputed"]
        - 0.01199984 * df["lymphocyte_pct_imputed"]
        + 0.02676401 * df["mcv_imputed"]
        + 0.3306156 * df["rdw_imputed"]
        + 0.001868778 * df["alp_imputed"]
        + 0.05542406 * df["wbc_imputed"]
        + 0.08035356 * df["age_imputed"]
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

    df["phenoage"] = 141.50225 + (log2 / 0.09165)

    # Only clip extreme outliers (keep realistic biological ages)
    df["phenoage"] = np.clip(df["phenoage"], 10, 110)

    # Calculate PhenoAge acceleration
    df["phenoage_accel"] = df["phenoage"] - df["age_imputed"]

    log_message(
        f"  PhenoAge calculated for {df['phenoage'].notna().sum()} participants"
    )

    return df


def generate_phenoage_stats(df):
    """Generate summary statistics for PhenoAge"""
    log_message("Generating PhenoAge statistics...")

    stats = {}

    # Overall stats
    stats["phenoage_mean"] = df["phenoage"].mean()
    stats["phenoage_std"] = df["phenoage"].std()
    stats["phenoage_min"] = df["phenoage"].min()
    stats["phenoage_max"] = df["phenoage"].max()

    stats["phenoage_accel_mean"] = df["phenoage_accel"].mean()
    stats["phenoage_accel_std"] = df["phenoage_accel"].std()

    stats["age_mean"] = df["age"].mean()

    log_message(f"  Mean PhenoAge: {stats['phenoage_mean']:.2f} years")
    log_message(
        f"  Mean PhenoAge acceleration: {stats['phenoage_accel_mean']:.2f} years"
    )

    # Save stats
    stats_df = pd.DataFrame([stats])
    stats_df.to_csv(OUTPUT_DIR / "tables" / "phenoage_summary.csv", index=False)

    # Age-stratified
    df["age_group"] = pd.cut(
        df["age"],
        bins=[17, 30, 40, 50, 60, 70, 100],
        labels=["18-29", "30-39", "40-49", "50-59", "60-69", "70+"],
    )
    age_stats = (
        df.groupby("age_group")
        .agg(
            {
                "phenoage": ["mean", "std"],
                "phenoage_accel": ["mean", "std"],
                "age": "count",
            }
        )
        .reset_index()
    )
    age_stats.to_csv(OUTPUT_DIR / "tables" / "phenoage_by_age.csv", index=False)

    return stats


def main():
    log_message("=" * 60)
    log_message("PFAS-PhenoAge Study: PhenoAge Calculation")
    log_message("=" * 60)

    # Load data
    df = load_analytic_data()
    log_message(f"Loaded data: {len(df)} records")

    # Prepare components
    df = prepare_phenoage_components(df)

    # Calculate PhenoAge
    df = calculate_phenoage(df)

    # Generate stats
    stats = generate_phenoage_stats(df)

    log_message("PhenoAge calculation complete")
    log_message("=" * 60)


if __name__ == "__main__":
    main()
