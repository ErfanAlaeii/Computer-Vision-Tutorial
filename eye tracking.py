import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Initialize the face mesh detector and live plot
detector = FaceMeshDetector(maxFaces=1)
plotY = LivePlot(640, 480, [20, 50], invert=True)

# List of facial landmark IDs for the eyes
idlist = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]

# Initialize variables for blink detection
ratioList = []
blinkCount = 0
blinkThreshold = 30
blinkFrameCount = 0
color = 0

while True:
    # Reset the video frame position if at the end
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    ret, frame = cap.read()

    # Detect face mesh in the frame
    frame, faces = detector.findFaceMesh(frame, draw=False)

    if faces:
        face = faces[0]

        # for i in range(0, len(faces[0])):
        #     cv2.putText(frame, str(i), (faces[0][i][0], faces[0][i][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.2,
        #                 (0, 0, 255), 1, cv2.LINE_AA)

        # Draw circles on the eye landmarks
        for id in idlist:
            cv2.circle(frame, face[id], 3, (0, 255, 255), -1)

        # Calculate vertical and horizontal distances across the eye
        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        lenghtVer, _ = detector.findDistance(leftUp, leftDown)
        lenghtHor, _ = detector.findDistance(leftLeft, leftRight)
        cv2.line(frame, leftUp, leftDown, (0, 255, 0), 3)
        cv2.line(frame, leftLeft, leftRight, (0, 200, 0), 3)

        # print(int((lenghtVer/lenghtHor)*100))

        # Calculate the eye aspect ratio
        ratio = int((lenghtVer / lenghtHor) * 100)
        ratioList.append(ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)

        # Detect blinks based on the average ratio
        if ratioAvg < blinkThreshold:
            blinkFrameCount += 1
            color = (0, 255, 0)
        else:
            if blinkFrameCount > 0:
                blinkCount += 1
                blinkFrameCount = 0
                color = (255, 0, 255)

        # Display the blink count
        cvzone.putTextRect(frame, f"blinkCount:{blinkCount}", (50, 100), scale=2, thickness=2, colorR=color)

        # Update and display the plot with the ratio
        imgPlot = plotY.update(ratioAvg, color=color)

        # Resize and stack the frames
        frame = cv2.resize(frame, (640, 480))
        imgStack = cvzone.stackImages([imgPlot, frame], 2, 1)

    else:
        # If no face is detected, stack the frame twice
        frame = cv2.resize(frame, (640, 480))
        imgStack = cvzone.stackImages([frame, frame], 2, 1)

    # Show the stacked images
    cv2.imshow("frame", imgStack)
    if cv2.waitKey(25) & 0xFF == 27:
        break

# Clean up and close windows
cv2.destroyAllWindows()
