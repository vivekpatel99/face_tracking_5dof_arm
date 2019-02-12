# Created by viv at 26.10.18
import logging

log = logging.getLogger("main." + __name__)

# -----------------------------------------------
PROJECT_TITLE = """Closed Loop Object Tracking based on Image Recognition"""

# -----------------------------------------------
# button index of gui, to find which button press
# TASK_INDEX = 0 --> waiting to start
# TASK_INDEX = 1 --> face recognition
# TASK_INDEX = 2 --> motion detection
# TASK_INDEX = 3 --> Object recognition
TASK_INDEX = 1

# video frame position on display
VID_FRAME_POS = (50, 100)  # x, y

# -----------------------------------------------
# flag for video on/off
VID_STOP = False

# change video frame
# VID_FRAME_CHANGE_INDEX = 0 --> original frame
# VID_FRAME_CHANGE_INDEX = 1 --> processed frame
# VID_FRAME_CHANGE_INDEX = 2 --> gray frame

VID_FRAME_INDEX = 0

# start/stop cam
CAM_START = False  # camera  True = ON/ False = OFF

EXIT = False