# Parking Slot Detection using OpenCV and Deep Learning

This project aims to automate the detection of available parking spaces in a parking lot using computer vision techniques. By analyzing live or recorded video streams, the system identifies free and occupied slots with high accuracy.

---

## Project Objectives

- Detect and track individual parking spaces in a given frame or video
- Classify each slot as "occupied" or "available"
- Provide real-time visualization of slot availability
- Optional: Generate alerts or statistics on slot usage

---

## Features

- Region of Interest (ROI) marking for fixed parking lots
- Background subtraction and contour detection using OpenCV
- Optional deep learning model integration (e.g., YOLOv5 or MobileNet)
- Visual output with color-coded slot overlays

---
## Technologies Used

- Python 3.8+
- OpenCV for image processing
- NumPy for matrix operations
- Matplotlib for debugging visualizations
- Optional: PyTorch/TensorFlow for deep learning-based classification

---

## How It Works

1. Load the parking lot video or image frames
2. Define parking slot ROIs manually (or auto-detect in future updates)
3. For each frame:
   - Crop out each slot
   - Perform thresholding or inference to determine occupancy
4. Overlay results and update visualization

---

## Limitations

- Current implementation assumes fixed-angle cameras
- ROI setup is manual
- Shadows and lighting changes may affect accuracy

---

## Future Improvements

- Automatic ROI detection using object detection models
- Real-time processing from IP camera feed
- Cloud dashboard integration for smart city parking systems
