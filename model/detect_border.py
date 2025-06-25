import cv2
import numpy as np
import os
import csv

def detect_border(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    border = {"top": 0, "bottom": 0, "left": 0, "right": 0}
    sides = []

    for i in range(h):
        if np.std(gray[i]) > 5:
            border["top"] = i
            sides.append("top")
            break
    for i in range(h - 1, -1, -1):
        if np.std(gray[i]) > 5:
            border["bottom"] = h - i - 1
            sides.append("bottom")
            break
    for i in range(w):
        if np.std(gray[:, i]) > 5:
            border["left"] = i
            sides.append("left")
            break
    for i in range(w - 1, -1, -1):
        if np.std(gray[:, i]) > 5:
            border["right"] = w - i - 1
            sides.append("right")
            break

    return border, sides

def process_images(input_path, output_csv):
    results = []
    files = [os.path.join(input_path, f) for f in os.listdir(input_path)
             if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    for path in files:
        filename = os.path.basename(path)
        image = cv2.imread(path)
        border, sides = detect_border(image)
        results.append([
            filename,
            border["top"], border["bottom"],
            border["left"], border["right"],
            ', '.join(sides)
        ])
    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["name", "Top", "Bottom", "Left", "Right", "Detected_Sides"])
        writer.writerows(results)
