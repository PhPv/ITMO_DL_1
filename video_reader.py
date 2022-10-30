import sys

import cv2

from model.base import Frame
from model.pipeline import Pipeline


def video_process(video_path: str):
    pipeline = Pipeline()

    vidcap = cv2.VideoCapture(video_path)
    while True:
        try:
            _, image = vidcap.read()
            frame = Frame(img=image)
            pipeline.process(frame)
            pipeline.draw(frame)
            cv2.imshow("Preprocess Video", frame.img)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
        except:
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    video_path = sys.argv[1]
    video_process(video_path)
