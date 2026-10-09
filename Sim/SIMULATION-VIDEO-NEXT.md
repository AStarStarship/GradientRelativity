# Next: unlocking the manim video path

The Flash player and the 12s MP4 (from the validated sim frames) are done and
verified. The richer 3Blue1Brown-style manim scenes for Chapters 1, 5, 6, 8, 9
need three system packages that `sudo` installs (this session can't run sudo —
it needs your password).

## One command to run (in a normal terminal, as your user)

```bash
sudo apt-get update && sudo apt-get install -y \
  libcairo2-dev libpango1.0-dev pkg-config \
  libopenjp2-7-dev \
  texlive-latex-base texlive-latex-extra texlive-fonts-extra
```

- `libcairo2-dev libpango1.0-dev pkg-config` — lets `pycairo`/`manim` build.
- `texlive-latex-*` — manim renders `MathTex` (the equations) via LaTeX.
- `libopenjp2-7-dev` — manim's image handling.

## Then, in this repo (I'll do it, or you can)

```bash
cd /home/astarcale/AStarStarship/GradientRelativity
export PATH="$HOME/.local/bin:$PATH"
uv pip install --python .venv/bin/python manim
.venv/bin/python -c "import manim; print('manim', manim.__version__)"
```

## Then the render (I'll build the scenes)

```bash
# draft (fast, 480p15)
.venv/bin/python -m manim -ql Sim/videos/script.py Scene1_BinaryEquilibrium Scene3_FeedbackBudget
# production (1080p60)
.venv/bin/python -m manim -qh Sim/videos/script.py Scene3_FeedbackBudget
```

Scenes map to the chaptered `Sim/Script.md`. The honest-beat scenes
(Ch 3 feedback 2.6e-44, Ch 4 chiral-field caveat, Ch 7 two C-forms) are the
ones that make the video rigorous — I'll pull their numbers from
`Sim/run_report.json`, never hand-type them.

## What's already working (no installs needed)
- Flash player: `http://127.0.0.1:8742/index.html`
- MP4 (validated sim frames): `gradient_relativity_planck_field.mp4`
- Still PNGs: `Sim/fdtd_final_frame.png`, `Sim/fdtd_source_track.png`
