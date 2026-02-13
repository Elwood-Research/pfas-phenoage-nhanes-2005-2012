#!/usr/bin/env python3
"""
Script 03: Descriptive Statistics
Generate Table 1 and other descriptive statistics
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
        f.write(f"[03_descriptive_stats] {msg}\n")
    print(msg)


def load_and_calculate_phenoage():
    """Load data and calculate PhenoAge"""
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
                {1: "<HS", 2: "<HS", 3: "HS grad", 4: "Some college", 5: "College+"}
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
    for col in ["LBXLYPCT", "LBXMCVSI", "LBXRBWSI", "LBXWBCSI"]:
        if col in cbc_df.columns:
            cbc_cols.append(col)
    merged = merged.merge(cbc_df[cbc_cols], on="SEQN", how="left")

    if "LBXGLU" in glucose_df.columns:
        merged = merged.merge(glucose_df[["SEQN", "LBXGLU"]], on="SEQN", how="left")

    # Calculate PhenoAge components
    merged["albumin"] = (
        merged["LBXSAT"] * 10
        if "LBXSAT" in merged.columns
        else merged.get("LBXSAL", np.nan) * 10
    )
    merged["creatinine"] = (
        merged["LBXSCR"] * 88.4 if "LBXSCR" in merged.columns else np.nan
    )
    merged["glucose"] = (
        merged["LBXGLU"] * 0.0555 if "LBXGLU" in merged.columns else np.nan
    )
    merged["crp"] = merged["LBXCRP"] * 10 if "LBXCRP" in merged.columns else np.nan
    merged["log_crp"] = np.log(merged["crp"] + 0.01)
    merged["lymphocyte_pct"] = merged["LBXLYPCT"]
    merged["mcv"] = merged["LBXMCVSI"]
    merged["rdw"] = (
        merged["LBXRDW"]
        if "LBXRDW" in merged.columns
        else (merged["LBXRBWSI"] if "LBXRBWSI" in merged.columns else np.nan)
    )
    merged["alp"] = merged["LBXSAPSI"]
    merged["wbc"] = merged["LBXWBCSI"]

    # Calculate PhenoAge
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
    xb_clipped = np.clip(xb, -10, 10)
    m_inner = (-1.51714 * np.exp(xb_clipped)) / 0.007692696
    m_inner = np.clip(m_inner, -700, 700)
    m = 1 - np.exp(m_inner)
    m = np.clip(m, 1e-10, 1 - 1e-10)
    log_term = -0.0055305 * np.log(1 - m)
    log_term = np.clip(log_term, 1e-300, 1e300)
    merged["phenoage"] = (np.log(log_term) / 0.09165) + 141.50225
    merged["phenoage"] = np.clip(merged["phenoage"], 0, 120)
    merged["phenoage_accel"] = merged["phenoage"] - merged["age"]

    return merged


def create_pfas_quartiles(df):
    """Create PFAS quartile groups"""
    # Calculate total PFAS burden
    df["total_pfas"] = df[["PFOA", "PFOS", "PFHxS", "PFNA"]].sum(axis=1, skipna=False)
    df["total_pfas"] = df["total_pfas"].fillna(
        df[["PFOA", "PFOS", "PFHxS", "PFNA"]].sum(axis=1, skipna=True)
    )

    # Create quartiles (excluding missing values)
    valid_pfas = df["total_pfas"].dropna()
    quartiles = valid_pfas.quantile([0, 0.25, 0.5, 0.75, 1.0])

    df["pfas_quartile"] = pd.cut(
        df["total_pfas"],
        bins=quartiles.values,
        labels=["Q1 (Low)", "Q2", "Q3", "Q4 (High)"],
        include_lowest=True,
    )

    return df, quartiles


def generate_table1(df):
    """Generate Table 1: Characteristics by PFAS quartile"""
    log_message("Generating Table 1...")

    # Create quartiles
    df, quartiles = create_pfas_quartiles(df)

    table1_rows = []

    # Sample size
    n_by_q = df["pfas_quartile"].value_counts().sort_index()
    table1_rows.append(
        [
            "N",
            n_by_q.get("Q1 (Low)", 0),
            n_by_q.get("Q2", 0),
            n_by_q.get("Q3", 0),
            n_by_q.get("Q4 (High)", 0),
        ]
    )

    # Age
    age_stats = df.groupby("pfas_quartile")["age"].agg(["mean", "std"])
    table1_rows.append(
        [
            "Age, years (mean±SD)",
            f"{age_stats.loc['Q1 (Low)', 'mean']:.1f}±{age_stats.loc['Q1 (Low)', 'std']:.1f}"
            if "Q1 (Low)" in age_stats.index
            else "NA",
            f"{age_stats.loc['Q2', 'mean']:.1f}±{age_stats.loc['Q2', 'std']:.1f}"
            if "Q2" in age_stats.index
            else "NA",
            f"{age_stats.loc['Q3', 'mean']:.1f}±{age_stats.loc['Q3', 'std']:.1f}"
            if "Q3" in age_stats.index
            else "NA",
            f"{age_stats.loc['Q4 (High)', 'mean']:.1f}±{age_stats.loc['Q4 (High)', 'std']:.1f}"
            if "Q4 (High)" in age_stats.index
            else "NA",
        ]
    )

    # Sex
    sex_cross = pd.crosstab(df["pfas_quartile"], df["sex"], normalize="index") * 100
    for sex in ["Male", "Female"]:
        row = [f"{sex} (%)"]
        for q in ["Q1 (Low)", "Q2", "Q3", "Q4 (High)"]:
            val = (
                sex_cross.loc[q, sex]
                if q in sex_cross.index and sex in sex_cross.columns
                else np.nan
            )
            row.append(f"{val:.1f}" if not np.isnan(val) else "NA")
        table1_rows.append(row)

    # Race/Ethnicity
    race_cross = (
        pd.crosstab(df["pfas_quartile"], df["race_ethnicity"], normalize="index") * 100
    )
    for race in [
        "Non-Hispanic White",
        "Non-Hispanic Black",
        "Mexican American",
        "Other",
    ]:
        row = [f"{race} (%)"]
        for q in ["Q1 (Low)", "Q2", "Q3", "Q4 (High)"]:
            val = (
                race_cross.loc[q, race]
                if q in race_cross.index and race in race_cross.columns
                else np.nan
            )
            row.append(f"{val:.1f}" if not np.isnan(val) else "NA")
        table1_rows.append(row)

    # Education
    edu_cross = (
        pd.crosstab(df["pfas_quartile"], df["education"], normalize="index") * 100
    )
    for edu in ["<HS", "HS grad", "Some college", "College+"]:
        row = [f"{edu} (%)"]
        for q in ["Q1 (Low)", "Q2", "Q3", "Q4 (High)"]:
            val = (
                edu_cross.loc[q, edu]
                if q in edu_cross.index and edu in edu_cross.columns
                else np.nan
            )
            row.append(f"{val:.1f}" if not np.isnan(val) else "NA")
        table1_rows.append(row)

    # PIR
    pir_stats = df.groupby("pfas_quartile")["pir"].agg(["mean", "std"])
    table1_rows.append(
        [
            "PIR (mean±SD)",
            f"{pir_stats.loc['Q1 (Low)', 'mean']:.2f}±{pir_stats.loc['Q1 (Low)', 'std']:.2f}"
            if "Q1 (Low)" in pir_stats.index
            else "NA",
            f"{pir_stats.loc['Q2', 'mean']:.2f}±{pir_stats.loc['Q2', 'std']:.2f}"
            if "Q2" in pir_stats.index
            else "NA",
            f"{pir_stats.loc['Q3', 'mean']:.2f}±{pir_stats.loc['Q3', 'std']:.2f}"
            if "Q3" in pir_stats.index
            else "NA",
            f"{pir_stats.loc['Q4 (High)', 'mean']:.2f}±{pir_stats.loc['Q4 (High)', 'std']:.2f}"
            if "Q4 (High)" in pir_stats.index
            else "NA",
        ]
    )

    # PhenoAge
    pheno_stats = df.groupby("pfas_quartile")["phenoage_accel"].agg(["mean", "std"])
    table1_rows.append(
        [
            "PhenoAge accel, years (mean±SD)",
            f"{pheno_stats.loc['Q1 (Low)', 'mean']:.2f}±{pheno_stats.loc['Q1 (Low)', 'std']:.2f}"
            if "Q1 (Low)" in pheno_stats.index
            else "NA",
            f"{pheno_stats.loc['Q2', 'mean']:.2f}±{pheno_stats.loc['Q2', 'std']:.2f}"
            if "Q2" in pheno_stats.index
            else "NA",
            f"{pheno_stats.loc['Q3', 'mean']:.2f}±{pheno_stats.loc['Q3', 'std']:.2f}"
            if "Q3" in pheno_stats.index
            else "NA",
            f"{pheno_stats.loc['Q4 (High)', 'mean']:.2f}±{pheno_stats.loc['Q4 (High)', 'std']:.2f}"
            if "Q4 (High)" in pheno_stats.index
            else "NA",
        ]
    )

    # Create DataFrame
    table1_df = pd.DataFrame(
        table1_rows, columns=["Characteristic", "Q1 (Low)", "Q2", "Q3", "Q4 (High)"]
    )
    table1_df.to_csv(OUTPUT_DIR / "tables" / "table1_characteristics.csv", index=False)

    log_message(f"  Table 1 saved: {len(table1_df)} rows")
    return table1_df


def generate_pfas_summary(df):
    """Generate PFAS summary statistics"""
    log_message("Generating PFAS summary...")

    pfas_cols = ["PFOA", "PFOS", "PFHxS", "PFNA"]

    summary_data = []
    for col in pfas_cols:
        if col in df.columns:
            data = {
                "Compound": col,
                "N": df[col].notna().sum(),
                "Mean": df[col].mean(),
                "SD": df[col].std(),
                "Median": df[col].median(),
                "Min": df[col].min(),
                "Max": df[col].max(),
                "IQR_25": df[col].quantile(0.25),
                "IQR_75": df[col].quantile(0.75),
            }
            summary_data.append(data)

    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(OUTPUT_DIR / "tables" / "table1_pfassummary.csv", index=False)

    log_message(f"  PFAS summary: {len(summary_df)} compounds")
    return summary_df


def main():
    log_message("=" * 60)
    log_message("PFAS-PhenoAge Study: Descriptive Statistics")
    log_message("=" * 60)

    # Load data
    df = load_and_calculate_phenoage()
    log_message(f"Loaded data: {len(df)} records")

    # Generate tables
    table1 = generate_table1(df)
    pfas_summary = generate_pfas_summary(df)

    log_message("Descriptive statistics complete")
    log_message("=" * 60)


if __name__ == "__main__":
    main()
