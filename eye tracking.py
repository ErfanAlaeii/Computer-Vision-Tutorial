import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

# Initialize the video capture (use 0 for webcam or the file path for a video file)
cap = cv2.VideoCapture(0)  # Change 0 to the path of your video file if needed

# Initialize the face mesh detector
detector = FaceMeshDetector(maxFaces=1)

# Initialize the plot for displaying blink count over time
plotY = LivePlot(yLimit=[20, 50])

# Blink variables
blinkCount = 0
blinkThreshold = 30  # Adjust the threshold based on testing
blinkFrameCount = 0
ratioList = []

# List of landmark IDs for left eye (example set, adjust as needed)
leftEyeIDs = [159, 23, 130, 243, 27, 130]

while True:

    # Check if the video has ended, and if so, restart it
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Capture frame-by-frame
    success, frame = cap.read()

    # Detect face mesh
    frame, faces = detector.findFaceMesh(frame, draw=False)
    frame = cv2.resize(frame, (640, 480))  # Resize frame for better display

    if faces:
        face = faces[0]

        # Extract left eye landmarks
        leftEyePoints = [face[i] for i in leftEyeIDs]

        # Calculate vertical and horizontal distances
        leftUp = leftEyePoints[0]
        leftDown = leftEyePoints[1]
        leftLeft = leftEyePoints[2]
        leftRight = leftEyePoints[3]

        lengthVer, _ = detector.findDistance(leftUp, leftDown)
        lengthHor, _ = detector.findDistance(leftLeft, leftRight)

        # Calculate the ratio of vertical to horizontal distances
        ratio = int((lengthVer / lengthHor) * 100)
        ratioList.append(ratio)

        # Maintain a list of the last three ratios
        if len(ratioList) > 3:
            ratioList.pop(0)

        # Calculate the average ratio
        ratioAvg = sum(ratioList) / len(ratioList)

        # Detect blinks based on the ratio average and threshold
        if ratioAvg < blinkThreshold:
            blinkFrameCount += 1
        else:
            if blinkFrameCount > 0:
                blinkCount += 1
                blinkFrameCount = 0

        # Draw circles at each left eye landmark
        for point in leftEyePoints:
            cv2.circle(frame, point, 5, (255, 0, 0), -1)

        # Display the blink count on the frame
        cvzone.putTextRect(frame, f'Blink Count: {blinkCount}', (50, 100), scale=2, thickness=2, colorR=(255, 0, 255))

        # Update and display the plot of the ratio average
        imgPlot = plotY.update(ratioAvg)

        # Stack the frame and plot images side by side
        imgStack = cvzone.stackImages([frame, imgPlot], 2, 1)
        cv2.imshow("Image", imgStack)
    else:
        # Display the frame if no faces are detected
        cv2.imshow("Image", frame)

    # Break the loop on 'Esc' key press
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
