# Multimedia Analyser

Multimedia subject project - 3 tools in one Flask app.

1. Image Analyser - shows format, dimensions, size (using Pillow)
2. Video Analyser - shows resolution, fps, duration (using OpenCV)
3. Audio Analyser - shows duration, bitrate (using Mutagen)

New dark theme with gradient glow, subtle grain texture and orange/purple accents. Each tool also shows a preview of the uploaded file.

## Project structure

```
app.py              # Flask backend (unchanged)
requirements.txt
templates/          # base.html, index.html, image.html, video.html, audio.html
static/style.css    # theme (colors, texture, layout)
uploads/            # created automatically on first run
```

## How to run

```
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in browser.
