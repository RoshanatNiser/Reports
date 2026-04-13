"""
UV-Vis Band Gap Analysis
========================
Tauc plot method for direct and indirect band gap semiconductors.
- Direct band gap: α² vs hν  (n = 1/2 → α ∝ (hν - Eg)^0.5 → α² linear)
- Indirect band gap: √α vs hν (n = 2  → α ∝ (hν - Eg)^2   → √α linear)

Usage: python bandgap_analysis.py
Outputs: PNG figures saved to ./figures/
"""

import os
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path

# ── Output directory ──────────────────────────────────────────────────────────
FIG_DIR = Path("figures")
FIG_DIR.mkdir(exist_ok=True)

# ── Plot style ────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":       "serif",
    "font.size":         11,
    "axes.labelsize":    12,
    "axes.titlesize":    13,
    "legend.fontsize":   10,
    "figure.dpi":        150,
    "lines.linewidth":   1.5,
    "axes.grid":         True,
    "grid.alpha":        0.3,
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

COLORS = {"CdS": "#E67E22", "TiO2": "#2980B9", "ZnO": "#27AE60",
          "ZnTe": "#8E44AD", "indirect": "#C0392B"}

# ── Physical constants ────────────────────────────────────────────────────────
HC_EV_NM = 1239.8  # hc in eV·nm

# ── Spectrometer wavelength calibration ──────────────────────────────────────
WL_MIN, WL_MAX = 386.542, 995.585   # nm  (from Holmarc software screenshot)
N_PIX          = 3648


def pixel_to_wavelength(pixel: np.ndarray) -> np.ndarray:
    """Convert CCD pixel index (1-based) to wavelength in nm."""
    return WL_MIN + (pixel - 1) * (WL_MAX - WL_MIN) / (N_PIX - 1)


def absorbance_to_alpha(A: np.ndarray, d_nm: float) -> np.ndarray:
    """
    Beer-Lambert: α (cm⁻¹) = 2.303 A / d
    d_nm : film thickness in nm  →  convert to cm
    """
    d_cm = d_nm * 1e-7
    return 2.303 * A / d_cm


def photon_energy(wl_nm: np.ndarray) -> np.ndarray:
    """hν in eV from wavelength in nm."""
    return HC_EV_NM / wl_nm


# ─────────────────────────────────────────────────────────────────────────────
# DIRECT BAND GAP SAMPLES
# ─────────────────────────────────────────────────────────────────────────────

# Film thicknesses (nm) — from lab context / literature estimates
# These must be provided; adjust if your actual values differ.
DIRECT_SAMPLES = {
    "CdS":  {"file": "CdS.xlsx",         "d_nm": 200,  "fit_lo": 2.10, "fit_hi": 2.40,
             "note": "linear onset; background abs. shifts intercept",
             "skip_fit": False},
    "TiO2": {"file": "TiO2_sample.xlsx", "d_nm": 200,  "fit_lo": 2.90, "fit_hi": 3.10,
             "note": "data saturated/noisy at band edge; Eg not reliably extractable",
             "skip_fit": True},
    "ZnO":  {"file": "ZnO.xlsx",         "d_nm": 200,  "fit_lo": 2.90, "fit_hi": 3.15,
             "note": "band edge near detector limit (3.21 eV)",
             "skip_fit": False},
    "ZnTe": {"file": "ZnTe.xlsx",        "d_nm": 200,  "fit_lo": 2.10, "fit_hi": 2.40,
             "note": "clean linear onset",
             "skip_fit": False},
}

def load_direct_sample(name, cfg):
    """Load an xlsx direct-gap sample and return a tidy DataFrame."""
    df_raw = pd.read_excel(f"/mnt/user-data/uploads/{cfg['file']}", header=None)
    pix  = df_raw.iloc[1:, 0].astype(float).values
    abs_ = df_raw.iloc[1:, 6].astype(float).values

    wl   = pixel_to_wavelength(pix)
    E    = photon_energy(wl)
    alpha = absorbance_to_alpha(abs_, cfg["d_nm"])

    df = pd.DataFrame({"wl": wl, "E": E, "A": abs_, "alpha": alpha,
                        "alpha2": alpha**2, "sqrt_alpha": np.sqrt(np.maximum(alpha, 0))})
    # Keep UV-Vis window, drop bad values
    mask = (wl >= 300) & (wl <= 800) & np.isfinite(alpha) & (alpha > 0)
    return df[mask].sort_values("E").reset_index(drop=True)


def fit_linear(E, y, lo, hi):
    """OLS fit of y vs E in the range [lo, hi].  Returns slope, intercept, Eg, R²."""
    mask = (E >= lo) & (E <= hi)
    if mask.sum() < 5:
        return None
    sl, ic, r, p, se = stats.linregress(E[mask], y[mask])
    Eg  = -ic / sl          # x-intercept
    R2  = r**2
    return dict(slope=sl, intercept=ic, Eg=Eg, R2=R2, se_slope=se,
                lo=lo, hi=hi, n=mask.sum())


# ─────────────────────────────────────────────────────────────────────────────
# INDIRECT BAND GAP SAMPLE  (Si-based polymer, 150 nm)
# ─────────────────────────────────────────────────────────────────────────────
INDIRECT_D_NM  = 150
INDIRECT_FITLO = 1.2
INDIRECT_FITHI = 2.0

def load_indirect():
    """Load indirect.txt (wavelength [nm], absorbance)."""
    rows = []
    with open("/mnt/user-data/uploads/indirect.txt") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("Thickness"):
                continue
            parts = line.split()
            if len(parts) == 2:
                rows.append((float(parts[0]), float(parts[1])))
    wl_arr  = np.array([r[0] for r in rows])
    abs_arr = np.array([r[1] for r in rows])
    E       = photon_energy(wl_arr)
    alpha   = absorbance_to_alpha(abs_arr, INDIRECT_D_NM)
    df = pd.DataFrame({"wl": wl_arr, "E": E, "A": abs_arr,
                        "alpha": alpha, "sqrt_alpha": np.sqrt(np.maximum(alpha, 0))})
    mask = np.isfinite(alpha) & (alpha > 0) & (E >= 1.2)
    return df[mask].sort_values("E").reset_index(drop=True)


# ─────────────────────────────────────────────────────────────────────────────
# PLOTTING HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def plot_absorbance_all(datasets):
    """Fig 1: Absorbance vs wavelength for all direct-gap samples."""
    fig, ax = plt.subplots(figsize=(7, 4))
    for name, (df, _) in datasets.items():
        ax.plot(df["wl"], df["A"], label=name, color=COLORS[name])
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Absorbance (a.u.)")
    ax.set_title("Absorbance spectra — direct band gap samples")
    ax.legend()
    ax.set_xlim(380, 800)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig1_absorbance.png", dpi=200)
    plt.close(fig)
    print("Saved fig1_absorbance.png")


def plot_tauc_direct_all(datasets):
    """Fig 2: α² vs hν for all direct-gap samples (2×2 grid)."""
    names = list(datasets.keys())
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    axes = axes.flatten()

    results = {}
    for i, name in enumerate(names):
        df, cfg = datasets[name]
        ax = axes[i]
        E, a2 = df["E"].values, df["alpha2"].values

        ax.plot(E, a2, color=COLORS[name], lw=1.2, label=r"$\alpha^2$")

        if not cfg.get("skip_fit", False):
            fit = fit_linear(E, a2, cfg["fit_lo"], cfg["fit_hi"])
        else:
            fit = None

        if fit and np.isfinite(fit["Eg"]) and 1.0 < fit["Eg"] < 5.0:
            Eg = fit["Eg"]
            x_line = np.linspace(max(Eg - 0.1, cfg["fit_lo"] - 0.2),
                                  cfg["fit_hi"] + 0.05, 200)
            y_line = fit["slope"] * x_line + fit["intercept"]
            ax.plot(x_line, np.maximum(y_line, 0), "r--", lw=1.5,
                    label=f"Linear fit\n$E_g = {Eg:.3f}$ eV\n$R^2={fit['R2']:.3f}$")
            ax.axvline(Eg, color="grey", ls=":", lw=1)
            ymax = np.percentile(a2[(E >= 1.5) & np.isfinite(a2)], 90)
            ax.annotate(f"$E_g={Eg:.3f}$ eV",
                        xy=(Eg, 0), xytext=(Eg + 0.12, ymax * 0.08),
                        arrowprops=dict(arrowstyle="->", color="grey"),
                        fontsize=9, color="darkred")
            results[name] = Eg
        elif cfg.get("skip_fit", False):
            ax.text(0.5, 0.5, "Band edge beyond\ndetector range\nor data saturated",
                    transform=ax.transAxes, ha="center", va="center",
                    fontsize=9, color="grey",
                    bbox=dict(boxstyle="round", fc="lightyellow", ec="orange"))

        ax.set_xlabel(r"Photon energy $h\nu$ (eV)")
        ax.set_ylabel(r"$\alpha^2$ (cm$^{-2}$)")
        ax.set_title(f"{name} — Tauc plot (direct)")
        ax.set_xlim(max(1.5, df["E"].min()), 3.3)
        # Clip y to 95th percentile to avoid noise spikes dominating
        valid = a2[(E >= 1.5) & (E <= 3.3) & np.isfinite(a2)]
        if len(valid):
            ax.set_ylim(0, np.percentile(valid, 97))
        ax.legend(fontsize=9)

    fig.tight_layout(pad=2)
    fig.savefig(FIG_DIR / "fig2_tauc_direct.png", dpi=200)
    plt.close(fig)
    print("Saved fig2_tauc_direct.png")
    return results


def plot_tauc_indirect(df_ind):
    """Fig 3: √α vs hν for indirect band gap."""
    fit = fit_linear(df_ind["E"].values, df_ind["sqrt_alpha"].values,
                     INDIRECT_FITLO, INDIRECT_FITHI)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(df_ind["E"], df_ind["sqrt_alpha"], color=COLORS["indirect"],
            lw=1.2, label=r"$\sqrt{\alpha}$ data ($h\nu \geq 1.2$ eV)")

    Eg = None
    if fit:
        Eg = fit["Eg"]
        x_line = np.linspace(max(Eg - 0.05, 1.0), INDIRECT_FITHI + 0.1, 300)
        y_line = fit["slope"] * x_line + fit["intercept"]
        ax.plot(x_line, np.maximum(y_line, 0), "k--", lw=2,
                label=f"Linear fit  ($R^2={fit['R2']:.3f}$)")
        ax.axvline(Eg, color="grey", ls=":", lw=1.2)
        ax.axhline(0, color="k", lw=0.7)
        ymax = df_ind["sqrt_alpha"].max()
        ax.annotate(f"$E_g = {Eg:.3f}$ eV",
                    xy=(Eg, 0), xytext=(Eg + 0.1, ymax * 0.12),
                    arrowprops=dict(arrowstyle="->", color="grey"),
                    fontsize=11, color="darkred", fontweight="bold")

    # Shade excluded impurity region
    ax.axvspan(1.0, 1.2, alpha=0.1, color="orange",
               label="Impurity shoulder (excluded)")

    ax.set_xlabel(r"Photon energy $h\nu$ (eV)")
    ax.set_ylabel(r"$\sqrt{\alpha}$ (cm$^{-1/2}$)")
    ax.set_title("Tauc plot — Si-based thin film (indirect band gap)")
    ax.set_xlim(1.0, 3.0)
    ax.set_ylim(bottom=0)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig3_tauc_indirect.png", dpi=200)
    plt.close(fig)
    print("Saved fig3_tauc_indirect.png")
    return Eg, fit


def plot_alpha_vs_energy_indirect(df_ind):
    """Fig 4: α vs hν for indirect sample."""
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(df_ind["E"], df_ind["alpha"], color=COLORS["indirect"], lw=1.4)
    ax.set_xlabel(r"Photon energy $h\nu$ (eV)")
    ax.set_ylabel(r"$\alpha$ (cm$^{-1}$)")
    ax.set_title("Absorption coefficient — Si-based thin film")
    ax.set_xlim(1.2, 4.2)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig4_alpha_indirect.png", dpi=200)
    plt.close(fig)
    print("Saved fig4_alpha_indirect.png")


def plot_individual_tauc_direct(datasets):
    """Fig 5–8: Individual Tauc plots for each direct-gap sample."""
    for i, (name, (df, cfg)) in enumerate(datasets.items(), 5):
        skip = cfg.get("skip_fit", False)
        fit = None if skip else fit_linear(df["E"].values, df["alpha2"].values,
                                            cfg["fit_lo"], cfg["fit_hi"])
        # Validate fit
        if fit and (not np.isfinite(fit["Eg"]) or not (1.0 < fit["Eg"] < 5.0)):
            fit = None

        fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

        # Left: absorbance
        axes[0].plot(df["wl"], df["A"], color=COLORS[name])
        axes[0].set_xlabel("Wavelength (nm)")
        axes[0].set_ylabel("Absorbance (a.u.)")
        axes[0].set_title(f"{name} — Absorbance spectrum")

        # Right: Tauc plot
        E, a2 = df["E"].values, df["alpha2"].values
        valid = a2[(E >= 1.5) & (E <= 3.3) & np.isfinite(a2)]
        ylim_top = np.percentile(valid, 97) if len(valid) else None

        axes[1].plot(E, a2, color=COLORS[name], lw=1.3, label=r"$\alpha^2$")
        if fit:
            Eg = fit["Eg"]
            x_line = np.linspace(max(Eg - 0.05, cfg["fit_lo"] - 0.15),
                                  cfg["fit_hi"] + 0.05, 300)
            y_line = fit["slope"] * x_line + fit["intercept"]
            axes[1].plot(x_line, np.maximum(y_line, 0), "r--", lw=2,
                          label=f"Linear fit\n$E_g={Eg:.3f}$ eV, $R^2={fit['R2']:.3f}$")
            axes[1].axvline(Eg, color="grey", ls=":", lw=1)
        elif skip:
            axes[1].text(0.5, 0.55,
                         "Band edge beyond detector range\nor data saturated — Eg not extracted",
                         transform=axes[1].transAxes, ha="center", va="center",
                         fontsize=9, color="grey",
                         bbox=dict(boxstyle="round", fc="lightyellow", ec="orange"))

        axes[1].set_xlabel(r"Photon energy $h\nu$ (eV)")
        axes[1].set_ylabel(r"$\alpha^2$ (cm$^{-2}$)")
        axes[1].set_title(f"{name} — Tauc plot (direct)")
        axes[1].set_xlim(max(1.5, df["E"].min()), 3.3)
        if ylim_top:
            axes[1].set_ylim(0, ylim_top)
        axes[1].legend(fontsize=9)

        fig.suptitle(f"{name} — Direct Band Gap Analysis", fontweight="bold")
        fig.tight_layout()
        fname = FIG_DIR / f"fig{i}_{name.lower()}_tauc.png"
        fig.savefig(fname, dpi=200)
        plt.close(fig)
        print(f"Saved {fname.name}")


# ─────────────────────────────────────────────────────────────────────────────
# ERROR ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

def error_analysis(fit, d_nm, delta_A=0.005, delta_d_nm=5.0):
    """
    Propagate uncertainties through:
      α = 2.303 A / d
      δα/α = sqrt((δA/A)² + (δd/d)²)
      δEg   from regression standard errors
    """
    d_cm = d_nm * 1e-7
    dd_cm = delta_d_nm * 1e-7

    # Typical α at band onset (use a representative A ~ 0.3)
    A_rep = 0.3
    alpha_rep = 2.303 * A_rep / d_cm
    delta_alpha = alpha_rep * np.sqrt((delta_A / A_rep)**2 + (dd_cm / d_cm)**2)

    # δ(√α) via chain rule
    delta_sqrt_alpha = delta_alpha / (2 * np.sqrt(alpha_rep))

    # δEg from regression
    if fit:
        m, b = fit["slope"], fit["intercept"]
        dm, db = fit["se_slope"], fit.get("se_slope", 0) * abs(b / m)
        Eg = fit["Eg"]
        delta_Eg = Eg * np.sqrt((dm / m)**2 + (db / abs(b))**2) if b != 0 else 0
    else:
        delta_Eg = None

    return {"delta_alpha": delta_alpha,
            "delta_sqrt_alpha": delta_sqrt_alpha,
            "delta_Eg": delta_Eg}


# ─────────────────────────────────────────────────────────────────────────────
# SUMMARY TABLE
# ─────────────────────────────────────────────────────────────────────────────

LITERATURE = {
    "CdS":  2.42, "TiO2": 3.20, "ZnO": 3.37, "ZnTe": 2.26,
    "Si-polymer": 1.12
}

def print_summary(direct_results, Eg_ind, fit_ind):
    print("\n" + "=" * 62)
    print("BAND GAP SUMMARY")
    print("=" * 62)
    print(f"{'Sample':<14} {'Eg (eV)':>9} {'Lit. (eV)':>10} {'Δ (%)':>8}  Type")
    print("-" * 62)
    for name, cfg in DIRECT_SAMPLES.items():
        if name in direct_results:
            Eg = direct_results[name]
            lit = LITERATURE.get(name, float("nan"))
            pct = 100 * (Eg - lit) / lit
            note = cfg.get("note", "")
            print(f"{name:<14} {Eg:>9.3f} {lit:>10.2f} {pct:>+8.1f}%  Direct  [{note}]")
        else:
            note = cfg.get("note", "")
            print(f"{name:<14} {'N/A':>9} {LITERATURE.get(name, float('nan')):>10.2f} {'—':>8}   Direct  [{note}]")
    Eg_lit = LITERATURE["Si-polymer"]
    pct = 100 * (Eg_ind - Eg_lit) / Eg_lit
    print(f"{'Si-polymer':<14} {Eg_ind:>9.3f} {Eg_lit:>10.2f} {pct:>+8.1f}%  Indirect")
    if fit_ind:
        print(f"\nIndirect fit: R² = {fit_ind['R2']:.4f}, "
              f"slope = {fit_ind['slope']:.1f}, intercept = {fit_ind['intercept']:.1f}")
    print("=" * 62)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("Loading data ...")

    # ── Direct gap samples ─────────────────────────────────────────────────
    datasets = {}
    for name, cfg in DIRECT_SAMPLES.items():
        df = load_direct_sample(name, cfg)
        datasets[name] = (df, cfg)
        print(f"  {name}: {len(df)} data points, "
              f"E = {df['E'].min():.2f}–{df['E'].max():.2f} eV")

    # ── Indirect gap sample ────────────────────────────────────────────────
    df_ind = load_indirect()
    print(f"  Indirect: {len(df_ind)} data points, "
          f"E = {df_ind['E'].min():.2f}–{df_ind['E'].max():.2f} eV")

    # ── Figures ────────────────────────────────────────────────────────────
    print("\nGenerating figures ...")
    plot_absorbance_all(datasets)
    direct_results = plot_tauc_direct_all(datasets)
    Eg_ind, fit_ind = plot_tauc_indirect(df_ind)
    plot_alpha_vs_energy_indirect(df_ind)
    plot_individual_tauc_direct(datasets)

    # ── Error analysis ─────────────────────────────────────────────────────
    print("\nError analysis (indirect sample):")
    err = error_analysis(fit_ind, INDIRECT_D_NM)
    if err["delta_Eg"]:
        print(f"  δEg = ±{err['delta_Eg']:.4f} eV")
        print(f"  Eg  = {Eg_ind:.3f} ± {err['delta_Eg']:.3f} eV")

    # ── Console summary ────────────────────────────────────────────────────
    print_summary(direct_results, Eg_ind, fit_ind)

    return direct_results, Eg_ind, fit_ind


if __name__ == "__main__":
    main()
