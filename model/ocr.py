import os
import sys
import re

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import easyocr

ROOT_DIR = os.path.abspath(os.curdir)
print(ROOT_DIR)


def show_image(image_path):
    image = mpimg.imread(image_path)
    plt.imshow(image, cmap="gray")


def detection_recognize(image_path):

    reader = easyocr.Reader(["ru"],gpu=True)
    result = reader.readtext(image_path, detail=0)
    result = result[0].upper()
    result_rec = []

    for i, character in enumerate(result):
        try:
            ch = re.match(u"[А-Яа-яA-Za-z]",character)[0]
            if ch=='О':
                ch='0'
            if int(i)<=5:
                result_rec.append(ch)
        except TypeError:
            try:
                ch = re.match(r"\d",character)[0]
                result_rec.append(ch)
            except TypeError:
                continue
    
    return ''.join(result_rec)


if __name__ == "__main__":
    image_path = sys.argv[1]
    show_image(image_path)
    plt.show()
    print(detection_recognize(image_path))


# python3 ocr.py /home/nikolaypavlychev/ITMO_DL_1/car_tracking/ITMO_DL_1/autoriaNumberplateOcrRu/test/img/A001BP54.png
# /home/nikolaypavlychev/ITMO_DL_1/car_tracking/ITMO_DL_1/itmo_dl_env/bin/python -m  ./model/ocr.py /home/nikolaypavlychev/ITMO_DL_1/car_tracking/ITMO_DL_1/autoriaNumberplateOcrRu/test/img/A001PC71.png
# image_path = '/home/pavlychev/ITMO_DL_1/car_tracking/ITMO_DL_1/autoriaNumberplateOcrRu/test/img/A001PC71.png'
# print(detection_recognize(image_path))

