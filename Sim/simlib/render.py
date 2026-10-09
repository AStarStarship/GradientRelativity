"""Rendering: write a JSON bundle for the Flash player + optional PNG stills.

The Flash player (Web/index.html) is a plain-JS canvas that reads
Web/sim_bundle.json and animates the field. This module produces that
bundle deterministically from a FDTD run + validation report.

Outputs (all under Sim/ unless a target dir is given):
    sim_bundle.json   -- frames (normalized), electron track, validation
    fdtd_final_frame.png  -- matplotlib snapshot (if matplotlib available)
    fdtd_source_track.png -- field sampled along the orbit (if available)

The JSON bundle is the source of truth for the browser; the PNGs are
convenience stills for the paper.
"""

from __future__ import annotations

import json
import math
import os

import numpy as np

from . import constants, validation


def _normalize(phi):
    """Normalize a field frame to [0,1] for 8-bit visualization."""
    lo, hi = float(phi.min()), float(phi.max())
    if hi - lo < 1e-300:
        return np.zeros_like(phi)
    return (phi - lo) / (hi - lo)


def make_bundle(run, sol, c_form, report, max_frames=64, max_dim=160):
    """Downsample frames to a browser-friendly size and build the bundle.

    Frames are capped at max_frames and the grid at max_dim so the JSON
    stays small (<~2MB) and the canvas animates smoothly at 30fps.
    """
    frames = run["frames"]
    # Downsample in time: pick evenly spaced frames.
    n_avail = len(frames)
    if n_avail > max_frames:
        idx = np.linspace(0, n_avail - 1, max_frames).astype(int)
        frames = [frames[i] for i in idx]

    # Downsample in space if the grid is large.
    n = sol.n
    if n > max_dim:
        factor = n // max_dim + 1
        frames = [f[::factor, ::factor] for f in frames]

    norm = [_normalize(f) for f in frames]
    # Flatten each frame to a 1-D array (row-major) so the JS canvas can
    # index it directly. A 2-D nested list would make the JS loop only
    # write the first row (a known bug: frame.length == rows, not pixels).
    norm = [f.ravel().tolist() for f in norm]
    # Grid dimension AFTER any spatial downsampling (the player sizes to this).
    grid_dim = int(np.sqrt(len(norm[0])))

    # Electron track, resampled to the same length as frames.
    x_e = run["x_e"]
    y_e = run["y_e"]
    m = len(norm)
    if len(x_e) >= m:
        idx_e = np.linspace(0, len(x_e) - 1, m).astype(int)
        x_e = x_e[idx_e]
        y_e = y_e[idx_e]

    # C(sigma) profile for the C-form comparison chart (downsampled).
    cc = report["c_form_comparison"]
    sigma = np.asarray(cc["sigma"], dtype=float)
    step = max(1, len(sigma) // 48)
    cc_small = {
        "sigma": sigma[::step].tolist(),
        "C_P1": np.asarray(cc["C_P1"], dtype=float)[::step].tolist(),
        "C_bounded": np.asarray(cc["C_bounded"], dtype=float)[::step].tolist(),
        "P1_name": cc["P1_name"],
        "bounded_name": cc["bounded_name"],
        "note": cc["note"],
        "verdict": cc.get("verdict", "INFO"),
    }

    bundle = {
        "meta": {
            "version": "0.1",
            "c_form": c_form,
            "n_grid": int(grid_dim),
            "n_frames": int(m),
            "L_m": float(run["L"]),
            "lambda_C_m": float(constants.LAMBDA_C),
            "dt_s": float(run["dt"]),
            "cfl": float(run["cfl"]),
            "C_range": run["C_range"],
            "source_strength": float(run["source_strength"]),
        },
        "frames": norm,  # already flat 1-D lists (row-major), see above
        "electron": {
            "x_m": x_e.tolist(),
            "y_m": y_e.tolist(),
        },
        "validation": {
            "manufactured_solution": report["manufactured_solution"],
            "complex_known_case": report.get("complex_known_case", {}),
            "feedback_budget": report["feedback_budget"],
            "c_form_comparison": cc_small,
        },
        "constants": {
            "a_c_m_s2": float(constants.A_C),
            "P_larmor_W": float(constants.larmor_power_si()),
            "omega0_rad_s": float(constants.OMEGA0),
            "lambda_C_m": float(constants.LAMBDA_C),
            "feedback_ratio": float(constants.feedback_ratio()),
            "x_p_m": float(constants.driven_amplitude_si()),
        },
    }
    return bundle


def write_bundle(bundle, path):
    """Write the JSON bundle. Records its own sha256 in meta; returns bytes + digest."""
    data = json.dumps(bundle)
    import hashlib
    digest = hashlib.sha256(data.encode()).hexdigest()
    bundle["meta"]["sha256"] = digest
    data = json.dumps(bundle)
    with open(path, "w") as f:
        f.write(data)
    return len(data.encode()), digest


def render_pngs(run, sol, outdir):
    """matplotlib stills (final frame + orbit track). Returns list of paths."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    paths = []
    L = sol.L
    # Final frame.
    frame = _normalize(run["phi_final"])
    fig, ax = plt.subplots(figsize=(8, 8))
    im = ax.imshow(frame, origin="lower", cmap="magma",
                   extent=[-L/2, L/2, -L/2, L/2])
    ax.plot(run["x_e"][-1], run["y_e"][-1], "co", ms=8, label="electron (final)")
    if len(run["x_e"]) > 50:
        ax.plot(run["x_e"][-200:], run["y_e"][-200:], "c-", alpha=0.5, lw=0.8)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title(f"Planck field $\\phi$ — {sol.c_form} C-form, CFL={run['cfl']:.3f}")
    ax.legend(loc="upper right")
    fig.colorbar(im, ax=ax, label="normalized $\\phi$")
    fig.tight_layout()
    p1 = os.path.join(outdir, "fdtd_final_frame.png")
    fig.savefig(p1, dpi=120)
    plt.close(fig)
    paths.append(p1)

    # Orbit track: field sampled along the orbit path over time.
    mid = int(run["phi_final"].shape[0] / 2)
    track = []
    for f in run["frames"]:
        # sample the row through the grid center at the electron's x index
        xi = int(round((run["x_e"][len(track)] / sol.dx) + run["phi_final"].shape[0] / 2))
        track.append(f[mid, min(max(xi, 0), f.shape[1]-1)] if f.ndim == 2 else 0.0)
    t_norm = run["t"] / (constants.LAMBDA_C / constants.C_SI)
    fig2, ax2 = plt.subplots(figsize=(9, 4))
    ax2.plot(t_norm, track, lw=0.8)
    ax2.set_xlabel("t / (lambda_C / c)")
    ax2.set_ylabel("field amplitude along orbit (mid-row)")
    ax2.set_title("Field history sampled along the electron orbit")
    fig2.tight_layout()
    p2 = os.path.join(outdir, "fdtd_source_track.png")
    fig2.savefig(p2, dpi=120)
    plt.close(fig2)
    paths.append(p2)
    return paths
