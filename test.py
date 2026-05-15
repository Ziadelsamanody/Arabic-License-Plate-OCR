# this file for testing video detection (not part of system)
import os
import random
import time
from pathlib import Path

import cv2
import torch
from PIL  import Image, ImageDraw, ImageFont
import numpy as np 

from detectors import PlateDetector, VeichleDetector, PlateRecognation
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu' )


VIDEO_PATH = Path('testvideos/traffic.mp4')
OUT_PATH = Path('testvideos/out1.mp4')
frame_test = Path('test_images/car2.jpg')
plate_detector = PlateDetector()
veichle_detector = VeichleDetector()
ocr_result = PlateRecognation()


def process_frame(frame, vehicle_detector, plate_detector, ocr_result):
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
            plate_crop = car_crop[py1:py2, px1:px2]
            # plate_detection.append({
            #     'label': mapped_name,
            #     'bbox': bbox,
            # })
          
            plate_recognizer = ocr_result.detect_frame(plate_crop, conf=0.15, imgsz=640)
            
            recognized_text = " ".join([det['label'] for det in plate_recognizer])
            if recognized_text:
                frame_data[track_id]['plate_text'] = recognized_text

   


    return frame_data

def draw_system_annotations(frame, frame_data, font_path=r'C:\Windows/Fonts/arial.ttf'):
    annotated_frame = frame.copy()

    # --- STEP 1: Fast OpenCV Drawing (Boxes) ---
    for track_id, data in frame_data.items():
        vx1, vy1, vx2, vy2 = data['car_box']
        cv2.rectangle(annotated_frame, (vx1, vy1), (vx2, vy2), (0, 255, 0), 2)
        cv2.putText(annotated_frame, f'Car:{track_id}', (vx1, max(0, vy1-10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        if data['plate_box'] is not None: 
            px1, py1, px2, py2 = data['plate_box']
            cv2.rectangle(annotated_frame, (px1, py1), (px2, py2), (0, 0, 255), 2)

    # --- STEP 2: PIL Drawing (Arabic Text) ---
    # Convert image ONCE for PIL
    pil_img = Image.fromarray(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    
    # Load Font safely
    try:
        font = ImageFont.truetype(font_path, 32)
    except OSError:
        font = ImageFont.load_default()

    # Draw text for every valid plate
    for track_id, data in frame_data.items():
        if data['plate_text'] is not None and data['plate_box'] is not None:
            px1, py1, px2, py2 = data['plate_box']
            
            text_x = px1
            text_y = max(0, py1 - 40) # Push text above the plate box
            
            draw.text((text_x, text_y), data['plate_text'], fill=(255, 0, 0), font=font)

    # Convert back to OpenCV format
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        

def process_random_frames(input_video, num_frames, vehicle_detector, plate_detector, ocr_result, output_dir='test_images/random_frames'):
    '''
    Extracts multiple random frames from a video clip, processes them, and saves the annotated results.
    '''
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(str(input_video))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if total_frames <= 0:
        print("Error: Video has no frames or could not be opened.")
        cap.release()
        return
        
    num_to_select = min(num_frames, total_frames)
    random_indices = random.sample(range(total_frames), num_to_select)
    print(f'Randomly selected {num_to_select} frames out of {total_frames}.')
    
    saved_count = 0
    for frame_idx in random_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        
        if not ret:
            print(f'Failed to read frame {frame_idx}')
            continue
            
        print(f'Processing random frame {frame_idx}...')
        frame_data = process_frame(frame, vehicle_detector, plate_detector, ocr_result)
        annotated_frame = draw_system_annotations(frame, frame_data)
        
        out_file = os.path.join(output_dir, f'random_frame_{frame_idx}.jpg')
        cv2.imwrite(out_file, annotated_frame)
        saved_count += 1
        
    cap.release()
    print(f'Done processing random frames. Saved {saved_count} frames to {output_dir}')


# replace read videos to  stream video to prevent memory crash

def process_video_stream(input_video, output_path, vehicle_detector, plate_detector, ocr_result):
    '''
    read  process save   a video on frame 
    '''
    dir = os.path.dirname(output_path)
    if dir and not os.path.exists(dir):
        os.makedirs(dir)
    
    cap = cv2.VideoCapture(input_video)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    print(f'Start stream processing... Resolution : {width}x{height} at {fps}FPS')
    frame_count = 0 

    while True : 
        ret, frame = cap.read()
        if not ret : 
            break 
        frame_data = process_frame(frame, vehicle_detector, plate_detector, ocr_result)
        annotated_frame = draw_system_annotations(frame, frame_data)
        out.write(annotated_frame)

        frame_count += 1
        if frame_count % 30 == 0 :
            print(f'Processed {frame_count} frames....')
        
    cap.release()
    out.release()
    print(f'Done processing.. Saved to {output_path}')


if __name__ == '__main__':
    print(device)
    
    # Process the entire video as a stream
    # process_video_stream(
    #     input_video= str(VIDEO_PATH),
    #     output_path= str(OUT_PATH),
    #     vehicle_detector= veichle_detector,
    #     plate_detector= plate_detector,
    #     ocr_result = ocr_result
    # )

    # Get multiple random frames from the clip and process them
    process_random_frames(
        input_video=str(VIDEO_PATH),
        num_frames=5,
        vehicle_detector=veichle_detector,
        plate_detector=plate_detector,
        ocr_result=ocr_result,
        output_dir='test_images/random_frames'
    )

    # # Read the image first using cv2
    # img = cv2.imread(str(frame_test))
    # if img is None:
    #     print(f"Error: Could not read image at {frame_test}")
    # else:
    #     frame_data = process_frame(img, vehicle_detector=veichle_detector, 
    #                                plate_detector=plate_detector, 
    #                                ocr_result=ocr_result)
    #     anntotated_frame = draw_system_annotations(img, frame_data)
        
    #     # Save or display using cv2 instead of matplotlib to avoid numpy/matplotlib version issues
    #     output_image_path = 'testvideos/out_image.jpg'
    #     cv2.imwrite(output_image_path, anntotated_frame)
    #     print(f"Saved annotated image to {output_image_path}")
        
    #     # Display the image using OpenCV (press any key to close the window)
    #     cv2.imshow("Detected Frame", anntotated_frame)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()