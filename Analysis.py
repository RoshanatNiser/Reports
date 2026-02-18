import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# -------------------------
# GIVEN DATA
# -------------------------
theta_deg_brass = np.array([30,45,60,90,120])
Area_brass = np.array([1115.0,915.0,799.0,662.0,446.0])

theta_deg_al = np.array([45,60,90,120])  # removed 30° outlier
Area_al = np.array([743.0,600.0,481.0,413.0])

E0 = 662
me = 511

theta_rad_brass = np.deg2rad(theta_deg_brass)
theta_rad_al = np.deg2rad(theta_deg_al)

# -------------------------
# Klein-Nishina function
# -------------------------
def klein_nishina(theta):
    E_prime = E0/(1 + (E0/me)*(1-np.cos(theta)))
    return (E_prime/E0)**2 * (E_prime/E0 + E0/E_prime - np.sin(theta)**2)

# Model with scale factor
def model(theta, C):
    return C * klein_nishina(theta)

# -------------------------
# FIT BRASS
# -------------------------
popt_brass, pcov_brass = curve_fit(model, theta_rad_brass, Area_brass)
C_brass = popt_brass[0]

fit_brass = model(theta_rad_brass, C_brass)

# R^2
ss_res = np.sum((Area_brass - fit_brass)**2)
ss_tot = np.sum((Area_brass - np.mean(Area_brass))**2)
R2_brass = 1 - ss_res/ss_tot

# Chi-square (Poisson errors)
sigma_brass = np.sqrt(Area_brass)
chi2_brass = np.sum(((Area_brass - fit_brass)/sigma_brass)**2)

# -------------------------
# FIT ALUMINIUM
# -------------------------
popt_al, pcov_al = curve_fit(model, theta_rad_al, Area_al)
C_al = popt_al[0]

fit_al = model(theta_rad_al, C_al)

ss_res_al = np.sum((Area_al - fit_al)**2)
ss_tot_al = np.sum((Area_al - np.mean(Area_al))**2)
R2_al = 1 - ss_res_al/ss_tot_al

sigma_al = np.sqrt(Area_al)
chi2_al = np.sum(((Area_al - fit_al)/sigma_al)**2)

# -------------------------
# PRINT RESULTS
# -------------------------
print("Brass:")
print("Scale factor C =", C_brass)
print("R^2 =", R2_brass)
print("Chi^2 =", chi2_brass)

print("\nAluminium:")
print("Scale factor C =", C_al)
print("R^2 =", R2_al)
print("Chi^2 =", chi2_al)

# -------------------------
# Plot
# -------------------------
theta_plot = np.linspace(20,130,200)
theta_plot_rad = np.deg2rad(theta_plot)

plt.figure()
plt.scatter(theta_deg_brass, Area_brass, label="Brass Data")
plt.plot(theta_plot, model(theta_plot_rad, C_brass), label="KN Fit")
plt.xlabel("Theta (deg)")
plt.ylabel("Intensity (Area)")
plt.legend()
plt.title("Brass Fit")
plt.savefig("Brass Fit.png")
plt.close()

plt.figure()
plt.scatter(theta_deg_al, Area_al, label="Al Data")
plt.plot(theta_plot, model(theta_plot_rad, C_al), label="KN Fit")
plt.xlabel("Theta (deg)")
plt.ylabel("Intensity (Area)")
plt.legend()
plt.title("Aluminium Fit")
plt.savefig("Aluminium Fit.png")
plt.close()
