import cv2
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import os

def browse_video():
    path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if path:
        video_path_entry.delete(0, tk.END)
        video_path_entry.insert(0, path)

def browse_json():
    path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if path:
        json_path_entry.delete(0, tk.END)
        json_path_entry.insert(0, path)

def highlight_track():
    video_path = video_path_entry.get()
    json_path = json_path_entry.get()
    selected_id = track_id_entry.get()

    if not os.path.exists(video_path) or not os.path.exists(json_path) or not selected_id.isdigit():
        status_label.config(text="❌ Invalid input")
        return

    selected_id = int(selected_id)
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    out_name = f"highlighted_{selected_id}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
    out_path = os.path.join("recordings", out_name)
    os.makedirs("recordings", exist_ok=True)

    out_writer = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    with open(json_path, 'r') as f:
        tracking_data = json.load(f)

    frame_to_tracks = {}
    for entry in tracking_data:
        frame = entry['frame']
        frame_to_tracks.setdefault(frame, []).append(entry)

    current_frame = 0
    # Store path points for the selected track
    path_points = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        tracks = frame_to_tracks.get(current_frame, [])

        # Only process the selected track
        for track in tracks:
            track_id = track['track_id']
            if track_id == selected_id:
                x1, y1, x2, y2 = track['bbox']
                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                # Add center point for path
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                path_points.append((cx, cy))
                # Draw path in red
                for i in range(1, len(path_points)):
                    cv2.line(frame, path_points[i-1], path_points[i], (0, 0, 255), 2)
                break  # Only one track with this ID per frame

        out_writer.write(frame)
        current_frame += 1

    cap.release()
    out_writer.release()
    status_label.config(text=f"✅ Output saved: {out_path}")
    messagebox.showinfo("Done", f"Output saved: {out_path}")

# --- GUI SETUP ---
root = tk.Tk()
root.title("Track Highlighter")

tk.Label(root, text="Video File:").grid(row=0, column=0, sticky='e')
video_path_entry = tk.Entry(root, width=50)
video_path_entry.grid(row=0, column=1)
tk.Button(root, text="Browse", command=browse_video).grid(row=0, column=2)

tk.Label(root, text="Tracking JSON:").grid(row=1, column=0, sticky='e')
json_path_entry = tk.Entry(root, width=50)
json_path_entry.grid(row=1, column=1)
tk.Button(root, text="Browse", command=browse_json).grid(row=1, column=2)

tk.Label(root, text="Track ID to Highlight:").grid(row=2, column=0, sticky='e')
track_id_entry = tk.Entry(root, width=10)
track_id_entry.grid(row=2, column=1, sticky='w')

tk.Button(root, text="Track", command=highlight_track, bg='green', fg='white').grid(row=3, column=1, pady=10)

status_label = tk.Label(root, text="")
status_label.grid(row=4, column=0, columnspan=3)

root.mainloop()