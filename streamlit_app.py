import streamlit as st
import cv2
import numpy as np
from ultralyticsplus import YOLO
from PIL import Image

# Load model
model_path = 'thermal_detection.pt'
model = YOLO(model_path)

# Set model parameters
model.overrides['conf'] = 0.25  # NMS confidence threshold
model.overrides['iou'] = 0.45  # NMS IoU threshold
model.overrides['agnostic_nms'] = False  # NMS class-agnostic
model.overrides['max_det'] = 1000  # maximum number of detections per image

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

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    stframe = st.empty()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Perform object detection
        results = detect_objects(frame)
        
        # Draw boxes on the frame
        frame = draw_boxes(frame, results)
        
        # Convert BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        
        stframe.image(img, channels="RGB")
    
    cap.release()

def main():
    st.set_page_config(layout="wide")
    st.title("Object Detection Using Normal/Infrared CCTV")

    col1, col2 = st.columns(2)

    with col1:
        st.header("Normal CCTV")
        video_file1 = 'video/CCTV_Detection_Real.mp4'
        video_bytes1 = open(video_file1, 'rb').read()
        video_html1 = f"""
            <video id="video1" width="100%" autoplay loop>
                <source src="data:video/mp4;base64,{video_bytes1.decode('latin-1')}" type="video/mp4">
            </video>
        """
        st.markdown(video_html1, unsafe_allow_html=True)

    with col2:
        st.header("Infrared CCTV")
        video_file2 = 'video/CCTV_Detection_Thermal.mp4'
        video_bytes2 = open(video_file2, 'rb').read()
        video_html2 = f"""
            <video id="video2" width="100%" autoplay loop>
                <source src="data:video/mp4;base64,{video_bytes2.decode('latin-1')}" type="video/mp4">
            </video>
        """
        st.markdown(video_html2, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-top: 20px; padding: 10px; background-color: #f0f0f0; border: 1px solid #ccc;">
        <h2>About This Demo</h2>
        <p>해당 서비스는 현재 편의를 위해 서비스의 성능을 잘 나타낼 수 있는 동영상을 업로드 하여 시범중입니다. 실제 서비스에서는 CCTV에서 촬영된 영상을 실시간으로 확인하여 사람과 동물 등을 탐지합니다.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
