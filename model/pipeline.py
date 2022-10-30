import cv2

from model.base import Frame
from model.detection import Detection
from model.ocr_model import OCR


class Pipeline:
    def __init__(self):
        self.detection = Detection()
        self.ocr = OCR()

    def process(self, frame: Frame):
        self.detection.process(frame)
        self.ocr.process(frame)

    def draw(self, frame):
        x1, y1, x2, y2 = frame.license
        cv2.rectangle(frame.img, (x1, y1), (x2, y2), (255, 0, 0), -1)
        print("License:", frame.recognition_license)
