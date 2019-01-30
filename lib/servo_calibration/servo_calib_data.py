# Created by viv at 22.12.18

from collections import namedtuple
import sys

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

servo_1 = Servo((0, 0.),
                (180., 9.5))  # 9.5

servo_2 = Servo((0., 1.),  # 0.0.
                (80., 9.5))  # 5 (5dof safety limit)  # 9.2 (3dof safety limit) # 9.5 (limit)

servo_3 = Servo((0., 0.),
                (80., 9.4))  # 6 (5dof safety limit ) # 7. (3dof safety limit)  # 9.4 (limit)

servo_4 = Servo((0., 0.),
                (100., 10.))  # 6 (5dof safety limit ) # 9. (3dof safety limit)  # 10  (limit)

servo_5 = Servo((0., 0.),
                (180., 10.))  # 10

# testing entered servo calibration data
servos_tuple = (servo_1, servo_2, servo_3, servo_4, servo_5)

for servo in servos_tuple:
    if not isinstance(servo.min_range[0], int) and not isinstance(servo.min_range[0], float) \
            or not isinstance(servo.min_range[1], int) and not isinstance(servo.min_range[1], float) \
            or not isinstance(servo.max_range[0], int) and not isinstance(servo.max_range[0], float) \
            or not isinstance(servo.max_range[1], int) and not isinstance(servo.max_range[1], float):

        print("[ERROR] servo limits must be in digits {}".format(servo))
        sys.exit(1)

    elif not servo.min_range[0] <= 180. or not servo.max_range[0] <= 180.:  # min and max angle must be less than 180
        print("[ERROR] please set proper servo limits {}".format(servo))
        sys.exit(1)

    elif type(servo.min_range[1]) != float or type(servo.max_range[1]) != float:
        print("[WARNING] servo calibration values should be in float {}".format(servo))

    elif not servo.min_range[1] < 15. or not servo.max_range[1] < 15.: # min and max % duty cycles are less then 15
        print("[ERROR] servo limits must be less than 15% duty cycle {}".format(servo))
        sys.exit(1)

    elif not servo.min_range[1] < servo.max_range[1]:  # min angle must be less than max angle
        print("[ERROR] servo minimum limit must be less than maximum limit {}".format(servo))
        sys.exit(1)
    else:
        pass
