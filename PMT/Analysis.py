import numpy as np
import matplotlib.pyplot as plt
import os

# ==========================================================
# CREATE OUTPUT DIRECTORY
# ==========================================================
output_dir = "PMT_results"
os.makedirs(output_dir, exist_ok=True)

# ==========================================================
# USER INPUT (REPLACE WITH YOUR DATA)
# ==========================================================

# ----------- GAIN DATA -----------
control_voltage = np.array([0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75])
output_voltage = np.array([0.8,2.80,7.60,11.6,15.2,23.6,32.4,43.6,58.0,74.8])

# ----------- SPECTRAL RESPONSE DATA -----------
wavelength = np.array([460, 500,540,570,635])
V_out_spec = np.array([10.6,10.2,6.24,12.0,12.4])
P_in = (1e-6) * np.array([0.0192,0.0197,0.0194,0.0190,0.0196])

# ----------- DARK CURRENT DATA -----------
control_voltage_dark = np.array([0.750,0.800,0.850,0.900,0.950,0.975,1.000])
V_dark = np.array([0.001,0.002,0.004,0.007,0.009,0.011,0.013])

# ----------- CONSTANTS -----------
R = 1e6
delta_V = 0.001
delta_P_fraction = 0.1

# ==========================================================
# 1. GAIN ANALYSIS
# ==========================================================

log_V = np.log10(control_voltage)
log_G = np.log10(output_voltage)

slope, intercept = np.polyfit(log_V, log_G, 1)

# Error in slope
y_fit = slope * log_V + intercept
residuals = log_G - y_fit
N = len(log_V)

sigma_y2 = np.sum(residuals**2) / (N - 2)
sigma_m = np.sqrt(sigma_y2 / np.sum((log_V - np.mean(log_V))**2))

print("\n===== GAIN ANALYSIS =====")
print("Slope (alpha * n) =", slope)
print("Error in slope =", sigma_m)

# Plot
plt.figure()
plt.scatter(log_V, log_G, label='Data')
plt.plot(log_V, y_fit, label='Fit')
plt.xlabel('log(Control Voltage)')
plt.ylabel('log(Output Voltage)')
plt.title('Gain Analysis (Log-Log Plot)')
plt.legend()
plt.grid()
plt.tight_layout()

# Save
plt.savefig(f"{output_dir}/gain_plot.pdf", dpi=300)
plt.show()

# ==========================================================
# 2. SPECTRAL RESPONSE
# ==========================================================

I_out = V_out_spec / R
sensitivity = I_out / P_in

delta_P = delta_P_fraction * P_in

rel_I = delta_V / V_out_spec
rel_P = delta_P / P_in

rel_S = rel_I + rel_P
delta_S = sensitivity * rel_S

print("\n===== SPECTRAL RESPONSE =====")
print("Sensitivity =", sensitivity)
print("Error =", delta_S)

# Plot
plt.figure()
plt.errorbar(wavelength, sensitivity, yerr=delta_S, fmt='o')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Sensitivity (A/W)')
plt.title('Spectral Response')
plt.grid()
plt.tight_layout()

# Save
plt.savefig(f"{output_dir}/spectral_response.pdf", dpi=300)
plt.show()

# ==========================================================
# 3. DARK CURRENT
# ==========================================================

I_dark = V_dark / R
delta_I_dark = delta_V / R

print("\n===== DARK CURRENT =====")
print("Dark current =", I_dark)
print("Error =", delta_I_dark)

# Plot
plt.figure()
plt.errorbar(control_voltage_dark, I_dark, yerr=delta_I_dark, fmt='o')
plt.xlabel('Control Voltage (V)')
plt.ylabel('Dark Current (A)')
plt.title('Dark Current vs Voltage')
plt.grid()
plt.tight_layout()

# Save
plt.savefig(f"{output_dir}/dark_current.pdf", dpi=300)
plt.show()
