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
        result = self.model.track(frame,classes=[2,3,5,7] ,persist=True)[0]
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
    
    def draw_boxes(self, frames, car_detection):  
        annotated_frames = []
        for frame, detection in zip(frames, car_detection): 
            for track_id, bbox in detection.items(): 
                x1, y1, x2, y2 = map(int, bbox)
                cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
                cv.putText(frame, f'CAR:{track_id}', (x1, max(0, y2 - 10)), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            annotated_frames.append(frame)
        return annotated_frames

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    
  
    



