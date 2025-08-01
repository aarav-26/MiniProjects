import cv2
import pickle
import cvzone
import numpy as np

# Video feed
cap = cv2.VideoCapture('carPark.mp4')

# Load parking positions
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 107, 48

# Sorting positions row-wise first (by y, then x for left to right order)
posList.sort(key=lambda p: (p[1], p[0]))

def checkParkingSpace(imgPro, img):
    spaceCounter = 0
    available_slots = []
    
    for idx, pos in enumerate(posList, 1):
        x, y = pos
        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)

        if count < 900:  # Threshold for empty space detection
            color = (0, 255, 0)  # Green for available
            thickness = 5
            spaceCounter += 1
            available_slots.append(str(idx))  # Store available slot number
        else:
            color = (0, 0, 255)  # Red for occupied
            thickness = 2
        
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(idx), (x + 5, y + height - 5), scale=1, thickness=2, offset=0, colorR=color)

    # Show free spaces in a separate window
    available_text = "Available Slots: " + ", ".join(available_slots)
    free_space_display = np.zeros((250, 600, 3), dtype=np.uint8)
    cv2.putText(free_space_display, f"Total Available: {spaceCounter}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Split available slots into multiple lines for better readability
    max_per_line = 10
    for i in range(0, len(available_slots), max_per_line):
        cv2.putText(free_space_display, ", ".join(available_slots[i:i+max_per_line]), (20, 100 + (i//max_per_line) * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Available Parking", free_space_display)

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    success, img = cap.read()
    if not success:
        break
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate, img)

    cv2.imshow("Parking Camera", img)
    cv2.waitKey(10)

