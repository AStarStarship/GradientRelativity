# Copyright AStarship <https://astarship.net>.
"""Sequential, restartable narrated render. Run with the Manim virtualenv Python."""
import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

Root = Path(__file__).resolve().parent


def CaptionTime(seconds):
  if seconds < 0:
    raise ValueError("Caption time cannot be negative")
  milliseconds = round(seconds * 1000)
  hours, milliseconds = divmod(milliseconds, 3600000)
  minutes, milliseconds = divmod(milliseconds, 60000)
  seconds, milliseconds = divmod(milliseconds, 1000)
  return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def Probe(path):
  return json.loads(subprocess.check_output([
    "ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)
  ], text=True))


async def Audio(document):
  import edge_tts
  directory = Root / "media" / "narration"
  directory.mkdir(parents=True, exist_ok=True)
  timing_path = directory / "timing.json"
  timings = json.loads(timing_path.read_text())["beats"] if timing_path.exists() else {}
  for scene in document["scenes"]:
    for beat in scene["beats"]:
      digest = hashlib.sha256((beat["text"] + document["voice"] + document["rate"]).encode()).hexdigest()
      clip = directory / (beat["id"] + ".mp3")
      if beat["id"] in timings and timings[beat["id"]].get("sha256") == digest and clip.exists():
        continue
      print("Narrating", beat["id"], flush=True)
      communicator = edge_tts.Communicate(beat["text"], document["voice"], rate=document["rate"],
                                         boundary="WordBoundary")
      words = []
      with clip.open("wb") as output:
        async for event in communicator.stream():
          if event["type"] == "audio":
            output.write(event["data"])
          elif event["type"] == "WordBoundary":
            words.append({"start": event["offset"] / 10000000,
                          "end": (event["offset"] + event["duration"]) / 10000000,
                          "text": event["text"]})
      duration = float(Probe(clip)["format"]["duration"])
      cues = []
      for index in range(0, len(words), 10):
        group = words[index:index + 10]
        cues.append({"start": group[0]["start"], "end": group[-1]["end"],
                     "text": " ".join(word["text"] for word in group)})
      if not cues:
        raise RuntimeError("TTS returned no caption timing")
      timings[beat["id"]] = {"duration": duration, "audio_file": clip.name,
                              "sha256": digest, "cues": cues}
      timing_path.write_text(json.dumps({"provider": "edge-tts", "beats": timings}, indent=2))
  return timings


def Main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--audio-only", action="store_true")
  parser.add_argument("--quality", choices=["draft", "final"], default="draft")
  parser.add_argument("--scene", help="Render only this chapter")
  parser.add_argument("--assemble-only", action="store_true", help="Reuse existing scene MP4 files")
  args = parser.parse_args()
  document = json.loads((Root / "narration.json").read_text())
  timings = asyncio.run(Audio(document))
  if args.audio_only:
    return
  os.environ.update({"OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"})
  resolution, fps = (("854,480", 15) if args.quality == "draft" else ("1920,1080", 30))
  tag = f"{resolution.split(',')[1]}p{fps}"
  scenes = [scene for scene in document["scenes"] if not args.scene or scene["class_name"] == args.scene]
  if not scenes:
    raise ValueError("Unknown scene")
  for scene in scenes:
    if args.assemble_only:
      continue
    subprocess.run([sys.executable, "-m", "manim", "--renderer", "cairo", "--media_dir",
                    str(Root / "media"), "--resolution", resolution, "--fps", str(fps),
                    "--verbosity", "WARNING", str(Root / "gradient_relativity.py"),
                    scene["class_name"]], cwd=Root, check=True)
  if args.scene:
    return
  clips = [Root / "media" / "videos" / "gradient_relativity" / tag /
           (scene["class_name"] + ".mp4") for scene in scenes]
  concatenate = Root / "media" / f"concat_{args.quality}.txt"
  concatenate.write_text("\n".join(f"file '{clip}'" for clip in clips) + "\n")
  final = Root / f"gradient_relativity_{args.quality}.mp4"
  subprocess.run(["ffmpeg", "-v", "warning", "-y", "-threads", "2", "-f", "concat", "-safe", "0",
                  "-i", str(concatenate), "-c", "copy", "-movflags", "+faststart", str(final)], check=True)
  offset = 0.0
  subtitles = []
  chapters = []
  audio_events = []
  for scene, clip in zip(scenes, clips):
    chapters.append({"title": scene["title"], "start": offset})
    record = json.loads((Root / "media" / "scene_timing" /
                         f"{scene['class_name']}_{tag}.json").read_text())
    for beat in record["beats"]:
      audio_events.append((Root / "media" / "narration" / timings[beat["id"]]["audio_file"],
                           offset + beat["audio_start"]))
      for cue in timings[beat["id"]]["cues"]:
        start = offset + beat["audio_start"] + cue["start"]
        end = offset + beat["audio_start"] + cue["end"]
        subtitles.append(f"{len(subtitles)+1}\n{CaptionTime(start)} --> {CaptionTime(end)}\n{cue['text']}\n")
    offset += float(Probe(clip)["format"]["duration"])
  final.with_suffix(".srt").write_text("\n".join(subtitles))
  import re
  vtt = re.sub(r"(\d\d:\d\d:\d\d),(\d\d\d)", r"\1.\2", "\n".join(subtitles))
  final.with_suffix(".vtt").write_text("WEBVTT\n\n" + vtt)
  (Root / f"chapters_{args.quality}.json").write_text(json.dumps(chapters, indent=2))
  # Manim can skip add_sound after a cached animation. Reconstruct the complete
  # soundtrack from measured beat events, independently of renderer cache state.
  muxed = Root / "media" / f"muxed_{args.quality}.mp4"
  command = ["ffmpeg", "-v", "warning", "-y", "-threads", "2", "-i", str(final)]
  filters = []
  for index, (audio_file, start) in enumerate(audio_events, 1):
    command.extend(["-i", str(audio_file)])
    filters.append(f"[{index}:a]adelay={round(start * 1000)}:all=1[a{index}]")
  labels = "".join(f"[a{index}]" for index in range(1, len(audio_events) + 1))
  filters.append(labels + f"amix=inputs={len(audio_events)}:normalize=0,volume=-1dB,apad[audio]")
  command.extend(["-filter_complex_threads", "1", "-filter_complex", ";".join(filters),
                  "-map", "0:v:0", "-map", "[audio]", "-c:v", "copy", "-c:a", "aac",
                  "-b:a", "192k", "-t", str(offset), "-movflags", "+faststart", str(muxed)])
  subprocess.run(command, check=True)
  muxed.replace(final)
  probe = Probe(final)
  if not any(stream["codec_type"] == "audio" for stream in probe["streams"]):
    raise RuntimeError("Missing audio stream")
  subprocess.run(["ffmpeg", "-v", "error", "-threads", "2", "-i", str(final), "-f", "null", "-"], check=True)
  report = {"file": str(final), "probe": probe, "full_decode": "passed",
            "sha256": hashlib.sha256(final.read_bytes()).hexdigest(), "caption_count": len(subtitles)}
  (Root / f"verification_{args.quality}.json").write_text(json.dumps(report, indent=2))
  print(json.dumps(report, indent=2))


if __name__ == "__main__":
  Main()
