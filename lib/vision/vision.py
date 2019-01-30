import numpy as np
import cv2
import sys
from imutils.video import VideoStream
import imutils
import time

# minimum size (in pixel) for a region of image to be considered actual "motion"
MIN_AREA = 500
CAM_NUM = 0


class Vision:
    def __init__(self):
        print("setting up the video capture ......")
        self.cap = cv2.VideoCapture(CAM_NUM)
        self.frame_width = 0
        self.frame_height = 0

    def isCameraConnected(self):
        return self.cap.isOpened()

    def getVideo(self):

        ret, frame = self.cap.read()

        try:  # check if it is really a frame
            self.frame = frame.copy()

        except:
            print("ERROR: frame  is not captured")

        if not ret:  # check if there was no frame captured
            print ("ERROR: while capturing frame")

        return ret, frame

    def getFrameSize(self):
        """ return the size of the frame """
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        return [self.frame_width, self.frame_height]

    def display(self, window, frame):
        cv2.imshow(window, frame)

    def videoCleanUp(self):
        self.cap.release()
        cv2.destroyAllWindows()


def test():
    vid = Vision()
    vid.isCameraConnected()

    while True:
        ret, frame = vid.getVideo()
        vid.display('img', frame)

        if cv2.waitKey(30) & 0xFF == ord("q"):
            break

    vid.videoCleanUp()


if __name__ == '__main__':
    test()
