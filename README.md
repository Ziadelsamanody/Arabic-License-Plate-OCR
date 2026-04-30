# Arabic License Plate OCR

A FastAPI service for detecting Egyptian license plate characters with a custom YOLO model, mapping the detections to Arabic characters, and returning a cleaned plate string through an HTTP API.

## What This Project Does

The project takes an uploaded plate image, runs object detection on the characters, sorts the detections from left to right, maps class names to Arabic glyphs, and returns the final detected sequence.

## Project Structure

- `main.py` - FastAPI application entrypoint.
- `routes/health.py` - health-check endpoint.
- `routes/routes.py` - detection endpoint that accepts uploaded images.
- `detectors/plate_detector.py` - YOLO wrapper, Arabic class mapping, drawing helpers, and label filtering.
- `detectors/best.pt` - trained YOLO weights used by the detector.
- `test.py` - simple standalone YOLO inference script.
- `test_images/` - sample input and output images.
- `OCR.ipynb` - notebook for experimentation.

## How It Works

1. `main.py` creates the FastAPI app and mounts the routes under `/api`.
2. `routes/health.py` returns a basic status response for service checks.
3. `routes/routes.py` accepts an uploaded image, decodes it with OpenCV, and calls the detector.
4. `detectors/plate_detector.py` loads the YOLO model, maps model classes to Arabic characters, sorts detections by X position, and returns the final label list.

## Setup

### 1. Create and activate the virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

Install the packages used by the project:

```powershell
pip install fastapi uvicorn ultralytics opencv-python numpy matplotlib pillow torch
```

If your YOLO / PyTorch setup needs a CUDA-specific build, install the matching wheel for your machine instead of the default CPU package.

### 3. Run the API

```powershell
python main.py
```

The server will start at `http://0.0.0.0:8000`.

## API Documentation

### Base URL

All routes are mounted under `/api`.

### Swagger / OpenAPI Docs

FastAPI exposes interactive API documentation automatically.

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Use Swagger UI to try the endpoints directly from the browser and upload test images to `/api/detect`.

### Health Check

#### `GET /api/health`

Returns the service status and whether PyTorch sees CUDA.

Example response:

```json
{
  "status": "working",
  "device": "cpu"
}
```

### Detect Plate Characters

#### `POST /api/detect`

Accepts a single uploaded image file and returns the detected plate characters.

#### Request

- Content type: `multipart/form-data`
- Field name: `image`
- Type: image file

#### Example with `curl`

```powershell
curl -X POST "http://127.0.0.1:8000/api/detect" ^
  -F "image=@test_images/plate2.jpg"
```

#### Example response

```json
{
  "success": true,
  "labels": ["٩", "٨", "٣", "د", "س", "ي"],
  "plate_text": "٩٨٣دسي",
  "detections": [
    {
      "label": "٩",
      "bbox": [63.6, 131.3, 123.1, 255.5]
    }
  ]
}
```

#### Error responses

- `400 Bad Request` - no file uploaded or the image could not be decoded.
- `500 Internal Server Error` - unexpected runtime failure during detection.

## Detector Notes

- The detector sorts boxes from left to right before filtering the labels.
- Arabic class mapping is defined in `detectors/plate_detector.py`.
- `draw_boxes()` can be used for visual debugging and annotation.

## Testing the Model Manually

`test.py` is a quick one-off script for running YOLO inference on a sample image and saving an annotated output.

## Next Improvements

- Add plate-specific grouping logic if the number/letter order needs post-processing.
- Return confidence scores alongside each detection.
- Add automated tests for the API and detector output.
