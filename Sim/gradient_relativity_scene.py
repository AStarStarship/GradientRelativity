#!/usr/bin/env python3
"""
Manim Community scene: Gradient Relativity overview, timed to Sim/Script.md.

Render (from repo root, with manim + matplotlib fonts available):
    manim -qm Sim/gradient_relativity_scene.py GRGalacticEquilibrium
    manim -qm Sim/gradient_relativity_scene.py GRCentripetalKick
    manim -qm Sim/gradient_relativity_scene.py GRWhirlpool
    manim -qm Sim/gradient_relativity_scene.py GRSpaceEnergyGradient
    manim -qm Sim/gradient_relativity_scene.py GRCosmologyAndEnd

Scenes:
    GRGalacticEquilibrium : two stars orbiting the galactic center,
                            L1 equilibrium point, comoving electron.
    GRCentripetalKick     : the equilibrium point's centripetal acceleration,
                            electron forced to accelerate, EM wavelet emitted.
    GRWhirlpool           : electron internal whirlpool, space<->mass
                            corkscrew, spin-1/2 (720 degree) statement.
    GRSpaceEnergyGradient : C = sqrt(E_space / E_mass) bar visualization,
                            black-hole limit C -> 0.
    GRCosmologyAndEnd     : expansion + closing summary.
"""

import numpy as np
from manim import *


def _title(text, size=28):
    return Text(text, font_size=size).to_edge(UP)


def _Rotate(mobj, angle, about_point=ORIGIN, **kwargs):
    """Rotate animation about an arbitrary point."""

    class _R(Animation):
        def __init__(self, mobj, angle, about_point, **kw):
            self._angle = angle
            self._about = about_point
            super().__init__(mobj, **kw)

        def interpolate_mobject(self, alpha):
            self.mobject.restore()
            self.mobject.rotate(self._angle * alpha, about_point=self._about)

    return _R(mobj, angle, about_point, **kwargs)


class GRGalacticEquilibrium(Scene):
    def construct(self):
        title = _title("Gradient Relativity")
        self.play(Write(title), run_time=1)

        bh = Dot(radius=0.35, color=YELLOW).move_to(ORIGIN)
        bh_label = Text("galactic center", font_size=20).next_to(bh, DOWN, buff=0.2)

        orbit = Circle(radius=2.6, color=GREY_A, stroke_width=2)
        m1 = Dot(radius=0.25, color=ORANGE).move_to(2.6 * np.array([np.cos(0.9), np.sin(0.9), 0]))
        m2 = Dot(radius=0.2, color=ORANGE).move_to(2.6 * np.array([np.cos(1.4), np.sin(1.4), 0]))
        l1 = Dot(radius=0.12, color=WHITE).move_to(
            2.6 * np.array([np.cos(1.15), np.sin(1.15), 0])
        )
        l1_label = Text("equilibrium (C=1)", font_size=18).next_to(l1, RIGHT)
        e_dot = Dot(radius=0.1, color=BLUE).move_to(l1)
        e_label = Text("electron", font_size=18).next_to(e_dot, LEFT)

        self.play(Create(orbit), GrowFromCenter(bh), run_time=1.5)
        self.play(Write(bh_label), run_time=0.8)
        self.play(GrowFromCenter(m1), GrowFromCenter(m2), run_time=1)
        self.play(
            GrowFromCenter(l1), Write(l1_label),
            GrowFromCenter(e_dot), Write(e_label),
            run_time=1.2,
        )

        binary = VGroup(m1, m2, l1, e_dot)
        self.play(_Rotate(binary, TAU, about_point=ORIGIN, run_time=8), run_time=8)
        self.wait(0.5)


class GRCentripetalKick(Scene):
    def construct(self):
        title = _title("Centripetal acceleration at the equilibrium")
        self.play(Write(title), run_time=1)

        eq = MathTex("a_c = \\Omega_G^2\\, R_G").to_edge(DOWN)
        self.play(Write(eq), run_time=1)

        e_dot = Dot(radius=0.15, color=BLUE).move_to(ORIGIN)
        e_label = Text("electron (comoving)", font_size=20).next_to(e_dot, UP)
        a_vec = Arrow(ORIGIN, 1.8 * LEFT, color=RED, buff=0.2)
        a_label = Text("a_c toward galactic center", font_size=18, color=RED).next_to(a_vec, DOWN)

        self.play(GrowFromCenter(e_dot), Write(e_label), run_time=1)
        self.play(GrowArrow(a_vec), Write(a_label), run_time=1)
        self.play(e_dot.animate.shift(0.15 * LEFT), run_time=0.3)
        self.play(e_dot.animate.shift(0.15 * RIGHT), run_time=0.3)
        self.play(e_dot.animate.shift(0.15 * LEFT), run_time=0.3)

        wavelet = Circle(radius=0.3, color=BLUE, stroke_width=3)
        wavelet.move_to(e_dot)
        self.play(wavelet.animate.scale(4).set_opacity(0), run_time=2)

        cap = Text("radiated EM energy has nowhere to go at C=1", font_size=22)
        cap.next_to(eq, UP, buff=0.4)
        self.play(FadeIn(cap), run_time=1)
        self.wait(1)


class GRWhirlpool(Scene):
    def construct(self):
        title = _title("The whirlpool: mass and spin-1/2 emerge")
        self.play(Write(title), run_time=1)

        spiral = Spiral(rate=0.35, color=BLUE, stroke_width=4)
        spiral.set_width(3)
        self.play(Create(spiral), run_time=2)

        txt1 = Text("two-phase space <-> mass corkscrew", font_size=24)
        txt1.to_edge(UP, buff=1.4)
        txt2 = Text("720 degrees rotation -> spin-1/2", font_size=24).next_to(txt1, DOWN, buff=0.3)
        txt3 = Text("stored oscillation energy -> m = E/c^2 (mass)", font_size=24).next_to(txt2, DOWN, buff=0.3)

        self.play(
            AnimationGroup(
                Write(txt1),
                _Rotate(spiral, 2 * TAU, about_point=ORIGIN, run_time=4),
                run_time=4,
            )
        )
        self.play(Write(txt2), Write(txt3), run_time=2)
        self.wait(1)


class GRSpaceEnergyGradient(Scene):
    def construct(self):
        title = _title("The space-energy gradient")
        self.play(Write(title), run_time=1)

        eq = MathTex("C = \\sqrt{\\frac{E_{\\text{space}}}{E_{\\text{mass}}}}")
        eq.to_edge(UP, buff=0.9)
        self.play(Write(eq), run_time=1.5)

        bar_total = 4.0
        space_bar = Rectangle(width=bar_total, height=0.5, color=BLUE, fill_opacity=0.8)
        space_bar.to_edge(DOWN, buff=1.0).to_edge(LEFT, buff=1.6)
        mass_bar = Rectangle(width=bar_total, height=0.5, color=RED, fill_opacity=0.8)
        mass_bar.next_to(space_bar, DOWN, buff=0.3)
        lbl_s = Text("E_space", font_size=20, color=BLUE).next_to(space_bar, LEFT)
        lbl_m = Text("E_mass", font_size=20, color=RED).next_to(mass_bar, LEFT)

        self.play(GrowFromEdge(space_bar, RIGHT), Write(lbl_s), run_time=1)
        self.play(GrowFromEdge(mass_bar, RIGHT), Write(lbl_m), run_time=1)
        cap = Text("E_space + E_mass = constant", font_size=22).next_to(mass_bar, DOWN)
        self.play(Write(cap), run_time=1)

        bh = Dot(radius=0.3, color=YELLOW).to_corner(DR, buff=1.0)
        bh_l = Text("black hole: C -> 0", font_size=20).next_to(bh, LEFT)
        self.play(GrowFromCenter(bh), Write(bh_l), run_time=1)
        self.play(
            space_bar.animate.set_width(0.01).set_stroke(width=0),
            mass_bar.animate.set_width(bar_total),
            run_time=2,
        )
        self.wait(1)


class GRCosmologyAndEnd(Scene):
    def construct(self):
        title = _title("Cosmology and the big picture")
        self.play(Write(title), run_time=1)

        txt = VGroup(
            Text("The gradient drives expansion", font_size=26),
            Text("mass, spin and gravity = self-interaction of", font_size=26),
            Text("accelerating quanta in the space-energy field", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN, buff=1.2)
        self.play(LaggedStart(*[Write(t) for t in txt], lag_ratio=0.4), run_time=3)

        end = Text("On the Electrodynamics of Gravitational Equilibriums", font_size=24)
        end.to_edge(DOWN, buff=0.4)
        self.wait(1)
        self.play(FadeIn(end), run_time=1)
        self.wait(2)
