#!/usr/bin/env python3
"""
Manim simulation of Solar System with Galactic Motion:
Sun at center, Earth (and other planets) orbiting Sun,
and the entire system orbiting the galactic center.

Relevant Gradient Relativity equations:
- Gravitational equilibrium: GM1/d1^2 = GM2/d2^2, d1+d2 = r.
- Centripetal acceleration from galactic orbit: a_c = Ω^2 R.
- Speed of light normalization: C = 1 at equilibrium, C = sqrt(E_space/E_mass).
- Time dilation relation: 1 = (dx/dt)^2 + (dτ/dt)^2 (when C=1).
- Force vanishes as acceleration → 0: F = m_e a → 0 (black hole limit).
"""