from model.base import Model, Frame
import torch
import cv2


class Detection(Model):

    TORCH_HUB_YOLO_VERSION = "ultralytics/yolov5:v6.0"

    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='data/models/best.pt')
        self.model.conf = 0.05
        self.model.iou = 0.9

    def process(self, frame):
        results = self.model(frame.img)
        frame.car = ...
        frame.licence = list(map(int, results.xyxy[0][0][:4]))

        # cv2.rectangle(frame.img, (x1, y1), (x2, y2), (255, 0, 0), -1)
        # # cv2.rectangle(image, (100, 150), (500, 600), (0, 255, 0), -1)
        # cv2.imwrite('data/test.png', frame.img)

if __name__ == "__main__":
    yolo = Detection()
    img = cv2.imread("data/Cars109.png")
    frame = Frame(img)
    yolo.process(frame)
