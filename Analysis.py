import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# ---------- Constants ----------
q = 1.602e-19
eps0 = 8.854e-12
eps_s = 11.7

# ---------- Load JSON ----------
with open("Data.json", "r") as f:
    data = json.load(f)

# ---------- Circuit parameters ----------
f = data["Frequency (in kHz)"] * 1e3
omega = 2*np.pi*f
R_f = data["R_F (in Kilo ohms"] * 1e3
C_f = data["C_F (in nF)"] * 1e-9

factor = np.sqrt(1 + 1/(omega*R_f*C_f)**2)

# ---------- Function to compute capacitance ----------
def compute_capacitance(Vdut, Vout_mv):

    Vdut = np.array(Vdut)
    Vout = np.array(Vout_mv) * 1e-3  # convert mV → V

    C = (Vout / np.abs(Vdut)) * C_f * factor

    return C.tolist()


# ---------- Compute C_DUT and store in JSON ----------

dark = data["For Dark (No light)"]
amb = data["For Ambient light"]
red = data["With Red Filter"]

if len(dark["C_DUT"]) == 0:
    dark["C_DUT"].extend(
        compute_capacitance(
            dark["V_DUT(in Volts)"],
            dark["V_out(in milliVolts)"]
        )
    )

if len(amb["C_DUT"]) == 0:
    amb["C_DUT"].extend(
        compute_capacitance(
            amb["V_DUT(in Volts)"],
            amb["V_out(in milliVolts)"]
        )
    )

if len(red["C_DUT"]) == 0:
    red["C_DUT"].extend(
        compute_capacitance(
            red["V_DUT(in Volts)"],
            red["V_OUT(in milliVolts)"]
        )
    )

# ---------- Save JSON ----------
with open("Data.json", "w") as f:
    json.dump(data, f, indent=4)

print("C_DUT added to Data.json")

# ---------- Extract arrays for analysis ----------

Vdc_dark = np.array(dark["V_DC(in Volts)"])
C_dark = np.array(dark["C_DUT"])
invC2_dark = 1/(C_dark**2)

Vdc_amb = np.array(amb["V_DC(in Volts)"])
C_amb = np.array(amb["C_DUT"])
invC2_amb = 1/(C_amb**2)

Vdc_red = np.array(red["V_DC(in Volts)"])
C_red = np.array(red["C_DUT"])
invC2_red = 1/(C_red**2)

# ---------- Plot C-V ----------
plt.figure(figsize=(7,5))

plt.plot(Vdc_dark, C_dark*1e12, 'o-', label='Dark')
plt.plot(Vdc_amb, C_amb*1e12, 'o-', label='Ambient')
plt.plot(Vdc_red, C_red*1e12, 'o-', label='Red filter')

plt.xlabel("Reverse Bias Voltage V_DC (V)")
plt.ylabel("Capacitance (pF)")
plt.title("C-V Characteristics of Solar Cell")
plt.legend()
plt.grid()

plt.savefig("CV_characteristics.png", dpi=300, bbox_inches='tight')
plt.show()

# ---------- Plot 1/C² ----------
plt.figure(figsize=(7,5))

plt.plot(Vdc_dark, invC2_dark, 'o-', label='Dark')
plt.plot(Vdc_amb, invC2_amb, 'o-', label='Ambient')
plt.plot(Vdc_red, invC2_red, 'o-', label='Red filter')

plt.xlabel("Reverse Bias Voltage V_DC (V)")
plt.ylabel("1 / C²")
plt.title("1/C² vs V_DC")
plt.legend()
plt.grid()

plt.savefig("inverseC2_vs_V.png", dpi=300, bbox_inches='tight')
plt.show()

# ---------- Linear fit (Dark data) ----------

slope, intercept, r, p, std = linregress(Vdc_dark, invC2_dark)

Vbi = -intercept/slope

print("Built-in potential V_bi =", Vbi, "Volts")
print("Linear fit R² =", r**2)

# ---------- Doping density ----------
A = 1e-4  # solar cell area (m²)

Nd = 2/(q*eps0*eps_s*A*A*slope)

print("Doping density Nd =", Nd, "m^-3")