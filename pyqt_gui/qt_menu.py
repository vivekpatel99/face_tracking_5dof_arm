# Created by viv at 26.02.19
""" https://www.aparat.com/v/zZCnk/OpenCV_Python_GUI_Development_Tutorial_4%3A_Laod_and_Display_OpenCV """
from PyQt4 import QtGui
from PyQt4.QtGui import QPixmap, QImage
from PyQt4.QtCore import QTimer
import cv2

import menu
# from lib.vision.vision import Vision


class Menu(menu.Ui_objectName, QtGui.QMainWindow):

    def __init__(self):
        super(Menu, self).__init__()
        self.setupUi(self)  # to be able to see interface
        self.frame = None

        self.Stop_btn.clicked.connect(lambda: self.stop_webcam)
        self.Start_btn.clicked.connect(self.start_webcam)
        self.Stop_btn.clicked.connect(self.stop_webcam)

    def start_webcam(self):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # self.vid = Vision()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame) # connected until timeout
        self.timer.start(1)

    def update_frame(self):
        ret, self.frame = self.capture.read()
        self.image = cv2.flip(self.frame, 1)
        self.display_image(self.frame, 1)

    def stop_webcam(self):
        self.timer.stop() 

        # release the resources
        self.capture.release()
        cv2.destroyAllWindows()

    def display_image(self, img, window=1):
        if img is not None:
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
                self.video_label.setPixmap(QPixmap.fromImage(out_img))
                self.video_label.setScaledContents(True)


if __name__ == "__main__":
    app = QtGui.QApplication([])
    my_menu = Menu()
    my_menu.show()
    app.exec_()
