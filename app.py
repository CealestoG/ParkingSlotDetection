from flask import Flask, render_template, jsonify
import cv2
import pickle
import cvzone
import numpy as np
import time
import threading
import base64

app = Flask(__name__)

# Initialize your parking system
cap = cv2.VideoCapture('carPark.mp4')
width, height = 103, 43

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

parking_times = {}
rate_per_minute = 0.5
parking_data = {
    'available_spaces': 0,
    'total_spaces': len(posList),
    'parking_slots': [],
    'frame': None
}


def process_parking():
    while True:
        success, img = cap.read()
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
        imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
        imgThres = cv2.medianBlur(imgThres, 5)
        kernel = np.ones((3, 3), np.uint8)
        imgThres = cv2.dilate(imgThres, kernel, iterations=1)

        current_time = time.time()
        spaces = 0
        slots = []

        for i, pos in enumerate(posList):
            x, y = pos
            w, h = width, height
            imgCrop = imgThres[y:y + h, x:x + w]
            count = cv2.countNonZero(imgCrop)

            if count < 900:
                color = (0, 200, 0)
                thic = 5
                spaces += 1
                status = "Available"

                if i in parking_times:
                    entry_time = parking_times.pop(i)
                    duration = (current_time - entry_time) / 60
                    cost = round(duration * rate_per_minute, 2)
                    print(f"Car in Slot {i + 1} left. Duration: {round(duration, 2)} min. Cost: ${cost}")
            else:
                color = (0, 0, 200)
                thic = 2
                status = "Occupied"
                if i not in parking_times:
                    parking_times[i] = current_time

            cv2.rectangle(img, (x, y), (x + w, y + h), color, thic)
            cvzone.putTextRect(img, str(i + 1), (x + w // 2 - 10, y + h // 2), scale=1, thickness=2, colorR=color)

            slots.append({
                'number': i + 1,
                'status': status,
                'duration': round((current_time - parking_times[i]) / 60, 2) if i in parking_times else 0,
                'cost': round((current_time - parking_times[i]) / 60 * rate_per_minute, 2) if i in parking_times else 0
            })

        cv2.putText(img, f'Free: {spaces}/{len(posList)}', (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 0), 3)

        _, buffer = cv2.imencode('.jpg', img)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')

        parking_data['available_spaces'] = spaces
        parking_data['parking_slots'] = slots
        parking_data['frame'] = frame_base64


# Start processing thread
processing_thread = threading.Thread(target=process_parking)
processing_thread.daemon = True
processing_thread.start()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def get_data():
    return jsonify(parking_data)


if __name__ == '__main__':
    app.run(debug=True)