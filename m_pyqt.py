# Created by viv at 14.03.19
# -*- coding: utf-8 -*-
# @Author: vivekpatel99
# @Date:   2018-10-06 15:43:12
# @Last Modified by:   vivekpatel99
# @Last Modified time: 2018-10-06 16:43:29

"""
The main script calls functions from all the modules

"""

import sys
import cv2
import imutils
from PyQt4 import QtGui
from PyQt4.QtGui import QPixmap, QImage
from PyQt4.QtCore import QTimer
from imutils.video import FPS
from imutils.video import VideoStream

# modules
# import config
from pyqt_gui import menu
from lib._logger import _logging
from tasks.face_recog import face_recog
from tasks.motion_detection import motion_detect
from tasks.object_recognition import object_recognition

# -----------------------------------------------
""" constants declaration  """
WHITE = (255, 255, 255)

# Frames per second
# FPS = 60

TASK_INDEX = 0


# TODO
#  1. create a class for face recognition
#  2. inherite the class into Menu class
#  3. run the face detection
#  4. benchnark the frame rate

class VideoCaptureThread():
    def __init__(self):

        self.frame = None
        self.vid = VideoStream(src=0)

    def run(self):

        while (RUNNING):
            _, self.frame = self.vid.getVideo()
            resize_frame = self.vid.resize_frame(self.frame)
            frame = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2RGB)
            out_frame = QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)

            if self.queue.qsize() < 10:
                self.queue.put(out_frame)


# ------------------------------------------------------------------------------
# """ Menu to display all items on screen """
# ------------------------------------------------------------------------------
class Menu(menu.Ui_objectName, QtGui.QMainWindow):

    def __init__(self):
        super(Menu, self).__init__()
        self.setupUi(self)  # to be able to see interface
        self.frame = None
        self.timer = QTimer(self)
        # self.timer.setTimerType(Qt.PreciseTimer)
        self.Stop_btn.clicked.connect(self.stop_webcam)
        self.Start_btn.clicked.connect(self.start_webcam)
        self.Stop_btn.clicked.connect(self.stop_webcam)
        self.Closed_btn.clicked.connect(self.close)

        self.face_recognition_btn.clicked.connect(self.face_recognition)

        self.vid = VideoStream(src=0)
        self.fps = FPS()

    # -------------------------------------------------------------------
    # """ start_webcam """
    # -------------------------------------------------------------------

    def start_webcam(self):
        """  """
        self.vid.start()
        self.timer.timeout.connect(self.update_frame)  # connected until timeout
        self.timer.start(1000.0 / 28.0)

        # start the FPS counter
        self.fps.start()

    # -------------------------------------------------------------------
    # """ capture_and_resize_frame """
    # -------------------------------------------------------------------
    def capture_and_resize_frame(self):
        """ """
        self.frame = self.vid.read()
        resize_frame = imutils.resize(self.frame, width=640)

        return resize_frame

    # -------------------------------------------------------------------
    # """ main """
    # -------------------------------------------------------------------
    def update_frame(self):
        """ """
        resize_frame = self.capture_and_resize_frame()
        frame = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2RGB)
        self.display_image(frame)

        # update the FPS counter
        self.fps.update()

    # -------------------------------------------------------------------
    # """ stop_webcam """

    def stop_webcam(self):
        self.timer.stop()

        # stop the timer and display FPS information
        self.fps.stop()
        log.info("Elapsed time: {:.2f}".format(self.fps.elapsed()))
        log.info("Approx. FPS: {:.2f}".format(self.fps.fps()))

    # -------------------------------------------------------------------
    # """ display_image """
    # -------------------------------------------------------------------
    def display_image(self, image):
        out_img = QImage(image, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(out_img))

    # -------------------------------------------------------------------
    # """ main """
    # -------------------------------------------------------------------
    def face_recognition(self):
        pass

    # -------------------------------------------------------------------
    # """ close """
    # -------------------------------------------------------------------
    def close(self):
        log.info("close button pressed")
        self.timer.stop()

        # stop the timer and display FPS information
        self.fps.stop()
        log.info("Elapsed time: {:.2f}".format(self.fps.elapsed()))
        log.info("Approx. FPS: {:.2f}".format(self.fps.fps()))

        log.info("cleaning up")
        cv2.destroyAllWindows()
        self.vid.stop()  # release the resources
        log.info("closing Application safely")
        sys.exit(0)


# ----------------------------------------------------------------------------------------------------------------------
# """ main """
# ----------------------------------------------------------------------------------------------------------------------

def main():
    """
    """
    log = _logging.logger_init(log_filepath="obj_track_img_recog.log", project_name="main")
    log.info("main script starts")

    while True:

        if config.EXIT:
            break

        while config.CAM_START:

            if config.TASK_INDEX is 1:
                face_recog.face_recog_pygm(screen, disply_obj, FPS)

            if config.TASK_INDEX is 2:
                motion_detect.motion_detection_pygm(screen, disply_obj, FPS)

            if config.TASK_INDEX is 3:
                object_recognition.object_recog_pygm(screen, disply_obj)

            if not config.CAM_START or config.EXIT:
                log.info("Camera is OFF")
                break

        if config.EXIT:
            break

    pygame.quit()
    log.info("exiting from the main...")


if __name__ == '__main__':
    log = _logging.logger_init(log_filepath="obj_track_img_recog.log", project_name="main")
    app = QtGui.QApplication([])
    my_menu = Menu()
    my_menu.show()
    app.exec_()
