
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# LOAD DATA
# -----------------------------
filename = "f2.txt"
data = np.loadtxt(filename)

time = data[:, 0]
voltage = data[:, 1]

# -----------------------------
# REMOVE DC OFFSET
# -----------------------------
voltage = voltage - np.mean(voltage)

# -----------------------------
# SAMPLING PARAMETERS
# -----------------------------
dt = time[1] - time[0]
fs = 1 / dt
N = len(voltage)

print("Sampling frequency =", fs, "Hz")

# -----------------------------
# TIME DOMAIN PLOT
# -----------------------------
plt.figure()
plt.plot(time, voltage)
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.title("Noise Signal (Time Domain)")
plt.grid()
plt.close()

# -----------------------------
# APPLY WINDOW (important for FFT)
# -----------------------------
window = np.hanning(N)
voltage_windowed = voltage * window

# -----------------------------
# FFT
# -----------------------------
fft_vals = np.fft.rfft(voltage_windowed) / N
freqs = np.fft.rfftfreq(N, dt)

# Power Spectral Density (optional but useful)
psd = np.abs(fft_vals)**2

# -----------------------------
# FFT PLOT
# -----------------------------
plt.figure()
plt.plot(freqs, psd)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power")
plt.title("FFT Spectrum (PSD)")
plt.grid()
plt.close()

# -----------------------------
# USER SELECTS TIME WINDOW
# -----------------------------

"""
cw = int(input("Choose time window? (0 = full, 1 = custom): "))

if cw == 0:
    selected_time = time
    selected_voltage = voltage
else:
    t_start = float(input("Enter start time: "))
    t_end = float(input("Enter end time: "))
    
    mask = (time >= t_start) & (time <= t_end)
    selected_time = time[mask]
    selected_voltage = voltage[mask]
"""
selected_time = time
selected_voltage = voltage

# Remove DC again in selected window
selected_voltage = selected_voltage - np.mean(selected_voltage)

# -----------------------------
# RMS VOLTAGE
# -----------------------------
Vrms = np.sqrt(np.mean(selected_voltage**2))
print("Vrms =", Vrms, "V")

# -----------------------------
# CONSTANTS
# -----------------------------
R1 = 1e3
Rf = 2.2e6
R = 2.2e6
T = 300

# Gain (IMPORTANT: change if needed)
# For inverting amplifier:
G = 1 + Rf / R1

# If non-inverting, use:
# G = 1 + (Rf / R1)

print("Gain =", G)

# -----------------------------
# BANDWIDTH
# -----------------------------
delta_f = fs / 2   # Nyquist bandwidth
print("Bandwidth (Hz) =", delta_f)

# -----------------------------
# BOLTZMANN CONSTANT
# -----------------------------
kB = (Vrms**2) / (4 * (G**2) * T * R * delta_f)

print("Estimated Boltzmann constant =", kB)

# -----------------------------
# SELECTED WINDOW PLOT
# -----------------------------
plt.figure()
plt.plot(selected_time, selected_voltage)
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.title("Selected Time Window")
plt.grid()
plt.close()
