from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import routes, health
from detectors import PlateRecognation
import uvicorn
import contextlib



app = FastAPI(title='Plate Detector V1')


# frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'], # update this to front end url
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=health.router, prefix='/api', tags=["Health"])
app.include_router(router=routes.router, prefix='/api', tags=['Detect'])

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
    


