from fastapi import APIRouter, HTTPException, Response, UploadFile, File
import uvicorn
import torch
import sys
import os
import uuid
import tempfile
import subprocess
import shutil
from pathlib import Path
from collections import Counter
import cv2 as cv
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.append('./detectors')
from detectors import  PlateRecognation, PlateDetector, VeichleDetector

ocr_model = PlateRecognation()
plate_detector = PlateDetector()
veichle_detector = VeichleDetector()

router = APIRouter()

OUTPUTS_DIR = Path(__file__).resolve().parents[1] / 'outputs'
OUTPUTS_DIR.mkdir(exist_ok=True)

FONT_PATH = r'C:\Windows\Fonts\arial.ttf'

def process_frame(frame, detect_vehicles, plate_detector, ocr_result):
    frame_data = {}

    car_detector  = detect_vehicles(frame)

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


def draw_system_annotations(frame, frame_data, font_path=FONT_PATH):
    annotated_frame = frame.copy()

    for track_id, data in frame_data.items():
        vx1, vy1, vx2, vy2 = data['car_box']
        cv.rectangle(annotated_frame, (vx1, vy1), (vx2, vy2), (0, 255, 0), 2)
        cv.putText(annotated_frame, f'Car:{track_id}', (vx1, max(0, vy1 - 10)),
                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        if data['plate_box'] is not None:
            px1, py1, px2, py2 = data['plate_box']
            cv.rectangle(annotated_frame, (px1, py1), (px2, py2), (0, 0, 255), 2)

    pil_img = Image.fromarray(cv.cvtColor(annotated_frame, cv.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    try:
        font = ImageFont.truetype(font_path, 32)
    except OSError:
        font = ImageFont.load_default()

    for track_id, data in frame_data.items():
        if data['plate_text'] and data['plate_box'] is not None:
            px1, py1, px2, py2 = data['plate_box']
            text_x = px1
            text_y = max(0, py1 - 40)
            draw.text((text_x, text_y), data['plate_text'], fill=(255, 0, 0), font=font)

    return cv.cvtColor(np.array(pil_img), cv.COLOR_RGB2BGR)

@router.post('/detect')
async def detect(image  : UploadFile = File(...)):
    try :
        if image is None :
            raise HTTPException(status_code=400, detail='No Image uploaded')
        
        image_bytes = await image.read()
        np_image = np.frombuffer(image_bytes, np.uint8)
        frame = cv.imdecode(np_image, cv.IMREAD_COLOR)

        if frame is None:
            raise HTTPException(status_code=400, detail='Could not decode image')

        plate_detection = ocr_model.detect_frame(frame)
        labels = ocr_model.filter_result(plate_detection)

        return {
            'success': True,
            'labels': labels,
            'plate_text': ''.join(labels),
            'detections': plate_detection,
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.post('/detect_vehicle_and_plate')
async def detect_vehicle_and_plate(image: UploadFile = File(...)):
    try :
        if image is None :
            raise HTTPException(status_code=400, detail='No Image uploaded')
        
        image_bytes = await image.read()
        np_image = np.frombuffer(image_bytes, np.uint8)
        frame = cv.imdecode(np_image, cv.IMREAD_COLOR)

        if frame is None:
            raise HTTPException(status_code=400, detail='Could not decode image')

        frame_data = process_frame(frame, veichle_detector.detect_frame_static, plate_detector, ocr_model)

        vehicles = [
            {
                'track_id': track_id,
                'car_box': data['car_box'],
                'plate_box': data['plate_box'],
                'plate_text': data['plate_text'],
            }
            for track_id, data in frame_data.items()
        ]

        return {
            'success': True,
            'count': len(vehicles),
            'vehicles': vehicles,
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post('/detect_video')
async def detect_video(video: UploadFile = File(...)):
    tmp_path = None
    try:
        if video is None:
            raise HTTPException(status_code=400, detail='No video uploaded')

        suffix = Path(video.filename or 'upload.mp4').suffix or '.mp4'
        tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        tmp_path = tmp_in.name
        contents = await video.read()
        tmp_in.write(contents)
        tmp_in.flush()
        tmp_in.close()

        cap = cv.VideoCapture(tmp_path)
        if not cap.isOpened():
            raise HTTPException(status_code=400, detail='Could not open video')

        width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv.CAP_PROP_FPS) or 25.0

        run_id = uuid.uuid4().hex
        raw_path = OUTPUTS_DIR / f'{run_id}_raw.mp4'

        out = cv.VideoWriter(str(raw_path), cv.VideoWriter_fourcc(*'avc1'), fps, (width, height))
        if not out.isOpened():
            out = cv.VideoWriter(str(raw_path), cv.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
        if not out.isOpened():
            cap.release()
            raise HTTPException(status_code=500, detail='Could not initialize video writer')

        track_summary = {}
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_data = process_frame(frame, veichle_detector.detect_frame, plate_detector, ocr_model)

            for track_id, data in frame_data.items():
                entry = track_summary.setdefault(track_id, {'texts': Counter(), 'car_box': data['car_box']})
                entry['car_box'] = data['car_box']
                if data['plate_text']:
                    entry['texts'][data['plate_text']] += 1

            annotated_frame = draw_system_annotations(frame, frame_data)
            out.write(annotated_frame)
            frame_count += 1

        cap.release()
        out.release()

        out_name = f'{run_id}.mp4'
        final_path = OUTPUTS_DIR / out_name

        transcoded = False
        if shutil.which('ffmpeg'):
            ffmpeg_result = subprocess.run(
                ['ffmpeg', '-y', '-i', str(raw_path), '-c:v', 'libx264',
                 '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                 '-an', str(final_path)],
                capture_output=True,
            )
            transcoded = ffmpeg_result.returncode == 0 and final_path.exists() and final_path.stat().st_size > 0

        if transcoded:
            os.unlink(raw_path)
        else:
            raw_path.rename(final_path)

        vehicles = []
        for track_id, entry in track_summary.items():
            texts = entry['texts']
            best_text, occurrences = texts.most_common(1)[0] if texts else (None, 0)
            vehicles.append({
                'track_id': track_id,
                'car_box': entry['car_box'],
                'plate_text': best_text,
                'occurrences': occurrences,
            })

        return {
            'success': True,
            'video_url': f'/outputs/{out_name}',
            'fps': fps,
            'frame_count': frame_count,
            'width': width,
            'height': height,
            'count': len(vehicles),
            'vehicles': vehicles,
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)

