"""
https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

# find center of countor
https://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/
"""

import cv2
from imutils.video import VideoStream
import imutils
import time

import logging

# -----------------------------------------------
""" Modules """

import config
from lib.vision.vision import Vision
from lib.display import display
from lib.display import display_gui
from lib.udp import udp

log = logging.getLogger("main." + __name__)

# -----------------------------------------------
""" globals """

TASK_INFO = "TASK INFO: move something "
TASK_TITLE = "TASK: Motion Detection "

TASK_TITLE_POS = (config.VID_FRAME_CENTER - (len(TASK_TITLE) * 4), 100)

# minimum size (in pixel) for a region of image to be considered actual "motion"
MIN_AREA = 500
CAM_NUM = 0


# ------------------------------------------------------------------------------
# """ MotionDetection """
# ------------------------------------------------------------------------------
class MotionDetection:
    def __init__(self):
        self.back_gnd_sub = cv2.createBackgroundSubtractorMOG2()

    # -------------------------------------------------------------------
    # """ run_motion_subtrator """
    # -------------------------------------------------------------------
    def run_motion_subtrator(self, frame, frame_display_indx):
        # color has no bearing on motion detection algorithm
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # if the first stream is not initialized, store it for reference
        # to smooth the image and remove noise(if not then could throw algorithm off)
        # smothing avarage pixel intensities across an 21x21 region
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # apply background subtraction
        fgmask = self.back_gnd_sub.apply(gray)
        im2, contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if len(contours) != 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            try:  # avoid division error
                center_x = int(M["m10"] / M["m00"])
                center_y = int(M["m01"] / M["m00"])
            except ZeroDivisionError:
                pass
            # get bounding box from countour
            (x, y, w, h) = cv2.boundingRect(c)

            # draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            try:
                cv2.circle(frame, (center_x, center_y), 7, (0, 0, 225), -1)
            except UnboundLocalError:
                center_x, center_y = 0, 0

            if frame_display_indx == 0:
                out_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            elif frame_display_indx == 1:
                out_frame = fgmask
            else:
                out_frame = frame
            return (center_x, center_y), out_frame


# ------------------------------------------------------------------------------
# """ motion_detection_pygm """
# ------------------------------------------------------------------------------

def motion_detection_pygm(screen, disply_obj, fbs):
    """ """
    log.info("motion_detection_pygm starts... ")

    image_title = display_gui.Menu.Text(text=TASK_TITLE, font=display_gui.Font.Medium)

    vid = Vision()
    udp_send = udp.UdpPacket(udp_ip=config.IP, udp_port=config.PORT)

    fgbg = cv2.createBackgroundSubtractorMOG2()
    while vid.isCameraConnected():
        _, frame = vid.getVideo()
        # resize frame for required size
        resize_frame = cv2.resize(frame, config.VID_FRAME_SIZE)

        # opencv understand BGR, in order to display we need to convert image  form   BGR to RGB
        frame = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2RGB)  # for display

        # color has no bearing on motion detection algorithm
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # if the first stream is not initialized, store it for reference
        # to smooth the image and remove noise(if not then could throw algorithm off)
        # smoothing average pixel intensities across an 21x21 region
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # apply background subtraction
        fgmask = fgbg.apply(gray)
        # im2, contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        im2, contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if len(contours) != 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            try:  # avoid division error
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            except:
                pass
            # get bounding box from countour
            (x, y, w, h) = cv2.boundingRect(c)
            udp_send.udp_packet_send(x=cX, y=cY, frame=frame)
            # draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (cX, cY), 7, (0, 0, 225), -1)

        if config.VID_FRAME_INDEX == 0:
            frame = fgmask

        elif config.VID_FRAME_INDEX == 1:

            frame = frame

        elif config.VID_FRAME_INDEX == 2:
            frame = frame

        # Display the frame
        display.display_render(screen, frame, disply_obj, TASK_INFO)
        image_title.Render(to=screen, pos=TASK_TITLE_POS)

        # check if TASK_INDEX is not 1 then it means another buttons has pressed
        if not config.TASK_INDEX == 2:
            log.info("TASK_INDEX is not 2 but {}".format(config.TASK_INDEX))
            break

        if not config.CAM_START or config.EXIT:
            break

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    vid.videoCleanUp()
    log.info("closing motion detection")


def _motion_detection_pygm(screen, disply_obj, fbs):
    """ """
    log.info("motion_detection_pygm starts... ")

    image_title = display_gui.Menu.Text(text=TASK_TITLE, font=display_gui.Font.Medium)

    cap = VideoStream(src=CAM_NUM).start()
    time.sleep(2.0)

    # initialize the firstFrame in video stream
    firstFrame = None

    while True:

        # if ret is true than no error with cap.isOpened
        frame = cap.read()

        if frame is None:
            log.error("No frame available !!")
            # print("ERROR: No frame available !!")
            break

        # resize frame for required size
        resize_frame = cv2.resize(frame, config.VID_FRAME_SIZE)

        # opencv understand BGR, in order to display we need to convert image  form   BGR to RGB
        frame = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2RGB)  # for display

        # color has no bearing on motion detection algorithm
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # to smooth the image and remove noise(if not then could throw algorithm off)
        # smoothing average pixel intensities across an 21x21 region
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first stream is not initialized, store it for reference
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and firstFrame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the threshold image to fill in holes, then find contours on the thresholded image
        # apply background subtraction
        thresh = cv2.dilate(thresh, None, iterations=2)

        # im2, contours, hierarchy  = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if imutils.is_cv2() else contours[1]

        # # looping for contours
        for c in contours:
            if cv2.contourArea(c) < MIN_AREA:
                continue
            print(c)
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # get bounding box from contour
            (x, y, w, h) = cv2.boundingRect(c)

            # draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (cX, cY), 7, (0, 0, 225), -1)

        if config.VID_FRAME_INDEX == 0:
            frame = thresh

        elif config.VID_FRAME_INDEX == 1:

            frame = frame

        elif config.VID_FRAME_INDEX == 2:
            frame = frameDelta

        # Display the frame
        display.display_render(screen, frame, disply_obj, TASK_INFO)
        image_title.Render(to=screen, pos=TASK_TITLE_POS)

        # check if TASK_INDEX is not 1 then it means another buttons has pressed
        if not config.TASK_INDEX == 2:
            log.info("TASK_INDEX is not 2 but {}".format(config.TASK_INDEX))
            break

        if not config.CAM_START or config.EXIT:
            # print(f"face_recog config.CAM_START {config.CAM_START}")
            break
        # cv2.imshow('Original', frame)
        # cv2.imshow('threshold', thresh)
        # cv2.imshow('FrameDelta', frameDelta)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.stop()
    cv2.destroyAllWindows()
    log.info("closing motion detection")


# ----------------------------------------------------------------------------------------------------------------------
# """ main  """
# ----------------------------------------------------------------------------------------------------------------------
def main():
    """
    """
    cap = VideoStream(src=CAM_NUM).start()
    time.sleep(2.0)

    # initialize the firstFrame in video stream
    firstFrame = None

    while True:

        # if ret is true than no error with cap.isOpened
        frame = cap.read()

        if frame is None:
            print("ERROR: No frame available !!")
            break

        # resize the image inorder to have less processing time
        frame = imutils.resize(frame, width=500)
        # color has no bearing on motion detection algorithm
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # to smooth the image and remove noise(if not then could throw algorithm off)
        # smothing avarage pixel intensities across an 21x21 region
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first stream is not initialized, store it for reference
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and firstFrame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the threshold image to fill in holes, then find contours on the thresholded image
        # apply background substraction
        thresh = cv2.dilate(thresh, None, iterations=2)

        # im2, contours, hierarchy  = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if imutils.is_cv2() else contours[1]

        # looping for contours
        for c in contours:
            if cv2.contourArea(c) < MIN_AREA:
                continue
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # get bounding box from countour
            (x, y, w, h) = cv2.boundingRect(c)

            # draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (cX, cY), 7, (0, 0, 225), -1)

        cv2.imshow('Original', frame)
        cv2.imshow('threshold', thresh)
        cv2.imshow('FrameDelta', frameDelta)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
