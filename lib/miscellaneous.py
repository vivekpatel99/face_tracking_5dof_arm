# Created by viv at 16.12.18
import os
import numpy as np
import logging

log = logging.getLogger("__main__." + __name__)
# ------------------------------------------------------------------------------
# """ FUNCTION: to convert degree to radian """
# ------------------------------------------------------------------------------
def deg_to_rad(deg):
    return float(deg) * (np.pi / 180)
    # return (deg/180)*np.pi


# ------------------------------------------------------------------------------
# """ FUNCTION: to convert radian to degree """
# ------------------------------------------------------------------------------
def rad_to_deg(rad):
    return float(rad) * (180 / np.pi)


# ------------------------------------------------------------------------------
# """ FUNCTION: to open file and write something """
# ------------------------------------------------------------------------------
def write_into_file(path, mode, value):
    if not os.path.exists(path):
        log.error("Path does not exist {}".format(path))
    try:
        with open(path, mode) as fil:
            fil.write(str(value))
            # return True
    except Exception as error:
        log.error(error, path)
        # raise


