import customtkinter as ctk
import cv2, os, csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime

# Ensure necessary directories exist
def assure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Take Images function
def take_images():
    Id = id_entry.get()
    name = name_entry.get()

    if not Id.isdigit() or name.strip() == "":
        status_label.configure(text="Enter valid ID and Name!")
        return

    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    sampleNum = 0

    assure_path_exists("TrainingImage")

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            sampleNum += 1
            cv2.imwrite(f"TrainingImage/{name}.{Id}.{sampleNum}.jpg", gray[y:y+h, x:x+w])
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Capturing Images [Press q to quit]", img)

        if cv2.waitKey(100) & 0xFF == ord('q') or sampleNum >= 30:
            break

    cam.release()
    cv2.destroyAllWindows()

    assure_path_exists("StudentDetails")
    csv_path = "StudentDetails/StudentDetails.csv"

    if not os.path.isfile(csv_path):
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["SERIAL NO.", "ID", "NAME"])

    serial_no = sum(1 for _ in open(csv_path))  # to get next serial number

    with open(csv_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([serial_no, Id, name])

    status_label.configure(text="Images captured successfully.")

# Train the Model
def train_model():
    assure_path_exists("TrainingImageLabel")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, ids = get_images_and_labels("TrainingImage")

    if len(faces) == 0:
        status_label.configure(text="No images found!")
        return

    recognizer.train(faces, np.array(ids))
    recognizer.save("TrainingImageLabel/Trainer.yml")
    status_label.configure(text="Model trained successfully.")

def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    face_samples, ids = [], []

    for image_path in image_paths:
        img = Image.open(image_path).convert('L')
        img_np = np.array(img, 'uint8')
        id = int(os.path.split(image_path)[-1].split(".")[1])
        face_samples.append(img_np)
        ids.append(id)

    return face_samples, ids

# Track Attendance with Confirmation
def track_attendance():
    assure_path_exists("Attendance")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    try:
        recognizer.read("TrainingImageLabel/Trainer.yml")
    except:
        status_label.configure(text="Train model first!")
        return

    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    df = pd.read_csv("StudentDetails/StudentDetails.csv")

    if "NAME" not in df.columns:
        status_label.configure(text="Invalid CSV header in StudentDetails.")
        return

    cam = cv2.VideoCapture(0)

    attendance_set = set()

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            id_predicted, conf = recognizer.predict(gray[y:y+h, x:x+w])

            if conf < 50:
                row = df.loc[df["ID"] == id_predicted]
                if not row.empty:
                    name = row.iloc[0]["NAME"]
                    label = f"{name} ({id_predicted})"

                    if id_predicted not in attendance_set:
                        cv2.putText(img, f"{label} - Press 'c' to Confirm", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

                        if cv2.waitKey(1) & 0xFF == ord('c'):
                            log_attendance(id_predicted, name)
                            attendance_set.add(id_predicted)
                            status_label.configure(text=f"{name} attendance marked.")
                else:
                    label = f"Unknown ({id_predicted})"
            else:
                label = "Unknown"

            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, label, (x, y-40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

        cv2.imshow("Attendance [Press q to quit, c to confirm]", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    status_label.configure(text="Attendance completed.")

# Log Attendance
def log_attendance(id, name):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    timeStamp = datetime.datetime.now().strftime("%H:%M:%S")
    filename = f"Attendance/Attendance_{date}.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["ID", "NAME", "DATE", "TIME"])
        writer.writerow([id, name, date, timeStamp])

# View Today's Attendance
def view_attendance():
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"Attendance/Attendance_{date}.csv"

    if not os.path.isfile(filename):
        status_label.configure(text="No attendance for today yet.")
        return

    attendance_df = pd.read_csv(filename)

    # New CustomTkinter window
    attendance_window = ctk.CTkToplevel(window)
    attendance_window.title(f"Attendance for {date}")
    attendance_window.geometry("600x400")

    title = ctk.CTkLabel(attendance_window, text=f"Attendance - {date}",
                         font=ctk.CTkFont(size=22, weight="bold"))
    title.pack(pady=10)

    frame = ctk.CTkFrame(attendance_window)
    frame.pack(pady=10, fill="both", expand=True)

    # Header row
    header_text = "ID     |     NAME     |     DATE     |     TIME"
    header_label = ctk.CTkLabel(frame, text=header_text, font=ctk.CTkFont(weight="bold"))
    header_label.pack(anchor="w", padx=10)

    # Divider
    divider = ctk.CTkLabel(frame, text="-"*90)
    divider.pack(anchor="w", padx=10)

    # Attendance rows
    for index, row in attendance_df.iterrows():
    # Convert date to dd-mm-yyyy format
        try:
            date_obj = datetime.datetime.strptime(row['DATE'], "%Y-%m-%d")
            formatted_date = date_obj.strftime("%d-%m-%Y")
        except:
            formatted_date = row['DATE']  # fallback if already in correct format or bad value

        row_text = f"{row['ID']}     |     {row['NAME']}     |     {formatted_date}     |     {row['TIME']}"
        row_label = ctk.CTkLabel(frame, text=row_text, anchor="w")
        row_label.pack(anchor="w", padx=10)

    # Close button
    close_btn = ctk.CTkButton(attendance_window, text="Close", command=attendance_window.destroy)
    close_btn.pack(pady=10)


# CustomTkinter GUI
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("Face Recognition Attendance System")
window.geometry("720x560")

title_label = ctk.CTkLabel(window, text="Face Recognition Attendance System", font=ctk.CTkFont(size=25, weight="bold"))
title_label.pack(pady=20)

frame_right = ctk.CTkFrame(window)
frame_right.pack(pady=10)

id_label = ctk.CTkLabel(frame_right, text="Enter ID:")
id_label.grid(row=0, column=0, padx=10, pady=10)
id_entry = ctk.CTkEntry(frame_right)
id_entry.grid(row=0, column=1, padx=10, pady=10)

name_label = ctk.CTkLabel(frame_right, text="Enter Name:")
name_label.grid(row=1, column=0, padx=10, pady=10)
name_entry = ctk.CTkEntry(frame_right)
name_entry.grid(row=1, column=1, padx=10, pady=10)

btn_frame = ctk.CTkFrame(window)
btn_frame.pack(pady=20)

capture_btn = ctk.CTkButton(btn_frame, text="Take Images", command=take_images, width=220)
capture_btn.grid(row=0, column=0, padx=20, pady=10)

train_btn = ctk.CTkButton(btn_frame, text="Train Model", command=train_model, width=220)
train_btn.grid(row=1, column=0, padx=20, pady=10)

track_btn = ctk.CTkButton(btn_frame, text="Track Attendance", command=track_attendance, width=220)
track_btn.grid(row=2, column=0, padx=20, pady=10)

view_attendance_btn = ctk.CTkButton(btn_frame, text="View Today's Attendance", command=view_attendance, width=220)
view_attendance_btn.grid(row=3, column=0, padx=20, pady=10)

exit_btn = ctk.CTkButton(btn_frame, text="Exit", command=window.destroy, width=220, fg_color="red")
exit_btn.grid(row=4, column=0, padx=20, pady=10)

status_label = ctk.CTkLabel(window, text="")
status_label.pack(pady=10)

window.mainloop()
