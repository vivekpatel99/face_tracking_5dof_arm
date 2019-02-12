# -*- coding: utf-8 -*-
# @Author: vivekpatel99
# @Date:   2018-10-06 15:10:40
# @Last Modified by:   vivekpatel99
# @Last Modified time: 2018-10-06 19:39:14

"""
This module contains class and functions for the gui

 pyuic5 -x qt_gui.ui -o qt_gui.py

"""

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
import cv2
import time
from PyQt5.uic import loadUi
import pygame

#from lib.vision.vision import Vision


class test(QMainWindow):
    def __init__(self):
        super(test, self).__init__()
        loadUi('test.ui', self)
        self.frame = None

        """ modification """
        # self.Start_btn.clicked.connect(self.start_webcam)
        self.Stop_btn.clicked.connect(self.stop_webcam)

    # def start_webcam(self):

        self.Start_btn.clicked.connect(self.start_webcam)
        self.Stop_btn.clicked.connect(self.stop_webcam)

    def start_webcam(self):

        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.timer.start(5)

    def update_frame(self):
        ret, self.frame = self.capture.read()
        self.image = cv2.flip(self.frame, 1)
        self.display_image(self.frame, 1)

        pygame.display.update()

    def stop_webcam(self):
        self.timer.stop()

    def display_image(self, img, window=1):
        qfomat = QImage.Format_Indexed8
        if len(img.shape) == 3:  # [0]=rows, [1]=cols, [2]=channels
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        out_img = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        # BGR >> RGB
        out_img = out_img.rgbSwapped()

        if window == 1:
            self.image_label.setPixmap(QPixmap.fromImage(out_img))
            self.image_label.setScaledContents(True)


def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = test()
    # ui.setupUi(MainWindow)
    ui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
