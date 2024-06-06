import streamlit as st

# HTML과 JavaScript를 사용하여 동영상 동기화 및 자동 재생
html_code = """
<div style="display: flex; justify-content: space-around;">
    <div style="flex: 1; padding: 10px;">
        <h3>Normal CCTV</h3>
        <video id="video1" width="100%" autoplay muted loop>
            <source src="processed/CCTV_Detection_Real_Processed_reencoded.mp4" type="video/mp4">
        </video>
    </div>
    <div style="flex: 1; padding: 10px;">
        <h3>Infrared CCTV</h3>
        <video id="video2" width="100%" autoplay muted loop>
            <source src="processed/CCTV_Detection_Thermal_Processed_reencoded.mp4" type="video/mp4">
        </video>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function () {
    var video1 = document.getElementById('video1');
    var video2 = document.getElementById('video2');

    // 동영상이 재생될 때 동기화 시작
    function syncPlay() {
        if (video1.paused) {
            video1.play();
        }
        if (video2.paused) {
            video2.play();
        }
    }

    // 동영상이 일시 중지될 때 동기화 중지
    function syncPause() {
        if (!video1.paused) {
            video1.pause();
        }
        if (!video2.paused) {
            video2.pause();
        }
    }

    // 동영상이 끝날 때 동기화 재생
    video1.onended = function() {
        video2.currentTime = 0;
        video1.currentTime = 0;
        video2.play();
        video1.play();
    };

    video2.onended = function() {
        video1.currentTime = 0;
        video2.currentTime = 0;
        video1.play();
        video2.play();
    };

    video1.onplay = syncPlay;
    video2.onplay = syncPlay;
    video1.onpause = syncPause;
    video2.onpause = syncPause;
});
</script>
"""

# Streamlit에서 HTML 코드 실행
def main():
    st.set_page_config(layout="wide")
    st.title("Normal/Infrared CCTV Videos")

    # HTML과 JavaScript 코드를 Streamlit 앱에 삽입
    st.components.html(html_code, height=600)

    st.markdown("""
    <div style="margin-top: 20px; padding: 10px; background-color: #f0f0f0; border: 1px solid #ccc;">
        <h2>About This Demo</h2>
        <p>해당 서비스는 현재 편의를 위해 서비스의 성능을 잘 나타낼 수 있는 동영상을 업로드하여 시범중입니다. 실제 서비스에서는 CCTV에서 촬영된 영상을 실시간으로 확인하여 사람과 동물 등을 탐지합니다.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
