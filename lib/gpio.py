# Created by viv at 14.12.18
import os
import sys
import time

sys.path.append(os.path.dirname(__file__))

import miscellaneous as misc


# -----------------------------------------------
""" constants """
DIRECTION = "direction" # create path to direction dir for set gpio direction
WRITE = "w" # use to set gpio out

# ------------------------------------------------------------------------------
# """ CLASS: for GPIO set up """
# ------------------------------------------------------------------------------
class GPIO:
    def __init__(self, gpio_path):

        self.export_path = "/sys/class/gpio/export"
        self.unexport_path = "/sys/class/gpio/unexport"

        self.gpio_path = gpio_path
        self.pin_num = gpio_path[-3:]  # taking name pin number from the path

        # if not os.path.exists(gpio_path):
        #     print("[ERROR] gpio path does not exit {}".format(gpio_path))
        #     sys.exit(-1)

        # need to unexport otherwise it will through error "resources are busy"
        if os.path.exists(self.unexport_path):
            misc.write_into_file(self.unexport_path, WRITE, self.pin_num)
            print("[INFO] unexport successful {}".format(self.pin_num))
        else:
            print("[ERROR] path does not exist {}".format(self.unexport_path))

    # ------------------------------------------------------------------------------
    # """ FUNCTION: to export gpio"""
    # ------------------------------------------------------------------------------
    def export(self):

        if os.path.exists(self.export_path):
            misc.write_into_file(self.export_path, WRITE, self.pin_num)
            print("[INFO] export successful {}".format(self.pin_num))
        else:
            print("[ERROR] path does not exist {}".format(self.export_path))

    # ------------------------------------------------------------------------------
    # """ FUNCTION: to set direction of gpio input or output"""
    # ------------------------------------------------------------------------------
    def set_direction(self, direction="out"):

        dir_path = os.path.join(self.gpio_path, DIRECTION)

        misc.write_into_file(dir_path, WRITE, direction)
        print("[INFO] direction set {} {}".format(direction, self.pin_num))

    # ------------------------------------------------------------------------------
    # """ FUNCTION: to set gpio 1 or 0"""
    # ------------------------------------------------------------------------------
    def set_gpio_value(self, value):

        dir_path = os.path.join(self.gpio_path, "value")
        misc.write_into_file(dir_path, WRITE, value)

# ----------------------------------------------------------------------------------------------------------------------
# """ FUNCTION: main """
# ----------------------------------------------------------------------------------------------------------------------
def main():

    gpio_913 = "/sys/class/gpio/gpio913"
    export = open(gpio_913 + '/export', "w")
    export.write("913")
    export.close()
    dir = open(gpio_913 + '/direction', 'w')
    dir.write("out")
    dir.close()

    val = open(gpio_913 + '/value', 'w')
    val.write(1)
    time.sleep(10)
    val.close()

    # gpio_913 = GPIO(gpio_913, "913")
    # gpio_913.set_direction("out")
    # gpio_913.set_gpio_value("1")
    # time.sleep(10)

if __name__ == "__main__":
    main()