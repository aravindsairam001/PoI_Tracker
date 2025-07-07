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

## 👾 User Interface

<img width="675" alt="Screenshot 2025-07-07 at 10 35 58 AM" src="https://github.com/user-attachments/assets/be188b94-b9c9-46f3-83c1-7e86e42dd2f9" />


<img width="256" alt="Screenshot 2025-07-07 at 10 36 18 AM" src="https://github.com/user-attachments/assets/6caac113-65e9-4163-af7b-67baf1db6630" />


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

## 🚀 How to Run

1. Download YOLO model (YOLOv5s by Ultralytics)
  - The script automatically downloads it when you run the tracker.
  - If needed manually:
```bash
wget https://github.com/ultralytics/yolov5/releases/download/v6.0/yolov5s.pt
```
2. Run the Tracker Script
This script detects and tracks people using webcam input, saves:
  - A tracking video
  - A tracking_output.json with movement data
```bash
python tracker_with_JSON.py
```
3. Run the GUI to Highlight Person of Interest (PoI)
This will load the saved JSON file, let you select a track_id to highlight, and produce a new visualization image.
```bash
python Tracker_GUI.py
```
4. Check results in recordings/Folder
```bash
recordings/
├── tracking_yyyy-mm-dd-HH-MM-SS.mp4        # Video with tracked humans
├── tracking_output.json                    # Track data (coordinates, IDs)
└── highlighted_1_yyyy-mm-dd-HH-MM-SS.png   # Highlighted PoI image
```
---

## 📷 Sample Output

![intruders_2025-07-07_10-30-03](https://github.com/user-attachments/assets/77d5ffbf-01a8-4922-a7e7-43c881bc2b63)

![highlighted_1_2025-07-07_10-35-59](https://github.com/user-attachments/assets/66964fd0-5663-4184-891a-6ae3e581c67c)

---

## 📌 Notes
- YOLOv5 detects only person class
- Recording stops after 5 seconds of no detections
- GUI accepts only .mp4 and .json files
- Merged tracking is done to smooth ID switches between reappearances

---

## ⚠️ Limitations
- Works best with good lighting and stable frames
- Fast movement or dense crowds may cause ID switches
- Does not re-detect across completely different camera angles

---

## 🙌 Acknowledgments
- [Ultralytics YOLOv5]([url](https://github.com/ultralytics/yolov5.git))
- [DeepSORT Realtime]([url](https://github.com/mikel-brostrom/boxmot.git))
- [OpenCV]([url](https://opencv.org))

---
