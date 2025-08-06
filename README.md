# 🎛️ Gesture-Based Volume Control

A computer vision project that lets you control system volume using your fingers and webcam.

---

## 🚀 Features

- Control volume by changing distance between thumb and index finger
- Real-time hand tracking using webcam
- Volume percentage and bar display
- Smooth and jitter-free volume updates

---

## 🧠 How It Works

- Tracks your hand using Mediapipe
- Measures the distance between **thumb** and **index finger**
- Maps that distance to system volume (closer = lower, farther = higher)
- Updates system volume in real-time

---

## 🛠️ Tech Stack

- Python
- OpenCV
- Mediapipe
- Pycaw (for volume control on Windows)

---

## ▶️ How to Run

Clone the repo, install dependencies, run the main.py file:

```bash
git clone https://github.com/yourusername/gesture-volume-control.git
cd gesture-volume-control
pip install -r requirements.txt
python main.py

