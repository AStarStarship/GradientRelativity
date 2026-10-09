# Copyright AStarship <https://astarship.net>.
"""Export script and validate captions/audio against finished media, without rendering."""
import json
from pathlib import Path
import re
import subprocess

Root = Path(__file__).resolve().parent
script = json.loads((Root / "narration.json").read_text())
transcript = ["# " + script["title"], "", "Narration: synthesized, not the author's recorded voice.", ""]
for chapter in script["scenes"]:
  transcript.extend(["## " + chapter["title"], ""])
  transcript.extend(beat["text"] + "\n" for beat in chapter["beats"])
(Root / "script.md").write_text("\n".join(transcript))
final = Root / "gradient_relativity_final.mp4"
if not final.exists():
  raise SystemExit("Final video is not ready")
report = json.loads((Root / "verification_final.json").read_text())
duration = float(report["probe"]["format"]["duration"])
subtitles = final.with_suffix(".srt").read_text()

def Seconds(value):
  hours, minutes, seconds, milliseconds = map(int, re.split(r"[:,]", value))
  return hours * 3600 + minutes * 60 + seconds + milliseconds / 1000

intervals = re.findall(r"(\d\d:\d\d:\d\d,\d\d\d) --> (\d\d:\d\d:\d\d,\d\d\d)", subtitles)
previous = 0
for start, end in intervals:
  start, end = Seconds(start), Seconds(end)
  if not previous <= start < end <= duration + 0.05:
    raise RuntimeError(f"Invalid caption interval: {start}, {end}; previous {previous}")
  previous = end
# Replace only timestamp commas, never punctuation in the caption text.
vtt = re.sub(r"(\d\d:\d\d:\d\d),(\d\d\d)", r"\1.\2", subtitles)
final.with_suffix(".vtt").write_text("WEBVTT\n\n" + vtt)
chapters = json.loads((Root / "chapters_final.json").read_text())
chapter_copy = []
for chapter in chapters:
  total = int(chapter["start"])
  minutes, seconds = divmod(total, 60)
  chapter_copy.append(f"{minutes:02}:{seconds:02} {chapter['title']}")
(Root / "youtube_chapters.txt").write_text("\n".join(chapter_copy) + "\n")
audio = subprocess.run(["ffmpeg", "-hide_banner", "-threads", "2", "-i", str(final),
  "-vn", "-af", "volumedetect,silencedetect=noise=-45dB:d=5", "-f", "null", "-"],
  text=True, capture_output=True, check=True).stderr
(Root / "audio_check.log").write_text(audio)
peak = re.search(r"max_volume: ([-\d.]+) dB", audio)
if not peak or not -40 < float(peak[1]) < 0:
  raise RuntimeError("Audio peak missing, silent, or clipped")
long_silences = re.findall(r"silence_duration: ([\d.]+)", audio)
checks = {"duration_seconds": duration, "caption_count": len(intervals),
          "captions_monotonic_and_in_duration": True, "max_volume_db": float(peak[1]),
          "long_silence_durations": list(map(float, long_silences)),
          "human_viewing_or_listening": False}
(Root / "publication_checks.json").write_text(json.dumps(checks, indent=2))
print(json.dumps(checks, indent=2))
