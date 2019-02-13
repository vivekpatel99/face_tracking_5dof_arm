# Created by viv at 15.12.18

import math
import os
import logging
import numpy as np

log = logging.getLogger("main." + __name__)

# -----------------------------------------------
""" paths of all GPIOs """
# from zybo_zybo_rm-pdf (page 25)

JF1_MIO13_919 = "/sys/class/gpio/gpio919"  # working
JF2_MIO10_916 = "/sys/class/gpio/gpio916"
JF3_MIO11_917 = "/sys/class/gpio/gpio917"
JF4_MIO12_918 = "/sys/class/gpio/gpio918"  # working

JF7_MIO0_906 = "/sys/class/gpio/gpio906"  # working
JF8_MIO09_915 = "/sys/class/gpio/gpio915"  # working
JF9_MIO14_920 = "/sys/class/gpio/gpio920"  # working
JF10_MIO15_921 = "/sys/class/gpio/gpio921"  # working

LD04_MIO07_913 = "/sys/class/gpio/gpio913"  # LED

# -----------------------------------------------
""" DH parameters for robotic arm """

THETA_1 = 0.
THETA_2 = 0.
THETA_3 = 0.
THETA_4 = 0.
THETA_5 = 0.

L_1 = 33  # mm 3.3cm
L_2 = 105  # mm 10.5cm
L_3 = 98  # mm 9.8cm
L_4 = 27  # mm 2.7cm
L_5 = 65  # mm 6.5cm

PT_5dof = [
    [math.radians(THETA_1), math.radians(90.0), 0, L_1],
    [math.radians(THETA_2), 0, L_2, 0],
    [math.radians(THETA_3), 0, L_3, 0],
    [math.radians(THETA_4) + math.radians(90.0), math.radians(90.0), 0, 0],
    [math.radians(THETA_5), 0, 0, L_4 + L_5]
]

PT_3dof = [
    [math.radians(THETA_1), math.radians(90.0), 0, L_1],
    [math.radians(THETA_2), 0, L_2, 0],
    [math.radians(THETA_3), 0, L_3, 0],
]

PT_2dof = [
    [math.radians(THETA_1), math.radians(90.0), 0, L_1],
    [math.radians(THETA_2), 0, L_2, 0],
]

# -----------------------------------------------
""" Video frame setting """
# configure video frame size
HORIZ_PIXELS_SMALL = 640
VERT_LINES_SMALL = 480
VID_FRAME_SIZE = (HORIZ_PIXELS_SMALL, VERT_LINES_SMALL)
VID_FRAME_CENTER = (50 + HORIZ_PIXELS_SMALL) / 2

# path to the haar cascade
module_path = os.path.dirname(os.path.abspath(__file__))
cascade_path = os.path.join(module_path, "cascades/haarcascade_frontalface_default.xml")

# -----------------------------------------------
""" Coordinates transform (Kinematics)"""
# the physical area covered by video frame in centimeter
# frame_physical_area = float(140)
frame_physical_area = float(180)

dist_from_cam = float(90)  # object distance from camera

# -----------------------------------------------
""" end-effector orientation """
# transformation from robotic arm frame coordinate to camera coordinate
# assume that camera is on the exactly above the origin of arm
R0_C = np.mat([[1, 0, 0],
               [0, 1, 0],
               [0, 0, 1]
               ],
              dtype=float
              )
d0_C = np.mat([[0.],
               [8.],  # assumed that the camera just at y axis  on arm's origin
               [0.]],
              dtype=float
              )
# creating Homogeneous transformation matrix
_H0_C = np.concatenate((R0_C, d0_C), 1)  # concatenate column
H0_C = np.concatenate((_H0_C, [[0., 0., 0., 1.]]), 0)  # concatenate row

# -----------------------------------------------
""" UDP """
IP = "192.168.1.103"
PORT = 47777

# -----------------------------------------------
""" Pygame GUI configuration"""

PROJECT_TITLE = """Closed Loop Object Tracking based on Image Recognition"""

# button index of gui, to find which button press
# TASK_INDEX = 0 --> waiting to start
# TASK_INDEX = 1 --> face recognition
# TASK_INDEX = 2 --> motion detection
# TASK_INDEX = 3 --> Object recognition
TASK_INDEX = 1

# video frame position on display
VID_FRAME_POS = (50, 100)  # x, y

# -----------------------------------------------
# flag for video on/off
VID_STOP = False

# change video frame
# VID_FRAME_CHANGE_INDEX = 0 --> original frame
# VID_FRAME_CHANGE_INDEX = 1 --> processed frame
# VID_FRAME_CHANGE_INDEX = 2 --> gray frame

VID_FRAME_INDEX = 0

# start/stop cam
CAM_START = False  # camera  True = ON/ False = OFF

# exit from the application
EXIT = False
