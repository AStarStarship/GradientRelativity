# Gradient Relativity — Agent Workplan

> For Hermes: this is the roster plan for astar-mary and astar-paul.
> astar-albert (this session) implements on the sandbox; Captain (Cale)
> gates hardware, apt, and GPU takedowns. Crabs is out of scope until
> there is a working experiment. Do not invent a Crabs data path.

**Goal:** Get one working, unit-honest, falsifiable Planck-field experiment
on the P720 compute socket, with numbers that survive Mary's audit and
Paul's Dirac-level critique, before any GPU drama or Crabs rewrite.

**Architecture:** Keep three planes separate. Control = experiment
manifests + Flash player + VS Code/nvim. Compute = NumPy FDTD on CPU
(socket B), later optional V100. Artifact = immutable `run_report.json`
+ sha256 bundles. Vector DB lives on socket A / the second P720 and is
not the sim runtime.

**Tech stack now:** Python 3.11 venv at `.venv`, NumPy, matplotlib,
plain-JS Flash player (`Sim/Web/index.html`). No manim until Captain
runs the apt line in `Sim/SIMULATION-VIDEO-NEXT.md`. No CUDA until a
CPU experiment is VALIDATED or PARTIAL with a predeclared metric.

---

## Hardware truth (do not mix these)

| Layer | What it actually is | Use for |
|---|---|---|
| **This Hermes session** | Cascadelake, 20 vCPU, **16 GB RAM**, 1 NUMA node, **no GPU**, Python 3.12 system + repo `.venv` 3.11 | Edit, unit tests, 96² FDTD, Flash player, writing plans |
| **Target P720 #1 (compute)** | Dual Xeon Gold 6230, 12×16 GB = **192 GB ECC** DDR4-2933 (~130 GB/s), NUMA A/B | Socket B (~96 GB) = sims. Socket A (~96 GB) = leave for OS + any local retrieval |
| **Target P720 #2 (identical)** | Same box | Bare-metal Ubuntu: vector DB + Hermes podman. Do not run FDTD here unless Captain says so |
| **eGPU now** | RTX 3080 10 GB | Optional later. Not required for the first experiment |
| **In use, do not steal without Captain** | Gemma 4 12B QAT TurboQuant on RTX 5060 Ti 16 GB | Ask Captain before taking it down |
| **Soon** | RTX 5080; two NVIDIA V100 32 GB | Quantum / field experiments *after* CPU ladder |
| **Python on this server** | New. House stack is Next.js. Flash server = run Python, VS Code server + nvim 0.12 = edit | web-engineer owns DB/Next; we own sim Python |

NUMA rule from the research-engineering skill: bind CPU and memory
together. Sim workers pin to socket B. Vector DB stays on socket A / P720 #2.
Silent cross-node spill is a bug, not normal.

---

## Roster

| Agent | Role | Does | Does not |
|---|---|---|---|
| **Captain (Cale)** | Gate | apt, sudo, GPU takedown, P720 login, "go/no-go" on stealing 5060 Ti | Babysit every pytest |
| **astar-albert** | Implementer | Python FDTD, Flash player, runners, tests, AGENT_PLAN updates | Invent Crabs bindings; take GPUs |
| **astar-mary** | Colorblind experimentalist | Given/When/Then claims, confounders, "did we misread the plot", Occam check, accept/reject sim *claims* | Write the solver. She is not the best programmer — she reviews evidence |
| **astar-paul** | Dirac critic | Relativistic QM / QED confrontation, Lagrangian vs ansatz, C(σ) conflict, "this is analogue not QED" | Rubber-stamp whirlpool-as-electron |
| **web-engineer** | Backend | Vector DB schema, Next.js, Hermes podman on P720 #2 | Physics solvers |
| **Crabs** | Later harness | Contiguous data-driven stack machine | Anything until a CPU experiment exists |

Mary's Room constraint: she cannot use color as a scientific channel.
Plots must carry **shape, line style, labels, and numbers**. Magma
colormaps in the Flash player are for humans with color vision; Mary's
verdicts come from `run_report.json` and azimuthal spectra, not hue.

Paul's posture: if it does not reduce to a known QED/GR limit, or if
units are SI-with-c=1, he rejects the number. He already has ammunition
(`Paper/EquationAudit.md`, feedback ratio 2.6×10⁻⁴⁴).

---

## What is already true (do not re-do)

From `Sim/README.md` and the last verified run:

- `python -m simlib --c-form bounded --n 96 --steps 480 --frames 32` works.
- CFL = 0.700, fails closed if unstable.
- Manufactured plane wave: PASS (L2 err 5.55×10⁻³).
- Complex known-case: PASS (solver does not invent m=1 swirl).
- Feedback ratio: **2.634×10⁻⁴⁴** (INFO, the honesty number).
- Two C(σ) forms disagree except at σ=1/2. Results must name the form.
- Flash player: `Sim/Web/index.html` + `sim_bundle.json`.
- MP4 of the field exists: `gradient_relativity_planck_field.mp4`.
- Manim is blocked on libcairo/pango/texlive (Captain apt).
- `Paper/Todo/README.md` still thinks matplotlib PNGs are missing — they
  are not. Albert updates that todo when touching paper tasks.
- Equation audit E1 is fixed in `calc_magnetic_field.py`; E2–E15 are not
  merged into the paper.

Paper honesty note (`Paper/ExperimentalConsiderations/README.md`):
**none of the candidate experiments has a number yet.** Path is
Lagrangian → whirlpool parameters → Δg, Δλ, fringe shifts.

---

## Non-goals (YAGNI this cycle)

- Crabs / SCRIPT / Uniprinter / Seam.
- 3+1D FDTD on Planck-length grids (Research.md §4.6 step 1 is physically
  impossible on any P720; Planck length ~10⁻³⁵ m).
- Taking the 5060 Ti or waiting on V100s.
- Dark-matter rotation-curve theater before C(σ) is one formula.
- Next.js rewrite of the Flash player.
- Claiming CO2 or quantum-gravity results from this stack.

---

## The one experiment this cycle

**Given** SI units throughout, CFL-stable 2D leapfrog, declared C(σ) form,
Compton-scale domain (8 λ_C),
**when** we run the bounded form and the P1 form at matched n, steps, and
output times,
**then** we report:

1. manufactured-wave L2 error (must stay < 0.05);
2. m=1 fraction of a centered source (must stay ~0 — no fake swirl);
3. feedback ratio (expected ~2.6×10⁻⁴⁴, **INFO not a win**);
4. C(σ) table at σ ∈ {0.05, 0.25, 0.5, 0.75, 0.95} for both forms.

Verdict language: VALIDATED / PARTIAL / INVALIDATED as in the
computational-simulation-validation skill. The whirlpool-as-mass claim
is **not** on the table this cycle. The chiral/handed field is the
*next* experiment after Paul writes the degree-of-freedom, not before.

---

## Task board

### Task 0 — Captain: name the boxes

**Owner:** Captain
**Objective:** One paragraph in this file's hardware table becomes
measured, not remembered.

- Confirm DIMM map: 12×16 GB = 192 GB total, ~96 GB/socket.
- Confirm which P720 is "vector DB + Hermes podman" vs "sim".
- Confirm whether this 16 GB Cascadelake is a VM on P720 #2.
- Do **not** take the 5060 Ti down.

Albert does not SSH around looking for this. Captain pastes `lscpu`,
`numactl -H`, `free -h`, `hostname` from each bare metal.

---

### Task 1 — Albert: freeze a CPU experiment contract

**Owner:** astar-albert
**Files:**
- Create: `Sim/experiments/001-cform-matched/README.md`
- Create: `Sim/experiments/001-cform-matched/run.sh`
- Modify: `Sim/simlib/run.py` only if a `--outdir` already works (it does)

**README Given/When/Then:** copy "The one experiment this cycle" above.
**run.sh:**

```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PY="$ROOT/.venv/bin/python"
cd "$ROOT/Sim"
"$PY" -m simlib --c-form bounded --n 96 --steps 480 --frames 32 --outdir experiments/001-cform-matched/bounded
"$PY" -m simlib --c-form P1 --n 96 --steps 480 --frames 32 --outdir experiments/001-cform-matched/p1 --no-png
```

`--outdir` currently dumps PNGs + `run_report.json` into one folder and
always writes `Web/sim_bundle.json`. If two sequential runs clobber the
bundle, Albert adds `--bundle-path` in a follow-up micro-task. Do not
redesign the package.

**Verify:** both `run_report.json` files exist; both CFL < 0.707;
sha256 differs; manufactured_solution PASS on both.

---

### Task 2 — Mary: write the acceptance sheet before looking at plots

**Owner:** astar-mary
**File:** `Sim/experiments/001-cform-matched/ACCEPT.md`

Mary fills, in prose, not color:

- What would make her say INVALIDATED (e.g. CFL ≥ 0.707, L2 > 0.05,
  m=1 > 10% from a centered source, units off by >3 orders).
- What is allowed to look "pretty" and still be PARTIAL (the magma
  whirlpool movie).
- Explicit: 2.6×10⁻⁴⁴ is **not** a failure of the pipeline and **not**
  a confirmation of mass-from-feedback.

She does this *before* Albert pastes numbers. If she writes the sheet
after seeing the run, it is not an acceptance sheet.

---

### Task 3 — Paul: C(σ) and the Lagrangian hole

**Owner:** astar-paul
**Files:**
- Modify: `Paper/Research.md` §4.4 (remove leftover draft voice if any)
- Create: `Paper/Todo/Csigma.md` (one page: pick or dual-track)
- Create: `Paper/Todo/ChiralDOF.md` (what handed field would even mean)

Paul must answer, in writing:

1. Is Postulate P1 (`C² = σ/(1−σ)`) the theory, and bounded
   `C = 2√(σ(1−σ))` a numerical proxy? Or the reverse?
2. Can a real scalar φ have spin-½ 720° structure? If no, what is the
   minimal extra DOF (complex scalar, two real fields, spinor analogue)?
3. Does Larmor feedback at a_c even belong in a Compton-frequency
   oscillator, or is that mixing galactic and quantum scales illegally?

He is allowed to say "the current FDTD is an analogue toy." That is a
successful Paul task. He is not allowed to "fix" it by setting c=1 inside
SI formulae (`Paper/EquationAudit.md` E10, `calc_magnetic_field.py`).

---

### Task 4 — Albert: one chiral *spike*, not a product

**Owner:** astar-albert
**Depends on:** Task 3's DOF note
**File:** `Sim/spikes/002-chiral-complex/` (throwaway)

If Paul says "complex scalar with m=±1 source," Albert implements that
*only* as a spike: manufactured m=1 must appear when driven, and must
not appear when the source is centered-real. No Flash player, no video,
no paper figure until Mary signs ACCEPT for the spike.

If Paul says "needs a spinor / QED," Albert **stops**. That is GPU/V100
territory and not this cycle.

---

### Task 5 — Mary: review 001 numbers

**Owner:** astar-mary
**Input:** the two `run_report.json` files, not screenshots
**Output:** three lines in `ACCEPT.md`: VALIDATED / PARTIAL / INVALIDATED
for (pipeline, C-form difference, whirlpool-as-mass). Expected:

- pipeline: VALIDATED (if CFL + manufactured wave hold)
- C-form difference: INFO / PARTIAL (they disagree by construction)
- whirlpool-as-mass: **not tested** — do not upgrade this to VALIDATED

---

### Task 6 — web-engineer: retrieval is not the solver

**Owner:** web-engineer
**Scope:** P720 #2 vector DB (`~/.gradient_research/docs.db` exists with
~138 chunks — do not silently replace embeddings).

- Freeze a gold question set *before* changing retrieval.
- Do not call hash vectors "semantic embeddings."
- Sim artifacts stay on disk (`Sim/experiments/...`), not in Postgres.
- Next.js stays the product UI; Flash/Python stays the lab UI.

Albert may message web-engineer with the artifact schema
(`run_report.json` keys) but does not design the DB.

---

### Task 7 — Captain: GPU policy

Do **not** take down the 5060 Ti for this cycle.

When (and only when) Task 5 is PARTIAL/VALIDATED on CPU:

| GPU | Allowed use |
|---|---|
| 3080 10 GB eGPU | Optional CuPy port of the *same* 2D leapfrog; must match CPU field to 1e-6 relative on a 64² manufactured wave |
| V100 32 GB ×2 (when installed) | Complex/chiral 2D or small 3D; not Planck-length meshing |
| 5060 Ti 16 GB | Off limits unless Captain pages Gemma off |
| 5080 (soon) | Same rule as 3080: numerical agreement first |

---

### Task 8 — Video / Flash (optional, after 001)

Manim still needs:

```bash
sudo apt-get install -y libcairo2-dev libpango1.0-dev pkg-config \
  texlive-latex-base texlive-latex-extra texlive-fonts-extra
```

Captain runs that. Albert does not sudo. Until then the 12 s MP4 and
Flash player are the visual. Script honest-beats are already in
`Sim/Script.md`. Mary checks the script does not launder 2.6×10⁻⁴⁴
into "the whirlpool works."

---

## Communication rhythm (all agents)

For every claim:

1. **Promise** — strongest physically plausible value.
2. **Pushback** — conservation, scale, confounders, what evidence cannot
   support.
3. **Constructive path** — one Given/When/Then with a number.

Paul is pushback. Mary is "did we measure the right thing." Albert is
the path. Captain is the stop sign.

---

## Files likely to change this cycle

- `Sim/experiments/001-cform-matched/` (new)
- `Sim/spikes/002-chiral-complex/` (maybe)
- `Paper/Todo/Csigma.md`, `Paper/Todo/ChiralDOF.md` (Paul)
- `Paper/Research.md` §4.4 (Paul, light)
- `Paper/Todo/README.md` (Albert: mark matplotlib PNGs done)
- `Sim/simlib/run.py` only if bundle clobber is real
- **Not:** Crabs, Next.js, OpenFOAM, manim, CUDA

---

## Tests / validation

```bash
cd /home/astarcale/AStarStarship/GradientRelativity/Sim
../.venv/bin/python -m simlib --c-form bounded --n 96 --steps 480 --frames 32
```

Expect: CFL 0.700 STABLE, manufactured PASS, feedback INFO 2.634e-44.

On P720 socket B later: same command with `--n 256 --steps 2000` still
must PASS manufactured wave. If it fails, the 96² result was not a
resolution proof — that is a Mary INVALIDATED on "pipeline scales."

---

## Risks

- **This session is not the P720.** Shipping a 16 GB-tuned grid as
  "workstation scale" is a lie. Label sandbox vs socket-B.
- **Unit trap** still lives in `calc_magnetic_field.py` (`r_e` with c=1
  → meters of nonsense). Paul flags; Albert does not use that script
  for 001.
- **Research.md §4.6** asks for Δx < Planck length. Ignore that as a
  run setting. Compton scale is the honest domain.
- **Mary programming pain:** do not assign her pytest. Assign her
  ACCEPT.md.
- **Agent count:** Captain caps agents. Mary + Paul + Albert is the
  roster. No extra swarms.

---

## Open questions (Captain)

1. Which physical host is this 16 GB VM?
2. Is vector DB already bound to P720 #2 socket A?
3. Flash server port policy (8742 is the current lab port)?
4. When do the V100s actually land?

Until those are answered, Albert stays on the sandbox experiment 001.
