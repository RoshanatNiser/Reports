import numpy as np
from Func_lib import*


# for Ge
I=np.array([0.45,1.10,1.58,1.74,2.02,2.32,2.51,3.55,4.14,4.30,4.70])
V=np.array([193,250,280,301,326,351,395,463,520,534,568])
R_Ge= V/I



print(linear_fit_analysis(I,V,title="I-V graph of Germanium (W= 0.5mm)",xlab="Current (mA)",ylab="Voltage (mV)"))

# For Si
I=np.array([50,90,130,170,210,250,290,331,370])
V=np.array([6,10,15,20,25,29,34,39,44])

R_si=V/I



print(linear_fit_analysis(I,V,title="I-V graph of Silicon (W= 0.5mm)",xlab="Current (mA)",ylab="Voltage (mV)"))

# For Al
W=3e-3
I=np.array([198.5,178.8,158.2,135.4,115.2,94.2,78.2,68.5,61.1,43.5,23.5,14.5])
V=np.array([54,75,67,56,45,39,31,28,25,17,8,5])

R_Al=V/I



print(linear_fit_analysis(I,V,title="I-V graph of Aluminium Foil (W=0.3mm)",xlab="Current (mA)",ylab="Voltage (mV)"))
