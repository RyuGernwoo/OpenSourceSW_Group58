import cv2
import numpy as np

def measure_object_dimensions(image_path, reference_object_width, reference_object_height, reference_pixels_width, reference_pixels_height, show_image=True):
    """
    이미지에서 물체의 가로와 세로 길이를 측정하는 함수
    
    :param image_path: 측정할 이미지 경로
    :param reference_object_width: 참조 객체의 실제 너비 (cm)
    :param reference_object_height: 참조 객체의 실제 높이 (cm)
    :param reference_pixels_width: 참조 객체의 이미지 상 픽셀 너비
    :param reference_pixels_height: 참조 객체의 이미지 상 픽셀 높이
    :param show_image: 처리된 이미지를 표시할지 여부
    :return: 측정된 물체들의 치수 정보
    """
    # 이미지 읽기
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("이미지를 불러올 수 없습니다.")
    
    # 원본 이미지 복사 (그리기용)
    draw_image = image.copy()
    
    # 그레이스케일로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 가우시안 블러 적용 (노이즈 제거)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Canny 엣지 검출
    edges = cv2.Canny(blurred, 50, 150)
    
    # 윤곽선 찾기
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 픽셀 대 실제 크기 비율 계산
    pixels_per_cm_width = reference_pixels_width / reference_object_width
    pixels_per_cm_height = reference_pixels_height / reference_object_height
    
    # 측정된 물체들 저장
    measured_objects = []
    
    for contour in contours:
        # 너무 작은 윤곽선은 무시
        if cv2.contourArea(contour) < 100:
            continue
        
        # 최소 경계 사각형 찾기
        x, y, w, h = cv2.boundingRect(contour)
        
        # 실제 길이 계산
        width_cm = w / pixels_per_cm_width
        height_cm = h / pixels_per_cm_height
        
        # 결과 저장
        measured_objects.append({
            'contour': contour,
            'width_pixels': w,
            'height_pixels': h,
            'width_cm': width_cm,
            'height_cm': height_cm
        })
        
        # 이미지에 경계 박스와 치수 표시
        cv2.rectangle(draw_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # 가로 길이 표시
        cv2.putText(draw_image, f'W: {width_cm:.2f} cm', (x, y - 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # 세로 길이 표시
        cv2.putText(draw_image, f'H: {height_cm:.2f} cm', (x, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # 이미지 표시 (선택)
    if show_image:
        cv2.imshow('Object Dimensions', draw_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return measured_objects

# 사용 예시
def main():
    try:
        # 참조 객체(예: A4용지)의 실제 너비와 높이 (cm)
        ref_width = 21.0  # A4 용지 너비
        ref_height = 29.7  # A4 용지 높이
        
        # 이미지에서 측정된 참조 객체의 픽셀 너비와 높이
        ref_pixels_width = 800  # 이미지에서 측정된 A4 용지 너비 픽셀
        ref_pixels_height = 1130  # 이미지에서 측정된 A4 용지 높이 픽셀
        
        # 이미지 경로
        image_path = '이미지.jpg'
        
        # 치수 측정
        results = measure_object_dimensions(
            image_path, 
            ref_width, 
            ref_height, 
            ref_pixels_width, 
            ref_pixels_height
        )
        
        # 결과 출력
        for idx, obj in enumerate(results, 1):
            print(f"물체 {idx}:")
            print(f"  픽셀 가로: {obj['width_pixels']:.2f}")
            print(f"  픽셀 세로: {obj['height_pixels']:.2f}")
            print(f"  실제 가로: {obj['width_cm']:.2f} cm")
            print(f"  실제 세로: {obj['height_cm']:.2f} cm")
    
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()