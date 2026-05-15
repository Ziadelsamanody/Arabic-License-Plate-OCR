# Arabic License Plate OCR

A full-stack application designed to detect and recognize Arabic license plates. It utilizes custom trained YOLOv8 models for accurate vehicle and character detection, paired with a FastAPI backend and a modern Nuxt.js/Vue frontend interface.

## Example Output

![Output Image](./out_image.jpg)

## Project Overview & Details

The project consists of a machine learning object detection pipeline served internally via a FastAPI backend, combined with an interactive Web UI for easy image uploads and historical tracking.

**Note on Current State (Two-Part System):**
Currently, the project is divided into two parts:
1. **Frontend (Plate Recognition Only):** The Nuxt.js frontend is actively configured to work only with the Plate Recognition part (processing cropped plate images directly). 
2. **Backend/Scripts (Full Pipeline):** The files and models for full vehicle processing and plate detection (`veichles_detector.py`, `plate_detector.pt`) are still included and functional in the repository. You can use these scripts manually or through the API for the complete vehicle-to-plate flow.

### Workflow:
1. **Vehicle & Plate Detection (Backend available)**: The system can identify vehicles and specific license plates in the frame using `yolov8n.pt` and `plate_detector.pt`.
2. **Character Recognition (Frontend & Backend)**: High-resolution cropped plate images are passed to `plate_recognation.pt`, which isolates overlapping, skewed, or noisy characters.
3. **Arabic Character Mapping**: Character classes detected by the YOLO model are sorted horizontally (left-to-right or right-to-left based on Arabic grammar/plate layout standard) and mapped to actual Arabic glyphs.
4. **Data Delivery**: The finalized text and rendered output image (bounding boxes applied) are exposed through REST API endpoints.
5. **Frontend Application**: A Nuxt.js SPA allows users to interactively drag and drop cropped plate images, view detections via HTML canvas, and browse a history of results.

## Project Structure

- `main.py` - FastAPI application entrypoint.
- `routes/` - API definitions (Health checks, image upload, and detection endpoints).
- `detectors/` - Core ML logic, YOLO wrappers, weight files (`plate_detector.pt`, `plate_recognation.pt`), Arabic class mapping, and drawing helpers.
- `utils/` - Utility functions for image processing and OpenCV operations.
- `frontend/` - Nuxt.js Vue application codebase (UI components, composables, and pages).
- `traing/` - Jupyter Notebooks (`Plate_Detection.ipynb`) used for experimentation and model training.

## Setup & Installation

### Backend

1. **Create and activate the virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
   *(Ensure you install CUDA-specific PyTorch wheels if you plan on utilizing a GPU)*

3. **Run the API:**
   ```powershell
   python main.py
   ```
   The backend will start at `http://localhost:8000`.

### Frontend

1. **Navigate to the frontend directory:**
   ```powershell
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```
   The frontend UI will be accessible typically at `http://localhost:3000`.

## API Documentation

### Base URL

All routes are mounted under `/api`.

### Swagger / OpenAPI Docs

FastAPI exposes interactive API documentation automatically.
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Use Swagger UI to try the endpoints directly from the browser and upload test images to `/api/detect`.

## Testing the Model Manually

`test.py` is a quick one-off script for running YOLO inference on a sample image and saving an annotated output.
