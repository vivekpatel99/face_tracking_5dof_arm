"""
https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

# find center of countor
https://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/
"""

import numpy as np
import cv2
# import sys
from imutils.video import VideoStream
import imutils
import time

import logging

# -----------------------------------------------
""" Modules """

from definition import define
from lib.vision.vision import Vision
from lib.display import display
from lib.display import display_gui
import globals

log = logging.getLogger("main." + __name__)

# -----------------------------------------------
""" globals """

TASK_INFO = " INFO move something "
TASK_TITLE = " Motion Detection "

TASK_TITLE_POS = (define.VID_FRAME_CENTER - (len(TASK_TITLE) * 4), 100)


# minimum size (in pixel) for a region of image to be considered actual "motion"
MIN_AREA = 500
CAM_NUM = 0


# ------------------------------------------------------------------------------
# """ motion_detection_pygm """
# ------------------------------------------------------------------------------

def motion_detection_pygm(screen, disply_obj, fbs):
    """ """
    log.info("motion_detection_pygm starts... ")

    image_title = display_gui.Menu.Text(text=TASK_TITLE, font=display_gui.Font.Medium)

    cap = VideoStream(src=CAM_NUM).start()
    time.sleep(2.0)

    # initialize the firstFrame in video stream
    firstFrame = None
    fgbg = cv2.createBackgroundSubtractorMOG2()
    while True:

        # if ret is true than no error with cap.isOpened
        frame = cap.read()

        if frame is None:
            log.error("No frame available !!")
            # print("ERROR: No frame available !!")
            break

        # resize frame for required size
        resize_frame = cv2.resize(frame, define.VID_FRAME_SIZE)

        # opencv understand BGR, in order to display we need to convert image  form   BGR to RGB
        frame = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2RGB)  # for display

        # color has no bearing on motion detection algorithm
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # to smooth the image and remove noise(if not then could throw algorithm off)
        # smoothing average pixel intensities across an 21x21 region
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first stream is not initialized, store it for reference
        # to smooth the image and remove noise(if not then could throw algorithm off)
        # smothing avarage pixel intensities across an 21x21 region
        gray = cv2.GaussianBlur(gray, (21, 21), 0)


        # apply background substraction
        fgmask = fgbg.apply(gray)
        (im2, contours, hierarchy) = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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


        if globals.VID_FRAME_INDEX == 0:
            frame = fgmask

        elif globals.VID_FRAME_INDEX == 1:

            frame = frame

        elif globals.VID_FRAME_INDEX == 2:
            frame = frame

        # Display the frame
        display.display_render(screen, frame, disply_obj, TASK_INFO)
        image_title.Render(to=screen, pos=TASK_TITLE_POS)

        # check if TASK_INDEX is not 1 then it means another buttons has pressed
        if not globals.TASK_INDEX == 2:
            log.info("TASK_INDEX is not 2 but {}".format(globals.TASK_INDEX))
            break

        if not globals.CAM_START or globals.EXIT:
            # print(f"face_recog globals.CAM_START {globals.CAM_START}")
            break
        # cv2.imshow('Original', frame)
        # cv2.imshow('threshold', thresh)
        # cv2.imshow('FrameDelta', frameDelta)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.stop()
    cv2.destroyAllWindows()
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
        resize_frame = cv2.resize(frame, define.VID_FRAME_SIZE)

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

            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # get bounding box from contour
            (x, y, w, h) = cv2.boundingRect(c)

            # draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (cX, cY), 7, (0, 0, 225), -1)

        if globals.VID_FRAME_INDEX == 0:
            frame = thresh

        elif globals.VID_FRAME_INDEX == 1:

            frame = frame

        elif globals.VID_FRAME_INDEX == 2:
            frame = frameDelta

        # Display the frame
        display.display_render(screen, frame, disply_obj, TASK_INFO)
        image_title.Render(to=screen, pos=TASK_TITLE_POS)

        # check if TASK_INDEX is not 1 then it means another buttons has pressed
        if not globals.TASK_INDEX == 2:
            log.info("TASK_INDEX is not 2 but {}".format(globals.TASK_INDEX))
            break

        if not globals.CAM_START or globals.EXIT:
            # print(f"face_recog globals.CAM_START {globals.CAM_START}")
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
