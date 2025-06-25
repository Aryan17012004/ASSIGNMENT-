import cv2
import numpy as np
import os

def detect_cropping(image):
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h, w = grey.shape
    top, bottom, left, right = 0, h - 1, 0, w - 1
    for i in range(h):
        if np.std(grey[i]) > 5:
            top = i
            break
    for i in range(h - 1, -1, -1):
        if np.std(grey[i]) > 5:
            bottom = i
            break
    for i in range(w):
        if np.std(grey[:, i]) > 5:
            left = i
            break
    for i in range(w - 1, -1, -1):
        if np.std(grey[:, i]) > 5:
            right = i
            break

    return top, bottom, left, right

def process_images(input_path, output_path):
    os.makedirs(output_path, exist_ok=True)
    for filename in os.listdir(input_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            image_path = os.path.join(input_path, filename)
            image = cv2.imread(image_path)
            top, bottom, left, right = detect_cropping(image)
            cropped = image[top:bottom + 1, left:right + 1]
            cv2.imwrite(os.path.join(output_path, filename), cropped)
