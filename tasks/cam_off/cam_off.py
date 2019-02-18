# Created by viv at 10.11.18
import os
import cv2
import sys
import logging

sys.path.append("../")

from lib.display import display_gui  # , colors
from lib.display import display
import config

TASK_TITLE = "Panda"
TASK_TITLE_POS = (config.VID_FRAME_CENTER - (len(TASK_TITLE) * 4), 100)
TASK_INFO = ""

log = logging.getLogger("__main__." + __name__)


# ------------------------------------------------------------------------------
# """ cam_off_loop """
# ------------------------------------------------------------------------------
def cam_off_loop(screen, disply_obj):
    """
    Function will display only a image when then camera is off.
    """
    log.info("cam_off_loop start")
    img_path = "1.jpg"

    if not os.path.isfile(img_path):
        log.error("[ERROR] image does not exist {}".format(img_path))
        # print("[ERROR] image does not exist {}".format(img_path))


    img = cv2.imread(img_path, 1)
    size = (config.HORIZ_PIXELS_SMALL, config.VERT_LINES_SMALL)
    resize_frame = cv2.resize(img, size)
    frame = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2RGB)

    image_title = display_gui.Menu.Text(text=TASK_TITLE, font=display_gui.Font.Medium)

    display.display_render(screen, frame, disply_obj)

    image_title.Render(to=screen, pos=TASK_TITLE_POS)
