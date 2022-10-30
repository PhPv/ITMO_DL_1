import cv2
import torch

from model.base import Frame, Model


class Detection(Model):

    TORCH_HUB_YOLO_VERSION = "ultralytics/yolov5:v6.0"

    def __init__(self):
        self.model = torch.hub.load(
            "ultralytics/yolov5", "custom", path="data/models/best_model.pt"
        )
        self.model.conf = 0.05
        self.model.iou = 0.9

    def process(self, frame):
        results = self.model(frame.img)
        frame.car = ...
        frame.licence = list(map(int, results.xyxy[0][0][:4]))


if __name__ == "__main__":
    yolo = Detection()
    img = cv2.imread("data/Cars109.png")
    frame = Frame(img)
    yolo.process(frame)
