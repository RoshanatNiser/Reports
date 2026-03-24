import numpy as np
from Func_lib import *

# For Germanium (out> EV1 or EV2> SV2)

print("\n"," For Germanium: \n")
t=[]
for i in range(80,185,5):
    t.append(i)

T=np.array(t)
V=np.array([0.228,0.195,0.166,0.142,0.120,0.102,0.092,0.079,0.068,0.060,0.053,0.048,0.040,0.036,0.031,0.028,0.025,0.022,0.020,0.018,0.016])

T_in= ((273.15 + T)**-1)

print("T^-1 : ", T_in,"\n")

I= 5.8e-3
S= 0.2e-2
W= 0.5e-3

G=2*S*(np.log(2))*(1/W)

rho=V/(I*G)

print("Rho : ", rho,"\n")

ln_rho=np.log(rho)

print("ln(rho) : ", ln_rho,"\n")

R_1= linear_fit_analysis(x=T_in, y=ln_rho,title="Temperature dependence of Resistivity for Germanium",xlab="T^-1",ylab="ln(rho)")

k_B= 1.380649 * 10**-23
E_g_1=(2*k_B) * R_1['slope']
err_1= (2*k_B) *R_1['slope_err']

print("Band Gap for Germanium: ",E_g_1, "\u00B1", err_1,"J\n")

# For Aluminium

print("\n"," For Aluminium: \n")


t=[]
for i in range(45,85,5):
    t.append(i)

T=np.array(t)
V=np.array([0.005,0.009,0.010,0.011,0.014,0.015,0.015,0.017])

T_in= ((273.15 + T)**-1)

print("T^-1 : ", T_in,"\n")

I= 100.7e-3
S= 1e-3
W= 0.5e-3

G=2*S*(np.log(2))*(1/W)

rho=V/(I*G)

print("Rho : ", rho,"\n")


ln_rho=np.log(rho)

print("ln(rho) : ", ln_rho,"\n")

R2= linear_fit_analysis(x=T_in, y=ln_rho,title="Temperature dependence of Resistivity for Aluminium",xlab="T^-1",ylab="ln(rho)")

R_sq_2=R2['R_squared']

print("R^2 for Aluminium  : ", R_sq_2)

