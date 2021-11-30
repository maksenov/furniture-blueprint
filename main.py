# -*- coding: utf-8 -*-

import os
import numpy as np
import cv2
from screeninfo import get_monitors

# requirements winsound
#import winsound

def find_all(basename, path):
    """ The function searches for the file name with given basename at the given path recursively.
The function ignores the extension of the file on disk. It returns all files with the basename at the different
subdirectories with different extensions. """
    result = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if basename == os.path.splitext(file)[0]:
                result.append(os.path.join(root, file))
    if len(result) == 0:
        print(f"File '{basename}' not found")

    return result

def create_default_image():
    """ The function creates the default image. The image is shown whenever the real image cannot be shown. """
    screen_id = 0
    is_color = True

    # get the size of the screeny
    width, height = 640, 480 #screen.width, screen.height

    # create image
    if is_color:
        offset = 200
        default_image = np.ones((height, width, 3), dtype=np.float32)
        default_image[:offset, :offset] = 0  # black at top-left corner
        default_image[height - offset:, :offset] = [1, 0, 0]  # blue at bottom-left
        default_image[:offset, width - offset:] = [0, 1, 0]  # green at top-right
        default_image[height - offset:, width - offset:] = [0, 0, 1]  # red at bottom-right
    else:
        default_image = np.ones((height, width), dtype=np.float32)
        default_image[0, 0] = 0  # top-left corner
        default_image[height - 2, 0] = 0  # bottom-left
        default_image[0, width - 2] = 0  # top-right
        default_image[height - 2, width - 2] = 0  # bottom-right

    return default_image

ERROR = 'Error'
SUCCESS = 'Success'

def beep(type):
    """ """
    if type == ERROR:
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 50  # Set Duration To 1000 ms == 1 second
    else:
        frequency = 5500  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)

def read_file_name_from_keyboard():
    """ """
    file_name = ""
    exit_app = False

    while (len(file_name) == 0) and not exit_app:
        key = cv2.waitKey()
        while (key != ord('\r')) and (key != ord('\n')):
            if key == 27:
                exit_app = True
                break

            file_name += chr(key)
            key = cv2.waitKey()
    return (file_name, exit_app)

def create_opencv_image_from_stringio(img_stream, cv2_img_flag=cv2.IMREAD_COLOR):
    img_stream.seek(0)
    img_array = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
    return cv2.imdecode(img_array, cv2_img_flag)

def get_image(files, default_image):
    """ """
    image = default_image
    type = ERROR

    if len(files) == 0:
        print(f"File not found")
    elif len(files) > 1:
        print(f"Duplicate files found for file '{file_name}' candidates are:")
        print(files)
    else:
        full_path = files[0]
        print(f"Load file: {full_path}")
        try:
            with open(files[0], "rb") as fstream:
                image = create_opencv_image_from_stringio(fstream)
                type = SUCCESS
        except cv2.error as error:
            print("[Error]: to load default_image {} {}".format(full_path, error))

    return (image, type)

def main_loop():
    """ """
    default_image = create_default_image()

    window_name = 'Scanner renderer (press Escape to exit)'
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    width = 600
    height = 400
    for m in get_monitors():
        width = m.width
        height = m.height

    cv2.moveWindow(window_name, 0, 0)
    task_bar_height = 100
    cv2.resizeWindow(window_name, width - 1, height - task_bar_height)
    cv2.imshow(window_name, default_image)

    exit_app = False
    file_name = "non existing file"

    directory = os.getcwd()
    cv2.imshow(window_name, default_image)

    while not exit_app:
        print('-----------------------------------------')
        print('Wait for scanner...')

        file_name, exit_app = read_file_name_from_keyboard()

        if exit_app:
            break

        print(f'Read from scanner: ')
        files = find_all(file_name, directory)

        image, type = get_image(files, default_image)

        try:
            cv2.imshow(window_name, image)
        except cv2.error as error:
            print("[Error]: show image falied {}".format(error))
            type = ERROR
            cv2.imshow(window_name, default_image)


#        beep(type)

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main_loop()
