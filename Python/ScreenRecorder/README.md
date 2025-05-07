
# 🎥📸 Python Screen Recorder with Audio Sync

A lightweight Python-based desktop screen recorder with audio capture and perfectly synced final video output using `ffmpeg`.  

---

## 📌 Features:
- Live screen capture preview
- Audio recording via microphone
- Adjustable frame rate and resolution
- Synchronizes video and audio durations automatically
- Outputs final synced MP4 video using `ffmpeg`
- Simple to use — press `q` to stop recording

---

## 🛠️ Technologies Used:
- Python 3
- OpenCV
- MSS (Multi Screen Shot)
- SoundDevice
- SoundFile
- FFmpeg

---

## 📥 Installation:

1️⃣ Install Python dependencies:

```bash
pip install -r requirements.txt
```

2️⃣ Install **FFmpeg** if not installed:

- **Linux (Ubuntu/Kali):**
```bash
sudo apt update && sudo apt install ffmpeg
```

- **Windows:**  
Download and install from [ffmpeg.org](https://ffmpeg.org/download.html)

---

## ▶️ How to Run:

1️⃣ Run the Python script:
```bash
python3 screen_recorder.py
```

2️⃣ A preview window opens — press `q` anytime to stop recording.

3️⃣ The following files will be generated:
- `recording.avi` → raw video
- `audio.wav` → audio recording
- `final_output.mp4` → final video with synced audio

---

## 📦 Output Example:
![screenshot](https://via.placeholder.com/800x400?text=Screen+Recording+Preview)

---

## 👤 Author:
**Aravind**  
[Aarav Profile](https://github.com/aarav-26)

---

## 📄 License:
Open-source — free to use, modify, and distribute.
