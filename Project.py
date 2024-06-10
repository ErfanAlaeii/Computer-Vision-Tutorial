import cv2
import time
import PoseModule as pm

cap = cv2.VideoCapture(0)
pTime = 0
detector = pm.PoseDetector()



while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    frame = detector.findPose(frame)
    lm_list = detector.findPosition(frame, draw=False)

    if lm_list:
        print(f"Landmark 10 position: {lm_list[10]}")
        cv2.circle(frame, (lm_list[10][1], lm_list[10][2]), 10, (100, 0, 110), -1)

    cTime = time.time()
    fps = 1 / (cTime - pTime) if cTime != pTime else 0
    pTime = cTime

    cv2.putText(frame, f'FPS: {int(fps)}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Pose Estimation', frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
detector.pose.close()
