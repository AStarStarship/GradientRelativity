"""Validation for the Gradient Relativity FDTD pipeline.

Three independent checks, each with a pass/fail verdict:

1. manufactured_solution -- a constant-amplitude traveling plane wave in a
   uniform-C domain should propagate without distortion over a few periods.
   This tests the *numerics* (leapfrog + CFL), not the physics.

2. feedback_budget -- the honest energy budget: Larmor power at galactic
   a_c times one galactic orbit, divided by the electron rest energy.
   Expect ~2.6e-44. This is the number the video confronts: the galactic
   acceleration does NOT drive the whirlpool at Compton frequency.

3. c_form_comparison -- the two C(sigma) parameterizations (P1 vs bounded)
   side by side, over sigma in (0,1). This is the unresolved
   reparameterization flagged in Research.md 4.4.

Each check returns a dict with "verdict" in {"PASS","PARTIAL","FAIL","INFO"}.
"""

from __future__ import annotations

import math

import numpy as np

from . import c_profiles, constants
from .fdtd import FDTDSolver, complex_known_case


def manufactured_solution(n=64, periods=4.0, c_form="bounded"):
    """Plane-wave propagation in a uniform-C domain.

    In a uniform domain with C = 1, the leapfrog scheme propagates a
    cos(k x - omega t) wave. We set up a pure +x traveling wave and measure
    the L2 error against the exact solution after `periods` cycles at a
    fixed point. The exact amplitude must be preserved (no dispersion growth
    within tolerance).
    """
    L = 8.0 * constants.LAMBDA_C
    # Uniform C=1: set sigma so C=1 -> bounded gives C=1 at sigma=1/2.
    # Force the whole grid to sigma=1/2 (uniform) for the numerics test.
    sol = FDTDSolver(n=n, L=L, c_form=c_form, n_steps=400,
                     t_end=periods * constants.LAMBDA_C / constants.C_SI)
    sol.sigma = np.full_like(sol.xx, 0.5)
    sol.C = np.full_like(sol.xx, 1.0)  # C = 1 everywhere
    sol.k = (sol.C * constants.C_SI * sol.dt / sol.dx) ** 2
    sol.cfl = float(sol.C.max()) * constants.C_SI * sol.dt / sol.dx

    # Traveling wave: phi(x,t) = cos(2 pi (x/L) - 2 pi (t / T0)), T0 = L/c.
    T0 = L / constants.C_SI
    k = 2.0 * np.pi / L

    def exact(x, t):
        return np.cos(k * x - 2.0 * math.pi * t / T0)

    x = sol.x
    t_hist = np.empty(400)
    x_hist = np.zeros(400)
    y_hist = np.zeros(400)
    phase0 = 0.0
    vis_step = 2.0 * np.pi / 100.0
    # Override electron_state to return a fixed source (we want a pure wave,
    # so zero source after the initial condition).
    # Simplest: initialize phi to the wave at t=0 and run with source_strength=0.
    sol.source_strength = 0.0
    phi0 = exact(x, 0.0)
    # phi depends on (x,y) but our wave is x-only; broadcast along y.
    phi_init, _ = np.meshgrid(phi0, phi0, indexing="xy")
    sol.phi = phi_init.copy()
    sol.phi_prev = exact(x, -sol.dt)
    phi_prev_b, _ = np.meshgrid(exact(x, -sol.dt), exact(x, -sol.dt), indexing="xy")
    sol.phi_prev = phi_prev_b.copy()

    # Manually step (bypass run() which re-initializes).
    phi = sol.phi.copy()
    phi_prev = sol.phi_prev.copy()
    err_hist = []
    for step in range(400):
        t = step * sol.dt
        lap = (
            np.roll(phi, -1, axis=0) + np.roll(phi, 1, axis=0)
            + np.roll(phi, -1, axis=1) + np.roll(phi, 1, axis=1)
            - 4.0 * phi
        )
        phi_new = 2.0 * phi - phi_prev + sol.k * lap
        phi_prev, phi = phi, phi_new
        if step % 40 == 0:
            ex, _ = np.meshgrid(exact(x, t), exact(x, t), indexing="xy")
            err = np.sqrt(np.mean((phi - ex) ** 2))
            err_hist.append(err)

    err = np.array(err_hist)
    # Tolerance: L2 error < 5% of amplitude (amplitude = 1) over 4 periods.
    passed = bool(err.max() < 0.05)
    return {
        "check": "manufactured_solution",
        "c_form": c_form,
        "cfl": sol.cfl,
        "periods": periods,
        "error_l2_by_time": err.tolist(),
        "error_max": float(err.max()),
        "tolerance": 0.05,
        "verdict": "PASS" if passed else "FAIL",
        "note": ("Plane wave propagates with <5% L2 error over "
                 f"{periods} periods; CFL={sol.cfl:.3f} (stable if <0.707)."),
    }


def feedback_budget():
    """Honest energy budget (the number the video confronts)."""
    p = constants.larmor_power_si()
    t_gal = 2.0 * np.pi / constants.OMEGA_G
    ratio = constants.feedback_ratio()
    return {
        "check": "feedback_budget",
        "P_larmor_W": p,
        "T_galactic_s": t_gal,
        "E_feedback_per_orbit_J": p * t_gal,
        "electron_rest_energy_J": constants.M_E * constants.C_SI ** 2,
        "feedback_ratio": float(ratio),
        "verdict": "INFO",
        "note": (
            "Larmor feedback at galactic a_c is "
            f"{ratio:.2e} of the electron rest energy per galactic orbit. "
            "The galactic acceleration does NOT drive the whirlpool at "
            "Compton frequency. The whirlpool is an ansatz the sim "
            "illustrates, not a derived consequence of the galactic term. "
            "This is the honest open problem the video must state."
        ),
    }


def c_form_comparison(sigma_grid=None):
    """Side-by-side C(sigma) for the two parameterizations."""
    if sigma_grid is None:
        sigma_grid = np.linspace(0.02, 0.98, 97)
    c_p1 = c_profiles.c_of_sigma(sigma_grid, c_profiles.P1)
    c_b = c_profiles.c_of_sigma(sigma_grid, c_profiles.BOUNDED)
    return {
        "check": "c_form_comparison",
        "sigma": sigma_grid.tolist(),
        "C_P1": c_p1.tolist(),
        "C_bounded": c_b.tolist(),
        "P1_name": c_profiles.name(c_profiles.P1),
        "bounded_name": c_profiles.name(c_profiles.BOUNDED),
        "verdict": "INFO",
        "note": (
            "Research.md 4.4 flags two C(sigma) forms that agree only at "
            "sigma=1/2 (C=1). P1 (Postulate) is unbounded; bounded is the "
            "FDTD choice. A video/sweep should show both and label which "
            "form produced a given result."
        ),
    }


def run_all(c_form="bounded"):
    """Run every validation check and return a combined report."""
    report = {
        "c_form_used": c_form,
        "manufactured_solution": manufactured_solution(c_form=c_form),
        "complex_known_case": complex_known_case(c_form=c_form),
        "feedback_budget": feedback_budget(),
        "c_form_comparison": c_form_comparison(),
    }
    return report
