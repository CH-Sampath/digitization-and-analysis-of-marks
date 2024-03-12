import cv2
from crop_to_square import remove_red_and_orange
from barcode import get_barcode
from pre_process import resize_and_pad
import os

def crop_final(sub, input_dir, output_dir):
    cols = [0.00931, 0.182, 0.365, 0.556, 0.745]
    rows = [0.01547, 0.093, 0.1725, 0.25, 0.331, 0.403, 0.48, 0.5633, 0.641, 0.7233, 0.8059, 0.9]
    dir = input_dir
    for fil in os.listdir(dir):
        f = os.path.join(dir, fil)
        # barcode = get_barcode(f)
        img = remove_red_and_orange(f)
        wid, hei = img.shape[:2]
        for i, row in enumerate(rows[:len(rows) - 1]):
            for j, col in enumerate(cols[:len(cols) - 1]):
                cropped = img[int(rows[i] * wid) - 4: int(rows[i + 1] * wid) + 3,
                          int(cols[j] * hei): int(cols[j + 1] * hei) + 2]
                cropped = resize_and_pad(cropped)
                # filename = input_dir + "-" + fil[: fil.find(".")] + "-" + barcode + f"result_{i}_{j}.bmp"
                filename = sub+"-"+fil[: fil.find(".")] + f"-result_{i}_{j}.jpg"
                if i == 0 or j == 0:
                    continue
                else:

                    cv2.imwrite(os.path.join(output_dir, filename), cropped)
                    # # cv2.imshow("lol", cropped))
    # pre process image


# cv2.imshow("lol", img[int(0.097*hei): int(0.172*hei), int(0.182*wid): int(0.365*wid)])
# cv2.waitKey(0)
