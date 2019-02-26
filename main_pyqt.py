# -*- coding: utf-8 -*-
# @Author: vivekpatel99
# @Date:   2018-10-06 15:43:12
# @Last Modified by:   vivekpatel99
# @Last Modified time: 2018-10-06 16:43:29

"""
The main script calls functions from all the modules

"""

import sys
from PyQt4 import QtGui
from PyQt4.QtGui import QPixmap, QImage
from PyQt4.QtCore import QTimer
import cv2

# modules
from pyqt_gui import menu
from lib.vision.vision import Vision
from tasks.face_recog import face_recog
from tasks.motion_detection import motion_detect
from tasks.object_recognition import object_recognition
import config

from lib._logger import _logging

# -----------------------------------------------
""" constants declaration  """
WHITE = (255, 255, 255)

# Frames per second
FPS = 60

TASK_INDEX = 0


# ------------------------------------------------------------------------------
# """ Menu to display all items on screen """
# ------------------------------------------------------------------------------
class Menu(menu.Ui_objectName, QtGui.QMainWindow):

    def __init__(self, log):
        super(Menu, self).__init__()
        self.setupUi(self)  # to be able to see interface
        self.frame = None
        self.timer = QTimer(self)
        self.log = log
        self.vid = Vision()

        self.Stop_btn.clicked.connect(self.stop_webcam)
        self.Start_btn.clicked.connect(self.start_webcam)
        self.Stop_btn.clicked.connect(self.stop_webcam)
        self.Closed_btn.clicked.connect(self.close)

        self.face_recognition_btn.clicked.connect(self.face_recognition)

    def start_webcam(self):
        """  """
        self.timer.timeout.connect(self.update_frame)  # connected until timeout
        self.timer.start(1)

    def capture_and_resize_frame(self):
        _, self.frame = self.vid.getVideo()
        resize_frame = self.vid.resize_frame(self.frame)
        cv2.flip(resize_frame, 1)
        return resize_frame

    def update_frame(self):
        """ """
        resize_frame= self.capture_and_resize_frame()
        self.display_image(resize_frame)

    def stop_webcam(self):
        self.timer.stop()

    def display_image(self, img):
        qformat = QImage.Format_Indexed8
        if img is not None:
            if len(img.shape) == 3:  # [0]=rows, [1]=cols, [2]=channels
                if img.shape[2] == 4:
                    qformat = QImage.Format_RGBA8888
                else:
                    qformat = QImage.Format_RGB888
            out_img = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
            # BGR >> RGB
            out_img = out_img.rgbSwapped()
            self.video_label.setPixmap(QPixmap.fromImage(out_img))
            self.video_label.setScaledContents(True)

    def face_recognition(self):
        pass

    def close(self):
        self.log.info("close button pressed")
        self.timer.stop()
        self.log.info("cleaning up")

        # release the resources
        self.vid.videoCleanUp()
        self.log.info("closing Application safely")
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
    my_menu = Menu(log)
    my_menu.show()
    app.exec_()
