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

from lib.udp import udp_receive

# ------------------------------------------------------------------------------
# """ FUNCTION: MAIN """
# ------------------------------------------------------------------------------
def main():
    """

    """
    end_eff_direction_mat = np.matrix([
        [-1., 0., 0.],
        [0., -1., 0.],
        [0., 0., 1.]
    ])

    while True:
        x = float(input("x: "))
        y = float(input("y: "))
        z = float(input("z: "))

        thetas = ik.ik_5dof(end_eff_direction_mat, x, y, z)

        print("theta_1 {}".format(math.degrees(thetas.theta_1)))
        print("theta_2 {}".format(math.degrees(thetas.theta_2)))
        print("theta_3 {}".format(math.degrees(thetas.theta_3)))
        print("theta_4 {}".format(math.degrees(thetas.theta_4)))
        print("theta_5 {}".format(math.degrees(thetas.theta_5)))

        l = pickle.dumps([math.degrees(thetas.theta_1),
                          math.degrees(thetas.theta_2),
                          math.degrees(thetas.theta_3),
                          math.degrees(thetas.theta_4),
                          math.degrees(thetas.theta_5)])
        udp_send.udp_send(l)
        # pwm_jf1.pwm_generate(thetas.theta_1)
        # time.sleep(0.5)
        #
        # pwm_jf4.pwm_generate(thetas.theta_2)
        # time.sleep(0.5)
        #
        # pwm_jf7.pwm_generate(thetas.theta_3)
        # time.sleep(0.5)
        #
        # pwm_jf8.pwm_generate(thetas.theta_4)
        # time.sleep(0.5)
        #
        # pwm_jf9.pwm_generate(thetas.theta_5)
        # time.sleep(0.5)


if __name__ == '__main__':
    tstart = time.time()
    from lib.udp import udp

    # print(udp_receive.udp_receive())
    # robo_main()
    from lib.vision import simple_face_detection
    simple_face_detection.coordinate_udpsend()
    print("Total time {}".format(time.time() - tstart))
