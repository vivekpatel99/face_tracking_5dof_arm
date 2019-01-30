# Created by viv at 15.12.18
"""

"""
import math
import time
import sys
import numpy as np

# -----------------------------------------------
from lib import pwm
import constants as const
from lib.servo_calibration import servo_calib_data as servo_calib
from lib import miscellaneous as misc
from lib.kinematics import ikine as ik


# ------------------------------------------------------------------------------
# """ FUNCTION: To control Servos with IK algorithm """
# ------------------------------------------------------------------------------
def robo_main():
    """
    906
    :return:
    """
    pwm_jf1 = pwm.PWM(gpio_path=const.JF1_MIO13_919, servo_cal_info=servo_calib.servo_1)
    pwm_jf4 = pwm.PWM(gpio_path=const.JF4_MIO12_918, servo_cal_info=servo_calib.servo_2)
    pwm_jf7 = pwm.PWM(gpio_path=const.JF7_MIO0_906, servo_cal_info=servo_calib.servo_3)
    pwm_jf8 = pwm.PWM(gpio_path=const.JF8_MIO09_915, servo_cal_info=servo_calib.servo_4)
    pwm_jf9 = pwm.PWM(gpio_path=const.JF9_MIO14_920, servo_cal_info=servo_calib.servo_5)

    while True:
        theta1 = float(input("theta1: "))
        theta2 = float(input("theta2: "))
        theta3 = float(input("theta3: "))
        theta4 = float(input("theta4: "))
        theta5 = float(input("theta5: "))

        pwm_jf1.pwm_generate(theta1)
        time.sleep(0.5)

        pwm_jf4.pwm_generate(theta2)
        time.sleep(0.5)

        pwm_jf7.pwm_generate(theta3)
        time.sleep(0.5)

        pwm_jf8.pwm_generate(theta4)
        time.sleep(0.5)

        pwm_jf9.pwm_generate(theta5)
        time.sleep(0.5)


# ------------------------------------------------------------------------------
# """ FUNCTION: MAIN """
# ------------------------------------------------------------------------------
def main():
    """

    """
    pwm_jf1 = pwm.PWM(gpio_path=const.JF1_MIO13_919, servo_cal_info=servo_calib.servo_1)
    pwm_jf4 = pwm.PWM(gpio_path=const.JF4_MIO12_918, servo_cal_info=servo_calib.servo_2)
    pwm_jf7 = pwm.PWM(gpio_path=const.JF7_MIO0_906, servo_cal_info=servo_calib.servo_3)
    pwm_jf8 = pwm.PWM(gpio_path=const.JF8_MIO09_915, servo_cal_info=servo_calib.servo_4)
    pwm_jf9 = pwm.PWM(gpio_path=const.JF9_MIO14_920, servo_cal_info=servo_calib.servo_5)

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

        pwm_jf1.pwm_generate(thetas.theta_1)
        time.sleep(0.5)

        pwm_jf4.pwm_generate(thetas.theta_2)
        time.sleep(0.5)

        pwm_jf7.pwm_generate(thetas.theta_3)
        time.sleep(0.5)

        pwm_jf8.pwm_generate(thetas.theta_4)
        time.sleep(0.5)

        pwm_jf9.pwm_generate(thetas.theta_5)
        time.sleep(0.5)


if __name__ == '__main__':
    tstart = time.time()

    # robo_main()
    main()

    print("Total time {}".format(time.time() - tstart))
