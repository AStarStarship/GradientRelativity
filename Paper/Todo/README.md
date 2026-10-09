# TODO — Gradient Relativity

Working task list. Check items off as they land.

The [current manuscript](../RoughDraftImproved.md) and its supporting section pages now
record the clarified spatial pressure/contraction, transport, and center-restart story.
That editorial update is not completion of the physical derivations below. See the
[falsification roadmap](electron_cycle_falsification.md), especially R13.

## 1. Equation corrections (from EquationAudit.md)
- [x] E1: ε₀ = 1/(μ₀·c²) — fixed in calc_magnetic_field.py (was c³)
- [ ] E2: rewrite (E−pv)/M = q·ε_c·sin(π/2) as a postulate in the paper
- [ ] E3: remove or reframe q·ε₀·sin(π/2) = C²
- [ ] E4/E13: driven oscillator uses q·E₀, not q·ε₀ — update RoughDraftImproved.md §3
- [ ] E5: m = E/c² in the paper (was (E−pv)/(q·ε₀))
- [ ] E6: Planck length ≈ 1.616×10⁻³⁵ m, not ≈ 0 — update paper
- [ ] E7: ω₀ = √(k_eff/m) — define k_eff in the whirlpool model
- [ ] E8: remove sin²+cos²=1 tautology as a "physical result"
- [ ] E9: ε_c = ε₀ (natural units: 1), not 1/ε₀
- [ ] E10: clarify unit conventions (natural vs SI) throughout
- [ ] E11: fix photon case (E = pc, not E = mc²) in paper §4
- [ ] E12: state c² = E_space/E_mass explicitly as a postulate
- [ ] E15: m = E/c², not c²/E

## 2. Paper structure
- [x] Fill Paper/CoreEquations/README.md with reference relations and unresolved candidate laws
- [x] Fill Paper/Discussion/README.md with pressure, distance, speed and conservation limitations
- [x] Fill Paper/ExperimentalConsiderations/README.md with candidate tests, not numerical predictions
- [ ] Resolve the speed-law conflict without assuming a reparameterization: P1 and the
  bounded form have incompatible pure-space limits under the same internal fraction.
- [ ] Remove draft artifact in Research.md §4.4 ("Wait we previously set C=1...")
- [ ] Convert paper to LaTeX source (deliverable in Research.md §5)

## 3. Simulation
- [x] calc_magnetic_field.py — runs, verified (a_c = 2.45×10⁻¹⁰ m/s², B at 1 µm = 3.9×10⁻⁹ T)
- [x] fdtd_planck_field.py — runs, CFL-stable, outputs fdtd_summary.txt + field frame
- [ ] Run FDTD with matplotlib installed → PNG outputs
- [ ] Fix unit-handling in calc_magnetic_field.py (c=1 block keeps SI length units; r_e "natural" = 253 m is a unit artifact, label it as such)
- [ ] Full whirlpool self-consistency run (solve x_e(t) and field simultaneously)
- [ ] Galaxy-scale space-energy gradient run (stellar velocities vs dark-matter rotation curves)

## 4. Video
- [x] Script.md — 4-minute narration script
- [x] gradient_relativity_scene.py — 5 scenes matching the script
- [ ] Install manim, render scenes (manim -qm)
- [ ] Generate audio from Script.md (TTS) and mux with video
- [ ] Render solar_system_sim.py scene (currently a stub)

## 5. Research next steps (from Research.md §1)
- [ ] Full Lagrangian for Planck field + fermions
- [ ] Electron self-energy from whirlpool oscillation vs measured m_e
- [ ] Nucleon extension (p/n mass ratios)
- [ ] Covariant form reducing to GR in the low-energy limit
- [ ] Stress-energy tensor of the Planck field
- [ ] Space-energy gradient ↔ cosmological constant / dark energy
- [ ] Predictions: g-2 deviation, Lamb-like shifts, GW spectra, Penning-trap anomalies, CMB polarization imprint
