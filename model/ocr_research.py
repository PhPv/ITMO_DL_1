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


data_dir = current_dir+'/autoriaNumberplateOcrRu/train/img/'


def rcg(data_dir):

    all_files = glob.glob(data_dir + "/*.png")[0:10]

    target_list = []
    files_list = []
    recognize_list = []

    pattern = re.compile('\/........\.png|\/.........\.png')

    for filename in all_files:
        try:
            number = pattern.search(filename)[0][1:].split('.')[0]
            if (len(number)==8)|(len(number)==9):
                files_list.append(filename)
                number_cyr = []
                for ch in number:
                    if ch in list(letters.keys()):
                        number_cyr.append(letters[ch])
                    else:
                        number_cyr.append(ch)
                number_cyr_str = ''.join(number_cyr)
                target_list.append(number_cyr_str)
        except TypeError:
            continue
        
    for file in tqdm(files_list):
        recognize = detection_recognize(file)
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

    return target_list, recognize_list


target_list, recognize_list = rcg(data_dir)
results = pd.DataFrame([], columns=['target','recognize'])
results['target'] = target_list
results['recognize'] = recognize_list

print('recognition accuracy : ',round(accuracy_score(results['target'],results['recognize']),2))

