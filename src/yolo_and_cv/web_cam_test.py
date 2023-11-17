import cv2

# 웹캠 연결
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)  # 0은 디폴트 웹캠을 의미, 다른 숫자를 사용하여 다른 카메라를 선택할 수 있음

while True:
    # 프레임 읽기
    ret, frame = cap.read()

    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    # 여기에 YOLOv5 모델을 적용하는 코드 추가

    # 화면에 프레임 표시
    cv2.imshow("Frame", frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 작업 완료 후 해제
cap.release()
#cv2.destroyAllWindows()