import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

cap = cv2.VideoCapture(0)

detector = FaceMeshDetector(maxFaces=1)



while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    ret, frame = cap.read()

    frame, faces = detector.findFaceMesh(frame, draw=False)


    if faces:
        for i in range(0, len(faces[0])):
            cv2.putText(frame, str(i), (faces[0][i][0], faces[0][i][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.2,
                        (0, 0, 255), 1, cv2.LINE_AA)



    cv2.imshow("farme", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
