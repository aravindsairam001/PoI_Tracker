# 🧍 Human Detection, Tracking & Highlighting System

This project is an end-to-end pipeline that:
- Detects people in a video stream
- Tracks each individual using a unique ID
- Starts/stops recording when people appear/disappear
- Saves tracking logs as JSON
- Provides a GUI for users to select a specific track ID and generate a highlight video showing the movement path of a specific individual

> Built using **YOLOv5**, **DeepSORT**, **OpenCV**, and **Tkinter**.

---

## 🚀 Features

✅ Detects humans in video using YOLOv5  
✅ Tracks people with unique track IDs (DeepSORT)  
✅ Automatically starts/stops video recording when people enter/exit the frame  
✅ Saves bounding box & track data in `.json`  
✅ GUI to input track ID and visualize their motion with a red path  
✅ Saves highlight video with the selected person tracked  

---

## 📁 Project Structure
```bash
human_tracker_project/
├── tracker_with_JSON.py                   # YOLO + DeepSORT script: detects, tracks, and saves outputs
├── Tracker_GUI.py                         # GUI: visualize tracks, highlight PoI, gray out others
├── requirements.txt                       # Python dependencies
├── README.md
├── recordings/                            # Output folder with all tracking artifacts
│   ├── tracking_yyyy-mm-dd-HH-MM-SS.mp4   # Video of the session (e.g. tracking_2025-07-07-10-30-03.mp4)
│   ├── tracking_output.json               # JSON file with movement data and track IDs
│   └── highlighted_1_yyyy-mm-dd-HH-MM-SS.png  # Visualization of highlighted track_id=1 (e.g. highlighted_1_2025-07-07_10-35-59.png)
```
---

## 🧠 Models Used

### 🟡 YOLOv5 (ultralytics)
- Model: `yolov5su.pt`
- Task: Detect `person` class from video frames
- Confidence threshold: `0.6`
- Automatically downloaded via `ultralytics.YOLO()`

### 🟢 DeepSORT (deep_sort_realtime)
- Purpose: Assign persistent IDs to detected people
- Helps in maintaining consistent identity even with occlusion or re-entry
- Tracks saved as JSON with:
  - Frame number
  - Track ID
  - Bounding box

---

## 💻 Installation

1. **Clone this repository**
```bash
git clone https://github.com/your-username/human-tracking-project.git
cd human-tracking-project
```
2. **Install Dependencies**
```bash
pip install -r requirements.txt
````
---

