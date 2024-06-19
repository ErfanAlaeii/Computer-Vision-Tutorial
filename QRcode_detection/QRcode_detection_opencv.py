import cv2
import matplotlib.pyplot as plt

# Read the image
qrcode_img = cv2.imread('qrcode.png')

# Create a QRCodeDetector object
detector = cv2.QRCodeDetector()

# Detect and decode the QR code
value, box, _ = detector.detectAndDecode(qrcode_img)

# Print the decoded value
print(value)

# Check if a QR code was found
if box is not None:
    # Convert the box points to integers and extract the corners
    top_left = tuple(box[0][0].astype(int))
    bottom_right = tuple(box[0][2].astype(int))

    # Draw a rectangle around the detected QR code
    cv2.rectangle(qrcode_img, top_left, bottom_right, (0, 255, 0), 10)

    # Convert BGR image to RGB
    qrcode_img_rgb = cv2.cvtColor(qrcode_img, cv2.COLOR_BGR2RGB)

    # Display the image using matplotlib
    plt.imshow(qrcode_img_rgb)
    plt.axis('off')  # Hide axis
    plt.show()
else:
    print("No QR code detected")
