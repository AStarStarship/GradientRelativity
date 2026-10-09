# Gradient Relativity video

Copyright AStarship <https://astarship.net>.

This is a narrated hypothesis explainer, not a numerical electron simulation.
It distinguishes reference physics, Cale McCollough's postulate, and speculation.

The revision adds the 100% space/EM endpoint BETWEEN masses; proposed positive-pressure
flow into both masses and contraction of the intervening space (the author's gravity
mechanism); the electron-to-electron/infinite-path proposal; and the center's proposed
slowing, mass storage, incoming hit, and return to space oscillation. The central majority
of electrons is labeled an assumption. The pressure arrows and shortening gap are an
imposed illustration, not a derived metric or quantitative force law.

## Reproduce

Python 3.11 environment: Manim Community 0.22.0, edge-tts, NumPy, system Cairo/Pango,
DejaVu Sans Mono, FFmpeg and FFprobe. Text equations require no LaTeX.
Install Manim and edge-tts into an isolated environment; do not change system Python.

From the repository root, using that environment's Python:

    python Sim/Video/render_video.py --audio-only
    python Sim/Video/render_video.py --quality draft
    python Sim/Video/audit_layout.py
    python Sim/Video/render_video.py --quality final
    python Sim/Video/check_publication.py

Formal contract tests are separate from visual approval. After reviewing the film, use
`python -m unittest discover -s Sim/Video -p test_video.py -v` if suite evidence is needed.
An actual render, layout bounds, full decode, and audio/caption checks are targeted
artifact verification, not human viewing or proof of the physical model.

For this machine the prepared interpreter is:

    /home/astarcale/.hermes/profiles/astar-albert/cache/scratch/gradient_animation_venv/bin/python

That cache environment is not a durable dependency installation. Recreate it elsewhere
for later production. Edge TTS requires network access and returns real synthesized
speech and word timestamps. Cached clips are reused only when their narration hash
matches; failures are not replaced with synthetic timing guesses.

The runner processes one scene at a time. BLAS/OpenMP are capped to one thread and
FFmpeg verification to two; use nice or your scheduler's CPU limits for shared servers.
Final output is 1920×1080 at nominal 30 fps to reduce shared-server rendering load.
A terminated render can be restarted using Manim's partial-animation cache.
The final soundtrack is reconstructed from original speech clips and measured beat
times because cached scene renders can omit `add_sound` calls. Do not run a layout
audit and a production render concurrently against the same Manim cache.
After rendering selected changed chapters with `--scene`, `--assemble-only` can rebuild
the full video from existing clips; it does not make stale chapters current.

## Artifacts

- gradient_relativity_final.mp4: narrated production video.
- gradient_relativity_v1.mp4: preserved first version before this narrative revision.
- gradient_relativity_final.srt / .vtt: timed sidecar captions; video also burns captions in.
- chapters_final.json: measured chapter starts.
- verification_final.json: FFprobe streams, full-decode status, SHA-256, caption count.
- verification_revision_draft.json / verification_revision_final.json: targeted ad-hoc
  evidence for the revised narrative, scene coverage, audio/captions, and sampled layouts;
  not formal-suite or physics-validation results.
- narration.json: exact authored script, voice and speaking rate.
- layout_audit.json: visible text bounds at each draft beat endpoint, not a human viewing.
- publication_copy.md: YouTube and astartup.net copy; neither site is automatically updated.
- source_inventory.json: pre-production Markdown paths, counts, and hashes.
- input_report.json: frozen legacy scalar-wave report, not experimental confirmation.
- ../../Paper/Todo/electron_cycle_falsification.md: sourced research roadmap.
- ../../Reseach/README.md: Markdown research context, sources, and retrieval limitations.

## Scientific limitations

The phase bars follow an imposed cosine interpolation. Their conservation is bookkeeping,
not a proof of a physical conserved current. The horizon and center are schematic, not
ray tracing in a solved spacetime. The standard spinor diagram shows a quantum phase,
not the postulated energy interchange. A local light-speed law and a coordinate speed
must not be conflated. The new incoming-photon coupling, losses, stable electron state,
and distinguishable observable predictions remain open. A schematic path fan is not
a solved path integral, and positive-pressure arrows alone do not prove gravity.
"0% space/EM" at the proposed center is not "zero total energy." Stored mass energy
and the author's maximum expansion state must not be conflated with each other or
with a known highest atomic excitation. No photon escape from the interior is claimed.

Tests and successful media decoding verify the software/media pipeline only. Automated
bounds checks do not verify visual aesthetics or every possible overlapping annotation.
Review the completed film before publication; the narration is synthesized, not the
researcher's voice. No commit, upload, or deployment is performed by this runner.
