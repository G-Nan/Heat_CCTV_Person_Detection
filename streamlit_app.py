import streamlit as st
import cv2
import numpy as np
from ultralyticsplus import YOLO

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

def main():
    st.title("Object Detection with YOLOv8")
    
    # Select video source
    video_source = st.selectbox("Select video source", ("CCTV_Detection_Real.mp4", "CCTV_Detection_Thermal.mp4"))
    
    # Display video
    stframe = st.empty()
    cap = cv2.VideoCapture(video_source)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        results = detect_objects(frame)
        frame = draw_boxes(frame, results)
        
        stframe.image(frame, channels="BGR")

    cap.release()

if __name__ == "__main__":
    main()
