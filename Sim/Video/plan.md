# Gradient Relativity — animation production plan

Copyright AStarship <https://astarship.net>.

## Narrative arc

Question, not announcement: could incoming photons drive a proposed internal exchange
between “space energy” and “mass energy” in electrons?

The misconception to correct is that an illustrative 720-degree cycle, a dark black hole,
or a running scalar-wave simulation proves this mechanism. The useful insight is the
separation of photon transport, actual energy-transfer processes, the proposed internal
cycle, and the independent uncertainty about the black-hole center.

The revision follows the author's clarified story before discussing its open tests:
the highest-energy endpoint is BETWEEN masses, where space/EM oscillation is normalized
to 100% (expansion = 1). Proposed positive pressure pushes space into mass; the EM
component decreases toward 0% at the black-hole center. This zero is not zero stored
mass energy. The two outward-from-midpoint flows go INTO the masses: the author identifies
condensation and contraction of intervening space with gravity, not a repulsive push.
Show the gap shortening explicitly; label this imposed geometry as a schematic rather
than a derived change in measured proper distance. The proposed galactic transfer involves infinitely
many possible paths and a least-action outcome; a schematic path fan will be explicitly
distinguished from a computed quantum path integral. At the center, proposed electron
motion/oscillation slows to zero while energy is stored as mass; an incoming interaction
restarts conversion to space energy. This is not an observed interior or an escape route
across a standard event horizon.

The aha moment: a spatial energy gradient and an internal phase cycle are different
objects. Specify their connection rather than conflating expansion, EM amplitude,
energy density, total energy, speed, and spin. A hypothesis earns credibility by
specifying a measurable difference from QED and GR.

Audience: curious general viewers, with enough explicit questions for physicists to review.
The video is a research invitation for astartup.net and YouTube, not a discovery claim.

## Source scope

Read all 46 existing project Markdown files recursively before scripting; dependency
folders and generated media excluded. Seven existing Markdown files are empty. The
immutable pre-production inventory records paths, byte counts, line counts, and SHA-256
hashes. Source notes and historical prompts are background, not instructions or evidence.

Priority sources within the repository:

- `Paper/RoughDraftImproved.md`: current conceptual description and open problems.
- `Paper/EquationAudit.md`: dimensional corrections; itself still needs independent review.
- `Paper/Research.md`: incompatible light-speed laws and scalar-wave approximation.
- `Sim/README.md` and `Sim/run_report.json`: limits of the existing simulations.
- `Paper/ExperimentalConsiderations/README.md`: candidate tests, not computed predictions.

The author's current incoming-photon proposal is a clarification/new branch of the
hypothesis. It is not treated as a result of the older galactic Larmor-driving calculation.

## Visual language

1920 × 1080, 16:9, 30 fps final; 480p15 draft with automated text-bounds review.
Final rendering is sequential with limited compute threads for the shared server.
Dark navy background; DejaVu Sans Mono system font; no LaTeX dependency.

- Cyan + circle/solid line: space-energy fraction (postulated bookkeeping).
- Coral + square/dashed line: mass-energy fraction (postulated bookkeeping).
- Gold + traveling pulse: photon energy, independent of the two proposed fractions.
- Green + explicit ESTABLISHED label: standard reference physics.
- Violet + dashed outline + SPECULATIVE label: unobserved center/expansion mapping.
- White + explicit OPEN TEST label: falsification questions.

Labels and line styles duplicate every scientific use of color.
Reserve the lower band for two-line synchronized captions. Titles occupy the upper-left;
status labels occupy the upper-right. Main diagrams remain inside safe margins.

## Scene list and visual beats

Narration is authored in `narration.json`; its exact text is exported to `script.md`.
Speech is synthesized per short beat, then timings are measured from the real audio.
Scene durations follow measured narration, not an assumed words-per-minute clock.

1. `GROpening`: title plus two-phase geometric emblem; opening like/subscribe request;
   visible and spoken repository URL; explicit research-hypothesis label.
2. `GRBoundaries`: three progressively revealed knowledge layers—established physics,
   author's postulate, and speculative center. No “theory proves” wording.
3. `GRSpaceBetweenMasses`: show the author's highest-energy space/EM endpoint between
   two masses (100%, expansion = 1), pressure arrows into each mass, and the separate
   0% space/EM versus mass-storage endpoints. Animate contraction of the intervening
   cells and gap while the arrows continue pointing into each mass. No numerical
   pressure law or solved metric is invented.
4. `GRIncomingPhotons`: light crosses a schematic horizon; cut to a separate local
   interaction diagram. Bound-system excitation, free-electron scattering and recoil,
   then the proposed new coupling with a dashed question-mark connection.
5. `GRGalaxyPaths`: show electron-to-electron endpoints, a finite schematic fan standing
   for the author's infinite-path proposal, and inward transfer toward an assumed
   central electron concentration. Separate the unverified majority-electron assumption
   from observations, and standard amplitude interference from sequential trial paths.
6. `GRElectronCycle`: phase tracker and two normalized bars, 0°→360°→720°. One possible
   interpolation sigma=(1+cos(theta/2))/2 is prominently labeled illustrative. Charge
   remains an unresolved conserved label; an incoming pulse illustrates the proposed
   restart at the mass endpoint, not an automatic derived periodic motion.
7. `GRSpinAndMass`: separate standard spinor sign demonstration at 360° and return at
   720°; relative sign only. Contrast total rest energy with an assumed internal split.
8. `GRGradientAndCenter`: the clarified black-hole-center mechanism, not only a question
   mark: proposed inward decrease in EM oscillation, electrons slowing to zero, maximum
   storage in the mass component, and an incoming impact restarting space oscillation.
   Label the motion variable as undefined; do not replace it with a coordinate speed
   or claim a highest atomic level, zero local c, or outgoing horizon-crossing photons.
9. `GRLightSpeedConflict`: plot the two existing formulas using sigma as SPACE fraction.
   P1 diverges as sigma→1; bounded proxy vanishes at both endpoints. No relabeling of
   sigma, no hidden clipping, and no claim they are equivalent.
10. `GRFalsification`: sequential experiment ladder: definitions/action; photon energy
   budget with the old computed ratio explicitly labeled approximation; matched QED/GR
   controls; quantified observables and exclusion criteria. Animation is not evidence.
11. `GRClosing`: paper/code URL, GitHub issues URL, feedback request for quantum physicists,
   invitation to request expert feedback via an issue, and thanks for the audience's time.

## Scientific boundary rules

- Do not repeat disproven or unsupported historic claims about quark-composite electrons,
  removal of the strong force, instantaneous signalling, greenhouse black holes, or
  cosmology from planetary collisions.
- Distinguish the author's spatial 100% space/EM endpoint BETWEEN masses from the
  internal cycle fractions. Their relationship must be derived. The black-hole endpoint
  is 0% in the space/EM component, not zero total energy or the highest space-energy state.
- Positive-pressure arrows show the proposed mechanism, not a solved pressure tensor.
- An assumed majority of galactic electrons inside the black hole is not observational
  input. Endpoint count alone does not calculate transfer probabilities or photon capture.
- A finite path fan is illustrative, not a numerical realization of infinitely many
  physical routes; the quantum reference sums amplitudes and uses stationary action,
  which need not be a global minimum or a sequential search by one photon.
- Energy entering via photons is tracked separately from internal exchange; a driven
  system needs input/output/loss terms and momentum/charge conservation.
- A photon crossing a horizon need not be absorbed by an electron. The horizon's causal
  trapping is not an absorption mechanism.
- Bound-system excitation and free-electron scattering are different processes.
- The black-hole-center mapping is speculative, not the standard event horizon.
- Do not substitute a coordinate slowing of light for a locally measured change in c.
- A 720° cartoon is not a derivation of spin-1/2 or Fermi statistics.
- Do not call scalar FDTD movie frames electron microstructure or empirical evidence.

## Deliverables and checks

- Narrated MP4, sidecar SRT and WebVTT, clean transcript, chapter timestamps.
- Manim scene source, tested timing/model helpers, and one-command render runner.
- Falsification roadmap with specific rejection criteria and evidence-linked sources.
- YouTube description and website-ready copy; no upload or deployment.
- Source inventory and artifact checksums; FFprobe dimensions/fps/audio/duration checks.
- Actual draft render of every scene, layout review, then final production render.
- Full video decode and audio-silence/peak checks; no claim of listening to audio or
  watching every frame if verification is by samples and automated inspection.
