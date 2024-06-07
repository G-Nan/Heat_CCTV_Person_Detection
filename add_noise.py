import cv2
import numpy as np

def add_gaussian_noise(image, mean=0, sigma=15):
    """
    
    Parameters:
        image (numpy.ndarray): 입력 영상
        mean (float): 노이즈의 평균
        sigma (float): 노이즈의 표준 편차
    
    Returns:
        numpy.ndarray: 노이즈가 추가된 영상
    """
    gaussian = np.random.normal(mean, sigma, image.shape).astype('uint8')
    noisy_image = cv2.add(image, gaussian)
    return noisy_image

def process_video(input_path, output_path, mean=0, sigma=15):
    """
    
    Parameters:
        input_path (str): 입력 비디오 파일 경로
        output_path (str): 출력 비디오 파일 경로
        mean (float): 노이즈의 평균
        sigma (float): 노이즈의 표준 편차
    """
    cap = cv2.VideoCapture(input_path)
    
    # 비디오의 폭, 높이 및 FPS 정보를 가져옵니다.
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # 비디오 저장을 위한 VideoWriter 객체를 생성합니다.
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # 가우시안 노이즈를 프레임에 추가합니다.
        noisy_frame = add_gaussian_noise(frame, mean, sigma)
        
        # 노이즈가 추가된 프레임을 비디오 파일에 씁니다.
        out.write(noisy_frame)
    
    cap.release()
    out.release()

# 비디오 파일 경로 설정
input_video_path = 'docs/video/CCTV_Detection_Real.mp4'
output_video_path = 'docs/video/CCTV_Detection_Real_Noised.mp4'

# 가우시안 노이즈를 추가하고 비디오 저장
process_video(input_video_path, output_video_path)

# 비디오 파일 경로 설정
input_video_path = 'docs/video/CCTV_Detection_Thermal.mp4'
output_video_path = 'docs/video/CCTV_Detection_Thermal_Noised.mp4'

# 가우시안 노이즈를 추가하고 비디오 저장
process_video(input_video_path, output_video_path)
