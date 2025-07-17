import cv2
import pickle
import cvzone
import numpy as np
import time

cap = cv2.VideoCapture('carPark.mp4')
width, height = 103, 43

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)


parking_times = {}

rate_per_minute = 0.5


def empty(a):
    pass


cv2.namedWindow("Vals")
cv2.resizeWindow("Vals", 640, 240)
cv2.createTrackbar("Val1", "Vals", 25, 50, empty)
cv2.createTrackbar("Val2", "Vals", 16, 50, empty)
cv2.createTrackbar("Val3", "Vals", 5, 50, empty)


def checkSpaces():
    spaces = 0
    current_time = time.time()

    for i, pos in enumerate(posList):
        x, y = pos
        w, h = width, height

        imgCrop = imgThres[y:y + h, x:x + w]
        count = cv2.countNonZero(imgCrop)

        if count < 900:  # Empty slot
            color = (0, 200, 0)
            thic = 5
            spaces += 1

            # If the slot was previously occupied, calculate time parked
            if i in parking_times:
                entry_time = parking_times.pop(i)  # Remove from dict & get entry time
                duration = (current_time - entry_time) / 60  # Convert to minutes
                cost = round(duration * rate_per_minute, 2)  # Calculate fee

                print(f"Car in Slot {i + 1} left. Duration: {round(duration, 2)} min. Cost: ${cost}")

        else:  # Occupied slot
            color = (0, 0, 200)
            thic = 2

            # If the slot is occupied for the first time, save entry time
            if i not in parking_times:
                parking_times[i] = current_time  # Store entry timestamp

        cv2.rectangle(img, (x, y), (x + w, y + h), color, thic)

        # Label parking slot number
        cvzone.putTextRect(img, str(i + 1), (x + w // 2 - 10, y + h // 2), scale=1, thickness=2, colorR=color)

    # Display available slots count
    cvzone.putTextRect(img, f'Free: {spaces}/{len(posList)}', (50, 60), thickness=3, offset=20, colorR=(0, 200, 0))


while True:
    success, img = cap.read()
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)

    val1 = cv2.getTrackbarPos("Val1", "Vals")
    val2 = cv2.getTrackbarPos("Val2", "Vals")
    val3 = cv2.getTrackbarPos("Val3", "Vals")
    if val1 % 2 == 0: val1 += 1
    if val3 % 2 == 0: val3 += 1

    imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, val1, val2)
    imgThres = cv2.medianBlur(imgThres, val3)
    kernel = np.ones((3, 3), np.uint8)
    imgThres = cv2.dilate(imgThres, kernel, iterations=1)

    checkSpaces()

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        pass
