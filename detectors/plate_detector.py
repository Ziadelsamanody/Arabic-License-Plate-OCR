from pathlib import Path

from ultralytics import YOLO
import cv2 as cv



MODEL_PATH = MODEL_PATH = Path(__file__).resolve().parent / 'plate_detector.pt'

class PlateDetector:
    def __init__(self, model_path=MODEL_PATH):
        self.model = YOLO(str(model_path))

    def detect_frames(self, frames):
        detections = []
        for frame in frames : 
            car_detection =  self.detect_frame(frame)
            detections.append(car_detection)
        return detections
    def detect_frame(self, frame):
        result = self.model.track(frame, persist=True, imgsz=1280, conf=0.1)[0]
        id_names_dict = result.names
        car_detection = {}
        for box in result.boxes : 
            # if tracking didn't assign an id, skip or use a random one. But track usually assigns an id.
            if box.id is None:
                continue
            track_id = int(box.id.item())
            bbox = box.xyxy[0].tolist()
            object_cls_id = int(box.cls.tolist()[0])
            object_cls_name = id_names_dict[object_cls_id]
   
            car_detection[track_id] = bbox

        return car_detection
    
    def draw_boxes(self, frames, car_detection):  
        annotated_frames = []
        for frame, detection in zip(frames, car_detection): 
            for track_id, bbox in detection.items(): 
                x1, y1, x2, y2 = map(int, bbox)
                cv.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)
                cv.putText(frame, f'PLATE:{track_id}', (x1, max(0, y2 - 10)), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            annotated_frames.append(frame)
        return annotated_frames 
    


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    
    video_path = Path(__file__).resolve().parents[1] / 'testvideos' / 'clip2.mp4'
    cap = cv.VideoCapture(str(video_path))
    
    plate_detector = PlateDetector()
    
    # Read frames at intervals
    frames_to_test = []
    frame_indices = [0, 30, 60, 90]  # Grab a frame every ~1 second (assuming 30fps)
    
    for idx in frame_indices:
        cap.set(cv.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            frames_to_test.append((idx, frame))
    
    cap.release()

    if frames_to_test:
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        axes = axes.ravel()
        
        for i, (idx, frame) in enumerate(frames_to_test):
            detections = plate_detector.detect_frame(frame)
            print(f'Detections for frame {idx}: {detections}')
            
            annotated_frames = plate_detector.draw_boxes([frame.copy()], [detections])
            annotated_image = annotated_frames[0]
            
            axes[i].imshow(cv.cvtColor(annotated_image, cv.COLOR_BGR2RGB))
            axes[i].set_title(f"Clip 2 - Frame {idx}")
            axes[i].axis('off')
            
        plt.tight_layout()
        plt.show()
    else:
        print("Failed to read frames from the video.")


