import streamlit as st
import os

def play_video(video_path):
    if os.path.exists(video_path):
        video_file = open(video_path, 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
    else:
        st.error(f"File not found: {video_path}")

def main():
    st.set_page_config(layout="wide")
    st.title("Normal/Infrared CCTV Videos")

    col1, col2 = st.columns(2)

    with col1:
        st.header("Normal CCTV")
        play_video('processed/CCTV_Detection_Real_Processed.mp4')

    with col2:
        st.header("Infrared CCTV")
        play_video('processed/CCTV_Detection_Thermal_Processed.mp4')
    
    st.markdown("""
    <div style="margin-top: 20px; padding: 10px; background-color: #f0f0f0; border: 1px solid #ccc;">
        <h2>About This Demo</h2>
        <p>해당 서비스는 현재 편의를 위해 서비스의 성능을 잘 나타낼 수 있는 동영상을 업로드 하여 시범중입니다. 실제 서비스에서는 CCTV에서 촬영된 영상을 실시간으로 확인하여 사람과 동물 등을 탐지합니다.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
