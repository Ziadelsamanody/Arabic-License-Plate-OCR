from ultralytics import YOLO
import cv2 as cv 
import  numpy as np
import matplotlib.pyplot as plt 
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


MODEL_PATH = Path(__file__).resolve().parent / 'egypt_plate_detector' / 'weights' / 'best.pt'



ARABIC_CLASS_MAP = {
    '0': '٠',
    '1': '١',
    '2': '٢',
    '3': '٣',
    '4': '٤',
    '5': '٥',
    '6': '٦',
    '7': '٧',
    '8': '٨',
    '9': '٩',
    'aain': 'ع',
    'alf': 'ا',
    'baa': 'ب',
    # In labels.jpg the class 'c' corresponds to the Arabic letter 'س'
    # map 'c' to 'س' to match the provided labels image
    'dal': 'د',
    'c': 'س',
    'faa': 'ف',
    'geem': 'ج',
    'haa': 'ه',
    'kaf': 'ك',
    'lam': 'ل',
    'meem': 'م',
    'non': 'ن',
    'raa': 'ر',
    'sad': 'ص',
    'sen': 'س',
    'taa': 'ط',
    'waaw': 'و',
    'yaa': 'ي',
    'zen': 'ز',
}


class PlateDetector:
    def __init__(self, model_path=MODEL_PATH):
        self.detector = YOLO(str(model_path))  # load a custom model
        self.font_path = r'C:\Windows\Fonts\arial.ttf'

    @staticmethod
    def map_class_to_arabic(class_name):
        return ARABIC_CLASS_MAP.get(class_name, class_name)

    def detect_frame(self, frame):
        result = self.detector.predict(frame)[0]
        id_names_dict = result.names

        plate_detection = []

        for box in result.boxes:
            bbox = box.xyxy[0].tolist()
            object_cls_id = int(box.cls.tolist()[0])
            object_cls_name = id_names_dict[object_cls_id]
            mapped_name = self.map_class_to_arabic(object_cls_name)

            plate_detection.append({
                'label': mapped_name,
                'bbox': bbox,
            })

        # Left-to-right sorting helps with reading sequence outputs.
        plate_detection.sort(key=lambda d: d['bbox'][0])

        return plate_detection
    

    def draw_boxes(self, frame, plate_detection):
        pil_img = Image.fromarray(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)

        try:
            font = ImageFont.truetype(self.font_path, 36)
        except OSError:
            font = ImageFont.load_default()

        for det in plate_detection:
            name = det['label']
            bbox = det['bbox']
            x1,y1,x2,y2 = bbox
            cv.rectangle(frame, (int(x1), int(y1)),(int(x2), int(y2)), (0,0,255), 2)
            text_x = int(x1)
            text_y = max(0, int(y1) - 34)
            draw.text((text_x, text_y), str(name), fill=(255, 0, 0), font=font)

        return cv.cvtColor(np.array(pil_img), cv.COLOR_RGB2BGR)

    def filter_result(self, plate_detection):
        labels = [det['label'] for det in plate_detection]
        return labels
        

if __name__ == '__main__':
    image_path = Path(__file__).resolve().parents[1] / 'test_images' / 'plate2.jpg'
    image = cv.imread(str(image_path))
    plate_detector = PlateDetector()

    detections = plate_detector.detect_frame(image)
    print(f'Detections: {detections}')
    print(f'filterd detection')
    frame = plate_detector.draw_boxes(image.copy(), detections)
    plt.imshow(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
    
    plt.axis('off')
    plt.show()