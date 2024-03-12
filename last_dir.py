import os
import glob
# step 1

def get_last_directory(path):
    # Get all directories in the given path
    directories = glob.glob(f"{path}/*/")

    # Check if there are directories in the path
    if not directories:
        return None

    # Get the last modified directory
    last_directory = max(directories, key=os.path.getmtime)

    return last_directory


def navigate_to_last_directory(path):
    while True:
        last_directory = get_last_directory(path)
        if last_directory is None:
            break
        else:
            path = last_directory
    return path


# # Test the function
# start_path = "C:\\major-version1.0\\runs"  # replace with your folder path
# print(navigate_to_last_directory(start_path))
