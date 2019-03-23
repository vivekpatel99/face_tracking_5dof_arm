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
from PyQt4 import QtGui
from PyQt4.QtGui import QPixmap, QImage
from PyQt4.QtCore import QTimer
from imutils.video import VideoStream
from imutils.video import FPS

# modules
import config
from lib.udp import udp
from pyqt_gui import menu
from lib._logger import _logging
from tasks.face_recog import face_recog
from tasks.motion_detection import motion_detect
from tasks.object_recognition import object_recognition
from tasks.feat_detect import feat_detect


# TODO
#  1. create a class for face recognition
#  2. inherite the class into Menu class
#  3. run the face detection
#  4. benchnark the frame rate


# ------------------------------------------------------------------------------
# """ Menu to display all items on screen """
# ------------------------------------------------------------------------------
class Menu(menu.Ui_objectName, QtGui.QMainWindow):
    frwd_bkwd_bnt_cnt = 0

    def __init__(self):
        super(Menu, self).__init__()

        self.setupUi(self)  # to be able to see interface
        self.timer = QTimer(self)
        self.vid = VideoStream(src=0)  # camera initialization
        self.fps = FPS()  # frame per second counter initialization
        self.udp_send = udp.UdpPacket(udp_ip=config.IP, udp_port=config.PORT)

        # Button pressed actions # ------------------
        self.Stop_btn.clicked.connect(self.stop_webcam)
        self.Start_btn.clicked.connect(self.start_webcam)
        self.Stop_btn.clicked.connect(self.stop_webcam)
        self.Closed_btn.clicked.connect(self.close)
        self.face_recognition_btn.clicked.connect(self.face_recog_btn_pressed)
        self.motion_detection_btn.clicked.connect(self.motion_detect_btn_pressed)
        self.object_tracking_btn.clicked.connect(self.object_recognition_btn_pressed)
        self.Feature_Detection_btn.clicked.connect(self.feature_detect_btn_pressed)
        self.backward_btn.clicked.connect(self.backward_btn_pressed)
        self.forward_btn.clicked.connect(self.forward_btn_pressed)

        # Tasks initialization # ------------------
        self.face_recog_obj = face_recog.FaceRecognition()
        self.motion_detect_ob = motion_detect.MotionDetection()
        self.object_recog_obj = object_recognition.ObjectRecognition()
        self.feat_detect_obj = feat_detect.FeatureDetection()

    # -------------------------------------------------------------------
    # """ start_webcam """
    # -------------------------------------------------------------------

    def start_webcam(self):
        """  """
        self.vid.start()  # start the camera
        self.timer.timeout.connect(self.update_frame)  # connected until timeout
        self.timer.start(1000.0 / 28.0)
        self.fps.start()  # start the FPS counter

    # -------------------------------------------------------------------
    # """ start_webcam """
    # -------------------------------------------------------------------
    def task_init_setup(self, task_function, frame_rate=28):
        """

        :param task_function:
        :param frame_rate:
        :return:
        """
        # closed  timer and fps counter
        self.timer.stop()
        self.fps.stop()

        # setup the timer and FPS counter
        self.timer = QTimer(self)
        self.fps = FPS()  # frame per second counter initialization

        self.timer.timeout.connect(task_function)  # connected until timeout

        self.timer.start(1000.0 / float(frame_rate))
        self.fps.start()  # start the FPS counter

    # -------------------------------------------------------------------
    # """ face_recog_btn_pressed """
    # -------------------------------------------------------------------

    def face_recog_btn_pressed(self):
        """

        :return:
        """
        self.task_init_setup(self.face_recognition)
        self.info_label.setText(face_recog.TASK_TITLE + '\n' + face_recog.TASK_INFO)

    # -------------------------------------------------------------------
    # """ motion_detect_btn_pressed """
    # -------------------------------------------------------------------

    def motion_detect_btn_pressed(self):
        """

        :return:
        """
        self.task_init_setup(self.motion_detection)
        self.info_label.setText(motion_detect.TASK_TITLE + '\n' + motion_detect.TASK_INFO)

    # -------------------------------------------------------------------
    # """ object_recognition_btn_pressed """
    # -------------------------------------------------------------------

    def object_recognition_btn_pressed(self):
        """

        :return:
        """
        self.task_init_setup(self.object_recognition)
        self.info_label.setText(object_recognition.TASK_TITLE + '\n' + object_recognition.TASK_INFO)

    # -------------------------------------------------------------------
    # """ feature_detect_btn_pressed """
    # -------------------------------------------------------------------

    def feature_detect_btn_pressed(self):
        """

        :return:
        """
        self.task_init_setup(self.feature_detection)
        self.info_label.setText(feat_detect.TASK_TITLE + '\n' + feat_detect.TASK_INFO)

    # -------------------------------------------------------------------
    # """ backward_btn_pressed """
    # -------------------------------------------------------------------
    @staticmethod
    def backward_btn_pressed():
        if Menu.frwd_bkwd_bnt_cnt >= 1:
            Menu.frwd_bkwd_bnt_cnt -= 1

    # -------------------------------------------------------------------
    # """ forward_btn_pressed """
    # -------------------------------------------------------------------
    @staticmethod
    def forward_btn_pressed():
        if Menu.frwd_bkwd_bnt_cnt <= 1:
            Menu.frwd_bkwd_bnt_cnt += 1

    # -------------------------------------------------------------------
    # """ capture_and_resize_frame """
    # -------------------------------------------------------------------
    def preprocessed_frame(self):
        """ """
        frame = self.vid.read()
        return frame

    # -------------------------------------------------------------------
    # """ update_frame """
    # -------------------------------------------------------------------
    def update_frame(self):
        """ """
        frame = self.preprocessed_frame()

        if frame is None:
            log.error('Camera is not connected')
            sys.exit(1)

        # covert image into gray for processing
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.display_image(frame)
        self.fps.update()  # update the FPS counter

    # -------------------------------------------------------------------
    # """ display_image """
    # -------------------------------------------------------------------
    def display_image(self, frame):
        qformat = QtGui.QImage.Format_Indexed8
        if len(frame.shape) == 3:
            if frame.shape[2] == 4:
                qformat = QtGui.QImage.Format_RGBA8888
            else:
                qformat = QtGui.QImage.Format_RGB888

        out_img = QImage(frame, frame.shape[1], frame.shape[0], qformat)
        # out_img = QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(out_img))

    # -------------------------------------------------------------------
    # """ face_recognition """
    # -------------------------------------------------------------------
    def face_recognition(self):
        """

        :return:
        """
        frame = self.preprocessed_frame()

        _frame = None  # processed output frame
        try:
            (x, y), _frame = self.face_recog_obj.run_face_recognition(frame, Menu.frwd_bkwd_bnt_cnt)
            self.udp_send.udp_packet_send(x=x, y=y, frame=_frame)
            self.fps.update()  # update the FPS counter
        except TypeError:
            pass
        if _frame is not None:
            frame = _frame
        self.display_image(frame)

    # -------------------------------------------------------------------
    # """ motion_detection """
    # -------------------------------------------------------------------
    def motion_detection(self):
        """

        :return:
        """
        frame = self.preprocessed_frame()

        _frame = None  # processed output frame
        center_x, center_y = None, None  # location  of motion
        try:

            (center_x, center_y), _frame = self.motion_detect_ob.run_motion_subtrator(frame, Menu.frwd_bkwd_bnt_cnt)
            self.fps.update()  # update the FPS counter
            self.udp_send.udp_packet_send(x=center_x, y=center_y, frame=_frame)

        except TypeError:
            pass

        if _frame is not None:
            frame = _frame

        self.display_image(frame)

    # -------------------------------------------------------------------
    # """ object_recognition """
    # -------------------------------------------------------------------
    def object_recognition(self):
        """

        :return:
        """
        frame = self.preprocessed_frame()

        _frame = None  # processed output frame
        try:
            (x, y), _frame = self.object_recog_obj.run_object_recognition(frame, Menu.frwd_bkwd_bnt_cnt)
            if x and y:
                self.udp_send.udp_packet_send(x=x, y=y, frame=_frame)
                self.fps.update()  # update the FPS counter
        except TypeError:
            pass
        if _frame is not None:
            frame = _frame

        self.display_image(frame)

    # -------------------------------------------------------------------
    # """ feature_detection """
    # -------------------------------------------------------------------
    def feature_detection(self):
        """

        :return:
        """
        frame = self.preprocessed_frame()

        _frame = None  # processed output frame
        try:
            (x, y), _frame = self.feat_detect_obj.run_feat_detect(frame, Menu.frwd_bkwd_bnt_cnt)
            self.udp_send.udp_packet_send(x=x, y=y, frame=_frame)
            self.fps.update()  # update the FPS counter
        except TypeError:
            pass
        if _frame is not None:
            frame = _frame
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.display_image(frame)

    # -------------------------------------------------------------------
    # """ stop_webcam """
    # -------------------------------------------------------------------
    def stop_webcam(self):
        """

        :return:
        """
        self.timer.stop()

        # stop the timer and display FPS information
        self.fps.stop()
        log.info("Elapsed time: {:.2f}".format(self.fps.elapsed()))
        log.info("Approx. FPS: {:.2f}".format(self.fps.fps()))

    # -------------------------------------------------------------------
    # """ close """
    # -------------------------------------------------------------------
    def close(self):
        log.info("Close button pressed")
        self.timer.stop()

        # stop the timer and display FPS information
        self.fps.stop()
        try:
            log.info("Elapsed time: {:.2f}".format(self.fps.elapsed()))
            log.info("Approx. FPS: {:.2f}".format(self.fps.fps()))
        except TypeError:
            pass

        log.info("Cleaning up")
        cv2.destroyAllWindows()
        self.vid.stop()  # release the resources
        log.info("Closing Application safely")
        sys.exit(0)


if __name__ == '__main__':
    log = _logging.logger_init(log_filepath="obj_track_img_recog.log", project_name="main")
    app = QtGui.QApplication([])
    my_menu = Menu()
    my_menu.show()
    app.exec_()
