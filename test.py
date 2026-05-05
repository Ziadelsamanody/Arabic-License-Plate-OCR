# this file for testing video detection (not part of system)
import os
import time
from pathlib import Path

import cv2
import torch

from detectors import PlateDetector, VeichleDetector


VIDEO_PATH = Path('testvideos/clip2.mp4')
OUT_PATH = Path('testvideos/out1.mp4')

# Speed knobs (override via env vars)
IMG_SIZE = int(os.getenv('IMG_SIZE', '640'))          # YOLO inference size
TARGET_W = int(os.getenv('TARGET_W', '640'))          # output width (<=0 keeps original)
VID_STRIDE = max(1, int(os.getenv('VID_STRIDE', '1')))  # process every Nth frame
MAX_FRAMES = int(os.getenv('MAX_FRAMES', '0'))        # 0 = unlimited
CONF = float(os.getenv('CONF', '0.25'))


def maybe_resize(frame, target_w):
	if target_w <= 0:
		return frame
	h, w = frame.shape[:2]
	if w == target_w:
		return frame
	new_h = max(1, int(target_w * h / w))
	return cv2.resize(frame, (target_w, new_h))


def format_eta(seconds):
	if seconds is None:
		return '?' 
	seconds = int(max(0, seconds))
	minutes, sec = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	if hours:
		return f'{hours}h{minutes:02d}m'
	if minutes:
		return f'{minutes}m{sec:02d}s'
	return f'{sec}s'


def main():
	if not VIDEO_PATH.exists():
		raise SystemExit(f'Video not found: {VIDEO_PATH}')

	vehicle_detector = VeichleDetector()
	plate_detector = PlateDetector()

	device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
	# move models to GPU if possible
	try:
		vehicle_detector.model.to(device)
	except Exception:
		pass
	try:
		plate_detector.detector.to(device)
	except Exception:
		pass

	cap = cv2.VideoCapture(str(VIDEO_PATH))
	if not cap.isOpened():
		raise SystemExit(f'Could not open video: {VIDEO_PATH}')

	fps_in = cap.get(cv2.CAP_PROP_FPS)
	if not fps_in or fps_in <= 0:
		fps_in = 30.0
	total_in = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)

	ok, first = cap.read()
	if not ok:
		cap.release()
		raise SystemExit('Could not read first frame')

	first = maybe_resize(first, TARGET_W)
	out_fps = fps_in / VID_STRIDE
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
	out = cv2.VideoWriter(str(OUT_PATH), fourcc, out_fps, (first.shape[1], first.shape[0]))
	if not out.isOpened():
		cap.release()
		raise SystemExit(f'Could not open VideoWriter for: {OUT_PATH}')

	start = time.time()
	processed = 0
	frame_index = 1

	def process_one(frame, idx):
		nonlocal processed
		processed += 1
		frame = maybe_resize(frame, TARGET_W)

		car_det = vehicle_detector.detect_frame(frame, imgsz=IMG_SIZE, conf=CONF)
		plate_det = plate_detector.detect_frame(frame, imgsz=IMG_SIZE, conf=CONF)

		annotated = vehicle_detector.draw_boxes([frame], [car_det])[0]
		annotated = plate_detector.draw_boxes(annotated, plate_det)

		if (annotated.shape[1], annotated.shape[0]) != (first.shape[1], first.shape[0]):
			annotated = cv2.resize(annotated, (first.shape[1], first.shape[0]))
		out.write(annotated)

		elapsed = max(1e-6, time.time() - start)
		fps_now = processed / elapsed

		if total_in:
			remaining_in = max(0, total_in - idx)
			remaining_out = remaining_in / VID_STRIDE
			eta = remaining_out / max(1e-6, fps_now)
			print(
				f'Frame {idx}/{total_in} | saved {processed} | {fps_now:.2f} FPS | ETA {format_eta(eta)}',
				end='\r',
				flush=True,
			)
		else:
			print(f'Frame {idx} | saved {processed} | {fps_now:.2f} FPS', end='\r', flush=True)

	try:
		if (frame_index - 1) % VID_STRIDE == 0:
			process_one(first, frame_index)

		while True:
			ok, frame = cap.read()
			if not ok:
				break
			frame_index += 1

			if (frame_index - 1) % VID_STRIDE != 0:
				continue

			process_one(frame, frame_index)

			if MAX_FRAMES and processed >= MAX_FRAMES:
				break
	finally:
		cap.release()
		out.release()

	print()
	elapsed = time.time() - start
	print(
		f'Done. Wrote {processed} frames to {OUT_PATH} in {elapsed:.2f}s '
		f'(device: {device}, stride: {VID_STRIDE}, imgsz: {IMG_SIZE}).'
	)


if __name__ == '__main__':
	main()

