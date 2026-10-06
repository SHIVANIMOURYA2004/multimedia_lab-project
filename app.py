from flask import Flask, request, render_template, send_from_directory
from PIL import Image
import cv2
import os
from mutagen import File as MutagenFile

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# home page
@app.route("/")
def home():
    return render_template("index.html")


# serve uploaded files so we can show preview (image/video/audio)
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# ---------------- IMAGE ANALYSER ----------------
@app.route("/image", methods=["GET", "POST"])
def image_analyser():
    data = None
    if request.method == "POST":
        file = request.files["file"]
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        img = Image.open(filepath)
        size_kb = os.path.getsize(filepath) / 1024

        data = {
            "filename": file.filename,
            "format": img.format,
            "mode": img.mode,
            "width": img.width,
            "height": img.height,
            "size_kb": round(size_kb, 2),
        }
    return render_template("image.html", data=data)


# ---------------- VIDEO ANALYSER ----------------
@app.route("/video", methods=["GET", "POST"])
def video_analyser():
    data = None
    if request.method == "POST":
        file = request.files["file"]
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        cap = cv2.VideoCapture(filepath)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

        duration = total_frames / fps if fps else 0
        size_mb = os.path.getsize(filepath) / (1024 * 1024)

        data = {
            "filename": file.filename,
            "width": width,
            "height": height,
            "fps": round(fps, 2),
            "frames": total_frames,
            "duration": round(duration, 2),
            "size_mb": round(size_mb, 2),
        }
    return render_template("video.html", data=data)


# ---------------- AUDIO ANALYSER ----------------
@app.route("/audio", methods=["GET", "POST"])
def audio_analyser():
    data = None
    if request.method == "POST":
        file = request.files["file"]
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        audio = MutagenFile(filepath)
        duration = audio.info.length if audio else 0
        bitrate = getattr(audio.info, "bitrate", 0) if audio else 0
        size_kb = os.path.getsize(filepath) / 1024

        data = {
            "filename": file.filename,
            "duration": round(duration, 2),
            "bitrate": round(bitrate / 1000, 1),
            "size_kb": round(size_kb, 2),
        }
    return render_template("audio.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)