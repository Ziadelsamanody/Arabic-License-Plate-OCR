from ultralytics import YOLO
import cv2


model_path = 'detectors/egypt_plate_detector/weights/best.pt'
detector = YOLO(model_path)  # load a custom model

# visulize the results
img_path = 'test_images/plate.png'


results = detector(img_path)  # predict on an image
if not results:
	raise RuntimeError('No inference results returned.')

# YOLO returns a list of Result objects; use the first result for single-image inference.
result = results[0]
print(f'result {result}')
annotated = result.plot()
cv2.imwrite('test_images/out1.png', annotated)
print('Saved annotated image to test_images/out1.png')