import cv2
from flask import Flask, Response, render_template

app = Flask(__name__)

# 일반 CCTV 영상 파일 경로
video1_path = 'video/CCTV_Detection_Real_Processed.mp4'
# 적외선 CCTV 영상 파일 경로
video2_path = 'video/CCTV_Detection_Thermal_Processed.mp4'

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
    app.run(host = '0.0.0.0', port = 5000)
