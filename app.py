import os
import cv2
from huggingface_hub import hf_hub_download
from ultralyticsplus import YOLO, render_result
from flask import Flask, Response, render_template, request, redirect, url_for

# load model
model_path = 'yolov8n.pt'

# load model
model = YOLO(model_path)

# set model parameters
model.overrides['conf'] = 0.25  # NMS confidence threshold
model.overrides['iou'] = 0.45  # NMS IoU threshold
model.overrides['agnostic_nms'] = False  # NMS class-agnostic
model.overrides['max_det'] = 1000  # maximum number of detections per image

app = Flask(__name__)

# 일반 CCTV 영상 파일 경로
video1_path = 'video/CCTV_Detection_Real.mp4'
# 적외선 CCTV 영상 파일 경로
video2_path = 'video/CCTV_Detection_Thermal.mp4'

def detect_objects(frame):
    results = model(frame)
    return results

def draw_boxes(frame, results):
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0]
            cls = int(box.cls[0])
            if cls in model.names:
                label = model.names[cls]
            else:
                label = f'Unknown {cls}'
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame

def generate_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    while True:
        if not cap.isOpened():
            cap = cv2.VideoCapture(video_path)
        
        ret, frame = cap.read()
        if not ret:
            cap.release()
            cap = cv2.VideoCapture(video_path)
            continue

        results = detect_objects(frame)
        frame = draw_boxes(frame, results)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed1')
def video_feed1():
    return Response(generate_frames(video1_path), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2')
def video_feed2():
    return Response(generate_frames(video2_path), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()
