Below is a **report-ready Introduction and Theory section**, written in formal lab-report style and aligned with your supplied manual .

---

# **Introduction**

Compton scattering is a fundamental example of the inelastic scattering of electromagnetic radiation by charged particles, in which the wavelength (and hence energy) of the scattered photon differs from that of the incident photon . In 1920, Arthur Holly Compton observed that X-rays scattered from electrons in a carbon target exhibited a measurable increase in wavelength that depended explicitly on the scattering angle. This phenomenon could not be explained using classical wave theory and provided direct evidence for the particle nature of light.

The wavelength shift observed in Compton scattering is given by the Compton relation:

[
\Delta \lambda = \lambda' - \lambda = \frac{h}{m_e c}(1 - \cos\theta)
]

where ( \lambda ) and ( \lambda' ) are the wavelengths of the incident and scattered photons respectively, ( h ) is Planck’s constant, ( m_e ) is the electron rest mass, ( c ) is the speed of light, and ( \theta ) is the photon scattering angle . The quantity

[
\lambda_C = \frac{h}{m_e c} = 0.02426 , \text{Å}
]

is known as the Compton wavelength of the electron.

In the present experiment, monoenergetic gamma rays of energy 662 keV from a (^{137})Cs source are scattered by electrons in an aluminium target. The energy of the scattered photons is measured using a calibrated NaI scintillation detector coupled to a multichannel analyzer (MCA). By studying the energy shift as a function of scattering angle, the Compton formula is experimentally verified. Additionally, the angular dependence of scattering intensity is compared with the Klein–Nishina theoretical prediction for the differential cross-section.

This experiment therefore provides experimental verification of photon momentum, relativistic energy–momentum conservation, and the quantum mechanical description of photon–electron interactions.

---

# **Theory**

## 1. Energy–Momentum Conservation in Compton Scattering

Compton scattering is treated as a relativistic two-body collision between a photon and a free electron initially at rest. Applying conservation of energy:

[
E + m_e c^2 = E' + \sqrt{(p_e c)^2 + (m_e c^2)^2}
]

and conservation of momentum (vector form), one obtains after simplification the Compton wavelength shift relation:

[
\Delta \lambda = \frac{h}{m_e c}(1 - \cos\theta)
]

Expressing the relation in terms of photon energy using ( E = \frac{hc}{\lambda} ), the scattered photon energy ( E_\theta ) is given by :

[
E_\theta = \frac{E_0}{1 + \frac{E_0}{m_e c^2}(1 - \cos\theta)}
]

where
( E_0 ) = incident photon energy,
( E_\theta ) = scattered photon energy at angle ( \theta ),
( m_e c^2 = 511 , \text{keV} ).

For high photon energies (( E_0 \gg 511 , \text{keV} )), the energy shift is significant and relativistic effects dominate. For low photon energies (( E_0 \ll 511 , \text{keV} )), the shift becomes negligible and the result approaches classical Thomson scattering .

---

## 2. Differential Scattering Cross Section (Klein–Nishina Formula)

The quantum mechanical treatment of Compton scattering was developed by Klein and Nishina (1928). The differential cross-section averaged over photon polarizations is given by :

[
\frac{d\sigma}{d\Omega} = \frac{r_0^2}{2}
\left(\frac{E'}{E}\right)^2
\left(
\frac{E'}{E} + \frac{E}{E'} - \sin^2\theta
\right)
]

where

* ( r_0 = \frac{e^2}{4\pi\varepsilon_0 m_e c^2} ) is the classical electron radius
* ( r_0 = 2.818 \times 10^{-15} , \text{m} ) 
* ( \theta ) is the photon scattering angle

This expression predicts the angular distribution of scattered photons and incorporates relativistic and quantum mechanical effects. Integration over all solid angles gives the total Compton cross-section.

---

## 3. Experimental Determination

In this experiment:

1. **Energy Calibration:**
   The MCA channels are calibrated using known gamma-ray peaks from a mixed source (Am-241 and Cs-137) .

2. **Measurement of Scattered Energy:**
   For each scattering angle ( \theta ), the energy spectrum is recorded. The difference between spectra with and without the scatterer is used to determine the peak scattered energy ( E_\theta ) .

3. **Differential Cross-Section and Calibration Factor:**
   The relative intensity of the Compton peak is compared with the theoretical Klein–Nishina prediction. A calibration factor ( C ) is determined to relate measured counts to theoretical cross-section values .

---





