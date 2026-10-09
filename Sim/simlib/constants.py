"""Physical constants (SI) and the Gradient Relativity galactic/binary scenario.

Unit discipline:
    All quantities here are SI. The FDTD solver works in the *same* SI
    meters/seconds; it never substitutes 1 for c inside a formula. Where a
    quantity is dimensionless (a speed ratio C = c_local / c_vacuum) it is
    reported as a ratio, not by overwriting c_si with 1.

The scenario follows Research.md 4.1-4.2:
    two equal solar-mass stars, a binary that co-orbits the galactic center
    with angular speed Omega_G, and an electron pinned at the gravitational
    equilibrium point between the stars. That point undergoes centripetal
    acceleration a_c = Omega_G^2 R_G.
"""

from __future__ import annotations

import math

# ---------------------------------------------------------------------------
# Fundamental constants (CODATA, SI)
# ---------------------------------------------------------------------------
C_SI = 2.99792458e8            # vacuum speed of light, m/s (exact)
MU0 = 4.0e-7 * math.pi         # vacuum permeability, N/A^2 (exact)
EPS0 = 1.0 / (MU0 * C_SI**2)   # vacuum permittivity, F/m
HBAR = 1.054571817e-34         # reduced Planck constant, J s
H_PLANCK = 2.0 * math.pi * HBAR
G_NEWTON = 6.67430e-11         # gravitational constant, m^3 kg^-1 s^-2
E_CHARGE = 1.602176634e-19     # elementary charge, C (exact)
M_E = 9.1093837015e-31         # electron mass, kg

# ---------------------------------------------------------------------------
# Electron characteristic scales
# ---------------------------------------------------------------------------
OMEGA0 = M_E * C_SI**2 / HBAR          # Compton angular frequency, rad/s (~7.76e20)
LAMBDA_C = HBAR / (M_E * C_SI)         # reduced Compton wavelength, m (~2.426e-12)
R_E_CLASSICAL = E_CHARGE**2 / (4.0 * math.pi * EPS0 * M_E * C_SI**2)
# classical electron radius, m (~2.818e-15)
# NOTE: do NOT compute "r_e in natural units" by dropping c_si; that yields
# ~8 m (28 orders off). If you need a natural-unit radius, convert the whole
# system (length AND time AND charge) consistently.

# ---------------------------------------------------------------------------
# Galactic / binary scenario (Research.md 4.1, 4.2)
# ---------------------------------------------------------------------------
M_SUN = 1.989e30                    # kg, solar mass
M1 = M_SUN
M2 = M_SUN
R_SEP = 1.0e10                      # m, binary separation (example scale)
# Gravitational equilibrium distance from M1 (Research.md 4.1):
D1 = R_SEP / (1.0 + math.sqrt(M2 / M1))
# Galactic rotation: 200 Myr period at galactocentric radius R_G:
GALACTIC_PERIOD_S = 200.0e6 * 365.25 * 24 * 3600.0
OMEGA_G = 2.0 * math.pi / GALACTIC_PERIOD_S   # rad/s (~9.96e-16)
R_G = 8.0e3 * 3.086e16                # m, 8 kpc in meters (~2.469e20)
A_C = OMEGA_G**2 * R_G                # m/s^2, centripetal acceleration (~2.45e-10)
V_GAL = OMEGA_G * R_G                 # m/s, galactic orbital speed (~2.46e5)

# ---------------------------------------------------------------------------
# Derived diagnostic quantities (SI, reported verbatim -- never rescaled)
# ---------------------------------------------------------------------------
def larmor_power_si(a: float = A_C) -> float:
    """Larmor radiated power P = q^2 a^2 / (6 pi eps0 c^3), SI watts.

    Computed entirely in SI. No c=1 substitution.
    """
    return E_CHARGE**2 * a**2 / (6.0 * math.pi * EPS0 * C_SI**3)


def driven_amplitude_si(a: float = A_C, omega0: float = OMEGA0) -> float:
    """Particular (driven) oscillator amplitude x_p = a_c / omega0^2, meters."""
    return a / omega0**2


def feedback_ratio(a: float = A_C, omega0: float = OMEGA0) -> float:
    """Feedback energy per galactic orbit / electron rest energy.

    E_feedback = P_larmor * T_galactic ; rest energy = m_e c^2.
    This is the honesty number: at galactic a_c it is ~2.6e-44, i.e. the
    Larmor feedback is utterly negligible. The whirlpool is an *ansatz*,
    not something the galactic acceleration drives at Compton frequency.
    """
    p = larmor_power_si(a)
    t_gal = 2.0 * math.pi / OMEGA_G
    return p * t_gal / (M_E * C_SI**2)


if __name__ == "__main__":
    # Self-check: print the scenario with independent magnitude sanity checks.
    print("Scenario (SI):")
    print(f"  d1        = {D1:.4e} m   (expect ~{0.5*R_SEP:.3e} m for equal masses)")
    print(f"  Omega_G   = {OMEGA_G:.4e} rad/s")
    print(f"  R_G       = {R_G:.4e} m")
    print(f"  a_c       = {A_C:.4e} m/s^2   (expect ~Omega_G^2 R_G)")
    print(f"  v_gal     = {V_GAL:.4e} m/s")
    print(f"  omega0    = {OMEGA0:.4e} rad/s  (Compton)")
    print(f"  lambda_C  = {LAMBDA_C:.4e} m   (expect ~2.426e-12)")
    print(f"  r_e       = {R_E_CLASSICAL:.4e} m  (expect ~2.818e-15)")
    print(f"  x_p       = {driven_amplitude_si():.4e} m")
    print(f"  P_larmor  = {larmor_power_si():.4e} W")
    print(f"  feedback  = {feedback_ratio():.4e}  (honesty number; expect ~2.6e-44)")
