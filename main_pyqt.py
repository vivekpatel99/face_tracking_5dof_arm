# -*- coding: utf-8 -*-
# @Author: vivekpatel99
# @Date:   2018-10-06 15:43:12
# @Last Modified by:   vivekpatel99
# @Last Modified time: 2018-10-06 16:43:29

"""

pyuic4 -x menu.ui -0 menu.py
The main script calls functions from all the modules

"""

import os
import sys
<<<<<<< HEAD
import os
import cv2
from PyQt5.uic import loadUi
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage
=======

import signal
import cv2
import numpy as np
from PIL import Image
from PyQt5 import QtGui
from PyQt5 import QtWidgets
>>>>>>> 195a8254b82368f501ad94d40bbe626df9032472
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
from imutils.video import FPS
import numpy as np
from PIL import Image

# modules
import config
<<<<<<< HEAD
from lib.udp import udp
from lib import platform_init
from lib._logger import _logging
from tasks.face_recog import face_recog
from tasks.motion_detection import motion_detect
from tasks.object_recognition import object_recognition
from tasks.feat_detect import feat_detect


=======
from lib import platfrom_init
from lib._logger import _logging
from lib.udp import udp
from lib.gpio import pwm
from lib.kinematics import ikine
from tasks.face_recog import face_recog
from tasks.feat_detect import feat_detect
from tasks.motion_detection import motion_detect
from tasks.object_recognition import object_recognition
>>>>>>> 195a8254b82368f501ad94d40bbe626df9032472

# UI_WINDOW, _ = uic.loadUiType('pyqt_gui/menu.ui')

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
UI_FILE = os.path.join(SCRIPT_PATH, 'pyqt_gui/menu.ui')
PLAY_ICON = os.path.join(SCRIPT_PATH, 'pyqt_gui/icons/play.png')
STOP_ICON = os.path.join(SCRIPT_PATH, 'pyqt_gui/icons/stop.png')
PAUSE_ICON = os.path.join(SCRIPT_PATH, 'pyqt_gui/icons/pause.png')
FORWD_ICON = os.path.join(SCRIPT_PATH, 'pyqt_gui/icons/forward.png')
BACKWD_ICON = os.path.join(SCRIPT_PATH, 'pyqt_gui/icons/backward.png')
CLOSE_ICON = os.path.join(SCRIPT_PATH, 'pyqt_gui/icons/close.png')
PALYER_ICON = os.path.join(SCRIPT_PATH, 'pyqt_gui/icons/player.png')


# ------------------------------------------------------------------------------
# """ Menu to display all items on screen """
# ------------------------------------------------------------------------------
class Menu(QtWidgets.QMainWindow):
    frwd_bkwd_bnt_cnt = 0

    def __init__(self):
        super(Menu, self).__init__()

<<<<<<< HEAD

=======
>>>>>>> 195a8254b82368f501ad94d40bbe626df9032472
        loadUi(UI_FILE, self)
        self.showFullScreen()

        # self.setupUi(self)  # to be able to see interface
        self.timer = QTimer(self)
        # self.vid = VideoStream(src=0)  # camera initialization
        self.fps = FPS()  # frame per second counter initialization
        self.udp_send = udp.UdpPacket(udp_ip=config.IP, udp_port=config.PORT)

        # Button pressed actions # ------------------
        self.Stop_btn.clicked.connect(self.stop_webcam)
        self.Stop_btn.setIcon(QtGui.QIcon(STOP_ICON))
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
<<<<<<< HEAD
=======

        # PWM initialization for each gpio pin # ------------------
        self.pwm_objs = [pwm.PulseWidthModulation(servo_port_addr=gpio_addr, servo_cal_info=servo_cal) for
                        gpio_addr, servo_cal in config.UTILIZED_GPIO]

        # finding appropriate function for given degrees of freedom
        self.cal_ik = ikine.IK_FUNC_DICT[[dof for dof in ikine.IK_FUNC_DICT if len(self.pwm_objs) == dof][0]]
        log.info('{} selected'.format(self.cal_ik))
>>>>>>> 195a8254b82368f501ad94d40bbe626df9032472

    # -------------------------------------------------------------------
    # """ start_webcam """
    # -------------------------------------------------------------------

    def start_webcam(self):
        """  """
        #       self.vid.start()  # start the camera
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
        # frame = self.vid.read()
        with open('/dev/fb1', 'rb') as img:
            frame = img.read()
<<<<<<< HEAD
=======

        # 'P' mode = 8-bit pixels mapped to any other mode using a color palette
        # 'L' mode = 8-bit pixels black and white
>>>>>>> 195a8254b82368f501ad94d40bbe626df9032472
        return np.array(Image.frombytes('L', (640, 480), frame))

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
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.display_image(frame)
        self.fps.update()  # update the FPS counter

    # -------------------------------------------------------------------
    # """ display_image """
    # -------------------------------------------------------------------
    def display_image(self, frame):
        with open('/dev/fb2', 'wb') as fil:
            fil.write(frame)
        # qformat = QtGui.QImage.Format_Indexed8
        # if len(frame.shape) == 3:
        #     if frame.shape[2] == 4:
        #         qformat = QtGui.QImage.Format_RGBA8888
        #     else:
        #         qformat = QtGui.QImage.Format_RGB888
        #
        # out_img = QImage(frame, frame.shape[1], frame.shape[0], qformat)
        # # out_img = QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        # self.video_label.setPixmap(QPixmap.fromImage(out_img))

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
<<<<<<< HEAD
            # self.udp_send.udp_packet_send(x=x, y=y, frame=_frame)
            self.fps.update()  # update the FPS counter
        except TypeError:
            pass
=======
            thetas_list = self.cal_ik(x_axis=x, y_axis=y)
            self.pwm_generate(thetas_list)
            print(thetas_list)
        except TypeError:
            pass

        self.fps.update()  # update the FPS counter
>>>>>>> 195a8254b82368f501ad94d40bbe626df9032472
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
<<<<<<< HEAD
            self.fps.update()  # update the FPS counter
            self.udp_send.udp_packet_send(x=center_x, y=center_y, frame=_frame)
=======
            thetas_list = self.cal_ik(x_axis=center_x, y_axis=center_y)

            self.pwm_generate(thetas_list)
>>>>>>> 195a8254b82368f501ad94d40bbe626df9032472

        except TypeError:
            pass

<<<<<<< HEAD
=======
        self.fps.update()  # update the FPS counter
>>>>>>> 195a8254b82368f501ad94d40bbe626df9032472
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
<<<<<<< HEAD
                self.udp_send.udp_packet_send(x=x, y=y, frame=_frame)
=======
                # self.udp_send.udp_packet_send(x=x, y=y, frame=_frame)
>>>>>>> 195a8254b82368f501ad94d40bbe626df9032472
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
<<<<<<< HEAD
            self.udp_send.udp_packet_send(x=x, y=y, frame=_frame)
            self.fps.update()  # update the FPS counter
        except TypeError:
            pass
=======
            # self.udp_send.udp_packet_send(x=x, y=y, frame=_frame)

        except TypeError:
            pass
        self.fps.update()  # update the FPS counter
>>>>>>> 195a8254b82368f501ad94d40bbe626df9032472
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
    # """ PWM Generate """
    # -------------------------------------------------------------------
    def pwm_generate(self, theta_list):
        for pwm_pin_obj, theta in zip(self.pwm_objs, theta_list):
            pwm_pin_obj.generate_pwm(theta)
            # pwm_jb0.generate_pwm(abs(thetas.theta_1))
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
        # self.vid.stop()  # release the resources
        log.info("Closing Application safely")
        sys.exit(0)

from pyqt_gui.icons import icons

if __name__ == '__main__':
<<<<<<< HEAD
    # platfrom_init.platform_clear()
    log = _logging.logger_init(log_filepath="obj_track_img_recog.log", project_name="main")
    # platform_init.platform_init()
    app = QtWidgets.QApplication(sys.argv)
    my_menu = Menu()
    my_menu.show()
    sys.exit(app.exec_())
#    app.exec_()
=======

    platfrom_init.platform_clear()
    log = _logging.logger_init(log_filepath="obj_track_img_recog.log", project_name="main")
    platfrom_init.platform_init()
    app = QtWidgets.QApplication(sys.argv)
    signal.signal(signal.SIGINT, lambda *a: app.quit())
    my_menu = Menu()
    my_menu.show()
    sys.exit(app.exec_())
    # app.exec_()
>>>>>>> 195a8254b82368f501ad94d40bbe626df9032472
