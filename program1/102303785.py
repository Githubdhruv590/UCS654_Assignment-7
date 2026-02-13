import sys
import os
import subprocess

FFMPEG = r"C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"

if len(sys.argv) != 5:
    print('Usage: python 102303785.py "SingerName" <NoOfVideos> <Duration> <OutputFile>')
    sys.exit(1)

singer = sys.argv[1]
count = int(sys.argv[2])
duration = int(sys.argv[3])
output = sys.argv[4]

if count <= 10 or duration <= 20:
    print("Invalid input values")
    sys.exit(1)

os.makedirs("videos", exist_ok=True)
os.makedirs("clips", exist_ok=True)

query = f"ytsearch{count}:{singer} songs"

subprocess.run([
    sys.executable, "-m", "yt_dlp",
    "-f", "best",
    "-o", "videos/%(id)s.%(ext)s",
    query
], check=True)

video_files = os.listdir("videos")
clip_files = []

for i, v in enumerate(video_files):
    clip_name = f"clip{i}.mp3"
    clip_path = os.path.join("clips", clip_name)
    subprocess.run([
        FFMPEG, "-y",
        "-i", os.path.join("videos", v),
        "-t", str(duration),
        "-vn",
        clip_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    clip_files.append(clip_name)

with open("clips/list.txt", "w") as f:
    for c in clip_files:
        f.write(f"file '{c}'\n")

subprocess.run([
    FFMPEG, "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", "list.txt",
    "-c", "copy",
    output
], cwd="clips", check=True)

print("Mashup created:", output)
