# Copyright AStarship <https://astarship.net>.
"""Execute the actual draft scene code and record visible text bounds at beat ends."""
import json
import sys
from pathlib import Path
from manim import Text, config
import gradient_relativity as video

Root = Path(__file__).resolve().parent
Original = video.GRNarratedScene.EndBeat
records = []
if len(sys.argv) > 1 and (Root / "layout_audit.json").exists():
  records = [record for record in json.loads((Root / "layout_audit.json").read_text())["records"]
             if record["scene"] != sys.argv[1]]


def Check(scene):
  Original(scene)
  labels = []
  for root in scene.mobjects:
    for item in root.get_family():
      if isinstance(item, Text) and item.get_fill_opacity() > 0.15:
        labels.append({"text": item.text, "left": float(item.get_left()[0]),
                       "right": float(item.get_right()[0]), "top": float(item.get_top()[1]),
                       "bottom": float(item.get_bottom()[1])})
  errors = [label for label in labels if label["left"] < -7.12 or label["right"] > 7.12
            or label["bottom"] < -4 or label["top"] > 4]
  records.append({"scene": type(scene).__name__, "time": scene.time,
                  "text_bounds": labels, "offscreen_text": errors})


video.GRNarratedScene.EndBeat = Check
config.pixel_width = 854
config.pixel_height = 480
config.frame_rate = 15
config.media_dir = str(Root / "media")
config.verbosity = "WARNING"
for chapter in video.Document["scenes"]:
  if len(sys.argv) > 1 and chapter["class_name"] != sys.argv[1]:
    continue
  getattr(video, chapter["class_name"])().render()
errors = sum(len(record["offscreen_text"]) for record in records)
(Root / "layout_audit.json").write_text(json.dumps({"beat_count": len(records),
  "offscreen_count": errors, "records": records}, indent=2))
print(f"Audited {len(records)} beat endpoints: {errors} offscreen text labels")
if errors:
  raise SystemExit(1)
