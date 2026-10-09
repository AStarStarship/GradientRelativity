# Copyright AStarship <https://astarship.net>.
"""Contract tests for the illustrative phase cycle, not tests of its physical truth."""

import importlib.util
import json
import math
from pathlib import Path
import unittest


class TPhaseContract(unittest.TestCase):
  def test_phase_endpoints_and_conserved_bookkeeping(self):
    path = Path(__file__).with_name("video_model.py")
    self.assertTrue(path.is_file(), "The video phase model has not been implemented")
    spec = importlib.util.spec_from_file_location("video_model", path)
    assert spec is not None and spec.loader is not None
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    for phase, expected in [(0, (1, 0)), (360, (0, 1)), (720, (1, 0))]:
      space, mass = model.EnergyFractions(phase)
      self.assertAlmostEqual(space, expected[0])
      self.assertAlmostEqual(mass, expected[1])
    for phase in range(-720, 1441, 7):
      space, mass = model.EnergyFractions(phase)
      self.assertAlmostEqual(space + mass, 1.0)
      self.assertGreaterEqual(space, 0.0)
      self.assertLessEqual(space, 1.0)
      self.assertAlmostEqual(model.EnergyFractions(phase + 720)[0], space)
    self.assertFalse(math.isclose(model.EnergyFractions(0)[0],
                                  model.EnergyFractions(360)[0]))

  def test_narration_has_independently_renderable_manim_scenes(self):
    path = Path(__file__).with_name("gradient_relativity.py")
    self.assertTrue(path.is_file(), "The Manim storyboard has not been implemented")
    spec = importlib.util.spec_from_file_location("gradient_relativity", path)
    assert spec is not None and spec.loader is not None
    scenes = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scenes)
    document = json.loads(Path(__file__).with_name("narration.json").read_text())
    for scene in document["scenes"]:
      scene_class = getattr(scenes, scene["class_name"])
      self.assertTrue(issubclass(scene_class, scenes.Scene))
      self.assertIn("construct", scene_class.__dict__)

  def test_render_pipeline_creates_valid_caption_timecodes(self):
    path = Path(__file__).with_name("render_video.py")
    self.assertTrue(path.is_file(), "The render pipeline has not been implemented")
    spec = importlib.util.spec_from_file_location("render_video", path)
    assert spec is not None and spec.loader is not None
    pipeline = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pipeline)
    self.assertEqual(pipeline.CaptionTime(0), "00:00:00,000")
    self.assertEqual(pipeline.CaptionTime(65.4321), "00:01:05,432")
    self.assertEqual(pipeline.CaptionTime(3599.9998), "01:00:00,000")
    with self.assertRaises(ValueError):
      pipeline.CaptionTime(-1)


if __name__ == "__main__":
  unittest.main()
