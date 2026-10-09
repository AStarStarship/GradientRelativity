# Gradient Relativity — Simulation Toolkit

A reproducible, unit-honest numerical pipeline for the Planck-field (FDTD)
model in `Paper/Research.md` §4.4–4.7, plus a browser "Flash player" for
watching the field evolve and a validation ladder that keeps the numbers
honest.

## Quick start

```bash
# from the repo root
cd Sim

# create the env (once) — the venv already exists at ../.venv
../.venv/bin/python -m simlib --c-form bounded --n 96 --steps 480 --frames 32

# open the Flash player in a browser
python3 -m http.server 8742 --bind 127.0.0.1 --directory Web
# -> http://127.0.0.1:8742/index.html
```

The one-command runner (`python -m simlib`) does the whole ladder:
1. runs the FDTD solver (CFL-stable `dt`, fails closed if unstable);
2. runs validation (manufactured wave, complex known-case, feedback budget,
   C-form comparison);
3. writes `Web/sim_bundle.json` (frames + validation for the player);
4. writes `fdtd_final_frame.png` + `fdtd_source_track.png` (if matplotlib);
5. writes `run_report.json` (provenance + all validation, sha256 of bundle).

## Layout

```
Sim/
  simlib/
    __init__.py        package docstring + version
    constants.py       SI constants + galactic/binary scenario + diagnostics
    c_profiles.py      C(sigma) parameterizations (P1 vs bounded)
    fdtd.py            2D leapfrog FDTD solver + complex known-case test
    validation.py      manufactured wave, complex known-case, feedback budget,
                       C-form comparison (each with a PASS/FAIL/INFO verdict)
    render.py          JSON bundle for the Flash player + matplotlib stills
    run.py             one-command runner (the CLI)
    __main__.py        `python -m simlib` entry point
  Web/
    index.html         the Flash player (plain-JS canvas, no build step)
    sim_bundle.json    generated: field frames + validation (sha256 in meta)
  fdtd_final_frame.png generated still
  fdtd_source_track.png generated still
  run_report.json      provenance + validation report
```

## The honest findings (do not paper over in the video)

1. **Feedback ratio = 2.6e-44.** Larmor power at galactic a_c, times one
   galactic orbit, divided by the electron rest energy. The galactic
   acceleration does NOT drive the whirlpool at Compton frequency. The
   whirlpool is an **ansatz** the sim illustrates, not a derived consequence
   of the galactic term. This is the open problem the video must state.

2. **Two C(sigma) forms disagree.** Postulate P1: `C^2 = sigma/(1-sigma)`
   (unbounded). FDTD: `C = 2 sqrt(sigma(1-sigma))` (bounded). They agree only
   at sigma=1/2 (C=1). Research.md §4.4 flags this as an *unresolved*
   reparameterization. Every result must declare which form it used.

3. **A real-valued point source cannot make a swirl.** The FDTD solver's
   source is a real-valued Gaussian; a centered one radiates a radially
   symmetric (m=0) wave. A genuine m=1 whirlpool requires a *handed/chiral*
   field (two counter-rotating modes, or a spinor-like degree of freedom).
   That is a model-building open question, not a numerics bug. The
   `complex_known_case` test validates that the solver does NOT invent a
   swirl from an isotropic source (m=1 fraction ~0).

4. **The legacy solver's dt was ~3500x too small.** `Sim/fdtd_planck_field.py`
   used `dt = 0.4 dx / c`, giving CFL ~0.0002 — stable but a silent no-op
   (800 steps barely moved the field). `simlib` derives `dt` from the CFL
   limit (`dt = cfl_target dx / (cmax c)`), so a modest step count actually
   evolves the field, and `default_run` raises if a user-supplied `t_end`
   would make `dt` unstable.

## Edit-and-refresh workflow

- Edit `simlib/*.py`, re-run `python -m simlib ...`, refresh the browser.
- Edit `Web/index.html` directly, refresh the browser (no build step).
- The player fetches `sim_bundle.json` with `no-store`, so a fresh bundle is
  always picked up on reload.

## Flags

| flag | default | meaning |
|------|---------|---------|
| `--c-form` | `bounded` | `bounded` (FDTD) or `P1` (Postulate). Declared in every output. |
| `--n` | 128 | grid cells per side (square domain). |
| `--steps` | 600 | leapfrog steps. `dt` is chosen CFL-stable for this count. |
| `--t-end` | (stable window) | physical end time in seconds; if set and unstable, the run FAILS CLOSED. |
| `--frames` | 48 | max frames in the browser bundle. |
| `--outdir` | `Sim/` | where PNGs + `run_report.json` land. |
| `--no-png` | off | skip matplotlib stills (JSON only). |

## What the Flash player shows

- The evolving Planck field (magma/inferno/viridis/phase colormaps).
- The electron position (white core + cyan ring) and its recent orbit trail.
- A side panel with the four validation verdicts, the honest physics budget
  (a_c, P_larmor, omega0, x_p, feedback ratio), the C(sigma) comparison chart,
  and the field scale.
- Controls: play/pause, step, reset, frame scrub, speed, colormap,
  electron/ring overlays. Space = play/pause, arrows = step.

## Validation ladder (why these checks)

Following the `computational-simulation-validation` skill: a solver exiting
cleanly validates the *pipeline*, not the *physics*. So before trusting any
whirlpool claim:

1. **manufactured_solution** — a plane wave in a uniform-C domain must
   propagate with <5% L2 error over 4 periods. Tests the leapfrog numerics.
2. **complex_known_case** — a centered point source must radiate isotropically
   (no spurious m=1). Tests that the solver doesn't invent a swirl.
3. **feedback_budget** — the honest energy number (2.6e-44).
4. **c_form_comparison** — the two C(sigma) forms side by side.

A PASS on 1–2 plus the honest 3–4 is the minimum before a video may say
"the sim shows a whirlpool."
