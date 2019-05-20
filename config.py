# Created by viv at 15.12.18
import logging
import os
import sys

import math
import numpy as np

from lib.servo_calibration import servo_calib_data as servo_calib

# from lib.kinematics import ikine

log = logging.getLogger("main." + __name__)

# -----------------------------------------------
""" Registers """

# Frame buffers addresses
FB0 = 0x1E000000
FB1 = 0x1E280000
FB2 = 0x1E500000
FB3 = 0x1E780000

FB0_size = 10240
FB1_size = 2400

# --related ip cores:  rtc_dma_bridge  sbus_zybo_core ---
# dma rd to sbus_zybo_core
# dma wr from video_core
CORE_BASE = 0x43C00000
CORE_REG = 0x43C10000

# --related ip cores:  video_dma_bridge   video_core   servo_core
# dma rd to video_core (fullscreen 1280x720 fb)
VID_BASE = 0x83C40000
VID_REG = 0x83C44000
SERVO_REG = 0x83C48000

# --related ip cores:  img_dma_bridge
# dma rd to video_core (640x480 fb)
IMG_BASE = 0x83C00000

# -----------------------------------------------
""" Address of JB port"""
# address start from 3 on words
JB0 = 3
JB1 = 4
JB2 = 5
JB3 = 6
JB4 = 7
JB5 = 8
JB6 = 9
# -----------------------------------------------
""" add or remove GPIO name and servo calibration information """
UTILIZED_GPIO = [[JB0, servo_calib.servo_1],
                 [JB1, servo_calib.servo_2],
                 [JB2, servo_calib.servo_3],
                 [JB4, servo_calib.servo_4],
                 [JB5, servo_calib.servo_5]
                 ]
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

# Denavit Hartenberg  Parameter table
DH_PT = [
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

# PT_2dof = [
#     [math.radians(THETA_1), math.radians(90.0), 0, L_1],
#     [math.radians(THETA_2), 0, L_2, 0],
# ]


# checks
if len(UTILIZED_GPIO) != len(DH_PT):
    log.error('[ERROR] number of UTILIZED_GPIO must be equal to number of row of DH_PT')
    sys.exit(1)

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
""" end-effector orientation """
end_eff_direction_mat = np.matrix([[-1, 0, 0],
                                   [0, -1, 0],
                                   [0, 0, 1]],
                                  dtype=float
                                  )


# checks
def is_correct_rotation_mat(matrix):
    """
    Check if the matrix is valid rotation matrix
    :param matrix:
    :return: valid rotation matrix
    """
    mat = np.matrix(matrix)

    #  check whether matrix is 3x3 or not
    if mat.shape != (3, 3):
        log.error("Matrix must be 3x3")

    # checking if the matrix is a rotation matrix or not
    #  step #1 Square of each element of row
    #  step #2 adding the the output of all the squares
    #  step #3 calculating square root of total
    #  step #4 it must be 1 then and then matrix said to be valid rotation matrix
    for row in range(np.shape(mat)[1]):
        vector_len = 0

        for column in range(np.shape(mat)[0]):
            vector_len += mat[column, row] ** 2

        if not np.sqrt(vector_len) == 1:
            log.error("Matrix is not a valid rotation matrix")
            sys.exit(1)
    return mat


end_eff_direction_mat = is_correct_rotation_mat(end_eff_direction_mat)

# -----------------------------------------------
""" UDP """
IP = r"192.168.1.104"
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

# --------------------            ---------------------------
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

# -----------------------------------------------
""" TASKS configuration """
# object recognition
#     CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
#                "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
#                "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
#                "sofa", "train", "tvmonitor"]
recog_object_name = "bottle"
