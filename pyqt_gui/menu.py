# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_objectName(object):
    def setupUi(self, objectName):
        objectName.setObjectName(_fromUtf8("objectName"))
        objectName.resize(1084, 915)
        objectName.setMinimumSize(QtCore.QSize(1084, 915))
        objectName.setMaximumSize(QtCore.QSize(1084, 915))
        self.centralwidget = QtGui.QWidget(objectName)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.video_label = QtGui.QLabel(self.centralwidget)
        self.video_label.setGeometry(QtCore.QRect(20, 20, 640, 480))
        self.video_label.setFrameShape(QtGui.QFrame.StyledPanel)
        self.video_label.setFrameShadow(QtGui.QFrame.Plain)
        self.video_label.setText(_fromUtf8(""))
        self.video_label.setObjectName(_fromUtf8("video_label"))
        self.Start_btn = QtGui.QPushButton(self.centralwidget)
        self.Start_btn.setGeometry(QtCore.QRect(670, 20, 99, 27))
        self.Start_btn.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/play.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Start_btn.setIcon(icon)
        self.Start_btn.setObjectName(_fromUtf8("Start_btn"))
        self.Stop_btn = QtGui.QPushButton(self.centralwidget)
        self.Stop_btn.setGeometry(QtCore.QRect(670, 60, 99, 27))
        self.Stop_btn.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/stop.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Stop_btn.setIcon(icon1)
        self.Stop_btn.setObjectName(_fromUtf8("Stop_btn"))
        self.backward_btn = QtGui.QPushButton(self.centralwidget)
        self.backward_btn.setGeometry(QtCore.QRect(670, 470, 99, 27))
        self.backward_btn.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/backward.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backward_btn.setIcon(icon2)
        self.backward_btn.setObjectName(_fromUtf8("backward_btn"))
        self.forward_btn = QtGui.QPushButton(self.centralwidget)
        self.forward_btn.setGeometry(QtCore.QRect(670, 430, 99, 27))
        self.forward_btn.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/forwad.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.forward_btn.setIcon(icon3)
        self.forward_btn.setObjectName(_fromUtf8("forward_btn"))
        self.face_recognition_btn = QtGui.QPushButton(self.centralwidget)
        self.face_recognition_btn.setGeometry(QtCore.QRect(900, 70, 131, 41))
        self.face_recognition_btn.setObjectName(_fromUtf8("face_recognition_btn"))
        self.Closed_btn = QtGui.QPushButton(self.centralwidget)
        self.Closed_btn.setGeometry(QtCore.QRect(1020, 0, 51, 41))
        self.Closed_btn.setStyleSheet(_fromUtf8(""))
        self.Closed_btn.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/close_blue.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Closed_btn.setIcon(icon4)
        self.Closed_btn.setObjectName(_fromUtf8("Closed_btn"))
        self.motion_detection_btn = QtGui.QPushButton(self.centralwidget)
        self.motion_detection_btn.setGeometry(QtCore.QRect(900, 140, 131, 41))
        self.motion_detection_btn.setObjectName(_fromUtf8("motion_detection_btn"))
        self.object_tracking_btn = QtGui.QPushButton(self.centralwidget)
        self.object_tracking_btn.setGeometry(QtCore.QRect(900, 210, 131, 41))
        self.object_tracking_btn.setObjectName(_fromUtf8("object_tracking_btn"))
        self.info_label = QtGui.QLabel(self.centralwidget)
        self.info_label.setGeometry(QtCore.QRect(20, 550, 1031, 231))
        self.info_label.setObjectName(_fromUtf8("info_label"))
        self.Feature_Detection_btn = QtGui.QPushButton(self.centralwidget)
        self.Feature_Detection_btn.setGeometry(QtCore.QRect(900, 280, 131, 41))
        self.Feature_Detection_btn.setObjectName(_fromUtf8("Feature_Detection_btn"))
        objectName.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(objectName)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1084, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        objectName.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(objectName)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        objectName.setStatusBar(self.statusbar)

        self.retranslateUi(objectName)
        QtCore.QMetaObject.connectSlotsByName(objectName)

    def retranslateUi(self, objectName):
        objectName.setWindowTitle(_translate("objectName", "Close Loop Object Tracking", None))
        self.face_recognition_btn.setText(_translate("objectName", "Face Recognition", None))
        self.motion_detection_btn.setText(_translate("objectName", "Motion Detection", None))
        self.object_tracking_btn.setText(_translate("objectName", "Object Tracking", None))
        self.info_label.setText(_translate("objectName", "Task Information", None))
        self.Feature_Detection_btn.setText(_translate("objectName", "Feature Detection", None))


from pyqt_gui.icons import icons_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    objectName = QtGui.QMainWindow()
    ui = Ui_objectName()
    ui.setupUi(objectName)
    objectName.show()
    sys.exit(app.exec_())
