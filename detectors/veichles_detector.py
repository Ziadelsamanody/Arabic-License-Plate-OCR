from ultralytics import YOLO
import cv2 as cv


model = 'yolov8n'

class VeichleDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect_frames(self, frames):
        detections = []
        for frame in frames : 
            car_detection =  self.detect_frame(frame)
            detections.append(car_detection)
        return detections
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

            car_detection[track_id] = result

        return car_detection
    
    def draw_boxes(self, frames, car_detection):  
        frames = []
        for frame , detection in zip(frames, car_detection): 
            for track_id, bbox in car_detection.items(): 
                x1,y1,x2,y2=  bbox.xyxy[0].tolist()
                cv.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 4)
                cv.putText(frame, f'CAR:{track_id}', (x1, y2 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0),2)
                frames.append(frame)
        return frame 




