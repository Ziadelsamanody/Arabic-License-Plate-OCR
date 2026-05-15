from pathlib import Path

from ultralytics import YOLO
import cv2 as cv


MODEL_PATH = Path(__file__).resolve().parents[1] / 'yolov8n.pt'


class VeichleDetector:
    def __init__(self, model_path=MODEL_PATH):
        self.model = YOLO(str(model_path))

    def detect_frames(self, frames):
        detections = []
        for frame in frames : 
            car_detection =  self.detect_frame(frame)
            detections.append(car_detection)
        return detections
    def detect_frame(self, frame):
        # Added tracker='bytetrack.yaml' for much stabler IDs
        # Added conf=0.3 to reduce false positive jitter but keep tracking solid
        result = self.model.track(frame, classes=[2,3,5,7], persist=True, tracker="bytetrack.yaml", conf=0.3, verbose=False)[0]
        id_names_dict = result.names
        car_detection = {}
        for box in result.boxes : 
            if box.id is None:
                continue
            track_id = int(box.id.item())
            bbox = box.xyxy[0].tolist()
            object_cls_id = int(box.cls.tolist()[0])
            object_cls_name = id_names_dict[object_cls_id]
            if object_cls_name in ['car', 'motorcycle', 'bus', 'truck']:
                car_detection[track_id] = bbox

        return car_detection


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    
  
    



