# Created by viv at 15.12.18
"""

"""
import math
import time
import sys
import numpy as np

# -----------------------------------------------
import constants as const
from lib import pwm
from lib.servo_calibration import servo_calib_data as servo_calib
from lib.servo_calibration.servo_calibration import servo_test
from lib import miscellaneous as misc
from lib.kinematics import ikine as ik
from lib.udp import udp


# ------------------------------------------------------------------------------
# """ FUNCTION: MAIN """
# ------------------------------------------------------------------------------
def main():
    """

    """
    # test all the servos before starting the other progress
    servo_test()
    end_eff_direction_mat = np.matrix([
        [-1., 0., 0.],
        [0., -1., 0.],
        [0., 0., 1.]
    ])

    pwm_jf1 = pwm.PWM(gpio_path=const.JF1_MIO13_919, servo_cal_info=servo_calib.servo_1)
    pwm_jf4 = pwm.PWM(gpio_path=const.JF4_MIO12_918, servo_cal_info=servo_calib.servo_2)
    pwm_jf7 = pwm.PWM(gpio_path=const.JF7_MIO0_906, servo_cal_info=servo_calib.servo_3)
    pwm_jf8 = pwm.PWM(gpio_path=const.JF8_MIO09_915, servo_cal_info=servo_calib.servo_4)
    pwm_jf9 = pwm.PWM(gpio_path=const.JF9_MIO14_920, servo_cal_info=servo_calib.servo_5)

    udp_ip = "192.168.1.103"
    udp_port = 47777
    udp_receive = udp.UdpPacket(udp_ip=udp_ip, udp_port=udp_port)

    while True:
        coordinates = udp_receive.udp_packet_receive()
        print(coordinates)
        thetas = ik.ik_5dof(end_eff_direction_mat, coordinates[0], coordinates[1], coordinates[2])

        print("theta_1 {}".format(math.degrees(thetas.theta_1)))
        print("theta_2 {}".format(math.degrees(thetas.theta_2)))
        print("theta_3 {}".format(math.degrees(thetas.theta_3)))
        print("theta_4 {}".format(math.degrees(thetas.theta_4)))
        print("theta_5 {}".format(math.degrees(thetas.theta_5)))

        pwm_jf1.pwm_generate(abs(thetas.theta_1))
        time.sleep(0.5)

        pwm_jf4.pwm_generate(abs(thetas.theta_2))
        time.sleep(0.5)

        pwm_jf7.pwm_generate(thetas.theta_3)
        time.sleep(0.5)

        pwm_jf8.pwm_generate(thetas.theta_4)
        time.sleep(0.5)

        pwm_jf9.pwm_generate(thetas.theta_5)
        time.sleep(0.5)


if __name__ == '__main__':
    tstart = time.time()

    main()

    print("Total time {}".format(time.time() - tstart))
