# Created by viv at 15.12.18
"""

"""
import time

# -----------------------------------------------
from lib.vision import simple_face_detection


# ------------------------------------------------------------------------------
# """ FUNCTION: MAIN """
# ------------------------------------------------------------------------------
def main():
    """

    """

    simple_face_detection.face_detect_coords_udpsend()


if __name__ == '__main__':
    tstart = time.time()

    main()

    print("Total time {}".format(time.time() - tstart))
