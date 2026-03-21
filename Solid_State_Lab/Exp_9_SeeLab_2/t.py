import eyes17.eyes as eyes
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# CONNECT DEVICE
# -----------------------------
p = eyes.open()

# -----------------------------
# PARAMETERS
# -----------------------------
R = 160          # series resistor (Ohms)
T = 300          # temperature (Kelvin)
q = 1.602e-19    # electron charge

# voltage sweep
V_start = 0.05
V_end = 0.7
step = 0.01

# -----------------------------
# DATA STORAGE
# -----------------------------
V_diode = []
I_diode = []

# -----------------------------
# SWEEP VOLTAGE
# -----------------------------
V_values = np.arange(V_start, V_end, step)

print("Starting voltage sweep...")

for V in V_values:
    p.set_pv1(V)
    p.delay(0.05)

    Vd = p.get_voltage('A2')   # voltage across diode

    I = (V - Vd) / R           # current through diode

    # ignore invalid or negative values
    if I > 1e-9:
        V_diode.append(Vd)
        I_diode.append(I)

V_diode = np.array(V_diode)
I_diode = np.array(I_diode)

print("Data collection complete.")

# -----------------------------
# ANALYSIS
# -----------------------------
lnI = np.log(I_diode)

# linear fit
m, c = np.polyfit(V_diode, lnI, 1)

print("Slope (q/kT) =", m)

# -----------------------------
# CALCULATE k_B
# -----------------------------
kB = q / (m * T)

print("Estimated Boltzmann constant =", kB)

# -----------------------------
# PLOT I-V CURVE
# -----------------------------
plt.figure()
plt.plot(V_diode, I_diode, 'o-')
plt.xlabel("Voltage across diode (V)")
plt.ylabel("Current (A)")
plt.title("Diode I-V Curve")
plt.grid()
plt.show()

# -----------------------------
# PLOT ln(I) vs V
# -----------------------------
plt.figure()
plt.plot(V_diode, lnI, 'o', label="Data")
plt.plot(V_diode, m*V_diode + c, '-', label="Linear Fit")
plt.xlabel("Voltage (V)")
plt.ylabel("ln(Current)")
plt.title("ln(I) vs V")
plt.legend()
plt.grid()
plt.show()

# -----------------------------
# CLEANUP
# -----------------------------
p.set_pv1(0)
print("Experiment finished safely.")
