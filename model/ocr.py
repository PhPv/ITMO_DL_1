import os
import sys

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import easyocr

ROOT_DIR = os.path.abspath(os.curdir)
print(ROOT_DIR)

# TODO: обернуть в класс Model, OCR будет на вход получать Frame.number, а зполнять frame.recognise_number
def show_image(image_path):
    image = mpimg.imread(image_path)
    plt.imshow(image, cmap="gray")


def detection_recognize(image_path):

    reader = easyocr.Reader(["ru"])
    result = reader.readtext(image_path, detail=0)
    if len(result) == 1:
        print("auto number:", result[0][:8])
        return result[0][:8]
    if len(result) == 3:
        print("auto number:", result[0][:6] + result[2])
        return result[0][:6] + result[2]
    else:
        print("Don't recognize")
        return None


if __name__ == "__main__":
    image_path = sys.argv[1]
    show_image(image_path)
    plt.show()
    print(detection_recognize(image_path))


# python3 ocr.py /home/nikolaypavlychev/ITMO_DL_1/autoriaNumberplateOcrRu/test/img/A001BP54.png
