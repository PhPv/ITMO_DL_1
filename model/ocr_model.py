import os
import glob
import re
import sys
from tqdm import tqdm

import pandas as pd
from sklearn.metrics import accuracy_score

current_dir=os.getcwd()
sys.path.append(current_dir)

from model import ocr
from model.ocr import detection_recognize
import importlib
importlib.reload(ocr)


letters = {
        u'A': u'А',
        u'B' : u'В',
        u'C' : u'С',
        u'E' : u'Е',
        u'H': u'Н',
        u'K': u'К',
        u'M': u'М',
        u'O' : u'О',
        u'P' : u'Р',
        u'T' : u'Т',
        u'Y' : u'У',
        u'X' : u'Х'      
    }


class Model(object):
    def __init__(self,image_path):
        self.image_path = image_path

    def recognize(self,image_path):
        recognize_list = []
        recognize = detection_recognize(image_path)
        recognize_post = []
        for i, ch in enumerate(recognize):
            if (ch=='О')&(i in [1,2,3]):
                recognize_post.append('0')
            if (ch=='0')&(i in [0]):
                recognize_post.append('О')
            else:
                recognize_post.append(ch)
            recognize_post_str = ''.join(recognize_post)

        recognize_list.append(recognize_post_str)

        return recognize_list[0]





