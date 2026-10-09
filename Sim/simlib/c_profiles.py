"""Local light-speed C(sigma) parameterizations.

Two forms exist in the paper and they disagree everywhere except sigma=1/2.
Research.md 4.4 flags this as an *unresolved* reparameterization. We expose
both so a run can declare which one it used and so a video/sweep can compare
them side by side.

Conventions:
    * C is reported as a dimensionless RATIO C = c_local / c_vacuum.
    * At the gravitational equilibrium sigma = 1/2 both forms give C = 1.
    * The FDTD solver works in SI; it multiplies the wave term by
      (C * c_si * dt / dx)^2. It never replaces c_si by 1.

Parameterizations
-----------------
P1  (Postulate, CoreEquations):      C^2 = sigma / (1 - sigma)
      Unbounded: C -> 0 as sigma -> 0, C -> inf as sigma -> 1. Physically
      problematic at the endpoints (infinite / zero light speed) but it is
      the theory's stated postulate.
BOUNDED (Research.md 4.4 / FDTD):    C   = 2 sqrt(sigma (1 - sigma))
      Bounded in [0,1], C = 1 at sigma = 1/2, C -> 0 at both endpoints.
      Numerically well-behaved; chosen for the FDTD for stability.

Both are normalized so C(1/2) = 1.
"""

from __future__ import annotations

import numpy as np

P1 = "P1"            # C^2 = sigma/(1-sigma)
BOUNDED = "bounded"  # C = 2 sqrt(sigma(1-sigma))

_NAMES = {P1: "C^2 = sigma/(1-sigma)  [Postulate P1, unbounded]",
          BOUNDED: "C = 2*sqrt(sigma*(1-sigma))  [bounded, FDTD]"}


def name(which: str) -> str:
    return _NAMES[which]


def c_of_sigma(sigma, which: str = BOUNDED):
    """Local light speed C(sigma) as a ratio to c_vacuum.

    Parameters
    ----------
    sigma : float or np.ndarray
        Space-energy fraction in [0, 1].
    which : str
        P1 or BOUNDED.

    Returns
    -------
    float or np.ndarray
        Dimensionless C. P1 is clipped near the singular endpoints to keep
        the FDTD stable; the clip value is reported by the caller.
    """
    s = np.asarray(sigma, dtype=float)
    # Keep interior to (0,1) to avoid 0/0 and division by zero.
    eps = 1e-12
    s = np.clip(s, eps, 1.0 - eps)
    if which == P1:
        c2 = s / (1.0 - s)
        # Clip the ratio to a finite value for numerics; the P1 tail is a
        # model-building open question, not a validated prediction.
        c2 = np.clip(c2, 1e-6, 1e6)
        return np.sqrt(c2)
    if which == BOUNDED:
        return 2.0 * np.sqrt(s * (1.0 - s))
    raise ValueError(f"unknown parameterization {which!r}; use {P1} or {BOUNDED}")


def describe(which: str) -> str:
    return _NAMES[which]


if __name__ == "__main__":
    grid = np.linspace(0.01, 0.99, 99)
    print("sigma   C(P1)        C(bounded)")
    for s in (0.05, 0.25, 0.5, 0.75, 0.95):
        print(f"{s:5.2f}  {c_of_sigma(s, P1):10.4e}  {c_of_sigma(s, BOUNDED):10.4f}")
    print()
    print("C range over grid [0.01,0.99]:")
    print(f"  P1      : {c_of_sigma(grid, P1).min():.3e} .. {c_of_sigma(grid, P1).max():.3e}")
    print(f"  bounded : {c_of_sigma(grid, BOUNDED).min():.3f} .. {c_of_sigma(grid, BOUNDED).max():.3f}")
