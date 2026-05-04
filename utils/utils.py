import cv2 as cv 
import os 


def read_video(video_path):
    cap = cv.VideoCapture(video_path)
    frames = []
    while True :
        ret, frame = cap.read()
        if not ret :
            break
        frames.append(frame)
    cap.release()
    return frames


def save_video(frames, output_path):
    dir = os.path.dirname(output_path)
    if  not os.path.exists(dir):
        os.makedirs(output_path)
    
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    out = cv.VideoWriter(output_path, fourcc, 30, (frames[0].shape[1], frames[0].shape[0]))
    for frame in frames:
        out.write(frame)
    out.release()



    