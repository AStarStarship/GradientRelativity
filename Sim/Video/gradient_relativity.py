# Copyright AStarship <https://astarship.net>.
"""Narrated Manim storyboard. All proposed microstructure is illustrative, not simulated.

Prepare real audio with render_video.py before rendering any scene. Text-only equations
avoid a LaTeX dependency. The phase interpolation is not a field equation or evidence.
"""

import json
import math
import os
from pathlib import Path
import textwrap

from manim import (
  Animation, Arrow, Axes, BOLD, Circle, Create, DashedLine, Dot, DOWN,
  FadeIn, FadeOut, GrowArrow, GrowFromCenter, Group, Indicate, LEFT, Line,
  linear, Mobject, ORIGIN, ParametricFunction, Rectangle, ReplacementTransform,
  RIGHT, Rotate, RoundedRectangle, Scene, Square, Text, UP, ValueTracker,
  VGroup, VMobject, Write,
)
import numpy as np

from video_model import EnergyFractions

Root = Path(__file__).resolve().parent
Background = "#0B1020"
Panel = "#141C30"
Space = "#58D5E8"
Mass = "#FF7D87"
Photon = "#FFD166"
Established = "#9BE2AD"
Speculative = "#C2A0FF"
Ink = "#F0F4FF"
Muted = "#B0BDCF"
Grid = "#52627B"
Font = "DejaVu Sans Mono"
Repo = "github.com/AStarStarship/GradientRelativity"
Document = json.loads((Root / "narration.json").read_text(encoding="utf-8"))


def Label(text: str, size: float = 26, color: str = Ink,
          width: float = 12.6, bold: bool = False) -> Text:
  label = Text(text, font=Font, font_size=size, color=color,
               weight=BOLD if bold else "NORMAL", line_spacing=0.8)
  if label.width > width:
    label.scale(width / label.width)
  return label


def Card(title: str, body: str, color: str, width: float = 4.0,
         height: float = 1.9) -> VGroup:
  box = RoundedRectangle(width=width, height=height, corner_radius=0.14,
                         stroke_color=color, stroke_width=1.6,
                         fill_color=Panel, fill_opacity=0.9)
  title_label = Label(title, 24, color, width - 0.4, True)
  body_label = Label(body, 22, Ink, width - 0.4)
  text = VGroup(title_label, body_label).arrange(DOWN, buff=0.28).move_to(box)
  return VGroup(box, text)


def WavePath(start: np.ndarray, end: np.ndarray, amplitude: float = 0.12) -> VMobject:
  delta = end - start
  perpendicular = np.array([-delta[1], delta[0], 0.0])
  perpendicular /= np.linalg.norm(perpendicular)
  points = [start + delta * step + amplitude * math.sin(10 * math.pi * step)
            * perpendicular for step in np.linspace(0, 1, 100)]
  path = VMobject(color=Photon, stroke_width=3)
  path.set_points_as_corners(points)
  return path


class GRNarratedScene(Scene):
  """Measured per-beat voiceover with burned-in word-timed caption groups."""

  def SetupChapter(self, status: str, color: str) -> None:
    self.camera.background_color = Background
    self.chapter_ = next(item for item in Document["scenes"]
                         if item["class_name"] == type(self).__name__)
    audio_dir = Path(os.environ.get("GR_AUDIO_DIR", str(Root / "media" / "narration")))
    timing_path = audio_dir / "timing.json"
    if not timing_path.is_file():
      raise RuntimeError("Measured narration is missing; run render_video.py --audio-only first")
    self.audio_dir_ = audio_dir
    self.timings_ = json.loads(timing_path.read_text(encoding="utf-8"))["beats"]
    self.caption_cues_ = []
    self.caption_key_ = None
    self.beat_end_ = 0.0
    self.beats_ = []
    title = Label(self.chapter_["title"], 33, Ink, 9.7, True)
    title.to_edge(UP, buff=0.55).to_edge(LEFT, buff=0.6)
    tag = Label(status, 18, color, 2.7).to_edge(UP, buff=0.66).to_edge(RIGHT, buff=0.6)
    rule = Line([-6.5, 2.93, 0], [6.5, 2.93, 0], stroke_color=color,
                stroke_width=1.5, stroke_opacity=0.7)
    caption_panel = Rectangle(width=13.4, height=1.05, stroke_width=0,
                              fill_color=Background, fill_opacity=0.97).move_to([0, -3.30, 0])
    self.caption_ = VGroup()
    self.caption_.add_updater(lambda mobject, dt: self.UpdateCaption(mobject))
    self.add(title, tag, rule, caption_panel, self.caption_)

  def UpdateCaption(self, mobject: Mobject) -> None:
    current = next((cue for cue in self.caption_cues_
                    if cue["start"] <= self.time < cue["end"]), None)
    key = current["text"] if current else ""
    if key == self.caption_key_:
      return
    self.caption_key_ = key
    if key:
      caption = Label(textwrap.fill(key, width=78), 21, Ink, 12.5)
      caption.move_to([0, -3.28, 0])
      mobject.become(VGroup(caption))
    else:
      mobject.become(VGroup())

  def BeginBeat(self, index: int) -> float:
    beat = self.chapter_["beats"][index]
    timing = self.timings_[beat["id"]]
    audio_path = self.audio_dir_ / timing["audio_file"]
    if not audio_path.is_file():
      raise RuntimeError(f"Narration clip is missing: {audio_path}")
    start = self.time + 0.30
    self.add_sound(str(audio_path), time_offset=0.30, gain=-1.0)
    self.caption_cues_ = [{"start": start + cue["start"], "end": start + cue["end"],
                           "text": cue["text"]} for cue in timing["cues"]]
    for cue in self.caption_cues_:
      self.add_subcaption(cue["text"], duration=cue["end"] - cue["start"],
                          offset=cue["start"] - self.time)
    self.beat_end_ = start + timing["duration"] + 0.80
    self.beats_.append({"id": beat["id"], "audio_start": start,
                        "audio_end": start + timing["duration"],
                        "text": beat["text"]})
    return timing["duration"]

  def EndBeat(self) -> None:
    remaining = self.beat_end_ - self.time
    if remaining < -0.10:
      raise RuntimeError(f"Animation overran measured narration by {-remaining:.3f}s")
    if remaining > 0:
      self.wait(remaining)

  def Narrate(self, index: int, *animations: Animation, run_time: float = 1.4) -> None:
    self.BeginBeat(index)
    if animations:
      self.play(*animations, run_time=run_time)
      self.wait(0.35)
    self.EndBeat()

  def Note(self, text: str, color: str = Muted) -> Text:
    return Label(text, 20, color, 12.7).move_to([0, -2.40, 0])

  def Finish(self) -> None:
    timing_dir = Root / "media" / "scene_timing"
    timing_dir.mkdir(parents=True, exist_ok=True)
    from manim import config
    tag = f"{config.pixel_height}p{int(config.frame_rate)}"
    timing_path = timing_dir / f"{type(self).__name__}_{tag}.json"
    timing_path.write_text(json.dumps({"scene": type(self).__name__, "beats": self.beats_},
                                      indent=2) + "\n", encoding="utf-8")
    for mobject in self.mobjects:
      mobject.clear_updaters(recursive=True)
    self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
    self.wait(0.15)


class GROpening(GRNarratedScene):
  def construct(self):
    self.SetupChapter("RESEARCH HYPOTHESIS", Speculative)
    center = np.array([-3.9, 0.45, 0])
    rings = VGroup(Circle(radius=1.45, color=Space, stroke_width=4),
                   Circle(radius=1.04, color=Mass, stroke_width=4)).move_to(center)
    core = Dot(center, radius=0.10, color=Ink)
    emblem = VGroup(rings, core)
    title = Label("A hypothesis\nunder test", 43, Ink, 6.5, True).move_to([2.3, 0.7, 0])
    cta = Label("LIKE + SUBSCRIBE", 27, Photon, 8.0, True).move_to([1.4, -1.00, 0])
    self.Narrate(0, GrowFromCenter(emblem), FadeIn(title), FadeIn(cta), run_time=1.8)
    link = Label(Repo, 25, Space, 12.1).move_to([0, -1.95, 0])
    note = self.Note("By Cale McCollough | Animation is not experimental evidence")
    self.Narrate(1, Write(link), FadeIn(note))
    self.Finish()


class GRBoundaries(GRNarratedScene):
  def construct(self):
    self.SetupChapter("SEPARATE THE CLAIMS", Established)
    cards = [
      Card("ESTABLISHED", "Photons carry energy\nMatter can absorb / scatter\nHorizons can capture light",
           Established, 4.05, 3.1).move_to([-4.35, 0.2, 0]),
      Card("POSTULATE", "Electron internal cycle\nSpace-energy / mass-energy\nNo derived mechanism yet",
           Space, 4.05, 3.1).move_to([0, 0.2, 0]),
      Card("SPECULATIVE", "Expansion-to-center map\nUnknown center structure\nNot an observed profile",
           Speculative, 4.05, 3.1).move_to([4.35, 0.2, 0]),
    ]
    for index, card in enumerate(cards):
      if index:
        self.play(cards[index - 1].animate.set_opacity(0.4), run_time=0.5)
      self.Narrate(index, FadeIn(card, shift=UP * 0.2))
    self.play(*[card.animate.set_opacity(1) for card in cards], run_time=0.7)
    self.add(self.Note("Established interactions do not establish the proposed internal cycle"))
    self.wait(1.0)
    self.Finish()


class GRSpaceBetweenMasses(GRNarratedScene):
  def construct(self):
    self.SetupChapter("AUTHOR'S POSTULATE", Space)
    phase = ValueTracker(0)
    span = ValueTracker(1)
    left_mass = VGroup(Circle(radius=0.70, color=Mass, fill_color=Mass, fill_opacity=0.15)
                      .move_to([-4.5, 0.45, 0]),
                      Label("MASS A", 23, Mass, 2.0).move_to([-4.5, -0.65, 0]))
    right_mass = VGroup(Circle(radius=0.70, color=Mass, fill_color=Mass, fill_opacity=0.15)
                       .move_to([4.5, 0.45, 0]),
                       Label("MASS B", 23, Mass, 2.0).move_to([4.5, -0.65, 0]))
    heading = Label("BETWEEN MASSES: highest space/EM energy", 26, Space, 12.3, True)
    heading.move_to([0, 2.1, 0])
    normalization = Label("100% oscillation  |  expansion = 1", 25, Ink, 10.5)
    normalization.move_to([0, 1.42, 0])
    cells = VGroup(*[Rectangle(width=0.46, height=1.05, stroke_color=Grid,
                              stroke_width=1.3).move_to([x, 0.45, 0])
                    for x in np.linspace(-2.55, 2.55, 9)])
    wave = VMobject(color=Space, stroke_width=3)
    def UpdateWave(mobject):
      points = [np.array([x * span.get_value(),
                         0.45 + 0.35 * math.sin(2.4 * x + phase.get_value()), 0])
                for x in np.linspace(-2.8, 2.8, 90)]
      mobject.set_points_as_corners(points)
    UpdateWave(wave)
    wave.add_updater(UpdateWave)
    note = self.Note("Qualitative postulate; no pressure law or spacetime metric is solved")
    self.BeginBeat(0)
    self.play(FadeIn(left_mass), FadeIn(right_mass), FadeIn(heading), FadeIn(normalization),
              Create(cells), FadeIn(wave), FadeIn(note), run_time=1.8)
    self.play(phase.animate.set_value(4 * math.pi), run_time=3, rate_func=linear)
    self.EndBeat()
    pressure = Label("positive pressure: space flows INTO each mass", 24, Photon, 11.8)
    pressure.move_to([0, -1.45, 0])
    arrows = VGroup(Arrow([-1.0, -0.32, 0], [-3.72, -0.32, 0], color=Photon, buff=0),
                    Arrow([1.0, -0.32, 0], [3.72, -0.32, 0], color=Photon, buff=0))
    self.Narrate(1, GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(pressure))
    gap = Line([-3.72, -1.1, 0], [3.72, -1.1, 0], color=Space, stroke_width=3)
    contraction = Label("Intervening space contracts\nnot a repulsive push", 25, Space, 8.2)
    contraction.move_to([0, -1.79, 0])
    self.BeginBeat(2)
    self.play(FadeOut(pressure), Create(gap), FadeIn(contraction), run_time=1.0)
    self.wait(0.7)
    self.play(left_mass.animate.shift(RIGHT * 1.2), right_mass.animate.shift(LEFT * 1.2),
              cells.animate.stretch(0.60, 0), gap.animate.stretch(0.68, 0),
              span.animate.set_value(0.60), phase.animate.set_value(8 * math.pi),
              arrows[0].animate.put_start_and_end_on([-0.7, -0.32, 0], [-2.52, -0.32, 0]),
              arrows[1].animate.put_start_and_end_on([0.7, -0.32, 0], [2.52, -0.32, 0]),
              run_time=4, rate_func=linear)
    self.EndBeat()
    wave.clear_updaters()
    self.play(FadeOut(Group(left_mass, right_mass, heading, normalization, cells, wave,
                           arrows, gap, contraction, note)), run_time=0.7)
    expanded = Card("BETWEEN MASSES", "100% space / EM\nMaximum expansion endpoint",
                    Space, 5.9, 2.6).move_to([-3.25, 0.4, 0])
    stored = Card("BLACK-HOLE CENTER", "0% space / EM\nMass storage is NOT zero total E",
                  Mass, 5.9, 2.6).move_to([3.25, 0.4, 0])
    boundary = self.Note("Spatial gradient ≠ internal phase cycle; their connection remains to be derived")
    self.Narrate(3, FadeIn(expanded), FadeIn(stored), FadeIn(boundary))
    self.Finish()


class GRIncomingPhotons(GRNarratedScene):
  def construct(self):
    self.SetupChapter("BASELINE → NEW CLAIM", Established)
    center = np.array([-2.8, 0.3, 0])
    hole = Circle(radius=1.25, stroke_width=2, stroke_color=Muted,
                  fill_color=Background, fill_opacity=1).move_to(center)
    horizon = Circle(radius=1.6, color=Muted, stroke_width=1.5).move_to(center)
    horizon_label = Label("schematic horizon", 23, Muted, 5.0).move_to([-2.8, -1.62, 0])
    inside = Label("interior\nnot imaged", 21, Speculative, 2.0).move_to(center)
    rays = VGroup(*[WavePath(np.array([-6.1, y, 0]), center + np.array([-0.2, 0.2 * y, 0]))
                   for y in (-0.8, 0.3, 1.4)])
    capture = Card("CAUSAL TRAPPING", "Not the same as\nelectron absorption", Established,
                   5.0, 2.0).move_to([3.1, 0.3, 0])
    self.BeginBeat(0)
    self.play(Create(horizon), FadeIn(hole), FadeIn(inside), FadeIn(horizon_label), run_time=1.2)
    self.wait(0.5)
    self.play(Create(rays), FadeIn(capture), run_time=2.2)
    self.wait(0.5)
    self.EndBeat()
    self.play(FadeOut(Group(hole, horizon, inside, horizon_label, rays, capture)), run_time=0.7)
    local = Label("Separate local interaction diagram", 24, Established).move_to([0, 2.30, 0])
    lower = Line([-5.8, -0.8, 0], [-2.2, -0.8, 0], color=Space, stroke_width=3)
    upper = Line([-5.8, 0.85, 0], [-2.2, 0.85, 0], color=Space, stroke_width=3)
    atom_dot = Dot([-4.0, -0.8, 0], radius=0.13, color=Space)
    pulse = WavePath(np.array([-6.0, 0.1, 0]), np.array([-4.2, 0.1, 0]))
    transition = Arrow([-4.0, -0.55, 0], [-4.0, 0.63, 0], color=Photon, buff=0.05)
    atom_label = Label("BOUND SYSTEM\nallowed excitation", 23, Ink, 5.0).move_to([-4.0, -1.65, 0])
    scatter = Card("FREE ELECTRON", "Scattering + recoil\nNot lone-photon absorption",
                   Established, 5.4, 2.3).move_to([3.15, 0.10, 0])
    self.BeginBeat(1)
    self.play(FadeIn(local), Create(lower), Create(upper), FadeIn(atom_dot), run_time=1.4)
    self.wait(0.4)
    self.play(Create(pulse), GrowArrow(transition), atom_dot.animate.move_to([-4, 0.85, 0]),
              run_time=1.8)
    self.play(FadeIn(atom_label), FadeIn(scatter), run_time=0.8)
    self.EndBeat()
    self.play(FadeOut(Group(local, lower, upper, atom_dot, pulse, transition, atom_label, scatter)),
              run_time=0.6)
    photon = Card("INPUT", "Photon energy\n+ momentum", Photon).move_to([-4.5, 0.2, 0])
    coupling = Card("OPEN STEP", "New field coupling?\nRecoil / losses?", Speculative).move_to([0, 0.2, 0])
    cycle = Card("POSTULATE", "Internal\nspace ↔ mass cycle", Space).move_to([4.5, 0.2, 0])
    arrows = VGroup(DashedLine([-2.45, 0.2, 0], [-2.05, 0.2, 0], color=Muted),
                    DashedLine([2.05, 0.2, 0], [2.45, 0.2, 0], color=Muted))
    note = self.Note("Capture ≠ absorption ≠ a derived space-to-mass mechanism")
    self.Narrate(2, FadeIn(photon), FadeIn(coupling), FadeIn(cycle), Create(arrows), FadeIn(note),
                 run_time=1.6)
    self.Finish()


class GRGalaxyPaths(GRNarratedScene):
  def construct(self):
    self.SetupChapter("PROPOSED TRANSPORT", Speculative)
    source = Dot([-5.25, 0.4, 0], radius=0.14, color=Space)
    receivers = VGroup(Dot([4.5, 0.4, 0], radius=0.14, color=Mass),
                       Dot([4.5, 1.6, 0], radius=0.09, color=Mass),
                       Dot([4.5, -0.8, 0], radius=0.09, color=Mass))
    source_label = Label("source\nelectron", 23, Space, 2.3).move_to([-5.25, -0.65, 0])
    receiver_label = Label("possible\nreceivers", 23, Mass, 2.6).move_to([4.5, -1.55, 0])
    connection = DashedLine(source.get_center(), receivers[0].get_center(), color=Muted)
    heading = Label("Any electron → any other electron?", 27, Ink, 12.1).move_to([0, 2.1, 0])
    note = self.Note("Author's proposed transfer picture; not an instantaneous or computed signal")
    self.Narrate(0, FadeIn(source), FadeIn(receivers), FadeIn(source_label),
                 FadeIn(receiver_label), Create(connection), FadeIn(heading), FadeIn(note))
    fan = VGroup()
    for amplitude in np.linspace(-1.3, 1.3, 9):
      path = VMobject(color=Speculative, stroke_width=1.5, stroke_opacity=0.45)
      path.set_points_as_corners([np.array([-5.25 + 9.75 * t,
                                           0.4 + amplitude * math.sin(math.pi * t), 0])
                                 for t in np.linspace(0, 1, 70)])
      fan.add(path)
    selected = VMobject(color=Photon, stroke_width=3.5)
    selected.set_points_as_corners([np.array([-5.25 + 9.75 * t,
                                             0.4 + 0.20 * math.sin(math.pi * t), 0])
                                   for t in np.linspace(0, 1, 70)])
    infinite = Label("∞ possible paths  |  least-action interpretation", 25, Speculative, 12.1)
    infinite.move_to(heading)
    path_note = self.Note("Finite schematic fan. Highlighted route is illustrated, not calculated.")
    self.BeginBeat(1)
    self.play(FadeOut(connection), ReplacementTransform(heading, infinite),
              ReplacementTransform(note, path_note), Create(fan), run_time=2.0)
    self.wait(0.5)
    self.play(Create(selected), run_time=1.5)
    self.EndBeat()
    self.play(FadeOut(Group(source, receivers, source_label, receiver_label, infinite,
                           path_note, fan, selected)), run_time=0.7)
    center = np.array([2.9, 0.4, 0])
    hole = Circle(radius=1.20, color=Speculative, stroke_width=2,
                  fill_color=Panel, fill_opacity=0.8).move_to(center)
    inner = VGroup(*[Dot(center + np.array([x, y, 0]), radius=0.07, color=Mass)
                    for x in (-0.45, -0.15, 0.15, 0.45) for y in (-0.3, 0, 0.3)])
    outer = VGroup(*[Dot([x, y, 0], radius=0.10, color=Space)
                    for x, y in [(-5.2, 1.4), (-5.2, -0.8), (-3.8, 0.4),
                                 (-2.3, 1.6), (-2.3, -0.9)]])
    rays = VGroup(*[DashedLine(dot.get_center(), center, color=Photon, stroke_opacity=0.45)
                   for dot in outer])
    assumed = Label("Assumed central electron concentration", 26, Speculative, 12.1)
    assumed.move_to([0, 2.1, 0])
    population = Label("not a galaxy census", 22, Muted, 5.0).move_to([2.9, -1.27, 0])
    population_note = self.Note("Surrounding stars ≠ interior electrons. Receiver counts alone do not derive flux.")
    self.Narrate(2, Create(hole), FadeIn(inner), FadeIn(outer), Create(rays), FadeIn(assumed),
                 FadeIn(population), FadeIn(population_note), run_time=1.8)
    self.play(FadeOut(Group(hole, inner, outer, rays, assumed, population, population_note)),
              run_time=0.7)
    standard = Card("STANDARD AMPLITUDE SUM", "A = ∫ D[path] exp(i S/ℏ)\nP = |A|²; interference matters",
                    Established, 5.9, 2.7).move_to([-3.25, 0.4, 0])
    proposed = Card("NEW TRANSPORT LAW", "Source / receiver coupling?\nRecoil + causal response?",
                    Speculative, 5.9, 2.7).move_to([3.25, 0.4, 0])
    quantum_note = self.Note("Stationary action ≠ sequential trial routes; no propagation calculation shown")
    self.Narrate(3, FadeIn(standard), FadeIn(proposed), FadeIn(quantum_note))
    self.Finish()


class GRElectronCycle(GRNarratedScene):
  def construct(self):
    self.SetupChapter("ILLUSTRATIVE POSTULATE", Space)
    center = np.array([-3.5, 0.25, 0])
    phase = ValueTracker(0)
    orbit = Circle(radius=1.65, color=Grid, stroke_width=2).move_to(center)
    ring = Circle(radius=1.45, color=Space, stroke_width=4).move_to(center)
    ring.add_updater(lambda m: m.set(width=1.15 + 1.80 * EnergyFractions(phase.get_value())[0]))
    marker = Dot(center + np.array([1.65, 0, 0]), radius=0.12, color=Ink)
    marker.add_updater(lambda m: m.move_to(center + 1.65 * np.array([
      math.cos(math.radians(phase.get_value())), math.sin(math.radians(phase.get_value())), 0])))
    schematic = Label("configuration cartoon\nnot a particle trajectory", 21, Muted, 5.3)
    schematic.move_to([-3.5, -1.80, 0])
    space_outline = Rectangle(width=5.0, height=0.48, color=Space).move_to([3.0, 0.90, 0])
    mass_outline = Rectangle(width=5.0, height=0.48, color=Mass).move_to([3.0, -0.38, 0])
    space_fill = Rectangle(width=5.0, height=0.48, stroke_width=0,
                           fill_color=Space, fill_opacity=0.9).move_to(space_outline)
    mass_fill = Rectangle(width=0.0001, height=0.48, stroke_width=0,
                          fill_color=Mass, fill_opacity=0.9).move_to(mass_outline).align_to(mass_outline, LEFT)
    space_fill.add_updater(lambda m: m.stretch_to_fit_width(
      max(0.0001, 5 * EnergyFractions(phase.get_value())[0])).align_to(space_outline, LEFT))
    mass_fill.add_updater(lambda m: m.stretch_to_fit_width(
      max(0.0001, 5 * EnergyFractions(phase.get_value())[1])).align_to(mass_outline, LEFT))
    labels = VGroup(Label("SPACE ENERGY  ○", 24, Space).move_to([3.0, 1.47, 0]),
                    Label("MASS ENERGY   □", 24, Mass).move_to([3.0, 0.19, 0]))
    state = Label("0°   |   100% space", 27, Space, 6.0).move_to([2.7, -1.35, 0])
    formula = self.Note("σ = [1 + cos(θ/2)] / 2   |   illustrative interpolation, NOT derived")
    self.Narrate(0, Create(orbit), FadeIn(ring), FadeIn(marker), FadeIn(schematic),
                 FadeIn(VGroup(space_outline, mass_outline, space_fill, mass_fill, labels, state)),
                 FadeIn(formula), run_time=1.6)
    duration = self.BeginBeat(1)
    self.play(phase.animate.set_value(360), run_time=max(3.0, duration - 1.5), rate_func=linear)
    next_state = Label("360° |   100% mass", 27, Mass, 6.0).move_to(state)
    self.play(ReplacementTransform(state, next_state), run_time=0.5)
    state = next_state
    self.EndBeat()
    duration = self.BeginBeat(2)
    trigger = WavePath(np.array([-6.1, 0.25, 0]), center + np.array([-0.55, 0, 0]))
    self.play(Create(trigger), run_time=0.8)
    self.play(FadeOut(trigger), phase.animate.set_value(720),
              run_time=max(3.0, duration - 2.3), rate_func=linear)
    next_state = Label("720° |   100% space", 27, Space, 6.0).move_to(state)
    self.play(ReplacementTransform(state, next_state), run_time=0.5)
    self.EndBeat()
    charge = Label("Charge: -e throughout?\nDerive a conserved current.", 23, Photon, 6.4)
    charge.move_to([2.7, -1.95, 0])
    self.Narrate(3, FadeOut(formula), FadeIn(charge))
    self.Finish()


class GRSpinAndMass(GRNarratedScene):
  def construct(self):
    self.SetupChapter("STANDARD ≠ CARTOON", Established)
    center = np.array([-3.6, 0.35, 0])
    angle = ValueTracker(0)
    circle = Circle(radius=1.4, color=Grid, stroke_width=2).move_to(center)
    axes = VGroup(Line(center + LEFT * 1.7, center + RIGHT * 1.7, color=Grid),
                  Line(center + DOWN * 1.7, center + UP * 1.7, color=Grid))
    amplitude = Arrow(center, center + RIGHT * 1.3, buff=0, color=Established)
    amplitude.add_updater(lambda m: m.put_start_and_end_on(center, center + 1.3 * np.array([
      math.cos(-math.radians(angle.get_value()) / 2),
      math.sin(-math.radians(angle.get_value()) / 2), 0])))
    phase_label = Label("one spinor amplitude\nphase exp(-iθ/2)", 22, Muted, 5.0)
    phase_label.move_to([-3.6, -1.75, 0])
    equations = VGroup(Label("STANDARD SPINOR LAW", 25, Established, 6.5, True),
                        Label("U(360°) = -I", 34, Ink),
                        Label("U(720°) = +I", 34, Ink)).arrange(DOWN, buff=0.48)
    equations.move_to([2.8, 0.5, 0])
    note = self.Note("Global sign: same physical ray. Relative sign: interferometry can detect it.")
    duration = self.BeginBeat(0)
    self.play(Create(circle), Create(axes), FadeIn(amplitude), FadeIn(phase_label),
              FadeIn(equations), FadeIn(note), run_time=1.4)
    self.wait(0.5)
    self.play(angle.animate.set_value(360), run_time=3, rate_func=linear)
    self.wait(1.0)
    self.play(angle.animate.set_value(720), run_time=3, rate_func=linear)
    self.EndBeat()
    warning = Label("Two turns alone do NOT derive:\nspin-1/2  •  magnetic moment  •  Fermi statistics",
                    26, Photon, 12.5).move_to([0, -1.95, 0])
    self.Narrate(1, FadeOut(phase_label), FadeOut(note), FadeIn(warning))
    amplitude.clear_updaters()
    self.play(FadeOut(Group(circle, axes, amplitude, equations, warning)), run_time=0.6)
    observed = Card("MEASURED REST ENERGY", "mₑ c² ≈ 511 keV\nObservable mass needs a definition",
                    Established, 5.8, 2.5).move_to([-3.25, 0.4, 0])
    assumed = Card("ASSUMED INTERNAL SPLIT", "Eₛ + Eₘ = E₀\nA fixed sum need not change mass",
                   Space, 5.8, 2.5).move_to([3.25, 0.4, 0])
    note = self.Note("NIST CODATA rest energy | Internal repartition is not a measured mass oscillation")
    self.Narrate(2, FadeIn(observed), FadeIn(assumed), FadeIn(note))
    self.Finish()


class GRGradientAndCenter(GRNarratedScene):
  def construct(self):
    self.SetupChapter("CENTER: SPECULATIVE", Speculative)
    activity = ValueTracker(1)
    phase = ValueTracker(0)
    center = np.array([-3.3, 0.35, 0])
    hole = Circle(radius=1.5, color=Speculative, stroke_width=1.8,
                  fill_color=Panel, fill_opacity=0.8).move_to(center)
    electrons = VGroup()
    for index, (x, y) in enumerate([(-0.45, 0.4), (0.45, 0.4), (-0.45, -0.4), (0.45, -0.4)]):
      base = center + np.array([x, y, 0])
      dot = Dot(base, radius=0.12, color=Mass)
      dot.add_updater(lambda m, base=base, index=index: m.move_to(base + np.array([
        0.22 * activity.get_value() * math.sin(phase.get_value() + index),
        0.16 * activity.get_value() * math.cos(phase.get_value() + index), 0])))
      electrons.add(dot)
    center_label = Label("proposed center", 23, Speculative, 5.0).move_to([-3.3, -1.52, 0])
    gradient = Label("Inward gradient: space / EM  1 → 0", 25, Space, 12.1)
    gradient.move_to([0, 2.15, 0])
    outlines = VGroup(Rectangle(width=4.9, height=0.44, color=Space).move_to([3.15, 0.8, 0]),
                      Rectangle(width=4.9, height=0.44, color=Mass).move_to([3.15, -0.4, 0]))
    space_fill = Rectangle(width=4.9, height=0.44, stroke_width=0,
                           fill_color=Space, fill_opacity=0.8).move_to(outlines[0])
    mass_fill = Rectangle(width=0.0001, height=0.44, stroke_width=0,
                          fill_color=Mass, fill_opacity=0.8).move_to(outlines[1]).align_to(outlines[1], LEFT)
    space_fill.add_updater(lambda m: m.stretch_to_fit_width(max(0.0001, 4.9 * activity.get_value()))
                          .align_to(outlines[0], LEFT))
    mass_fill.add_updater(lambda m: m.stretch_to_fit_width(max(0.0001, 4.9 * (1 - activity.get_value())))
                         .align_to(outlines[1], LEFT))
    bar_labels = VGroup(Label("SPACE / EM OSCILLATION", 23, Space, 5.5).move_to([3.15, 1.34, 0]),
                        Label("MASS STORAGE (schematic)", 23, Mass, 5.5).move_to([3.15, 0.14, 0]))
    state = Label("slowing is a proposed\ninternal motion variable", 22, Muted, 5.7)
    state.move_to([3.15, -1.47, 0])
    note = self.Note("Imposed animation, not dynamics. Bars are not a measured energy budget.")
    self.Narrate(0, Create(hole), FadeIn(electrons), FadeIn(center_label), FadeIn(gradient),
                 FadeIn(outlines), FadeIn(space_fill), FadeIn(mass_fill), FadeIn(bar_labels),
                 FadeIn(state), FadeIn(note), run_time=1.6)
    stopped = Label("EM oscillation → 0\nenergy stored as mass", 23, Mass, 5.7).move_to(state)
    self.BeginBeat(1)
    self.play(phase.animate.set_value(6 * math.pi), activity.animate.set_value(0),
              ReplacementTransform(state, stopped), run_time=4, rate_func=linear)
    self.EndBeat()
    pulse = WavePath(np.array([-6.1, 0.35, 0]), center + np.array([-0.45, 0, 0]))
    restarted = Label("Incoming hit → restart\nspace component returns", 23, Space, 5.7).move_to(stopped)
    self.BeginBeat(2)
    self.play(Create(pulse), run_time=1.2)
    self.play(Indicate(electrons, color=Photon), run_time=0.8)
    self.play(FadeOut(pulse), ReplacementTransform(stopped, restarted),
              phase.animate.set_value(12 * math.pi), activity.animate.set_value(0.65),
              run_time=4, rate_func=linear)
    self.EndBeat()
    space_fill.clear_updaters()
    mass_fill.clear_updaters()
    electrons.clear_updaters(recursive=True)
    self.play(FadeOut(Group(outlines, space_fill, mass_fill, bar_labels, restarted, note)), run_time=0.7)
    questions = Card("UNRESOLVED CENTER DYNAMICS", "Which local motion / clock?\nCharge + recoil + losses?\nAccessible exterior prediction?",
                     Speculative, 5.9, 3.0).move_to([3.15, 0.15, 0])
    caution = self.Note("Zero EM activity ≠ zero total E or local c. Interior mechanism unobserved.", Photon)
    self.Narrate(3, FadeIn(questions), FadeIn(caution))
    self.Finish()


class GRLightSpeedConflict(GRNarratedScene):
  def construct(self):
    self.SetupChapter("UNRESOLVED EQUATIONS", Photon)
    axes = Axes(x_range=[0, 1, 0.25], y_range=[0, 3, 1], x_length=6.8,
                y_length=3.55, tips=False, axis_config={"color": Grid,
                "include_ticks": True, "include_numbers": False})
    axes.move_to([-2.25, 0.1, 0])
    x_label = Label("σ = SPACE-energy fraction", 22, Ink, 7.0).next_to(axes, DOWN, buff=0.38)
    y_label = Label("u = C / c₀", 22, Ink).move_to([-4.9, 2.25, 0])
    tick_labels = VGroup(*[Label(str(value), 18, Muted).next_to(axes.c2p(value, 0), DOWN, buff=0.13)
                          for value in (0, 0.5, 1)],
                         *[Label(str(value), 18, Muted).next_to(axes.c2p(0, value), LEFT, buff=0.15)
                           for value in (1, 2, 3)])
    p1 = axes.plot(lambda sigma: math.sqrt(sigma / (1 - sigma)),
                   x_range=[0, 0.90, 0.006], color=Mass, stroke_width=4)
    bounded_curve = axes.plot(lambda sigma: 2 * math.sqrt(max(0, sigma * (1 - sigma))),
                              x_range=[0, 1, 0.006], color=Space, stroke_width=4)
    bounded = VGroup(*[Line(bounded_curve.point_from_proportion(value),
                           bounded_curve.point_from_proportion(min(value + 0.024, 1)),
                           color=Space, stroke_width=4)
                      for value in np.arange(0, 0.97, 0.042)])
    p1_card = Card("P1  /  SOLID", "u² = σ / (1 - σ)\nDiverges as σ → 1", Mass,
                   4.8, 1.70).move_to([4.2, 1.10, 0])
    bounded_card = Card("FDTD  /  DASHED", "u = 2 √[σ(1 - σ)]\nZero at BOTH endpoints", Space,
                        4.8, 1.70).move_to([4.2, -0.92, 0])
    tail = Arrow(axes.c2p(0.90, 2.8), axes.c2p(0.90, 3.25), color=Mass, buff=0,
                 stroke_width=2)
    self.Narrate(0, Create(axes), FadeIn(x_label), FadeIn(y_label), FadeIn(tick_labels),
                 Create(p1), GrowArrow(tail), FadeIn(p1_card), run_time=2.0)
    self.Narrate(1, Create(bounded), FadeIn(bounded_card), run_time=1.7)
    equal_point = Dot(axes.c2p(0.5, 1), color=Ink, radius=0.08)
    zero_point = Dot(axes.c2p(0, 0), color=Ink, radius=0.08)
    note = self.Note("Equal at σ=1/2; also σ→0 in the endpoint limit. Not equivalent on (0,1).")
    note.move_to([0, -2.62, 0])
    self.Narrate(2, FadeIn(equal_point), FadeIn(zero_point), FadeIn(note))
    self.Finish()


class GRFalsification(GRNarratedScene):
  def construct(self):
    self.SetupChapter("OPEN TESTS", Ink)
    labels = ["1  Define + derive", "2  Budget + losses", "3  Matched controls", "4  Observable prediction"]
    rows = VGroup(*[Card(label, "", Ink, 4.5, 0.74) for label in labels]).arrange(DOWN, buff=0.27)
    rows.move_to([-4.15, 0.25, 0])
    for row in rows:
      row.set_opacity(0.3)
    self.add(rows)
    detail = Card("FIELD MODEL", "Units • action • conserved current\nStable state, not imposed motion", Space,
                  7.2, 2.6).move_to([2.05, 0.35, 0])
    self.Narrate(0, rows[0].animate.set_opacity(1), FadeIn(detail))
    report = json.loads((Root / "input_report.json").read_text(encoding="utf-8"))
    ratio = report["validation"]["feedback_budget"]["feedback_ratio"]
    budget = Card("OLD APPROXIMATION — NOT PHOTON TEST", f"E_feedback / (mₑ c²) = {ratio:.2e}\n"
                  "New driver needs its own flux / loss budget", Photon, 7.2, 2.6)
    budget.move_to(detail)
    self.Narrate(1, rows[0].animate.set_opacity(0.35), rows[1].animate.set_opacity(1),
                 ReplacementTransform(detail, budget))
    controls = Card("MATCHED COMPARISONS", "Photon-driven | no photons | QED/GR\nSame inputs, timing and uncertainties",
                    Established, 7.2, 2.6).move_to(budget)
    self.Narrate(2, rows[1].animate.set_opacity(0.35), rows[2].animate.set_opacity(1),
                 ReplacementTransform(budget, controls))
    prediction = Card("PREDECLARE REJECTION", "Magnetic moment • spectrum • scattering\n"
                      "Reject a SPECIFIED model variant", Mass, 7.2, 2.6).move_to(controls)
    note = self.Note("No measured confirmation shown here. The animation visualizes assumptions.")
    self.Narrate(3, rows[2].animate.set_opacity(0.35), rows[3].animate.set_opacity(1),
                 ReplacementTransform(controls, prediction), FadeIn(note))
    self.Finish()


class GRClosing(GRNarratedScene):
  def construct(self):
    self.SetupChapter("INVITATION TO REVIEW", Established)
    heading = Label("Quantum physicists:\ncritique the mechanism.", 39, Ink, 11.8, True)
    heading.move_to([0, 1.35, 0])
    repo = Label(Repo, 27, Space, 12.4).move_to([0, -0.05, 0])
    issues = Label(Repo + "/issues", 24, Photon, 12.4).move_to([0, -0.78, 0])
    request = Label("Open a GitHub issue ticket\nQuestion + equation + reproducible calculation",
                    23, Muted, 12.0).move_to([0, -1.75, 0])
    self.Narrate(0, FadeIn(heading), Write(repo), FadeIn(issues), FadeIn(request), run_time=2.0)
    thanks = Label("Thank you for your time.", 37, Established, 12.0, True).move_to([0, 1.35, 0])
    self.Narrate(1, ReplacementTransform(heading, thanks))
    self.wait(2.0)
    self.Finish()
