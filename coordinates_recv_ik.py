# Created by viv at 15.12.18
"""

"""
import math
import time

# -----------------------------------------------
import config
from lib.gpio import pwm
from lib.gpio.regBlock import RegBlock
from lib.servo_calibration import servo_calib_data as servo_calib
from lib.servo_calibration.servo_calibration import servo_test
from lib.kinematics import ikine as ik
from lib.udp import udp
import pickle

# ------------------------------------------------------------------------------
# """ FUNCTION: MAIN """
# ------------------------------------------------------------------------------


def main():
    """

    """
    # # test all the servos before starting the other progress
    # servo_test()

    pwm_jb0 = pwm.PulseWidthModulation(servo_port_addr=config.JB0, servo_cal_info=servo_calib.servo_1)
    pwm_jb1 = pwm.PulseWidthModulation(servo_port_addr=config.JB1, servo_cal_info=servo_calib.servo_2)
    pwm_jb2 = pwm.PulseWidthModulation(servo_port_addr=config.JB2, servo_cal_info=servo_calib.servo_3)
    pwm_jb3 = pwm.PulseWidthModulation(servo_port_addr=config.JB3, servo_cal_info=servo_calib.servo_4)
    pwm_jb4 = pwm.PulseWidthModulation(servo_port_addr=config.JB4, servo_cal_info=servo_calib.servo_5)

    udp_receive = udp.UdpPacket(udp_ip=config.IP, udp_port=config.PORT)
    with udp_receive as udp_recv:
        while True:

            coordinates = pickle.loads(udp_recv.recvfrom(1024)[0])

            thetas = ik.ik_5dof(config.end_eff_direction_mat, coordinates[0], coordinates[1], coordinates[2])

            print("theta_1 {}".format(math.degrees(thetas.theta_1)))
            print("theta_2 {}".format(math.degrees(thetas.theta_2)))
            print("theta_3 {}".format(math.degrees(thetas.theta_3)))
            print("theta_4 {}".format(math.degrees(thetas.theta_4)))
            print("theta_5 {}".format(math.degrees(thetas.theta_5)))

            pwm_jb0.generate_pwm(abs(thetas.theta_1))
            time.sleep(0.1)
            pwm_jb1.generate_pwm(abs(thetas.theta_2))
            time.sleep(0.1)
            pwm_jb2.generate_pwm(thetas.theta_3)
            time.sleep(0.1)
            pwm_jb3.generate_pwm(thetas.theta_4)
            time.sleep(0.1)
            pwm_jb4.generate_pwm(thetas.theta_5)


# ------------------------------------------------------------------------------
# """ FUNCTION: MAIN """
# ------------------------------------------------------------------------------
def _main():
    """

    """
    # test all the servos before starting the other progress
    servo_test()

    pwm_jf1 = pwm.PWM(gpio_path=config.JF1_MIO13_919, servo_cal_info=servo_calib.servo_1)
    pwm_jf4 = pwm.PWM(gpio_path=config.JF4_MIO12_918, servo_cal_info=servo_calib.servo_2)
    pwm_jf7 = pwm.PWM(gpio_path=config.JF7_MIO0_906, servo_cal_info=servo_calib.servo_3)
    pwm_jf8 = pwm.PWM(gpio_path=config.JF8_MIO09_915, servo_cal_info=servo_calib.servo_4)
    pwm_jf9 = pwm.PWM(gpio_path=config.JF9_MIO14_920, servo_cal_info=servo_calib.servo_5)

    udp_receive = udp.UdpPacket(udp_ip=config.IP, udp_port=config.PORT)

    while True:
        coordinates = udp_receive.udp_packet_receive()
        print(coordinates)
        thetas = ik.ik_5dof(config.end_eff_direction_mat, coordinates[0], coordinates[1], coordinates[2])

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

    udp_receive.close()


if __name__ == '__main__':
    tstart = time.time()

    main()
    # SERVO_REG = 0x83C48000
    # servo = RegBlock(SERVO_REG, 0x100)
    # # servo.set_u32(3, 0)
    # print(servo.get_u32(4))

    print("Total time {}".format(time.time() - tstart))
