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

fil_dir = os.path.dirname(__file__)
sys.path.append(fil_dir)
import gpio

# -----------------------------------------------
""" constants """
STATE_WRITE = "1"
STATE_READ = "0"

# -----------------------------------------------
servo_min = 150  # min pulse range
servo_max = 600  # max pulse range


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
    def angle_to_dcycle(self, angle, unit = 'rad'):
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
            print("[ERROR] Please enter proper unit 'deg' or 'rad' ")
            sys.exit(-1)

        if unit == 'rad':
            angle = math.degrees(angle)

        print(self.servo_cal_info)
        # slop = (self.servo_cal_info.end_pnt[1] - self.servo_cal_info.start_pnt[1]) / (
        #             self.servo_cal_info.end_pnt[0] - self.servo_cal_info.start_pnt[0])
        slop = (self.servo_cal_info.max_range[1] - self.servo_cal_info.min_range[1]) / (
                self.max_angle - self.min_angle)
        # duty_cycle = (slop * (angle - self.servo_cal_info.start_pnt[0])) + self.servo_cal_info.start_pnt[1]
        duty_cycle = (slop * (angle - self.servo_cal_info.min_range[0])) + self.servo_cal_info.min_range[1]
        print(duty_cycle)
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
        if unit != 'deg' and unit != 'rad':
            print("[ERROR] Please enter proper unit 'deg' or 'rad' ")
            sys.exit(-1)

        if unit == 'rad':
            angle = math.degrees(angle)

        if angle >= self.servo_cal_info.max_range[0]:
            angle = self.servo_cal_info.max_range[0]

        if angle <= self.servo_cal_info.min_range[0]:
            angle = self.servo_cal_info.min_range[0]

        total_time = float(1 / self.freq_hz)
        ton = float(total_time * (self.angle_to_dcycle(angle, unit='deg') / 100))
        toff = total_time - ton

        # PWM.set_duty_cycle(1)
        self.gpio_path.set_gpio_value(1)
        time.sleep(ton)

        # PWM.set_duty_cycle(0)
        self.gpio_path.set_gpio_value(0)
        time.sleep(toff)

        # return ton, toff
