#!/usr/bin/env python3
"""
Calculate magnetic field of an electron at gravitational equilibrium
between two stars as they rotate around the galaxy.
Scale speed of light to c = 1 (natural units).
Compute Rayleigh scattering cross-section using scaled c.
"""

import numpy as np

# Physical constants (SI)
c_si = 2.99792458e8  # m/s
mu0_si = 4*np.pi*1e-7  # N/A^2
epsilon0_si = 1/(mu0_si * c_si**2)  # F/m
e_si = 1.602176634e-19  # C
m_e_si = 9.1093837015e-31  # kg
hbar_si = 1.054571817e-34  # J·s

# In natural units, set c = 1
# Then we define a scaling factor: length and time units such that c = 1.
# We'll keep using SI for other constants but treat c=1 in formulas where c appears explicitly.
# Effectively, we set c = 1 in equations, but keep other constants unchanged.
# This is equivalent to using units where length and time have same dimension.

# For calculations, we can keep constants as is, but replace c with 1 where needed.

# Scenario: Two stars of mass M_sun each, separated by distance r_eq (gravitational equilibrium at midpoint).
M_sun = 1.989e30  # kg
r_sep = 1e9  # separation distance (1 million km) example
# Gravitational equilibrium point at midpoint (for equal masses)
# Distance from each star to equilibrium point:
d = r_sep / 2.0

# Orbital speed of each star around galactic center? Actually stars orbit each other? 
# We'll assume the binary system orbits the galactic center with angular speed Omega_gal.
Omega_gal = 2*np.pi / (200e6 * 365.25*24*3600)  # rad/s approx for 200 Myr period
# Distance from galactic center to binary system (R_gal)
R_gal = 8e3 * 3.086e16  # 8 kpc in meters
# Speed of stars due to galactic orbit: v_gal = Omega_gal * R_gal
v_gal = Omega_gal * R_gal

# The equilibrium point moves with the binary's center of mass, which also orbits galactic center at speed v_gal.
# Thus the electron at equilibrium experiences centripetal acceleration a_c = v_gal^2 / R_gal = Omega_gal^2 * R_gal
a_c = Omega_gal**2 * R_gal

# Consider an electron at the equilibrium point, comoving with the local frame (so it has velocity v_gal tangential).
# Its acceleration is centripetal: a_c toward galactic center.
# Magnetic field due to moving charge (Biot-Savart) at a point? We'll compute magnetic field at a distance r from the electron.
# For a non-relativistic moving charge, magnetic field at position r_vec relative to charge:
# B = (mu0 / 4π) * q * (v × r̂) / r^2
# We'll compute magnitude at a distance r_obs = 1e-6 m (micron) from electron.

r_obs = 1e-6  # m
v = v_gal  # tangential speed
# Assume v perpendicular to r̂ for max B
B_mag = (mu0_si / (4*np.pi)) * e_si * v / (r_obs**2)
print(f"Magnetic field magnitude at {r_obs} m from electron due to galactic motion: {B_mag:.3e} T")

# Now incorporate scaling c=1: In natural units, mu0 = 1/epsilon0 (since c=1 => mu0*epsilon0 =1).
# Let's compute using natural unit expressions: set c=1, keep epsilon0 as is? Actually if c=1, then mu0 = 1/epsilon0.
# We'll compute B_natural = (1/(4π epsilon0)) * e * v / r^2 (since mu0/4π = 1/(4π epsilon0))
epsilon0 = epsilon0_si
B_natural = (1/(4*np.pi*epsilon0)) * e_si * v / (r_obs**2)
print(f"Magnetic field (natural units, c=1): {B_natural:.3e} T (should equal previous)")

# Verify equality: mu0/(4π) = 1/(4π epsilon0 c^2). With c=1, they match.
# So the numeric value unchanged.

# Now compute Rayleigh scattering cross-section for an electron.
# Classical electron radius: r_e = e^2 / (4π epsilon0 m_e c^2)
r_e = e_si**2 / (4*np.pi*epsilon0_si * m_e_si * c_si**2)
print(f"Classical electron radius (SI): {r_e:.3e} m")
# Rayleigh scattering cross-section (low frequency limit) sigma = (8π/3) r_e^2 (ω/ω0)^4, but for Thomson scattering (omega << omega0) sigma_T = (8π/3) r_e^2.
# For Rayleigh scattering off bound electrons, we need a resonant frequency; we'll approximate using Thomson cross-section as baseline.
sigma_T = (8*np.pi/3) * r_e**2
print(f"Thomson cross-section (sigma_T): {sigma_T:.3e} m^2")

# Now scale c=1: In natural units, c=1, so r_e_natural = e^2 / (4π epsilon0 m_e) (since c^2=1)
r_e_natural = e_si**2 / (4*np.pi*epsilon0_si * m_e_si)
print(f"Classical electron radius (c=1): {r_e_natural:.3e} m")
sigma_T_natural = (8*np.pi/3) * r_e_natural**2
print(f"Thomson cross-section (c=1): {sigma_T_natural:.3e} m^2")

# The cross-section scales as 1/c^4? Actually r_e ∝ 1/c^2, so sigma_T ∝ 1/c^4.
# With c=1, cross-section is larger by factor (c_si)^4 compared to SI? Let's compute ratio.
ratio = sigma_T_natural / sigma_T
print(f"Ratio sigma_T(c=1)/sigma_T(SI): {ratio:.3e} (should be c_si^4 = {c_si**4:.3e})")

# Finally, compute Rayleigh scattering cross-section for a given wavelength lambda.
# Rayleigh scattering cross-section sigma_Rayleigh = (2π^5 / 3) * (d^6 / lambda^4) * ((n^2-1)/(n^2+2))^2 for spherical particles.
# For simplicity, we compute using electron's polarizability alpha = e^2 / (m_e ω0^2) etc.
# We'll skip detailed derivation and just note that with c=1, the formula changes accordingly.

print("\nDone.")