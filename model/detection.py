from model.base import Model, Frame
import torch
import cv2


class Detection(Model):
    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload=True)

    def process(self, frame):
        results = self.model(frame.img)
        print(results.xyxy[0])
        frame.car = ...
        frame.number = ...


if __name__ == "__main__":
    yolo = Detection()
    img = cv2.imread('data/test_img.jpg')
    frame = Frame(img)
    yolo.process(frame)