# Created by viv at 15.12.18
"""

"""
import math
import time
import sys
import numpy as np
import pickle

# -----------------------------------------------
from lib import pwm
import constants as const
from lib.servo_calibration import servo_calib_data as servo_calib
from lib import miscellaneous as misc
from lib.kinematics import ikine as ik
from lib.udp import udp_send
from lib.vision import simple_face_detection


# ------------------------------------------------------------------------------
# """ FUNCTION: MAIN """
# ------------------------------------------------------------------------------
def main():
    """

    """

    simple_face_detection.coordinate_udpsend()


if __name__ == '__main__':
    tstart = time.time()

    main()

    print("Total time {}".format(time.time() - tstart))
