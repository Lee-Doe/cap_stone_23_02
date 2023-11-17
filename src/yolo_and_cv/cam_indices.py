import cv2

for i in range(10):
    cap = cv2.VideoCapture(i)
    if not cap.isOpened():
        break
    print(f"Camera {i}: {cap.get(3)} x {cap.get(4)}")
    cap.release()