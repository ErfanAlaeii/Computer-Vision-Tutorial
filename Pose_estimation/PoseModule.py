# Importing required libraries
import cv2  # OpenCV library for video processing
import mediapipe as mp  # MediaPipe library for pose estimation
import time  # Time library for calculating FPS

# Define a class for pose detection
class PoseDetector:
    def __init__(self, mode=False, smooth=True, detectionCon=0.5, trackCon=0.5):
        """
        Initializes the PoseDetector class with configuration parameters.

        Parameters:
        mode (bool): Static image mode (True for image, False for video).
        smooth (bool): Apply smoothing to landmark coordinates.
        detectionCon (float): Minimum detection confidence threshold.
        trackCon (float): Minimum tracking confidence threshold.
        """
        self.mode = mode
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # Initialize MediaPipe pose components
        self.mpDraw = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=self.mode,
            model_complexity=1,
            smooth_landmarks=self.smooth,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )

    def findPose(self, frame, draw=True):
        """
        Detects pose landmarks in the frame and optionally draws them.

        Parameters:
        frame (numpy.ndarray): The input image frame.
        draw (bool): If True, draws landmarks on the frame.

        Returns:
        numpy.ndarray: The frame with landmarks drawn.
        """
        # Convert the frame to RGB as MediaPipe uses RGB images
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Process the frame to detect pose landmarks
        self.results = self.pose.process(frameRGB)
        # If landmarks are detected, draw them on the frame
        if self.results.pose_landmarks and draw:
            self.mpDraw.draw_landmarks(frame, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return frame

    def findPosition(self, frame, draw=True):
        """
        Extracts pose landmarks positions and optionally draws them.

        Parameters:
        frame (numpy.ndarray): The input image frame.
        draw (bool): If True, draws landmarks on the frame.

        Returns:
        list: A list of landmark positions with format [id, x, y].
        """
        lm_list = []
        if self.results.pose_landmarks:
            # Iterate over each landmark and store its id and position
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
                # Draw the landmark on the frame if draw is True
                if draw:
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
        return lm_list

# Main function to capture video and perform pose detection
def main():
    # Open a connection to the default webcam
    cap = cv2.VideoCapture(0)
    pTime = 0  # Previous time for FPS calculation
    detector = PoseDetector()  # Create an instance of PoseDetector

    # Check if the webcam is successfully opened
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        # Detect pose in the frame
        frame = detector.findPose(frame)
        # Extract landmark positions without drawing
        lm_list = detector.findPosition(frame, draw=False)

        # If landmarks are detected, print and highlight the 11th landmark
        if lm_list:
            print(f"Landmark 10 position: {lm_list[10]}")
            cv2.circle(frame, (lm_list[10][1], lm_list[10][2]), 10, (100, 0, 110), -1)

        # Calculate and display the frames per second (FPS)
        cTime = time.time()
        fps = 1 / (cTime - pTime) if cTime != pTime else 0
        pTime = cTime

        cv2.putText(frame, f'FPS: {int(fps)}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Show the frame with pose estimation
        cv2.imshow('Pose Estimation', frame)

        # Exit the loop if 'Esc' key is pressed
        if cv2.waitKey(5) & 0xFF == 27:  # Press 'Esc' to exit
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    detector.pose.close()  # Close the MediaPipe resources properly


if __name__ == "__main__":
    main()
