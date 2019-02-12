# Created by viv at 23.12.18

import sys
import time

sys.path.append("../")
from lib import pwm
from lib.servo_calibration import servo_calib_data as servo_calib
import config as const


# ------------------------------------------------------------------------------
# """ FUNCTION: servo calibration """
# ------------------------------------------------------------------------------
def servo_test():
    pwm_jf1 = pwm.PWM(gpio_path=const.JF1_MIO13_919, servo_cal_info=servo_calib.servo_1)
    pwm_jf4 = pwm.PWM(gpio_path=const.JF4_MIO12_918, servo_cal_info=servo_calib.servo_2)
    pwm_jf7 = pwm.PWM(gpio_path=const.JF7_MIO0_906, servo_cal_info=servo_calib.servo_3)
    pwm_jf8 = pwm.PWM(gpio_path=const.JF8_MIO09_915, servo_cal_info=servo_calib.servo_4)
    pwm_jf9 = pwm.PWM(gpio_path=const.JF9_MIO14_920, servo_cal_info=servo_calib.servo_5)

    pin_list = [pwm_jf1, pwm_jf4,pwm_jf7,pwm_jf8,pwm_jf9]

    for pin in pin_list:
        for angle in range(0, 200, 20):
            # print(angle)
            pin.pwm_generate(angle, unit="deg")
            time.sleep(0.1)

        pin.pwm_generate(0, unit="deg")


# ------------------------------------------------------------------------------
# """ FUNCTION: servo calibration """
# ------------------------------------------------------------------------------
def servo_calibration():
    """
    906
    :return:
    """
    pwm_jf1 = pwm.PWM(const.JF1_MIO13_919, "919")
    pwm_jf4 = pwm.PWM(const.JF4_MIO12_918, "918")

    pwm_jf7 = pwm.PWM(const.JF7_MIO0_906, "906")
    pwm_jf8 = pwm.PWM(const.JF8_MIO09_915, "915")
    pwm_jf9 = pwm.PWM(const.JF9_MIO14_920, "920")

    # duty = input("duty: ")
    # duty = 5

    while (True):
        # angle = int(input("angle: "))
        angle = float(input("PWM pulse duty cycle  0-10: "))

        pwm_jf7.pwm_generate(angle)
        # time.sleep(0.5)

        # pwm_jf8.pwm_generate(angle)
        # time.sleep(0.5)

        # pwm_jf9.pwm_generate(angle)


if __name__ == "__main__":
    servo_calibration()
