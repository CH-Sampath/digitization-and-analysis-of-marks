import cv2
import numpy as np
import os


def resize_and_pad(img, size=100):

    # Get the image's original dimensions
    h, w = img.shape[:2]

    # Determine padding
    if h > w:
        new_h, new_w = size, int(w * size / h)
        pad_vert = 0
        pad_horz = (size - new_w) // 2
    else:
        new_h, new_w = int(h * size / w), size
        pad_vert = (size - new_h) // 2
        pad_horz = 0

    # Resize image
    img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Pad image to make it square
    img = cv2.copyMakeBorder(img, pad_vert, pad_vert, pad_horz, pad_horz, cv2.BORDER_CONSTANT, value=[255, 255, 255])

    return img