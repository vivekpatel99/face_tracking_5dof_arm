import os

import numpy as np
import cv2
import sys
from imutils.video import FPS
from imutils.video import VideoStream
import config
import imutils
import time

# minimum size (in pixel) for a region of image to be considered actual "motion"
MIN_AREA = 500
CAM_NUM = 0


# ------------------------------------------------------------------------------
# """ CLASS: MAIN """
# ------------------------------------------------------------------------------
class Vision:
    """s
    Class for wrapping OpenCV functionality with some checks
    """

    def __init__(self):
        print("setting up the video capture ......")
        self.cap = cv2.VideoCapture(CAM_NUM)
        self.frame_width = 0
        self.frame_height = 0

        if not self.cap.isOpened():
            print("[ERROR] Camera is not connected")
            sys.exit(1)

    # ------------------------------------------------------------------------------
    # """ FUNCTION: checks if the camera is connected """
    # ------------------------------------------------------------------------------
    def isCameraConnected(self):
        """
        checks if the camera is connected
        :return: True or False if the camera is connected
        """
        return self.cap.isOpened()

    # ------------------------------------------------------------------------------
    # """ FUNCTION: taking frame from camera """
    # ------------------------------------------------------------------------------
    def getVideo(self):
        """
         The function will capture frame from camera and check that the frame is captured or not
        :return: ret: True or False if the frame is captured
                 frame : video frame
        """
        ret, frame = self.cap.read()

        try:  # check if it is really a frame
            self.frame = frame.copy()

        except:
            print("ERROR: frame  is not captured")

        if not ret:  # check if there was no frame captured
            print("ERROR: while capturing frame")

        return ret, frame

    # ------------------------------------------------------------------------------
    # """ FUNCTION: return size of the frame """
    # ------------------------------------------------------------------------------
    def getFrameSize(self):
        """
         return list of size of the frame
        :return: [width, height]
        """
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        return [self.frame_width, self.frame_height]
    # ------------------------------------------------------------------------------
    # """ FUNCTION: return size of the frame """
    # ------------------------------------------------------------------------------
    def resize_frame(self, frame, size=(config.HORIZ_PIXELS_SMALL, config.VERT_LINES_SMALL)):

        resize_frame = cv2.resize(frame, size)

        return resize_frame
    # ------------------------------------------------------------------------------
    # """ FUNCTION: Display the Video frame """
    # ------------------------------------------------------------------------------
    def display(self, window, frame):
        """
        Display Video frame with its name on the window

        :param window: name of the frame
        :param frame: Video frame
        :return:
        """
        cv2.imshow(window, frame)

    # ------------------------------------------------------------------------------
    # """ FUNCTION: Cleaning up  """
    # ------------------------------------------------------------------------------
    def videoCleanUp(self):
        """
        clean up
        :return:
        """
        self.cap.release()
        cv2.destroyAllWindows()


# ------------------------------------------------------------------------------
# """ FUNCTION: Demo function """
# ------------------------------------------------------------------------------
def test():
    vid = Vision()
    vid.isCameraConnected()
    fps = FPS().start()
    while True:
        ret, frame = vid.getVideo()
        vid.display('img', frame)
        fps.update()
        if cv2.waitKey(30) & 0xFF == ord("q"):
            break

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    vid.videoCleanUp()



def test_2():
    print("[INFO] sampling frames from webcam...")
    stream = VideoStream(src=0).start()
    fps = FPS().start()

    # loop over some frames
    while True:
        # grab the frame from the stream and resize it to have a maximum
        # width of 400 pixels
        frame = stream.read()
        # frame = imutils.resize(frame, width=640)

        cv2.imshow("Frame", frame)
        fps.update()

        # update the FPS counter
        if cv2.waitKey(30) & 0xFF == ord("q"):
            break

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    # do a bit of cleanup
    cv2.destroyAllWindows()
    stream.stop()
if __name__ == '__main__':
    test()
