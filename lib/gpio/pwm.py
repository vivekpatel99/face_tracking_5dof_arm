# Created by viv at 14.12.18

"""
servo control
 for 50Hz signal
  - 5% of duty cycle corresponds to 1ms pulse width (0 angle)
  - 10% of duty cycle corresponds to 2ms pulse width (180 angle)


  - Orange - pulse
  - Red - +V
  - Brown - gnd


  period T = 1 / frequency
  duty cycle D = (pulse width/T)*100
  pulse width = (duty cycle/100)*T

"""
import math
import sys
import os
import time
import logging

fil_dir = os.path.dirname(__file__)
sys.path.append(fil_dir)

import config
from lib.gpio import gpio
from lib.gpio.regBlock import RegBlock

log = logging.getLogger("__main__." + __name__)

# -----------------------------------------------
""" constants """
STATE_WRITE = "1"
STATE_READ = "0"


# ------------------------------------------------------------------------------
# """ CLASS: for PWM set up """
# ------------------------------------------------------------------------------
class PulseWidthModulation:
    def __init__(self, servo_port_addr, servo_cal_info, servo_reg=config.SERVO_REG, reg_size=0x100):
        self.servo_port_addr = servo_port_addr
        self.servo_cal_info = servo_cal_info
        self.servo_reg = servo_reg
        self.reg_size = reg_size
        self.servo = RegBlock(servo_reg, reg_size)
        self.max_angle = 180
        self.min_angle = 0

    def angle_to_dcycle(self, angle, unit='rad'):
        """
        calculation
        (0,0)
        (180,10)
        - fit the line of these two points, to get duty cycle for an angle
        - the slop of two point is
         slop (m) = (y2-y1)/(x2-x1)
         y-y1 = m(x-x1)
         where y = duty cycle
               x = angle
        """
        if unit != 'deg' and unit != 'rad':
            log.error("Please enter proper unit 'deg' or 'rad' ")
            sys.exit(-1)

        if unit == 'rad':
            angle = math.degrees(angle)

        slop = (self.servo_cal_info.max_range[1] - self.servo_cal_info.min_range[1]) / (
            self.max_angle - self.min_angle)

        duty_cycle = (slop * (angle - self.servo_cal_info.min_range[0])) + self.servo_cal_info.min_range[1]
        # print(duty_cycle)
        return int(duty_cycle)

    def generate_pwm(self, angle=90, unit='rad'):
        angle = float(angle)
        if unit != 'deg' and unit != 'rad':
            log.error("Please enter proper unit 'deg' or 'rad' ")
            sys.exit(1)

        if unit == 'rad':
            angle = math.degrees(angle)

        if angle >= self.servo_cal_info.max_range[0]:
            angle = self.servo_cal_info.max_range[0]

        if angle <= self.servo_cal_info.min_range[0]:
            angle = self.servo_cal_info.min_range[0]

        # self.angle_to_dcycle(angle, unit='deg')
        self.servo.set_u32(self.servo_port_addr, self.angle_to_dcycle(angle, unit='deg'))


# ------------------------------------------------------------------------------
# """ CLASS: for PWM set up """
# ------------------------------------------------------------------------------

class PWM:
    def __init__(self, gpio_path, servo_cal_info=None, freq_hz=50):
        self.gpio_path = gpio_path
        self.pin_num = gpio_path[-3:]  # taking  pin number from the path
        self.freq_hz = float(freq_hz)
        self.servo_cal_info = servo_cal_info
        self.max_angle = 180
        self.min_angle = 0

        # initialize gpio pin
        self.gpio_path = gpio.GPIO(self.gpio_path)
        self.gpio_path.export()
        self.gpio_path.set_direction()

    # ------------------------------------------------------------------------------
    # """ FUNCTION: to generate pwm pulse """
    # ------------------------------------------------------------------------------
    def set_duty_cycle(self, on_off):
        self.gpio_path.set_gpio_value(on_off)

    # ------------------------------------------------------------------------------
    # """ FUNCTION: angle to duty cycle conversion """
    # ------------------------------------------------------------------------------
    def angle_to_dcycle(self, angle, unit='rad'):
        """
        calculation
        (0,0)
        (180,10)
        - fit the line of these two points, to get duty cycle for an angle
        - the slop of two point is
         slop (m) = (y2-y1)/(x2-x1)
         y-y1 = m(x-x1)
         where y = duty cycle
               x = angle
        """
        if unit != 'deg' and unit != 'rad':
            log.error("Please enter proper unit 'deg' or 'rad' ")
            sys.exit(-1)

        if unit == 'rad':
            angle = math.degrees(angle)

        slop = (self.servo_cal_info.max_range[1] - self.servo_cal_info.min_range[1]) / (
            self.max_angle - self.min_angle)
        # duty_cycle = (slop * (angle - self.servo_cal_info.start_pnt[0])) + self.servo_cal_info.start_pnt[1]
        duty_cycle = (slop * (angle - self.servo_cal_info.min_range[0])) + self.servo_cal_info.min_range[1]

        return duty_cycle

    # ------------------------------------------------------------------------------
    # """ FUNCTION: to calculate pulse from given frequency """
    # ------------------------------------------------------------------------------
    def pwm_generate(self, angle, unit='rad'):
        """
        ton = total time (ts) * duty cycle
        toff = ts - ton
        :return:
        """
        angle = float(angle)
        if unit != 'deg' and unit != 'rad':
            log.error("Please enter proper unit 'deg' or 'rad' ")
            sys.exit(1)

        if unit == 'rad':
            angle = math.degrees(angle)
            # print("[INFO] unit of angle is taken into Radians")
        # else:
        #     print("[INFO] unit of angle is taken into Degree")
        if angle >= self.servo_cal_info.max_range[0]:
            angle = self.servo_cal_info.max_range[0]

        if angle <= self.servo_cal_info.min_range[0]:
            angle = self.servo_cal_info.min_range[0]

        total_time = float(1 / self.freq_hz)
        ton = float(total_time * (self.angle_to_dcycle(angle, unit='deg') / 100))
        toff = total_time - ton

        self.gpio_path.set_gpio_value(1)
        time.sleep(ton)

        self.gpio_path.set_gpio_value(0)
        time.sleep(toff)
