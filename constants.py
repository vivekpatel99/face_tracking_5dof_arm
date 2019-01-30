# Created by viv at 15.12.18
from lib import miscellaneous as misc
import math


# -----------------------------------------------
""" paths of all GPIOs """
# from zybo_zybo_rm-pdf (page 25)


JF1_MIO13_919 = "/sys/class/gpio/gpio919" # working
JF2_MIO10_916 = "/sys/class/gpio/gpio916"
JF3_MIO11_917 = "/sys/class/gpio/gpio917"
JF4_MIO12_918 = "/sys/class/gpio/gpio918" # working

JF7_MIO0_906 = "/sys/class/gpio/gpio906" # working
JF8_MIO09_915 = "/sys/class/gpio/gpio915" # working
JF9_MIO14_920 = "/sys/class/gpio/gpio920" # working
JF10_MIO15_921 = "/sys/class/gpio/gpio921" # working

LD04_MIO07_913 = "/sys/class/gpio/gpio913" # LED

# -----------------------------------------------
""" DH parameters for robotic arm """


THETA_1 = 0.
THETA_2 = 0.
THETA_3 = 0.
THETA_4 = 0.
THETA_5 = 0.

L_1 = 33.  # mm 3.3cm
L_2 = 105.  # mm 10.5cm
L_3 = 98.  # mm 9.8cm
L_4 = 27.  # mm 2.7cm
L_5 = 65.  # mm 6.5cm


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




