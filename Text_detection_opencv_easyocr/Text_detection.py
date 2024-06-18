import easyocr
import requests
import numpy as np
import cv2
import matplotlib.pyplot as plt


# Function to read image from URL and convert to RGB
def imread_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    image_array = np.array(bytearray(response.content), dtype=np.uint8)
    image_bgr = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    return image_rgb


# Use the function to load an image from a URL
url = 'https://cdn.bannerbuzz.com/media/catalog/product/resize/650/b/b/bbcomps6611_bb_03.jpg'
image = imread_from_url(url)

reader = easyocr.Reader(['en'], gpu=False)

text = reader.readtext(image)


for t in text:
    print(t)
