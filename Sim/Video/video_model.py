# Copyright AStarship <https://astarship.net>.
"""Illustrative bookkeeping; this module is not a physical electron model."""

import math


def EnergyFractions(phase_degrees: float) -> tuple[float, float]:
  """One chosen interpolation: space at 0°, mass at 360°, space at 720°."""
  space = (1.0 + math.cos(math.radians(phase_degrees) / 2.0)) / 2.0
  return space, 1.0 - space
