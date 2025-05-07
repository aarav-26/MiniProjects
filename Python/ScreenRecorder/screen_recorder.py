import cv2
import numpy as np
import mss
import sounddevice as sd
import soundfile as sf
import threading
import time
import subprocess

# Settings
resolution = (1920, 1080)
fps = 30.0
video_filename = "recording.avi"
audio_filename = "audio.wav"
output_filename = "final_output.mp4"

# Video writer
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter(video_filename, fourcc, fps, resolution)

# Audio settings
samplerate = 44100
channels = 2
audio_data = []

def record_audio():
    def callback(indata, frames, time_info, status):
        if status:
            print(status)
        audio_data.append(indata.copy())

    with sd.InputStream(samplerate=samplerate, channels=channels, callback=callback):
        while recording:
            time.sleep(0.1)

# Start audio thread
recording = True
audio_thread = threading.Thread(target=record_audio)
audio_thread.start()

# Screen capture
with mss.mss() as sct:
    monitor = sct.monitors[1]  # Fullscreen

    cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Live", 480, 270)

    frame_duration = 1 / fps
    next_frame_time = time.time()
    frame_count = 0  # <--- count frames

    try:
        while True:
            current_time = time.time()

            if current_time >= next_frame_time:
                img = np.array(sct.grab(monitor))
                frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

                out.write(frame)
                frame_count += 1  # increment frame count

                cv2.imshow("Live", frame)
                next_frame_time += frame_duration

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            sleep_time = next_frame_time - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        pass

# Stop recording
recording = False
audio_thread.join()
out.release()
cv2.destroyAllWindows()

# Save audio file
audio_array = np.concatenate(audio_data, axis=0)
sf.write(audio_filename, audio_array, samplerate)

# Calculate durations
audio_info = sf.info(audio_filename)
audio_duration = audio_info.frames / audio_info.samplerate
video_duration = frame_count / fps

print(f"🎥 Video duration: {video_duration:.2f} sec")
print(f"🎵 Audio duration: {audio_duration:.2f} sec")

# Calculate speed adjustment factor
speed_factor = audio_duration / video_duration
print(f"⏳ Speed adjustment factor: {speed_factor:.4f}")

# Merge with ffmpeg, adjusting video speed
subprocess.call([
    'ffmpeg', '-y',
    '-i', video_filename,
    '-i', audio_filename,
    '-filter:v', f"setpts={speed_factor}*PTS",
    '-c:a', 'aac',
    '-strict', 'experimental',
    output_filename
])

print("✅ Recording complete — Saved as:", output_filename)
