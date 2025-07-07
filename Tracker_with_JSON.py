import cv2
import os
import time
import json
from datetime import datetime
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import numpy as np

# Initialize YOLOv5
model = YOLO('yolov5su.pt')  # Downloaded automatically on first use
tracker = DeepSort(max_age=60)

#cap = cv2.VideoCapture(0)  # Webcam. Replace with filename for video
cap = cv2.VideoCapture('/Users/aravindsairams/Downloads/road_crossing.mp4')

CONFIDENCE_THRESHOLD = 0.6
recording = False
video_writer = None
last_detected_time = None
RECORD_AFTER_MISSING_SECONDS = 5

os.makedirs("recordings", exist_ok=True)

# Generate output file names
def get_output_filename(ext="mp4"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"recordings/intruders_{timestamp}.{ext}"

video_path = get_output_filename()
json_path = video_path.replace(".mp4", ".json")
frame_index = 0
tracking_log = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect with YOLO
    results = model(frame)[0]
    detections = []

    for box in results.boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        if class_id == 0 and confidence > CONFIDENCE_THRESHOLD:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            detections.append(([x1, y1, x2 - x1, y2 - y1], confidence, 'person'))

    # DeepSORT tracking
    tracks = tracker.update_tracks(detections, frame=frame)

    # Only check for confirmed tracks (all are persons)
    person_found = any(track.is_confirmed() for track in tracks)

    if person_found:
        last_detected_time = time.time()
        if not recording:
            h, w = frame.shape[:2]
            video_writer = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), 20, (w, h))
            print(f"[INFO] Recording started: {video_path}")
            recording = True

    if recording and last_detected_time and time.time() - last_detected_time > RECORD_AFTER_MISSING_SECONDS:
        print(f"[INFO] Recording stopped.")
        break

    for track in tracks:
        if not track.is_confirmed():
            continue
        track_id = track.track_id
        x1, y1, x2, y2 = map(int, track.to_ltrb())
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"ID: {track_id}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Save tracking info
        tracking_log.append({
            "frame": frame_index,
            "track_id": track_id,
            "bbox": [x1, y1, x2, y2]
        })

    if recording:
        video_writer.write(frame)

    cv2.imshow("Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_index += 1

# Cleanup
if video_writer and recording:
    video_writer.release()
cap.release()
cv2.destroyAllWindows()

# Save tracking log
with open(json_path, 'w') as f:
    json.dump(tracking_log, f, indent=2)

print(f"[INFO] Saved video to: {video_path}")
print(f"[INFO] Saved tracking data to: {json_path}")

# --- Auto-run merge_tracks logic ---
import numpy as np

def bbox_center(bbox):
    x1, y1, x2, y2 = bbox
    return ((x1 + x2) / 2, (y1 + y2) / 2)

def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def merge_tracks(tracking_log, max_gap=10, max_dist=50):
    tracks = {}
    for entry in tracking_log:
        tid = entry['track_id']
        tracks.setdefault(tid, []).append(entry)
    for tid in tracks:
        tracks[tid] = sorted(tracks[tid], key=lambda x: x['frame'])
    merged = {}
    used = set()
    new_id = 1
    for tid, entries in sorted(tracks.items()):
        if tid in used:
            continue
        merged[new_id] = entries
        used.add(tid)
        last_frame = entries[-1]['frame']
        last_center = bbox_center(entries[-1]['bbox'])
        for tid2, entries2 in tracks.items():
            if tid2 in used or entries2[0]['frame'] <= last_frame:
                continue
            gap = entries2[0]['frame'] - last_frame
            if gap > max_gap:
                continue
            first_center = bbox_center(entries2[0]['bbox'])
            if euclidean(last_center, first_center) < max_dist:
                merged[new_id].extend(entries2)
                used.add(tid2)
        new_id += 1
    merged_log = []
    for tid, entries in merged.items():
        for entry in entries:
            entry['track_id'] = tid
            merged_log.append(entry)
    return merged_log

# Run merging and save merged log
with open(json_path) as f:
    tracking_log = json.load(f)
merged_log = merge_tracks(tracking_log)
merged_json_path = json_path.replace('.json', '_merged.json')
with open(merged_json_path, 'w') as f:
    json.dump(merged_log, f, indent=2)
print(f"[INFO] Merged tracking data saved to: {merged_json_path}")