# Created by viv at 22.12.18

from collections import namedtuple
import sys
import logging

log = logging.getLogger("__main__." + __name__)

# ( min_angle, servo_start_dutycycle)    (max_angle, servo_end_dutycycle, )
# Servo = namedtuple("Servo", ['angle_0', 'angle_180'])
Servo = namedtuple("Servo", ['min_range', 'max_range'])
"""
calculation
(0,0)
(180,10)
- fit the line of these two points, to get duty cycle for an angle
- the slop of two point is
 m = (y2-y1)/(x2-x1)
 y-y1 = m(x-x1)
 where y = duty cycle
       x = angle
"""
# EXAMPLE
# servo_ = Servo((min safety angle limit, min duty cycle),
#                 (max safety angle limit, max duty cycle))

# servo_1 = Servo((0, 0.),
#                 (180., 9.5))  # 9.5

# servo_2 = Servo((0., 1.),  # 0.0.
#                 (100., 9.5))  # 5 (5dof safety limit)  # 9.2 (3dof safety limit) # 9.5 (limit)

# servo_3 = Servo((0., 0.),
#                 (90., 9.4))  # 6 (5dof safety limit ) # 7. (3dof safety limit)  # 9.4 (limit)

# servo_4 = Servo((0., 1.),
#                 (180., 10.))  # 6 (5dof safety limit ) # 9. (3dof safety limit)  # 10  (limit)

# servo_5 = Servo((0., 0.),
#                 (180., 10.))  # 10
servo_pulse_min = -1000
servo_pulse_max = 1000
servo_1 = Servo((0, servo_pulse_min),
                (180., servo_pulse_max))  # 9.5

servo_2 = Servo((0, servo_pulse_min),  # 0.0.
                (100, servo_pulse_max))  # 5 (5dof safety limit)  # 9.2 (3dof safety limit) # 9.5 (limit)

servo_3 = Servo((0, servo_pulse_min),
                (80, servo_pulse_max))  # 6 (5dof safety limit ) # 7. (3dof safety limit)  # 9.4 (limit)

servo_4 = Servo((0, servo_pulse_min),
                (180, servo_pulse_max))  # 6 (5dof safety limit ) # 9. (3dof safety limit)  # 10  (limit)

servo_5 = Servo((0, servo_pulse_min),
                (180, servo_pulse_max))  # 10

# testing entered servo calibration data
servos_tuple = (servo_1, servo_2, servo_3, servo_4, servo_5)

for servo in servos_tuple:
    if not isinstance(servo.min_range[0], int) and not isinstance(servo.min_range[0], float) \
            or not isinstance(servo.min_range[1], int) and not isinstance(servo.min_range[1], float) \
            or not isinstance(servo.max_range[0], int) and not isinstance(servo.max_range[0], float) \
            or not isinstance(servo.max_range[1], int) and not isinstance(servo.max_range[1], float):

        log.error("Servo limits must be in digits {}".format(servo))
        sys.exit(1)

    elif not servo.min_range[0] <= 180. or not servo.max_range[0] <= 180.:  # min and max angle must be less than 180
        log.error("Please set proper servo limits {}".format(servo))
        sys.exit(1)

    # elif type(servo.min_range[1]) != float or type(servo.max_range[1]) != float:
    #     log.error("Servo calibration values should be in float {}".format(servo))

    elif not servo.min_range[1] >= -1000. or not servo.max_range[
            1] <= 1000:  # min and max % duty cycles are less then 15
        log.error("Servo limits must be less than 15% duty cycle {}".format(servo))
        sys.exit(1)

    elif not servo.min_range[1] < servo.max_range[1]:  # min angle must be less than max angle
        log.error("Servo minimum limit must be less than maximum limit {}".format(servo))
        sys.exit(1)
    else:
        pass
