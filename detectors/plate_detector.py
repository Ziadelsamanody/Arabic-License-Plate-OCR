from pathlib import Path

from ultralytics import YOLO
import cv2 as cv



MODEL_PATH = Path(__file__).resolve().parent / 'plate_detector.pt'

class PlateDetector:
    def __init__(self, model_path=MODEL_PATH):
        self.model = YOLO(str(model_path))

    def detect_frames(self, frames):
        detections = []
        for frame in frames : 
            car_detection =  self.detect_frame(frame)
            detections.append(car_detection)
        return detections
    def detect_plate_crop(self, car_crop):
        # We lower conf to 0.15 so it catches blurry/tiny plates
        # (It was 0.45, which ignores anything slightly unclear)
        result = self.model.predict(car_crop, imgsz=320, conf=0.15, verbose=False)[0]
        if len(result.boxes) > 0:
            bbox = result.boxes.xyxy[0].tolist()
            return bbox
        return None
 

