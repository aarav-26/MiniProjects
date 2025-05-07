
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

### 📌 Execution Steps for Client:

1️⃣ **Download or clone the repository**
```bash
git clone https://github.com/aarav-26/MiniProjects.git
cd MiniProjects/Python/ScreenRecorder
```

2️⃣ **Install the required Python libraries**
```bash
pip install -r requirements.txt
```

3️⃣ **Ensure `ffmpeg` is installed and available in system PATH**

- Check if installed:
```bash
ffmpeg -version
```
- If not installed, follow the instructions in the Installation section above.

4️⃣ **Run the Python screen recorder script**
```bash
python3 screen_recorder.py
```

5️⃣ **During recording:**
- A live preview window titled `Live` will open.
- Press **`q`** in the preview window anytime to stop recording.

6️⃣ **After stopping:**
- `recording.avi` → raw screen recording
- `audio.wav` → audio recording from mic
- `final_output.mp4` → final video with audio perfectly synced to video (processed via ffmpeg)

7️⃣ **Play final output**
```bash
ffplay final_output.mp4
```
(*or open with any video player*)

---

## 📦 Output Example:
![screenshot](https://via.placeholder.com/800x400?text=Screen+Recording+Preview)

---

## 👤 Author:
**Aravind**  
[GitHub: aarav-26](https://github.com/aarav-26)

---

## 📄 License:
Open-source — free to use, modify, and distribute.
