from fastapi import APIRouter, HTTPException, Response, UploadFile, File
import uvicorn 
import torch
import sys
import cv2 as cv
import numpy as np
sys.path.append('./detectors')
from detectors import  PlateRecognation


detector = PlateRecognation()


router = APIRouter()

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

        plate_detection = detector.detect_frame(frame)
        labels = detector.filter_result(plate_detection)

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
    
