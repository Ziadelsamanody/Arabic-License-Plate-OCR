from ultralytics import YOLO
import cv2 as cv 
import  numpy as np
import matplotlib.pyplot as plt 
from pathlib import Path


MODEL_PATH = Path(__file__).resolve().parent / 'egypt_plate_detector' / 'weights' / 'best.pt'


class PlateDetector:
    def __init__(self, model_path=MODEL_PATH):
        self.detector = YOLO(str(model_path))  # load a custom model

    def detect_frame(self, frame):
        result = self.detector.predict(frame)[0]
        id_names_dict = result.names

        plate_detection = {}

        for box in result.boxes:
            bbox = box.xyxy[0].tolist()
            object_cls_id = int(box.cls.tolist()[0])
            object_cls_name = id_names_dict[object_cls_id]
            
            plate_detection[object_cls_name] = bbox

        return plate_detection
    

    def draw_boxes(self, frame, plate_detection):
        for name, bbox in plate_detection.items():
            x1,y1,x2,y2 = bbox
            cv.putText(frame, f'{name}', (int(bbox[0]), int(bbox[1] - 10)), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 2)
            cv.rectangle(frame, (int(x1), int(y1)),(int(x2), int(y2)), (0,0,255), 2)
        return frame 
    

if __name__ == '__main__':
    image_path = Path(__file__).resolve().parents[1] / 'test_images' / 'plate.png'
    image = cv.imread(str(image_path))
    plate_detector = PlateDetector()

    detections = plate_detector.detect_frame(image)
    frame = plate_detector.draw_boxes(image.copy(), detections)
    plt.imshow(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
    
    plt.axis('off')
    plt.show()