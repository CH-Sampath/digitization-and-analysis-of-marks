import os
import cv2
from excel_marks import txt2excel
from crop_final import crop_final
from remove_cache import rmcache
from resi import mod_img
from GUI import login_screen
from gpg import gpg
from gui_entry_final import process_marks

#######
if input("Enter yes for analysis: ") == "yes":
    login_screen()

else:
    sub = input("Enter the subject name: ")
    sem = input("Enter the semester: ")
    acyear = input("Enter the academic year: ")
    input_dir = input("Enter the input directory: ")
    output_dir = "C:\\major-version1.0\\output_test"
    image_files = [f for f in os.listdir(input_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    # Check if there are any images in the directory
    if len(image_files) > 0:
        # Read the first image in the directory
        first_image_path = os.path.join(input_dir, image_files[0])
        image = cv2.imread(first_image_path)

        # Get the width and height of the image
        height, width, _ = image.shape
        if width >= 1050 and width <= 1200:
            mod_img(input_dir, "C:\\major-version1.0\\resizedto1400", (1430, 822), (200, 200))
            input_dir = "C:\\major-version1.0\\resizedto1400"
    else:
        print("No image files found in the specified directory.")

    crop_final(sub, input_dir, output_dir)  # if this does not happen?? what will you do?

    os.system(
        "python yolov7/detect.py --weights C:\\major-version1.0\\best-epoch400.pt --save-conf --conf-thres 0.4 "
        "--conf 0.1 --source C:/major-version1.0/output_test --save-txt --img-size 128")

    # marks to excel
    txt2excel(sub, sem, acyear, input_dir)

    # delete any cache
    rmcache(output_dir)




