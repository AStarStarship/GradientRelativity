"""Gradient Relativity simulation toolkit.

Reproducible, unit-honest numerical pipeline for the Planck-field (FDTD)
model described in Paper/Research.md 4.4-4.7 and Paper/CoreEquations/README.md.

Public API:
    constants      -- SI physical constants + derived GR scenario quantities
    c_profiles     -- local light-speed C(sigma) parameterizations
    fdtd           -- 2D leapfrog FDTD solver (unit-honest, 1 unit = 1 m, 1 s)
    validation     -- manufactured-solution check + feedback energy budget
    render         -- matplotlib stills + ffmpeg MP4 from a frame sequence
    run            -- one-command end-to-end runner (write_run.py is the CLI)

Design rules (see SKILL: computational-research-engineering):
  * NEVER substitute 1 for c inside an SI formula. Either work in a declared
    unit system or keep SI throughout and only normalize ratios.
  * Every run labels its light-speed parameterization (bounded vs P1).
  * Every run records a conservation/CFL diagnostic and a validation verdict.
  * Raw + normalized outputs are both written; a checksum is recorded.
"""

__version__ = "0.1.0"
