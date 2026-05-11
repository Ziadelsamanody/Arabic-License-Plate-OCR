# this file for testing video detection (not part of system)
import os
import time
from pathlib import Path

import cv2
import torch

from detectors import PlateDetector, VeichleDetector, PlateRecognation

VIDEO_PATH = Path('testvideos/clip2.mp4')
OUT_PATH = Path('testvideos/out1.mp4')

plate_detector = PlateDetector()
veichle_detector = VeichleDetector()
plate_recognizer = PlateRecognation()


def process_frame(frame, vehicle_detector, plate_detector):
    frame_data = {}

    car_detector  = vehicle_detector.detect_frame(frame)

    # car_detector  = {id : box} 
    for track_id, car_box in car_detector.items():
        vx1, vy1, vx2, vy2 = map(int, car_box)
        car_crop = frame[vy1:vy2, vx1:vx2]
        frame_data[track_id] = {
            'car_box' : [vx1, vy1, vx2, vy2],
            'plate_box': None,
            'plate_text': None 
        }

        plate_bbox = plate_detector.detect_plate_crop(car_crop)

        if plate_bbox is not None:
            px1, py1, px2, py2 = map(int, plate_bbox)
            global_plate_box = [vx1 + px1, vy1 + py1, vx1 + px2, vy1 + py2]
            frame_data[track_id]['plate_box'] = global_plate_box
    return frame_data

def draw_system_annotations(frame, frame_data):
    annotated_frame = frame.copy()

    for track_id, data in frame_data.items():
        vx1, vy1, vx2, vy2 = data['car_box']
        cv2.rectangle(annotated_frame, (vx1, vy1), (vx2, vy2), (0,0,0), 2)
        cv2.putText(annotated_frame, f'Car:{track_id}', (vx1, max(0, vy1-10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
        if data['plate_box'] is not None : 
            px1, py1, px2, py2 = data['plate_box']
            cv2.rectangle(annotated_frame, (px1, py1), (px2, py2), (0,0,0), 2)
            cv2.putText(annotated_frame, f'Plate', (px1, max(0, py1-10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    return annotated_frame
        

if __name__ == '__main__':
    cap = cv2.VideoCapture(str(VIDEO_PATH))
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    os.makedirs(OUT_PATH.parent, exist_ok=True)
    out = cv2.VideoWriter(str(OUT_PATH), fourcc, fps, (width, height))
    
    frame_count = 0
    frame_skip = 5 # skip frames to speed up processing
    print(f"Starting processing of {total_frames} frames...")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        frame_data = process_frame(frame, veichle_detector, plate_detector)
        final_frame = draw_system_annotations(frame, frame_data)
        out.write(final_frame)
        
        frame_count += 1
        if frame_count % 10 == 0:
            print(f"Processed {frame_count}/{total_frames} frames...")
            
    cap.release()
    out.release()
    print("Processing complete!")