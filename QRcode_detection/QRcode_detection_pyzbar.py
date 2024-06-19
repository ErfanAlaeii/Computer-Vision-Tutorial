import numpy as np
import argparse
import os
from pyzbar.pyzbar import decode
import cv2


def preprocess_image(image: np.ndarray) -> np.ndarray:
    """Convert the image to grayscale and apply threshold to improve QR code detection."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    return binary


def draw_qr_bounds(image: np.ndarray, qr_codes) -> None:
    """Draw bounding boxes around detected QR codes and display their data."""
    for qr in qr_codes:
        points = qr.polygon
        if len(points) == 4:
            pts = np.array([[point.x, point.y] for point in points], dtype=np.int32)
            cv2.polylines(image, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
        rect = qr.rect
        cv2.putText(image, qr.data.decode('utf-8'), (rect.left, rect.top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


def process_img(image: np.ndarray) -> np.ndarray:
    """Process an image to detect QR codes and draw bounding boxes."""
    preprocessed_image = preprocess_image(image)
    qr_codes = decode(preprocessed_image)
    if qr_codes:
        draw_qr_bounds(image, qr_codes)
    return image


def main() -> None:
    parser = argparse.ArgumentParser(description='QR Code Detector.')
    parser.add_argument('-m', '--mode', required=True, choices=['image', 'video', 'webcam'],
                        help='Mode: image, video, or webcam.')
    parser.add_argument('-f', '--filePath', help='Path to the image or video file for QR code detection.')
    parser.add_argument('-d', '--deviceIndex', type=int, default=0, help='Index of the webcam device (default: 0).')
    parser.add_argument('-o', '--outputDir', default='output', help='Directory to save the output files.')

    args = parser.parse_args()
    output_dir = args.outputDir
    os.makedirs(output_dir, exist_ok=True)

    if args.mode == 'image':
        if not args.filePath or not os.path.isfile(args.filePath):
            print("Invalid image file path.")
            return

        img = cv2.imread(args.filePath)
        if img is None:
            print("Error reading image.")
            return

        processed_img = process_img(img)
        cv2.imwrite(os.path.join(output_dir, 'output.png'), processed_img)
        print("Image saved to", os.path.join(output_dir, 'output.png'))

    elif args.mode == 'video':
        if not args.filePath or not os.path.isfile(args.filePath):
            print("Invalid video file path.")
            return

        cap = cv2.VideoCapture(args.filePath)
        if not cap.isOpened():
            print("Error opening video file.")
            return

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_rate = cap.get(cv2.CAP_PROP_FPS) or 25

        output_video = cv2.VideoWriter(
            os.path.join(output_dir, 'output.mp4'),
            cv2.VideoWriter_fourcc(*'MP4V'),
            frame_rate,
            (frame_width, frame_height)
        )

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            processed_frame = process_img(frame)
            output_video.write(processed_frame)

        cap.release()
        output_video.release()
        print("Video saved to", os.path.join(output_dir, 'output.mp4'))

    elif args.mode == 'webcam':
        cap = cv2.VideoCapture(args.deviceIndex)
        if not cap.isOpened():
            print(f"Error opening webcam (index {args.deviceIndex}).")
            return

        print("Press 'q' to quit the webcam view.")
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            processed_frame = process_img(frame)
            cv2.imshow('Webcam', processed_frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()


# Example usage:
# You can run this script with the following commands in the terminal:
# python script_name.py -m image -f example.png
# python script_name.py-m video -f example.mp4
# python script_name.py -m webcam
