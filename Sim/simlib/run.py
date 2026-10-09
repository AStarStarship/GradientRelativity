"""One-command end-to-end runner for the Gradient Relativity sim.

Usage:
    python -m sim.run --c-form bounded --n 160 --steps 400
    python -m sim.run --c-form P1 --n 128 --steps 300 --frames 48

Outputs (under Sim/ by default):
    Web/sim_bundle.json     -- field frames + validation for the Flash player
    fdtd_final_frame.png    -- matplotlib snapshot (if available)
    fdtd_source_track.png   -- orbit-track history (if available)
    run_report.json         -- full validation report + provenance

This is the reproducible artifact: same flags -> same bundle (deterministic).
"""

from __future__ import annotations

import argparse
import json
import os

import numpy as np

from . import c_profiles, constants, fdtd, render, validation

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # Sim/
WEB = os.path.join(ROOT, "Web")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Gradient Relativity FDTD runner")
    ap.add_argument("--c-form", default="bounded",
                    choices=["bounded", "P1"],
                    help="C(sigma) parameterization (declared in the bundle).")
    ap.add_argument("--n", type=int, default=128, help="grid cells per side")
    ap.add_argument("--steps", type=int, default=600, help="leapfrog steps")
    ap.add_argument("--t-end", type=float, default=None,
                    help="physical end time in seconds (default: CFL-stable "
                         "window for --steps). If set, dt=t_end/steps; the "
                         "run FAILS CLOSED if that dt is CFL-unstable.")
    ap.add_argument("--frames", type=int, default=48,
                    help="max frames in the browser bundle")
    ap.add_argument("--outdir", default=ROOT, help="output directory")
    ap.add_argument("--no-png", action="store_true",
                    help="skip matplotlib stills (JSON only)")
    args = ap.parse_args(argv)

    # ------------------------------------------------------------------
    # 1. Run the FDTD solver (fails closed if CFL-unstable).
    # ------------------------------------------------------------------
    result, sol = fdtd.default_run(c_form=args.c_form, n=args.n,
                                   n_steps=args.steps, t_end=args.t_end)

    # ------------------------------------------------------------------
    # 2. Validate (manufactured wave, feedback budget, C-form comparison).
    # ------------------------------------------------------------------
    report = validation.run_all(c_form=args.c_form)

    # ------------------------------------------------------------------
    # 3. Build + write the JSON bundle for the Flash player.
    # ------------------------------------------------------------------
    os.makedirs(WEB, exist_ok=True)
    bundle = render.make_bundle(result, sol, args.c_form, report,
                                max_frames=args.frames)
    bundle_path = os.path.join(WEB, "sim_bundle.json")
    nbytes, digest = render.write_bundle(bundle, bundle_path)

    # ------------------------------------------------------------------
    # 4. Optional PNG stills.
    # ------------------------------------------------------------------
    png_paths = []
    if not args.no_png:
        try:
            png_paths = render.render_pngs(result, sol, args.outdir)
        except ImportError:
            print("matplotlib not installed -- skipping PNG stills.")

    # ------------------------------------------------------------------
    # 5. Provenance + report.
    # ------------------------------------------------------------------
    provenance = {
        "c_form": args.c_form,
        "c_form_name": c_profiles.name(args.c_form),
        "n": args.n,
        "steps": args.steps,
        "frames": args.frames,
        "grid_L_m": float(sol.L),
        "dx_m": float(sol.dx),
        "dt_s": float(sol.dt),
        "cfl": float(sol.cfl),
        "cfl_stable_2d": bool(sol.cfl < 1.0 / np.sqrt(2.0)),
        "bundle_sha256": digest,
        "bundle_bytes": nbytes,
        "numpy_version": np.__version__,
    }
    out = {
        "provenance": provenance,
        "validation": report,
        "outputs": {
            "bundle": bundle_path,
            "pngs": png_paths,
        },
    }
    report_path = os.path.join(args.outdir, "run_report.json")
    with open(report_path, "w") as f:
        json.dump(out, f, indent=2)

    # ------------------------------------------------------------------
    # 6. Print a concise summary.
    # ------------------------------------------------------------------
    ms = report["manufactured_solution"]
    fb = report["feedback_budget"]
    print("Gradient Relativity FDTD run")
    print("============================")
    print(f"  C-form          : {args.c_form}  ({c_profiles.name(args.c_form)})")
    print(f"  grid            : {args.n}^2, L={sol.L:.3e} m "
          f"({sol.L/constants.LAMBDA_C:.2f} lambda_C)")
    print(f"  dx, dt          : {sol.dx:.3e} m, {sol.dt:.3e} s")
    print(f"  steps, frames   : {args.steps}, {args.frames}")
    print(f"  CFL             : {sol.cfl:.3f}  "
          f"({'STABLE <0.707' if provenance['cfl_stable_2d'] else 'UNSTABLE!'})")
    print(f"  C range         : {result['C_range'][0]:.3f} .. "
          f"{result['C_range'][1]:.3f}")
    print()
    print("Validation:")
    print(f"  [manufactured wave] {ms['verdict']}  "
          f"(max L2 err={ms['error_max']:.3e}, tol={ms['tolerance']})")
    print(f"  [feedback budget]   {fb['verdict']}  "
          f"(ratio={fb['feedback_ratio']:.3e} -- the honesty number)")
    print(f"  [C-form comparison] {report['c_form_comparison']['verdict']}")
    print()
    print("Outputs:")
    print(f"  bundle : {bundle_path}  ({nbytes/1e6:.2f} MB, "
          f"sha256={digest[:12]}...)")
    for p in png_paths:
        print(f"  png    : {p}")
    print(f"  report : {report_path}")
    print()
    print("Open the Flash player:  Web/index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
