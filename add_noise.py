import cv2
import sys
import numpy as np

sigma = 5
noise_density = 1

def add_sparse_gaussian_noise(image, mean=0, sigma=10, noise_density=0.05):
    """
    입력 영상에 희소한 가우시안 노이즈를 추가합니다.
    
    Parameters:
        image (numpy.ndarray): 입력 영상
        mean (float): 노이즈의 평균
        sigma (float): 노이즈의 표준 편차
        noise_density (float): 노이즈가 추가될 픽셀의 비율 (0 ~ 1)
    
    Returns:
        numpy.ndarray: 노이즈가 추가된 영상
    """
    noisy_image = image.copy()
    num_noise_pixels = int(noise_density * image.size)
    
    # 랜덤하게 노이즈를 추가할 위치를 결정합니다.
    noise_coords = [
        np.random.randint(0, i - 1, num_noise_pixels)
        for i in image.shape
    ]
    
    gaussian_noise = np.random.normal(mean, sigma, num_noise_pixels).astype('uint8')
    
    noisy_image[noise_coords[0], noise_coords[1], noise_coords[2]] = gaussian_noise
    return noisy_image

def process_video(input_path, output_path, mean=0, sigma=10, noise_density=0.05):
    """
    입력 비디오 파일에 가우시안 노이즈를 추가하여 출력 비디오 파일로 저장합니다.
    
    Parameters:
        input_path (str): 입력 비디오 파일 경로
        output_path (str): 출력 비디오 파일 경로
        mean (float): 노이즈의 평균
        sigma (float): 노이즈의 표준 편차
        noise_density (float): 노이즈가 추가될 픽셀의 비율 (0 ~ 1)
    """
    cap = cv2.VideoCapture(input_path)
    
    # 비디오의 폭, 높이 및 FPS 정보를 가져옵니다.
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # 비디오 저장을 위한 VideoWriter 객체를 생성합니다.
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # 가우시안 노이즈를 프레임에 추가합니다.
        noisy_frame = add_sparse_gaussian_noise(frame, mean, sigma, noise_density)
        
        # 노이즈가 추가된 프레임을 비디오 파일에 씁니다.
        out.write(noisy_frame)
    
        frame_count += 1
        if frame_count % 30 == 0:  # 예시로 30 프레임마다 진행 상황 출력
            print(f'Processed {frame_count} frames...')
            sys.stdout.flush()
    
    cap.release()
    out.release()

# 비디오 파일 경로 설정
input_video_path = 'docs/video/CCTV_Detection_Real.mp4'
output_video_path = 'docs/video/CCTV_Detection_Real_Noised.mp4'

# 가우시안 노이즈를 추가하고 비디오 저장
print('Real_Video_Processing', sigma, noise_density)
sys.stdout.flush()
process_video(input_video_path, output_video_path, sigma, noise_density)

# 비디오 파일 경로 설정
input_video_path = 'docs/video/CCTV_Detection_Thermal.mp4'
output_video_path = 'docs/video/CCTV_Detection_Thermal_Noised.mp4'

# 가우시안 노이즈를 추가하고 비디오 저장
print('Thermal_Video_Processing', sigma, noise_density)
sys.stdout.flush()
process_video(input_video_path, output_video_path, sigma, noise_density)

print('Finished')
sys.stdout.flush()