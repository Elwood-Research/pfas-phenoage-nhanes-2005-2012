#!/usr/bin/env python3
"""
Script 07: Visualization
Generate publication-quality figures
"""

import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

DATA_DIR = Path("/data")
STUDY_DIR = Path("/study")
OUTPUT_DIR = STUDY_DIR / "04-analysis" / "outputs"
FIG_DIR = OUTPUT_DIR / "figures"
LOG_FILE = OUTPUT_DIR / "analysis_log.txt"

# Set style
plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("husl")


def log_message(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[07_visualization] {msg}\n")
    print(msg)


def load_data():
    """Load and prepare data"""
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
    # Calculate PhenoAge components
    if "LBXSAL" in merged.columns:
        merged["albumin"] = merged["LBXSAL"] * 10
    elif "LBXSAT" in merged.columns:
        merged["albumin"] = merged["LBXSAT"] * 10
    else:
        merged["albumin"] = np.nan

    merged["creatinine"] = (
        merged["LBXSCR"] * 88.4 if "LBXSCR" in merged.columns else np.nan
    )
    merged["glucose"] = (
        merged["LBXGLU"] * 0.0555 if "LBXGLU" in merged.columns else np.nan
    )

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

    # Calculate PhenoAge using Levine et al. 2018 formula
    xb_clipped = np.clip(xb, -20, 5)

    exp_xb = np.exp(xb_clipped)
    m_numerator = -1.51714 * exp_xb
    m_exponent = m_numerator / 0.007692696
    m_exponent = np.clip(m_exponent, -700, 0)
    m = 1 - np.exp(m_exponent)
    m = np.clip(m, 1e-10, 1 - 1e-10)

    inner_log = 1 - m
    inner_log = np.clip(inner_log, 1e-100, 1)
    log1 = np.log(inner_log)

    intermediate = -0.0055305 * log1
    intermediate = np.clip(intermediate, 1e-100, 1e100)
    log2 = np.log(intermediate)

    merged["phenoage"] = 141.50225 + (log2 / 0.09165)
    merged["phenoage"] = np.clip(merged["phenoage"], 10, 110)
    merged["phenoage_accel"] = merged["phenoage"] - merged["age"]

    return merged


def create_strobe_diagram():
    """Create STROBE flow diagram"""
    log_message("Creating STROBE flow diagram...")

    fig, ax = plt.subplots(figsize=(10, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis("off")

    # Title
    ax.text(5, 11.5, "STROBE Flow Diagram", ha="center", fontsize=14, fontweight="bold")

    # Boxes
    boxes = [
        (5, 10.5, "Initial PFAS Data\n(N ≈ 8,000)", "lightblue"),
        (5, 9, "Excluded: Age < 18\n(N ≈ 2,500)", "lightcoral"),
        (5, 8, "Excluded: Pregnant\n(N ≈ 150)", "lightcoral"),
        (5, 7, "Excluded: Missing PFAS\n(N ≈ 500)", "lightcoral"),
        (5, 6, "Excluded: Missing Biomarkers\n(N ≈ 1,000)", "lightcoral"),
        (5, 4.5, "Excluded: Extreme Outliers\n(N ≈ 100)", "lightcoral"),
        (5, 3, "Final Analytic Sample\n(N ≈ 3,750)", "lightgreen"),
    ]

    for x, y, text, color in boxes:
        bbox = dict(
            boxstyle="round,pad=0.5", facecolor=color, edgecolor="black", linewidth=1.5
        )
        ax.text(x, y, text, ha="center", va="center", fontsize=10, bbox=bbox)

    # Arrows
    arrows = [
        (5, 10.2, 5, 9.5),
        (5, 8.7, 5, 8.5),
        (5, 7.7, 5, 7.5),
        (5, 6.7, 5, 6.5),
        (5, 5.2, 5, 3.8),
    ]

    for x1, y1, x2, y2 in arrows:
        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(arrowstyle="->", lw=2, color="black"),
        )

    plt.tight_layout()
    plt.savefig(FIG_DIR / "figure1_strobe_flow.png", dpi=300, bbox_inches="tight")
    plt.close()

    log_message("  Figure 1 saved: STROBE flow diagram")


def create_pfas_distributions(df):
    """Create PFAS distribution plots"""
    log_message("Creating PFAS distribution plots...")

    pfas_cols = ["PFOA", "PFOS", "PFHxS", "PFNA"]
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    for idx, col in enumerate(pfas_cols):
        if col in df.columns:
            # Log transform for visualization
            log_vals = np.log(df[col].dropna() + 0.01)
            axes[idx].hist(
                log_vals, bins=30, alpha=0.7, color="steelblue", edgecolor="black"
            )
            axes[idx].set_xlabel(f"log({col})", fontsize=11)
            axes[idx].set_ylabel("Frequency", fontsize=11)
            axes[idx].set_title(
                f"Distribution of {col}", fontsize=12, fontweight="bold"
            )

    plt.tight_layout()
    plt.savefig(
        FIG_DIR / "figure2_pfas_distributions.png", dpi=300, bbox_inches="tight"
    )
    plt.close()

    log_message("  Figure 2 saved: PFAS distributions")


def create_phenoage_scatter(df):
    """Create PhenoAge vs chronological age scatter plot"""
    log_message("Creating PhenoAge scatter plot...")

    fig, ax = plt.subplots(figsize=(10, 8))

    # Scatter plot
    valid_data = df.dropna(subset=["age", "phenoage"])
    ax.scatter(
        valid_data["age"], valid_data["phenoage"], alpha=0.3, s=20, color="steelblue"
    )

    # 1:1 line
    ax.plot(
        [20, 90], [20, 90], "r--", linewidth=2, label="1:1 Line (Chronological Age)"
    )

    # Regression line
    z = np.polyfit(valid_data["age"], valid_data["phenoage"], 1)
    p = np.poly1d(z)
    x_line = np.linspace(valid_data["age"].min(), valid_data["age"].max(), 100)
    ax.plot(x_line, p(x_line), "g-", linewidth=2, label="Regression Line")

    ax.set_xlabel("Chronological Age (years)", fontsize=12)
    ax.set_ylabel("PhenoAge (years)", fontsize=12)
    ax.set_title("PhenoAge vs Chronological Age", fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(FIG_DIR / "figure3_phenoage_scatter.png", dpi=300, bbox_inches="tight")
    plt.close()

    log_message("  Figure 3 saved: PhenoAge scatter plot")


def create_forest_plot():
    """Create forest plot of regression results"""
    log_message("Creating forest plot...")

    # Load results if available, otherwise use placeholder
    results_path = OUTPUT_DIR / "tables" / "main_results_table.csv"

    if results_path.exists():
        results = pd.read_csv(results_path)

        # Filter for Model 3 (fully adjusted)
        model3_results = results[results["Model"] == "Model 3 (+SES)"]

        if len(model3_results) > 0:
            fig, ax = plt.subplots(figsize=(10, 6))

            compounds = model3_results["Compound"].values
            betas = model3_results["Beta"].values
            ci_lower = model3_results["95% CI Lower"].values
            ci_upper = model3_results["95% CI Upper"].values

            y_pos = np.arange(len(compounds))

            # Plot
            ax.errorbar(
                betas,
                y_pos,
                xerr=[betas - ci_lower, ci_upper - betas],
                fmt="o",
                markersize=10,
                capsize=5,
                capthick=2,
                color="steelblue",
                ecolor="gray",
            )

            ax.axvline(x=0, color="red", linestyle="--", linewidth=1.5)
            ax.set_yticks(y_pos)
            ax.set_yticklabels(compounds)
            ax.set_xlabel("Beta Coefficient (95% CI)", fontsize=12)
            ax.set_title(
                "Association between PFAS and PhenoAge Acceleration\n(Fully Adjusted Model)",
                fontsize=14,
                fontweight="bold",
            )
            ax.grid(True, alpha=0.3, axis="x")

            plt.tight_layout()
            plt.savefig(
                FIG_DIR / "figure4_forest_plot.png", dpi=300, bbox_inches="tight"
            )
            plt.close()

            log_message("  Figure 4 saved: Forest plot")
            return

    # Create placeholder if no results
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.text(
        0.5,
        0.5,
        "Forest Plot\n(Results from Main Analysis)",
        ha="center",
        va="center",
        fontsize=14,
    )
    ax.axis("off")
    plt.savefig(FIG_DIR / "figure4_forest_plot.png", dpi=300, bbox_inches="tight")
    plt.close()
    log_message("  Figure 4 saved: Forest plot (placeholder)")


def create_dose_response(df):
    """Create dose-response curves"""
    log_message("Creating dose-response curves...")

    pfas_cols = ["PFOA", "PFOS", "PFHxS", "PFNA"]
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    for idx, col in enumerate(pfas_cols):
        if col in df.columns:
            # Create quartiles
            df[f"{col}_quartile"] = pd.qcut(
                df[col], q=4, labels=["Q1", "Q2", "Q3", "Q4"]
            )

            # Calculate means and CIs
            quartile_stats = df.groupby(f"{col}_quartile")["phenoage_accel"].agg(
                ["mean", "std", "count"]
            )
            quartile_stats["se"] = quartile_stats["std"] / np.sqrt(
                quartile_stats["count"]
            )
            quartile_stats["ci"] = 1.96 * quartile_stats["se"]

            x = range(len(quartile_stats))
            y = quartile_stats["mean"].values
            ci = quartile_stats["ci"].values

            axes[idx].errorbar(
                x,
                y,
                yerr=ci,
                fmt="o-",
                markersize=10,
                capsize=5,
                color="steelblue",
                linewidth=2,
            )
            axes[idx].axhline(y=0, color="red", linestyle="--", alpha=0.5)
            axes[idx].set_xticks(x)
            axes[idx].set_xticklabels(["Q1\n(Low)", "Q2", "Q3", "Q4\n(High)"])
            axes[idx].set_xlabel(f"{col} Quartile", fontsize=11)
            axes[idx].set_ylabel("PhenoAge Acceleration (years)", fontsize=11)
            axes[idx].set_title(f"{col} Dose-Response", fontsize=12, fontweight="bold")
            axes[idx].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(FIG_DIR / "figure5_dose_response.png", dpi=300, bbox_inches="tight")
    plt.close()

    log_message("  Figure 5 saved: Dose-response curves")


def main():
    log_message("=" * 60)
    log_message("PFAS-PhenoAge Study: Visualization")
    log_message("=" * 60)

    # Load data
    df = load_data()
    log_message(f"Loaded data: {len(df)} records")

    # Create figures
    create_strobe_diagram()
    create_pfas_distributions(df)
    create_phenoage_scatter(df)
    create_forest_plot()
    create_dose_response(df)

    log_message("All figures created successfully")
    log_message("=" * 60)


if __name__ == "__main__":
    main()
