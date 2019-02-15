# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 12:53:33 2018

@author: patelviv

This face recognistion script contains all the code for face recognitions.
It uses opencv haarcascade for recognition of faces.
The haarcascade file name is "haarcascade_frontalface_default.xml" (provided by opencv)
The trainner file is trained from some hollywood actors (from game of thrones TV series) faces. Those actor names are following
   1. Emilia Clarke
   2. Kit harington
   3. Nikolaj Coster Waldau
   4. Peter Dinklage

"""

import sys
import cv2
import pickle
import os
import logging

# -----------------------------------------------
""" Modules """
import config
from lib.vision.vision import Vision
from lib.display import display
from lib.display import display_gui
from lib.udp import udp

# -----------------------------------------------
log = logging.getLogger("__main__." + __name__)

# -----------------------------------------------
""" globals """

TASK_INFO = " Face Names : Vivek, Emilia Clarke, Kit harington, Nikolaj Coster Waldau, Peter Dinklage"
TASK_TITLE = "Face Recognition"

TASK_TITLE_POS = (config.VID_FRAME_CENTER - (len(TASK_TITLE) * 4), 100)


# ------------------------------------------------------------------------------
# """ file_path_create """
# ------------------------------------------------------------------------------

def file_path_create(file_name_fm_same_dir):
    """ file_path_create """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name_fm_same_dir)

    if not os.path.exists(file_path):
        log.info("does not exist path  {} ".format(file_path))
        sys.exit(-1)
    else:
        log.info("checked path {} ".format(file_path))
        return file_path


# ------------------------------------------------------------------------------
# """ face_recog_pygm """
# ------------------------------------------------------------------------------

def face_recog_pygm(screen, disply_obj, fbs):
    """
    Face Recognition pygame function read info from haarcascade_frontalface_defualt.xml, trainner.yml
    (for predicting trained faces), labels.pickle (to get label of faces ) and predict name of the face.

    """

    log.info("face_recog_pygm start")
    # print("[INFO] face_recog_pygm start")

    # objected created for cascade classifier
    face_cascade_name = "haarcascade_frontalface_default.xml"
    face_cascade_path = file_path_create(face_cascade_name)
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    # recognizer = cv2.face.createLBPHFaceRecognizer() # for opencv 2.4
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # creating object from trained file
    recognizer_file = "trainner.yml"
    recognizer_path = file_path_create(recognizer_file)
    file_path_create(recognizer_path)
    # recognizer.load(recognizer_path) # for opencv 2.4
    recognizer.read(recognizer_path)

    # reading labels from label.pickle file
    labels = {"person_name": 1}
    labels_file = "labels.pickle"
    labels_path = file_path_create(labels_file)
    try:
        with open(labels_path, 'rb') as f:
            og_labels = pickle.load(f)
            labels = {v: k for k, v in og_labels.items()}
    except Exception as error:
        log.error(error)
        raise

    image_title = display_gui.Menu.Text(text=TASK_TITLE, font=display_gui.Font.Medium)
    image_title.Render(to=screen, pos=TASK_TITLE_POS)

    vid = Vision()
    udp_send = udp.UdpPacket(udp_ip=config.IP, udp_port=config.PORT)

    front = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 0, 0)
    stroke = 2  # width of text

    log.info("frame reading starts ")
    # task_info = display_gui.Menu.Text(text=TASK_INFO, font=display_gui.Font.Medium)
    # task_info.Render(to=screen, pos=display_gui.TITLE_POSTION)

    while vid.isCameraConnected():

        _, frame = vid.getVideo()

        # resize frame for required size
        resize_frame = vid.resize_frame(frame)

        # covert image into gray
        gray = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2GRAY)  # for processing

        # the detected objects are returned as a list of rectangles.
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            # create rectangle around face
            frame = cv2.rectangle(resize_frame, (x, y), (x + w, y + w), (255, 0, 0), 2)  # RGB
            roi_gray = gray[y:y + h, x:x + w]
            # roi_color = frame[y:y+h, x:x+w]

            id_, confidence = recognizer.predict(roi_gray)
            if confidence >= 20:
                name = labels[id_]
                cv2.putText(frame, name, (x, y), front, 1.0, color, stroke, cv2.LINE_AA)
                new_x = x + int(w / 2)  # centre of face's x
                # OpenCV frame origin is left-up side , shifting it to left-down side
                new_y = frame.shape[0] - (y + int(h / 2))  # centre of face's y
                udp_send.udp_packet_send(x=new_x, y=new_y, frame=frame)

        if config.VID_FRAME_INDEX == 0:
            display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        elif config.VID_FRAME_INDEX == 1:
            display_frame = gray

        else:
            display_frame = frame

        # Display the frame
        display.display_render(screen, display_frame, disply_obj)

        # check if TASK_INDEX is not 1 then it means another buttons has pressed
        if not config.TASK_INDEX == 1:
            log.info("TASK_INDEX is not 1 but {}".format(config.TASK_INDEX))
            break

        if not config.CAM_START or config.EXIT:
            # print(f"face_recog config.CAM_START {config.CAM_START}")
            break

        # frame rate control
        if cv2.waitKey(fbs) & 0xff == ord('q'):
            break

    log.info("Face Recognition closing ")
    vid.videoCleanUp()


# ----------------------------------------------------------------------------------------------------------------------
# """ main """
# ----------------------------------------------------------------------------------------------------------------------
def main():
    # objected created for cascade classifer
    face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
    recognizer = cv2.face.createLBPHFaceRecognizer()
    recognizer.load("trainner.yml")

    labels = {"person_name": 1}
    with open("labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v: k for k, v in og_labels.items()}

    cap = cv2.VideoCapture(0)
    cv2.namedWindow("frame")

    while cap.isOpened():

        ret, frame = cap.read()
        # covert image into gray
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detecte object of different size i nthe input image.
        # the detected objects are returned as a list of rectangles.
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + w), (0, 0, 225), 2)  # BGR
            roi_gray = gray[y:y + h, x:x + w]
            # roi_color = frame[y:y + h, x:x + w]

            id_, conf = recognizer.predict(roi_gray)

            if conf >= 30 or conf <= 85:
                front = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255, 255, 255)
                stroke = 2

            cv2.putText(frame, name, (x, y), front, 1, color, stroke, cv2.LINE_AA)

        # Display the frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(20) & 0xff == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
