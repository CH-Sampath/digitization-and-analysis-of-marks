import cv2
import numpy as np


def remove_red_and_orange(image_path):
    # read the image
    image = cv2.imread(image_path)
    # cv2.imshow("lol", image)
    img2 = image[:]  # make a copy

    # Grayscale image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Convert the image from BGR to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create the HSV/
    lowerValues1 = np.array([0, 50, 70])
    upperValues1 = np.array([9, 255, 255])

    red1mask = cv2.inRange(hsv_image, lowerValues1, upperValues1)

    lowerValues2 = np.array([159, 50, 70])
    upperValues2 = np.array([180, 255, 255])

    red2mask = cv2.inRange(hsv_image, lowerValues2, upperValues2)

    lowerValues3 = np.array([10, 50, 70])
    upperValues3 = np.array([24, 255, 255])

    ora1mask = cv2.inRange(hsv_image, lowerValues3, upperValues3)

    red1mask = red1mask + red2mask + ora1mask

    colorMask = cv2.add(gray_image, red1mask)
    _, binaryImage = cv2.threshold(colorMask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh, im_bw = cv2.threshold(binaryImage, 210, 230, cv2.THRESH_BINARY)
    kernel = np.ones((1, 1), np.uint8)
    imgfinal = cv2.dilate(im_bw, kernel=kernel, iterations=1)

    # cv2.imshow("imgfinal", red1mask)
    # cv2.waitKey(0)

    wid = red1mask.shape[0]
    hei = red1mask.shape[1]

    edged = cv2.Canny(red1mask, 30, 200)

    # Finding Contours
    # Use a copy of the image e.g. edged.copy()
    # since findContours alters the image
    contours, hierarchy = cv2.findContours(edged.copy(),
                                           cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Draw all contours
    # -1 signifies drawing all contours
    # cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
    for i in contours:
        (x, y, w, h) = cv2.boundingRect(i)
        if w > 0.55 * wid and h > 0.32 * hei:
            print(x, y)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            img2 = img2[y:y + h, x:x + w]
    # cv2.imshow("img2", img2)
    # cv2.waitKey(0)
    return img2
    # cv2.imwrite("4.bmp", img2)
# remove_red_and_orange("D:\CSE_SEM_III\DLD\840009_230865.bmp")
