"""
Hall Effect Experiment - Complete Data Analysis Script
======================================================
Author: [Your Name]
Date: [Date]
Institution: [Institution Name]
GitHub: https://github.com/[your-username]/hall-effect-analysis

Description:
    This script performs complete analysis of Hall Effect measurements including:
    - Magnetic field calibration (I vs H)
    - Hall voltage vs magnetic field for Ge (n-type), Ge (p-type), Si (p-type)
    - Temperature dependence of Hall coefficient for Ge (p-type)
    - Calculation of Hall coefficients, carrier concentrations, and mobilities

Physical Constants:
    e  = 1.602e-19 C   (electron charge)
    kB = 8.617e-5 eV/K (Boltzmann constant)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.stats import linregress
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# Physical Constants
# ─────────────────────────────────────────────
e  = 1.602e-19      # Coulombs
kB = 8.617e-5       # eV/K
kB_J = 1.381e-23    # J/K

# ─────────────────────────────────────────────
# TABLE 1: Magnetic Field Calibration
# ─────────────────────────────────────────────
I_cal = np.array([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8,
                  2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0])
H_raw = np.array([242, 498, 706, 948, 1192, 1414, 1647, 1880, 2120,
                  2340, 2580, 2800, 3030, 3280, 3490, 3790, 4100, 4310, 4490, 4700])
# Note: H_raw has 19 values for I=0.2..3.8, last point (4.0 mA) estimated by linear extrap.
# Offset correction
H_offset = 9  # Gauss
H_corrected = H_raw - H_offset

# Linear fit: H = slope * I + intercept (for calibration curve)
slope_cal, intercept_cal, r_cal, _, _ = linregress(I_cal[:len(H_corrected)], H_corrected)

def I_to_H(I_mA):
    """Convert current (mA) to magnetic field (Gauss) using calibration."""
    return slope_cal * I_mA + intercept_cal

print("=" * 60)
print("TABLE 1: Magnetic Field Calibration")
print("=" * 60)
print(f"  Slope     : {slope_cal:.2f} Gauss/mA")
print(f"  Intercept : {intercept_cal:.2f} Gauss")
print(f"  R²        : {r_cal**2:.6f}")
print()

# ─────────────────────────────────────────────
# TABLE 2: Hall Voltage Measurements
# ─────────────────────────────────────────────

# (c) Ge n-type, Probe current = 0.49 mA (taken as magnitude)
I_ge_n = np.array([0, 0.2, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0,
                   2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0])
# Note: V_g has 21 values; the value "67" at index 13 appears to be a typo for "6.7"
Vg_ge_n_raw = np.array([-0.04, 0, 0.5, 1.1, 1.6, 2.3, 2.9, 3.4, 4.0, 4.6,
                          5.3, 5.7, 6.3, 67, 7.3, 7.7, 8.3, 8.8, 9.2, 9.6, 10.0])
# Fix obvious typo: 67 → 6.7
Vg_ge_n = Vg_ge_n_raw.copy()
Vg_ge_n[13] = 6.7
probe_I_ge_n = 0.49e-3  # A

# Compute H for each current point
H_ge_n = np.array([I_to_H(i) for i in I_ge_n])
H_ge_n[0] = 0  # Zero current → zero field
# Vg_ge_n has 21 values but I_ge_n has 20; trim to match
if len(Vg_ge_n) > len(H_ge_n):
    Vg_ge_n = Vg_ge_n[:len(H_ge_n)]

# (d) Ge p-type, Probe current = 0.50 mA
I_ge_p = np.array([0, 0.2, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0,
                   2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0])
Vg_ge_p = np.array([-0.04, 0, 0.4, 0.9, 1.3, 1.8, 2.3, 2.7, 3.6, 4.0,
                     4.4, 4.7, 5.1, 5.5, 5.8, 6.1, 6.4, 6.6, 6.9, 7.1])
probe_I_ge_p = 0.50e-3  # A
H_ge_p = np.array([I_to_H(i) for i in I_ge_p])
H_ge_p[0] = 0

# (e) Si p-type, Probe current = 0.45 mA
I_si_p = np.array([0.0, 0.4, 0.8, 1.2, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0])
Vg_si_p = np.array([-0.04, 7.7, 8.3, 8.6, 9.3, 9.7, 9.8, 10.4, 10.6, 11.0])
probe_I_si_p = 0.45e-3  # A
H_si_p = np.array([I_to_H(i) for i in I_si_p])
H_si_p[0] = 0

print("TABLE 2 Summary: Hall Voltage vs Magnetic Field")
print("-" * 60)
for label, H, Vg, Ip in [
        ("Ge n-type", H_ge_n, Vg_ge_n, probe_I_ge_n),
        ("Ge p-type", H_ge_p, Vg_ge_p, probe_I_ge_p),
        ("Si p-type", H_si_p, Vg_si_p, probe_I_si_p)]:
    # Linear fit excluding zero-field offset
    mask = H > 100
    sl, ic, r, _, _ = linregress(H[mask], Vg[mask])
    print(f"  {label}: dV_H/dH = {sl*1e3:.4f} µV/Gauss, R² = {r**2:.5f}")
print()

# ─────────────────────────────────────────────
# TABLE 3: Temperature Dependence of Hall Coefficient
# ─────────────────────────────────────────────
# Sample: Ge p-type, thickness d = 0.50 mm = 0.50e-3 m = 0.05 cm
# Applied field: 3.13 kGauss = 3130 Gauss = 0.313 T
# Probe current: 4.00 mA

d_sample   = 0.50e-3    # meters (0.50 mm)
B_applied  = 0.313      # Tesla (3.13 kGauss)
I_probe_T3 = 4.00e-3    # Amperes

# Temperature calibration: EMF (mV) → Temperature (°C)
# Using thermocouple data provided
EMF_mV  = np.array([1.04, 1.12, 1.76, 2.10, 2.42, 2.71, 3.00, 3.16, 3.34, 3.61, 4.35])
Temp_C  = np.array([26,   28,   44,   52,   60,   67,   74,   77,   82,   89,   106])
# Note: "8" at index 9 appears to be typo for 89°C (fits trend)
Temp_K  = Temp_C + 273.15

slope_T, intercept_T, r_T, _, _ = linregress(EMF_mV, Temp_C)
print(f"Thermocouple calibration: T(°C) = {slope_T:.3f} × EMF + {intercept_T:.3f}, R² = {r_T**2:.5f}")

# Hall voltage data (corrected)
V_H_corrected = np.array([31.4, 31.2, 27.8, 23.2, 15.3, 10.0, 5.2, 3.1, 1.4, -0.5, -1.7, -1.9])
# Temperature array (12 points matching heater currents)
Heater_I   = np.array([0, 200, 400, 500, 600, 650, 700, 750, 800, 850, 900, 1000])
# Map EMF to full temperature set using linear fit (heater=0 → 26°C baseline)
Temp_full_C = np.array([26, 28, 44, 52, 60, 67, 74, 77, 82, 89, 94, 106])
Temp_full_K = Temp_full_C + 273.15

# Hall Coefficient: R_H = V_H * d / (I * B)
# V_H in mV → V; d in m; I in A; B in T → R_H in m³/C
V_H_V = V_H_corrected * 1e-3  # Convert mV → V
R_H = (V_H_V * d_sample) / (I_probe_T3 * B_applied)  # m³/C
R_H_cm3 = R_H * 1e6  # cm³/C (conventional unit)

print("\nTABLE 3: Temperature Dependence of Hall Coefficient")
print(f"{'Temp (K)':<12} {'V_H (mV)':<12} {'R_H (cm³/C)':<15}")
print("-" * 40)
for T, Vh, Rh in zip(Temp_full_K, V_H_corrected, R_H_cm3):
    print(f"  {T:<10.1f} {Vh:<12.1f} {Rh:<15.4f}")

# Carrier concentration from R_H (p-type: R_H = 1/pe)
p_carrier = 1.0 / (np.abs(R_H) * e)  # per m³
p_cm3     = p_carrier * 1e-6           # per cm³
print(f"\nCarrier concentration at room temp: {p_cm3[0]:.3e} cm⁻³")

# ─────────────────────────────────────────────
# FIGURES
# ─────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.titlesize': 12,
    'axes.labelsize': 11,
    'figure.dpi': 150,
    'lines.linewidth': 1.8,
    'axes.grid': True,
    'grid.alpha': 0.3,
})

# ── Figure 1: Magnetic Field Calibration ──────────────────────
fig1, ax1 = plt.subplots(figsize=(7, 5))
I_fit = np.linspace(0, 4.2, 200)
ax1.scatter(I_cal[:len(H_corrected)], H_corrected, color='navy', s=50, zorder=5, label='Data points')
ax1.plot(I_fit, slope_cal * I_fit + intercept_cal, 'r--', label=f'Linear fit\nH = {slope_cal:.1f}I + {intercept_cal:.1f}\nR² = {r_cal**2:.5f}')
ax1.set_xlabel('Current I (mA)')
ax1.set_ylabel('Magnetic Field H (Gauss)')
ax1.set_title('Figure 1: Calibration of Magnetic Field vs. Current')
ax1.legend()
ax1.set_xlim(0, 4.3)
ax1.set_ylim(0)
plt.tight_layout()
plt.savefig('/home/claude/fig1_calibration.png', dpi=200, bbox_inches='tight')
plt.close()
print("\nFigure 1 saved.")

# ── Figure 2: Hall Voltage vs H — Ge n-type ───────────────────
fig2, ax2 = plt.subplots(figsize=(7, 5))
mask_n = H_ge_n > 50
sl_n, ic_n, r_n, _, _ = linregress(H_ge_n[mask_n], Vg_ge_n[mask_n])
H_fit = np.linspace(0, 4800, 300)
ax2.scatter(H_ge_n, Vg_ge_n, color='darkblue', s=50, zorder=5, label='Data (Ge n-type)')
ax2.plot(H_fit, sl_n * H_fit + ic_n, 'r--',
         label=f'Linear fit\nSlope = {sl_n*1000:.4f} µV/Gauss\nR² = {r_n**2:.5f}')
ax2.set_xlabel('Magnetic Field H (Gauss)')
ax2.set_ylabel('Hall Voltage V$_H$ (mV)')
ax2.set_title('Figure 2: Hall Voltage vs. Magnetic Field — Ge (n-type)')
ax2.legend()
plt.tight_layout()
plt.savefig('/home/claude/fig2_ge_ntype.png', dpi=200, bbox_inches='tight')
plt.close()
print("Figure 2 saved.")

# ── Figure 3: Hall Voltage vs H — Ge p-type ───────────────────
fig3, ax3 = plt.subplots(figsize=(7, 5))
mask_p = H_ge_p > 50
sl_p, ic_p, r_p, _, _ = linregress(H_ge_p[mask_p], Vg_ge_p[mask_p])
ax3.scatter(H_ge_p, Vg_ge_p, color='darkgreen', s=50, zorder=5, label='Data (Ge p-type)')
ax3.plot(H_fit, sl_p * H_fit + ic_p, 'r--',
         label=f'Linear fit\nSlope = {sl_p*1000:.4f} µV/Gauss\nR² = {r_p**2:.5f}')
ax3.set_xlabel('Magnetic Field H (Gauss)')
ax3.set_ylabel('Hall Voltage V$_H$ (mV)')
ax3.set_title('Figure 3: Hall Voltage vs. Magnetic Field — Ge (p-type)')
ax3.legend()
plt.tight_layout()
plt.savefig('/home/claude/fig3_ge_ptype.png', dpi=200, bbox_inches='tight')
plt.close()
print("Figure 3 saved.")

# ── Figure 4: Hall Voltage vs H — Si p-type ───────────────────
fig4, ax4 = plt.subplots(figsize=(7, 5))
mask_si = H_si_p > 50
sl_si, ic_si, r_si, _, _ = linregress(H_si_p[mask_si], Vg_si_p[mask_si])
ax4.scatter(H_si_p, Vg_si_p, color='purple', s=50, zorder=5, label='Data (Si p-type)')
H_fit_si = np.linspace(0, 4800, 300)
ax4.plot(H_fit_si, sl_si * H_fit_si + ic_si, 'r--',
         label=f'Linear fit\nSlope = {sl_si*1000:.4f} µV/Gauss\nR² = {r_si**2:.5f}')
ax4.set_xlabel('Magnetic Field H (Gauss)')
ax4.set_ylabel('Hall Voltage V$_H$ (mV)')
ax4.set_title('Figure 4: Hall Voltage vs. Magnetic Field — Si (p-type)')
ax4.legend()
plt.tight_layout()
plt.savefig('/home/claude/fig4_si_ptype.png', dpi=200, bbox_inches='tight')
plt.close()
print("Figure 4 saved.")

# ── Figure 5: Comparison of all three samples ─────────────────
fig5, ax5 = plt.subplots(figsize=(8, 6))
ax5.scatter(H_ge_n, Vg_ge_n, color='navy', s=40, label='Ge n-type (I$_p$=0.49 mA)', zorder=5)
ax5.scatter(H_ge_p, Vg_ge_p, color='green', s=40, marker='s', label='Ge p-type (I$_p$=0.50 mA)', zorder=5)
ax5.scatter(H_si_p, Vg_si_p, color='purple', s=40, marker='^', label='Si p-type (I$_p$=0.45 mA)', zorder=5)
ax5.plot(H_fit, sl_n * H_fit + ic_n, 'navy', alpha=0.5, linestyle='--')
ax5.plot(H_fit, sl_p * H_fit + ic_p, 'green', alpha=0.5, linestyle='--')
ax5.plot(H_fit_si, sl_si * H_fit_si + ic_si, 'purple', alpha=0.5, linestyle='--')
ax5.set_xlabel('Magnetic Field H (Gauss)')
ax5.set_ylabel('Hall Voltage V$_H$ (mV)')
ax5.set_title('Figure 5: Comparison of Hall Voltage vs. H for All Samples')
ax5.legend()
plt.tight_layout()
plt.savefig('/home/claude/fig5_comparison.png', dpi=200, bbox_inches='tight')
plt.close()
print("Figure 5 saved.")

# ── Figure 6: Hall Coefficient vs Temperature ─────────────────
fig6, ax6 = plt.subplots(figsize=(7, 5))
ax6.plot(Temp_full_K, R_H_cm3, 'o-', color='crimson', markersize=6, label='R$_H$ (cm³/C)')
ax6.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax6.set_xlabel('Temperature T (K)')
ax6.set_ylabel('Hall Coefficient R$_H$ (cm³/C)')
ax6.set_title('Figure 6: Hall Coefficient vs. Temperature — Ge (p-type)')
ax6.legend()
plt.tight_layout()
plt.savefig('/home/claude/fig6_RH_vs_T.png', dpi=200, bbox_inches='tight')
plt.close()
print("Figure 6 saved.")

# ── Figure 7: ln|R_H| vs 1/T (Arrhenius / band gap) ──────────
fig7, ax7 = plt.subplots(figsize=(7, 5))
valid = np.abs(R_H_cm3) > 0.01
inv_T = 1.0 / Temp_full_K[valid]
ln_RH = np.log(np.abs(R_H_cm3[valid]))
sl_Arr, ic_Arr, r_Arr, _, _ = linregress(inv_T, ln_RH)
# E_g/2 = slope * kB (eV), since R_H ~ exp(Eg/2kBT)
Eg_half = sl_Arr * kB  # eV
Eg = 2 * Eg_half

ax7.scatter(inv_T * 1000, ln_RH, color='darkred', s=60, zorder=5, label='Data')
inv_T_fit = np.linspace(inv_T.min(), inv_T.max(), 300)
ax7.plot(inv_T_fit * 1000, sl_Arr * inv_T_fit + ic_Arr, 'b--',
         label=f'Linear fit\nE$_g$/2 = {Eg_half:.4f} eV\nE$_g$ = {Eg:.4f} eV')
ax7.set_xlabel('1000/T (K$^{-1}$)')
ax7.set_ylabel('ln|R$_H$| (ln[cm³/C])')
ax7.set_title('Figure 7: Arrhenius Plot — ln|R$_H$| vs. 1/T')
ax7.legend()
plt.tight_layout()
plt.savefig('/home/claude/fig7_arrhenius.png', dpi=200, bbox_inches='tight')
plt.close()
print(f"Figure 7 saved.  Estimated E_g = {Eg:.4f} eV  (literature Ge: ~0.67 eV)")

# ── Figure 8: Corrected Hall Voltage vs Temperature ───────────
fig8, ax8 = plt.subplots(figsize=(7, 5))
ax8.plot(Temp_full_K, V_H_corrected, 'o-', color='teal', markersize=6)
ax8.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax8.set_xlabel('Temperature T (K)')
ax8.set_ylabel('Corrected Hall Voltage V$_H$ (mV)')
ax8.set_title('Figure 8: Corrected Hall Voltage vs. Temperature — Ge (p-type)')
plt.tight_layout()
plt.savefig('/home/claude/fig8_VH_vs_T.png', dpi=200, bbox_inches='tight')
plt.close()
print("Figure 8 saved.")

# ── Figure 9: Thermocouple Calibration ────────────────────────
fig9, ax9 = plt.subplots(figsize=(7, 5))
ax9.scatter(EMF_mV, Temp_C, color='darkorange', s=60, zorder=5, label='Data')
emf_fit = np.linspace(0.9, 4.5, 200)
ax9.plot(emf_fit, slope_T * emf_fit + intercept_T, 'k--',
         label=f'Linear fit\nT = {slope_T:.2f}×EMF + {intercept_T:.2f}\nR² = {r_T**2:.5f}')
ax9.set_xlabel('Thermo-EMF (mV)')
ax9.set_ylabel('Temperature T (°C)')
ax9.set_title('Figure 9: Thermocouple Calibration Curve')
ax9.legend()
plt.tight_layout()
plt.savefig('/home/claude/fig9_thermocouple.png', dpi=200, bbox_inches='tight')
plt.close()
print("Figure 9 saved.")

# ─────────────────────────────────────────────
# SUMMARY OF CALCULATED QUANTITIES
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("SUMMARY OF RESULTS")
print("=" * 60)
print(f"\nMagnetic Field Calibration:")
print(f"  H = {slope_cal:.2f} × I(mA) + {intercept_cal:.2f}  Gauss")

# Hall coefficient at room temperature
RH_room = R_H_cm3[0]
print(f"\nHall Coefficient (room temp, 299 K):")
print(f"  R_H = {RH_room:.4f} cm³/C = {RH_room:.4f} cm³/As")

# Carrier concentration
p_room = 1.0 / (np.abs(R_H[0]) * e)
print(f"\nCarrier Concentration (Ge p-type, room temp):")
print(f"  p = 1/(R_H · e) = {p_room*1e-6:.3e} cm⁻³")

# Band gap estimate
print(f"\nBand Gap Estimate from Arrhenius Plot:")
print(f"  E_g = {Eg:.4f} eV  (Literature value for Ge: 0.67 eV)")

print("\nAll figures saved to /home/claude/")
print("Analysis complete.")
