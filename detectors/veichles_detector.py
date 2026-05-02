from ultralytics import YOLO
import cv2 as cv


model = 'yolov8n'

class VeichleDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect_frame(self, frame):
        result = self.model.track(frame, persist=True)[0]
        id_names_dict = result.names
        car_detection = {}
           #result.boxes :   
    #cls: tensor([0.]) conf: tensor([0.9049])id: tensor([1.]) .
        for box in result.boxes : 
            track_id = int(box.id.item())
            result = box.xyxy[0].tolist()
            object_cls_id = int(box.cls.tolist()[0])
            object_cls_name = id_names_dict[object_cls_id]