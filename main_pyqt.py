# -*- coding: utf-8 -*-
# @Author: vivekpatel99
# @Date:   2018-10-06 15:43:12
# @Last Modified by:   vivekpatel99
# @Last Modified time: 2018-10-06 16:43:29

"""

pyuic4 -x manu.ui -0 qt_menu.py
The main script calls functions from all the modules

"""

import sys
import time

import cv2
import imutils
from PyQt4 import QtGui
from PyQt4.QtGui import QPixmap, QImage
from PyQt4 import QtCore
from PyQt4.QtCore import QTimer
from imutils.video import VideoStream
from imutils.video import FPS

# modules
import config
from pyqt_gui import menu
from lib._logger import _logging
from tasks.face_recog import face_recog
from tasks.motion_detection import motion_detect
from tasks.object_recognition import object_recognition
from tasks.feat_detect import feat_detect

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


# ------------------------------------------------------------------------------
# """ Menu to display all items on screen """
# ------------------------------------------------------------------------------
class Menu(menu.Ui_objectName, QtGui.QMainWindow):

    def __init__(self):
        frwd_bkwd_bnt_cnt = 0
        super(Menu, self).__init__()
        # face_recog.FaceRecognition.__init__(self)

        self.setupUi(self)  # to be able to see interface
        self.frame = None
        self.timer = QTimer(self)
        self.vid = VideoStream(src=0)  # camera initialization
        self.fps = FPS()  # frame per second counter initialization

        # Button pressed actions # ------------------
        self.Stop_btn.clicked.connect(self.stop_webcam)
        self.Start_btn.clicked.connect(self.start_webcam)
        self.Stop_btn.clicked.connect(self.stop_webcam)
        self.Closed_btn.clicked.connect(self.close)
        self.face_recognition_btn.clicked.connect(self.face_recog_btn_pressed)
        self.motion_detection_btn.clicked.connect(self.motion_detect_btn_pressed)
        self.object_tracking_btn.clicked.connect(self.object_recognition_btn_pressed)
        self.Feature_Detection_btn.clicked.connect(self.feature_detect_btn_pressed)
        self.backward_btn.clicked.connect(self.backword_btn_pressed)
        self.forward_btn.clicked.connect(self.forword_btn_pressed)

        # Taskes  initialization # ------------------
        # Face Recognition #
        self.face_recog_obj = face_recog.FaceRecognition()
        self.face_recog_obj.classifier_init()
        self.face_recog_obj.recognizer_init()
        self.face_recog_obj.labels_load()

        # motion detection #
        self.motion_detect_ob = motion_detect.MotionDetection()

        # object Recognition detection #
        self.object_recog_obj = object_recognition.ObjectRecognition()

        # feature detection #
        self.feat_detect_obj = feat_detect.FeatureDetection()

    # -------------------------------------------------------------------
    # """ start_webcam """
    # -------------------------------------------------------------------

    def start_webcam(self):
        """  """
        self.vid.start()  # start the camera
        self.timer.timeout.connect(self.update_frame)  # connected until timeout
        self.timer.start(1000.0 / 28.0)

        # start the FPS counter
        self.fps.start()

    # -------------------------------------------------------------------
    # """ face_recog_btn_pressed """
    # -------------------------------------------------------------------

    def face_recog_btn_pressed(self):
        """  """
        self.fps.stop()
        self.timer.timeout.connect(self.face_recognition)  # connected until timeout
        self.timer.start(1000.0 / 12.0)
        self.info_label.setText(face_recog.TASK_TITLE + '\n' + face_recog.TASK_INFO)
        # start the FPS counter
        self.fps.start()

    # -------------------------------------------------------------------
    # """ motion_detect_btn_pressed """
    # -------------------------------------------------------------------

    def motion_detect_btn_pressed(self):
        """  """
        self.fps.stop()
        self.timer.timeout.connect(self.motion_detection)  # connected until timeout
        self.timer.start(1000.0 / 28.0)
        self.info_label.setText(motion_detect.TASK_TITLE + '\n' + motion_detect.TASK_INFO)
        # start the FPS counter
        self.fps.start()

    # -------------------------------------------------------------------
    # """ object_recognition_btn_pressed """
    # -------------------------------------------------------------------

    def object_recognition_btn_pressed(self):
        """  """
        self.fps.stop()
        self.timer.timeout.connect(self.object_recognition)  # connected until timeout
        self.timer.start(1000.0 / 28.0)
        self.info_label.setText(object_recognition.TASK_TITLE + '\n' + object_recognition.TASK_INFO)
        # start the FPS counter
        self.fps.start()

    # -------------------------------------------------------------------
    # """ feature_detect_btn_pressed """
    # -------------------------------------------------------------------

    def feature_detect_btn_pressed(self):
        """  """
        self.fps.stop()
        self.timer.timeout.connect(self.feature_detection)  # connected until timeout
        self.timer.start(1000.0 / 28.0)
        self.info_label.setText(feat_detect.TASK_TITLE + '\n' + feat_detect.TASK_INFO)
        # start the FPS counter
        self.fps.start()

    # -------------------------------------------------------------------
    # """ capture_and_resize_frame """
    # -------------------------------------------------------------------
    def preprocessed_frame(self):
        """ """
        self.frame = self.vid.read()
        # resize_frame = imutils.resize(self.frame, width=640)
        return self.frame

    # -------------------------------------------------------------------
    # """ main """
    # -------------------------------------------------------------------
    def update_frame(self):
        """ """
        frame = self.preprocessed_frame()

        # covert image into gray for processing
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.display_image(frame)
        self.fps.update()  # update the FPS counter

    # -------------------------------------------------------------------
    # """ display_image """
    # -------------------------------------------------------------------
    def display_image(self, image):
        out_img = QImage(image, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(out_img))

    # -------------------------------------------------------------------
    # """ face_recognition """
    # -------------------------------------------------------------------
    def face_recognition(self):
        frame = self.preprocessed_frame()

        try:
            (x, y), frame = self.face_recog_obj.run_face_recognition(frame)
            self.fps.update()  # update the FPS counter
        except TypeError:
            pass
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.display_image(frame)

    # -------------------------------------------------------------------
    # """ motion_detection """
    # -------------------------------------------------------------------
    def motion_detection(self):
        frame = self.preprocessed_frame()
        try:
            (center_x, center_y), _frame = self.motion_detect_ob.run_motion_subtrator(frame)
            self.fps.update()  # update the FPS counter
        except TypeError:
            pass
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.display_image(frame)

    # -------------------------------------------------------------------
    # """ object_recognition """
    # -------------------------------------------------------------------
    def object_recognition(self):
        frame = self.preprocessed_frame()
        try:
            (x, y), frame = self.object_recog_obj.run_object_recognition(frame)
            self.fps.update()  # update the FPS counter
        except TypeError:
            pass
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.display_image(frame)

    # -------------------------------------------------------------------
    # """ feature_detection """
    # -------------------------------------------------------------------
    def feature_detection(self):
        _frame = None
        frame = self.preprocessed_frame()
        try:
            _frame = self.feat_detect_obj.run_feat_detect(frame)
            self.fps.update()  # update the FPS counter
        except:
            pass
        if _frame is not None:
            frame = _frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.display_image(frame)

    # -------------------------------------------------------------------
    # """ stop_webcam """
    # -------------------------------------------------------------------
    def stop_webcam(self):
        self.timer.stop()

        # stop the timer and display FPS information
        self.fps.stop()
        log.info("Elapsed time: {:.2f}".format(self.fps.elapsed()))
        log.info("Approx. FPS: {:.2f}".format(self.fps.fps()))

    # -------------------------------------------------------------------
    # """ close """
    # -------------------------------------------------------------------
    def close(self):
        log.info("close button pressed")
        self.timer.stop()

        # stop the timer and display FPS information
        self.fps.stop()
        try:
            log.info("Elapsed time: {:.2f}".format(self.fps.elapsed()))
            log.info("Approx. FPS: {:.2f}".format(self.fps.fps()))
        except TypeError:
            pass
        log.info("cleaning up")
        cv2.destroyAllWindows()
        self.vid.stop()  # release the resources
        log.info("closing Application safely")
        sys.exit(0)


if __name__ == '__main__':
    log = _logging.logger_init(log_filepath="obj_track_img_recog.log", project_name="main")
    app = QtGui.QApplication([])
    my_menu = Menu()
    my_menu.show()
    app.exec_()
