import os
import subprocess
import sys
import zipfile
import smtplib
from email.message import EmailMessage
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

def create_mashup(singer, count, duration, email):
    os.makedirs("temp_files/videos", exist_ok=True)
    os.makedirs("temp_files/clips", exist_ok=True)

    query = f"ytsearch{count}:{singer} songs"

    subprocess.run([
        sys.executable, "-m", "yt_dlp",
        "-f", "bestaudio",
        "-o", "temp_files/videos/%(id)s.%(ext)s",
        query
    ], check=True)

    video_files = os.listdir("temp_files/videos")
    clips = []

    for i, v in enumerate(video_files):
        clip = f"clip{i}.mp3"
        subprocess.run([
            FFMPEG, "-y",
            "-i", f"temp_files/videos/{v}",
            "-t", str(duration),
            "-vn",
            f"temp_files/clips/{clip}"
        ])
        clips.append(clip)

    with open("temp_files/clips/list.txt", "w") as f:
        for c in clips:
            f.write(f"file '{c}'\n")

    subprocess.run([
        FFMPEG, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "list.txt",
        "-c", "copy",
        "final_mashup.mp3"
    ], cwd="temp_files/clips")

    zip_name = "mashup_output.zip"
    with zipfile.ZipFile(zip_name, "w") as z:
        z.write("temp_files/clips/final_mashup.mp3")

    msg = EmailMessage()
    msg["Subject"] = "Your Mashup"
    msg["From"] = os.environ["SENDER_EMAIL"]
    msg["To"] = email
    msg.set_content("Mashup attached")

    with open(zip_name, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="zip", filename=zip_name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.environ["SENDER_EMAIL"], os.environ["APP_PASSWORD"])
        server.send_message(msg)
