#!/usr/bin/env python3
"""
Script 01: Data Preparation for PFAS-PhenoAge Study
Loads and merges PFAS, demographic, and biomarker data
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

# Set paths
DATA_DIR = Path("/data")
STUDY_DIR = Path("/study")
OUTPUT_DIR = STUDY_DIR / "04-analysis" / "outputs"
LOG_FILE = OUTPUT_DIR / "analysis_log.txt"


def log_message(msg):
    """Log message to file"""
    with open(LOG_FILE, "a") as f:
        f.write(f"[01_data_prep] {msg}\n")
    print(msg)


def load_pfas_data():
    """Load PFAS datasets from multiple cycles"""
    log_message("Loading PFAS datasets...")

    pfas_files = {
        "D": "PFC_D.csv",  # 2005-2006
        "E": "PFC_E.csv",  # 2007-2008
        "F": "PFC_F.csv",  # 2009-2010
        "G": "PFC_G.csv",  # 2011-2012
    }

    pfas_list = []
    cycle_counts = {}

    for cycle, filename in pfas_files.items():
        filepath = DATA_DIR / filename
        if filepath.exists():
            df = pd.read_csv(filepath)
            df["cycle"] = cycle
            df["cycle_year"] = {
                "D": "2005-2006",
                "E": "2007-2008",
                "F": "2009-2010",
                "G": "2011-2012",
            }[cycle]
            pfas_list.append(df)
            cycle_counts[cycle] = len(df)
            log_message(f"  Cycle {cycle}: {len(df)} records")

    if pfas_list:
        pfas_all = pd.concat(pfas_list, ignore_index=True)
        log_message(f"Total PFAS records: {len(pfas_all)}")
        return pfas_all, cycle_counts
    else:
        log_message("ERROR: No PFAS data loaded!")
        return None, {}


def standardize_pfas_vars(df):
    """Standardize PFAS variable names across cycles"""
    log_message("Standardizing PFAS variable names...")

    # Map various naming conventions to standardized names
    var_mapping = {
        # PFOA variants
        "LBXPFOA": "PFOA",
        "LBDPFOA": "PFOA",
        "LBPFOA": "PFOA",
        "EPFPFOA": "PFOA",
        # PFOS variants
        "LBXPFOS": "PFOS",
        "LBDPFOS": "PFOS",
        "LBPFOS": "PFOS",
        "EPFPFOS": "PFOS",
        # PFHxS variants
        "LBXPFHS": "PFHxS",
        "LBDPFHS": "PFHxS",
        "LBPFHS": "PFHxS",
        "EPFPFHXS": "PFHxS",
        # PFNA variants
        "LBXPFNA": "PFNA",
        "LBDPFNA": "PFNA",
        "LBPFNA": "PFNA",
        "EPFPFNA": "PFNA",
        # Detection limit indicators
        "LBDPFOL": "PFOA_detect",
        "LBDPFOSL": "PFOS_detect",
        "LBDPFHSL": "PFHxS_detect",
        "LBDPFNAL": "PFNA_detect",
    }

    # Rename columns if they exist
    for old_name, new_name in var_mapping.items():
        if old_name in df.columns:
            df[new_name] = df[old_name]

    # Ensure required columns exist
    required_cols = ["SEQN", "PFOA", "PFOS", "PFHxS", "PFNA"]
    for col in required_cols:
        if col not in df.columns:
            log_message(f"  WARNING: Required column {col} not found")

    return df


def load_demographics():
    """Load demographic data for all relevant cycles"""
    log_message("Loading demographic data...")

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
            df["cycle"] = cycle
            demo_list.append(df)
            log_message(f"  Cycle {cycle}: {len(df)} records")

    if demo_list:
        demo_all = pd.concat(demo_list, ignore_index=True)
        log_message(f"Total demo records: {len(demo_all)}")
        return demo_all
    return None


def standardize_demo_vars(df):
    """Standardize demographic variables"""
    log_message("Standardizing demographic variables...")

    # Age
    if "RIDAGEYR" in df.columns:
        df["age"] = df["RIDAGEYR"]

    # Sex (1=Male, 2=Female)
    if "RIAGENDR" in df.columns:
        df["sex"] = df["RIAGENDR"].map({1: "Male", 2: "Female"})

    # Race/Ethnicity
    if "RIDRETH1" in df.columns:
        race_map = {
            1: "Mexican American",
            2: "Other Hispanic",
            3: "Non-Hispanic White",
            4: "Non-Hispanic Black",
            5: "Other Race",
        }
        df["race_ethnicity"] = df["RIDRETH1"].map(race_map)

    # Education
    if "DMDEDUC2" in df.columns:
        edu_map = {
            1: "Less than 9th grade",
            2: "9-11th grade",
            3: "High school graduate",
            4: "Some college",
            5: "College graduate or above",
        }
        df["education"] = df["DMDEDUC2"].map(edu_map)

    # Income (PIR - Poverty Income Ratio)
    if "INDFMPIR" in df.columns:
        df["pir"] = df["INDFMPIR"]

    # Pregnancy status
    if "RIDEXPRG" in df.columns:
        df["pregnant"] = df["RIDEXPRG"].map({1: "Yes", 2: "No", 3: "Unknown"})

    # Survey weights
    for weight_col in ["WTMEC2YR", "WTMEC4YR", "SDMVPSU", "SDMVSTRA"]:
        if weight_col in df.columns:
            df[weight_col] = df[weight_col]

    return df


def load_biomarkers():
    """Load biomarker data for PhenoAge calculation"""
    log_message("Loading biomarker data...")

    biomarker_data = {}

    # Standard biochemistry
    biopro_files = {
        "D": "BIOPRO_D.csv",
        "F": "BIOPRO_F.csv",
        "G": "BIOPRO_G.csv",
        "H": "BIOPRO_H.csv",
        "I": "BIOPRO_I.csv",
        "J": "BIOPRO_J.csv",
    }

    # CRP
    crp_files = {
        "D": "CRP_D.csv",
        "E": "CRP_E.csv",
        "F": "CRP_F.csv",
    }

    # CBC
    cbc_files = {
        "D": "CBC_D.csv",
        "E": "CBC_E.csv",
        "F": "CBC_F.csv",
        "G": "CBC_G.csv",
        "H": "CBC_H.csv",
        "I": "CBC_I.csv",
        "J": "CBC_J.csv",
    }

    # Glucose
    glucose_files = {
        "D": "GLU_D.csv",
        "E": "GLU_E.csv",
        "F": "GLU_F.csv",
        "G": "GLU_G.csv",
        "H": "GLU_H.csv",
        "I": "GLU_I.csv",
        "J": "GLU_J.csv",
    }

    # HbA1c
    hba1c_files = {
        "D": "GHB_D.csv",
        "E": "GHB_E.csv",
        "F": "GHB_F.csv",
        "G": "GHB_G.csv",
        "H": "GHB_H.csv",
        "I": "GHB_I.csv",
        "J": "GHB_J.csv",
    }

    # Albumin/Creatinine
    alb_cr_files = {
        "D": "ALB_CR_D.csv",
        "E": "ALB_CR_E.csv",
        "F": "ALB_CR_F.csv",
        "G": "ALB_CR_G.csv",
        "H": "ALB_CR_H.csv",
        "I": "ALB_CR_I.csv",
        "J": "ALB_CR_J.csv",
    }

    # Load each type
    for name, file_dict in [
        ("biopro", biopro_files),
        ("crp", crp_files),
        ("cbc", cbc_files),
        ("glucose", glucose_files),
        ("hba1c", hba1c_files),
        ("alb_cr", alb_cr_files),
    ]:
        dfs = []
        for cycle, filename in file_dict.items():
            filepath = DATA_DIR / filename
            if filepath.exists():
                df = pd.read_csv(filepath)
                df["cycle"] = cycle
                dfs.append(df)

        if dfs:
            biomarker_data[name] = pd.concat(dfs, ignore_index=True)
            log_message(f"  {name}: {len(biomarker_data[name])} records")

    return biomarker_data


def merge_all_data(pfas_df, demo_df, biomarker_data):
    """Merge all datasets on SEQN"""
    log_message("Merging datasets...")

    # Start with PFAS data
    merged = pfas_df.copy()

    # Merge demographics
    if demo_df is not None:
        demo_cols = [
            "SEQN",
            "age",
            "sex",
            "race_ethnicity",
            "education",
            "pir",
            "pregnant",
            "WTMEC2YR",
            "SDMVPSU",
            "SDMVSTRA",
        ]
        demo_cols = [c for c in demo_cols if c in demo_df.columns]
        merged = merged.merge(demo_df[demo_cols], on="SEQN", how="left")
        log_message(f"  After demo merge: {len(merged)} records")

    # Merge biomarkers
    for name, df in biomarker_data.items():
        if name == "biopro":
            # Albumin, Creatinine, ALP
            cols = ["SEQN"]
            for col in ["LBXSAT", "LBXSAL", "LBXSCR", "LBXSAPSI", "LBXSC3SI"]:
                if col in df.columns:
                    cols.append(col)
            if len(cols) > 1:
                merged = merged.merge(df[cols], on="SEQN", how="left")

        elif name == "crp":
            cols = ["SEQN"]
            for col in ["LBXCRP", "LBDCRP"]:
                if col in df.columns:
                    cols.append(col)
            if len(cols) > 1:
                merged = merged.merge(df[cols], on="SEQN", how="left")

        elif name == "cbc":
            cols = ["SEQN"]
            for col in ["LBXLYPCT", "LBXMCVSI", "LBXRBWSI", "LBXWBCSI"]:
                if col in df.columns:
                    cols.append(col)
            if len(cols) > 1:
                merged = merged.merge(df[cols], on="SEQN", how="left")

        elif name == "glucose":
            cols = ["SEQN"]
            for col in ["LBXGLU", "LBDGLUSI"]:
                if col in df.columns:
                    cols.append(col)
            if len(cols) > 1:
                merged = merged.merge(df[cols], on="SEQN", how="left")

        elif name == "hba1c":
            cols = ["SEQN"]
            for col in ["LBXGH"]:
                if col in df.columns:
                    cols.append(col)
            if len(cols) > 1:
                merged = merged.merge(df[cols], on="SEQN", how="left")

        elif name == "alb_cr":
            cols = ["SEQN"]
            for col in ["URXUMA", "URXUMS", "URXUCR"]:
                if col in df.columns:
                    cols.append(col)
            if len(cols) > 1:
                merged = merged.merge(df[cols], on="SEQN", how="left")

    log_message(f"  Final merged dataset: {len(merged)} records")
    return merged


def apply_exclusions(df):
    """Apply study exclusion criteria"""
    log_message("Applying exclusion criteria...")

    initial_n = len(df)
    exclusions = {"initial": initial_n}

    # Exclusion 1: Missing PFAS data
    pfas_cols = ["PFOA", "PFOS", "PFHxS", "PFNA"]
    available_pfas = [c for c in pfas_cols if c in df.columns]
    if available_pfas:
        has_pfas = df[available_pfas].notna().any(axis=1)
        df = df[has_pfas].copy()
    exclusions["after_pfas_missing"] = len(df)

    # Exclusion 2: Age < 18
    if "age" in df.columns:
        df = df[df["age"] >= 18].copy()
    exclusions["after_age"] = len(df)

    # Exclusion 3: Pregnant women
    if "pregnant" in df.columns:
        df = df[df["pregnant"] != "Yes"].copy()
    exclusions["after_pregnancy"] = len(df)

    # Exclusion 4: Missing key biomarkers (need at least 7 of 9 for PhenoAge)
    biomarker_cols = [
        "LBXSAT",
        "LBXSAL",
        "LBXSCR",
        "LBXGLU",
        "LBXGH",
        "LBXCRP",
        "LBXLYPCT",
        "LBXMCVSI",
        "LBXRBWSI",
        "LBXSAPSI",
        "LBXWBCSI",
    ]
    available_bio = [c for c in biomarker_cols if c in df.columns]
    if len(available_bio) >= 7:
        df["bio_count"] = df[available_bio].notna().sum(axis=1)
        df = df[df["bio_count"] >= 7].copy()
        df = df.drop("bio_count", axis=1)
    exclusions["after_biomarkers"] = len(df)

    # Exclusion 5: Extreme outliers (|z| > 4)
    continuous_vars = ["age", "PFOA", "PFOS", "PFHxS", "PFNA"]
    for var in continuous_vars:
        if var in df.columns:
            mean_val = df[var].mean()
            std_val = df[var].std()
            if std_val > 0:
                z_scores = np.abs((df[var] - mean_val) / std_val)
                df = df[z_scores <= 4].copy()
    exclusions["after_outliers"] = len(df)

    log_message(f"  Exclusions applied:")
    for key, val in exclusions.items():
        log_message(f"    {key}: {val}")

    return df, exclusions


def save_summary_stats(df, exclusions):
    """Save summary statistics (aggregated only)"""
    log_message("Generating summary statistics...")

    # Sample size by cycle
    if "cycle_year" in df.columns:
        cycle_counts = df["cycle_year"].value_counts().to_dict()
        log_message(f"  Sample by cycle: {cycle_counts}")

    # PFAS summary
    pfas_cols = ["PFOA", "PFOS", "PFHxS", "PFNA"]
    available_pfas = [c for c in pfas_cols if c in df.columns]
    if available_pfas:
        pfas_summary = df[available_pfas].describe()
        pfas_summary.to_csv(OUTPUT_DIR / "tables" / "pfas_summary_raw.csv")
        log_message(f"  PFAS summary saved")

    # Demographics summary
    demo_summary = {}
    if "sex" in df.columns:
        demo_summary["sex"] = df["sex"].value_counts().to_dict()
    if "race_ethnicity" in df.columns:
        demo_summary["race"] = df["race_ethnicity"].value_counts().to_dict()
    if "age" in df.columns:
        demo_summary["age_stats"] = {
            "mean": df["age"].mean(),
            "std": df["age"].std(),
            "min": df["age"].min(),
            "max": df["age"].max(),
        }

    log_message(f"  Final analytic sample: {len(df)}")

    # Save exclusions
    exclusion_df = pd.DataFrame(list(exclusions.items()), columns=["stage", "count"])
    exclusion_df.to_csv(OUTPUT_DIR / "tables" / "exclusion_flow.csv", index=False)

    return len(df)


def main():
    log_message("=" * 60)
    log_message("PFAS-PhenoAge Study: Data Preparation")
    log_message("=" * 60)

    # Load data
    pfas_df, cycle_counts = load_pfas_data()
    if pfas_df is None:
        log_message("FATAL: Could not load PFAS data")
        sys.exit(1)

    # Standardize PFAS
    pfas_df = standardize_pfas_vars(pfas_df)

    # Load demographics
    demo_df = load_demographics()
    demo_df = standardize_demo_vars(demo_df)

    # Load biomarkers
    biomarker_data = load_biomarkers()

    # Merge all
    merged_df = merge_all_data(pfas_df, demo_df, biomarker_data)

    # Apply exclusions
    analytic_df, exclusions = apply_exclusions(merged_df)

    # Save summary
    final_n = save_summary_stats(analytic_df, exclusions)

    # Save analytic dataset columns info (not the actual data for privacy)
    col_info = pd.DataFrame(
        {
            "column": analytic_df.columns,
            "dtype": analytic_df.dtypes.values,
            "non_null": analytic_df.count().values,
        }
    )
    col_info.to_csv(OUTPUT_DIR / "analytic_columns.csv", index=False)

    log_message(f"Data preparation complete. Final N: {final_n}")
    log_message("=" * 60)


if __name__ == "__main__":
    main()
