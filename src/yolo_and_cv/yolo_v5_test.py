import cv2
import torch
import numpy as np

# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5:master', 'yolov5s')

# 웹캠 열기 (웹캠 인덱스 0은 기본 웹캠을 의미합니다)
cap = cv2.VideoCapture(0)

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    frame_number = 0
    # YOLOv5 입력으로 변환
    results = model(frame)
    # 검출 결과 중 사람 클래스 (class_id=0) 의 개수를 확인
    person_boxes = results.pred[0][results.pred[0][:, 5] == 0, :4]
    num_people = person_boxes.shape[0]
    # 사람이 검출되면 1을 출력, 그렇지 않으면 0을 출력
    print(f"사람 수: {num_people}")
    for i, box in enumerate(person_boxes):
        x1, y1, x2, y2 = box.tolist()
        print(f"사람 {i + 1} 위치: (x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2})")
    
    for box in person_boxes:
        x1, y1, x2, y2 = box.tolist()
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)  # 초록색 박스 그리기

    # 이미지 파일로 저장
    frame_number += 1
    filename = f"D:\\\\yolo_cam\\frame_{frame_number:04d}.jpg"  # 파일 이름에 프레임 번호 추가
    cv2.imwrite(filename, frame)
    # 'q' 키를 눌러 종료
    #if cv2.waitKey(1) == ord('q'):
    #    break

# 종료
cap.release()
cv2.destroyAllWindows()