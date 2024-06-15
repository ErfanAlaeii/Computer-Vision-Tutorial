import cv2
import numpy as np

# Initialize the webcam
cap = cv2.VideoCapture(0)
cv2.namedWindow('Control Panel')


# The structure is as follows:

# lower=[The lower range of in hue_spectrum,50,50]
# upper=[The upper range of in hue_spectrum,255,255]


# Function to do nothing on trackbar change
def nothing(x):
    pass


# Create trackbars for color change
cv2.createTrackbar('LowerH', 'Control Panel', 0, 179, nothing)
cv2.createTrackbar('LowerS', 'Control Panel', 0, 255, nothing)
cv2.createTrackbar('LowerV', 'Control Panel', 0, 255, nothing)
cv2.createTrackbar('UpperH', 'Control Panel', 179, 179, nothing)
cv2.createTrackbar('UpperS', 'Control Panel', 255, 255, nothing)
cv2.createTrackbar('UpperV', 'Control Panel', 255, 255, nothing)


# Function to get current trackbar positions
def get_trackbar_values():
    lower_h = cv2.getTrackbarPos('LowerH', 'Control Panel')
    lower_s = cv2.getTrackbarPos('LowerS', 'Control Panel')
    lower_v = cv2.getTrackbarPos('LowerV', 'Control Panel')
    upper_h = cv2.getTrackbarPos('UpperH', 'Control Panel')
    upper_s = cv2.getTrackbarPos('UpperS', 'Control Panel')
    upper_v = cv2.getTrackbarPos('UpperV', 'Control Panel')
    return (lower_h, lower_s, lower_v), (upper_h, upper_s, upper_v)


# Main loop to capture video frames and apply color detection
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get current positions of the trackbars
    lower_bound, upper_bound = get_trackbar_values()

    # Create a mask with the specified bounds
    mask = cv2.inRange(hsv_frame, np.array(lower_bound), np.array(upper_bound))

    # Apply the mask to the original frame
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Display the original frame and the masked frame
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Masked Frame', result)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()
