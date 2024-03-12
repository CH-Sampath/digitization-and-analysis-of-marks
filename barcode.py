import cv2
from pyzbar.pyzbar import decode


def get_barcode(file_path):
    img = cv2.imread(file_path)
    detectedBarcodes = decode(img)
    for barcode in detectedBarcodes:
        (x, y, w, h) = barcode.rect
        # cv2.imshow("win", cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 5))
        # cv2.waitKey(0)
        # cv2.imwrite("resources/bar2.bmp", cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 5))
        dat = str(barcode.data)
        return dat[dat.find("\'") + 1:len(dat) - 1]


# file_path = "C:\\CVPROJECT3\\resources\\img1.bmp"
# get_barcode(file_path)
