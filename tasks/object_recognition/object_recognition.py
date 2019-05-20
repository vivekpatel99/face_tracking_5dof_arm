# USAGE
# python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import logging
import cv2
import os
import sys

# -----------------------------------------------
""" Modules """

import config
from lib.vision.vision import Vision

from lib.udp import udp

log = logging.getLogger("__main__." + __name__)

# -----------------------------------------------
""" globals """

TASK_INFO = "Objects Names : Bottle, Bus, Car, Cat, Chair" \
            "Diningtable, Dog, Person, Pottedplant, Sofa, TV Monitor"

TASK_TITLE = "Object Recognition and Tracking"

TASK_TITLE_POS = (config.VID_FRAME_CENTER - (len(TASK_TITLE) * 6), 100)


# ------------------------------------------------------------------------------
# """ file_path_check """
# ------------------------------------------------------------------------------

def file_path_check(file_name_fm_same_dir):
    """ file_path_check """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name_fm_same_dir)

    if not os.path.exists(file_path):
        log.info("does not exist path  {} ".format(file_path))
        sys.exit(-1)
    else:
        log.info("checked path {} ".format(file_path))
        return file_path

# ------------------------------------------------------------------------------
# """ ObjectRecognition """
# ------------------------------------------------------------------------------
class ObjectRecognition:
    def __init__(self, prototxt_file="MobileNetSSD_deploy.prototxt.txt", caffe_model="MobileNetSSD_deploy.caffemodel"):
        prototxt_file = prototxt_file
        caffe_model = caffe_model
        self.prototxt_file_path = file_path_check(prototxt_file)
        self.caffe_model_path = file_path_check(caffe_model)
        # initialize the list of class labels MobileNet SSD was trained to
        # detect, then generate a set of bounding box colors for each class
        self.classes = ["background", "aeroplane", "bicycle", "bird", "boat",
                   "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                   "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                   "sofa", "train", "tvmonitor"]

        self.color = np.random.uniform(0, 255, size=(len(self.classes), 3))

        # load our serialized model from disk
        self.net = cv2.dnn.readNetFromCaffe(self.prototxt_file_path, self.caffe_model_path)

    # -------------------------------------------------------------------
    # """ run_object_recognition """
    # -------------------------------------------------------------------
    def run_object_recognition(self, frame, frame_display_indx):
        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                     0.007843, (300, 300), 127.5)

        # pass the blob through the network and obtain the detections and
        # predictions
        self.net.setInput(blob)
        detections = self.net.forward()

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > 0.2:
                # extract the index of the class label from the
                # `detections`, then compute the (x, y)-coordinates of
                # the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (start_x, startY, endX, endY) = box.astype("int")

                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(self.classes[idx], confidence * 100)

                if self.classes[idx] == config.recog_object_name:
                    cv2.rectangle(frame, (start_x, startY), (endX, endY), self.color[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15

                    cv2.putText(frame, label, (start_x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color[idx], 2)

                    # if frame_display_indx == 0:
                    #     out_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # elif frame_display_indx == 1:
                    #     out_frame = frame
                    # else:
                    out_frame = frame
                    return (start_x, y), out_frame

# ------------------------------------------------------------------------------
# """ object_recog_pygm """
# ------------------------------------------------------------------------------
def object_recog_pygm(screen, disply_obj):
    """ """
    from lib.display import display
    from lib.display import display_gui

    log.info("object_recog_pygm start... ")

    # configuration file use to train caffe model
    prototxt_file = "MobileNetSSD_deploy.prototxt.txt"
    caffe_model = "MobileNetSSD_deploy.caffemodel"

    prototxt_file_path = file_path_check(prototxt_file)

    caffe_model_path = file_path_check(caffe_model)

    image_title = display_gui.Menu.Text(text=TASK_TITLE, font=display_gui.Font.Medium)

    # initialize the list of class labels MobileNet SSD was trained to
    # detect, then generate a set of bounding box colors for each class
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]

    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    # load our serialized model from disk
    net = cv2.dnn.readNetFromCaffe(prototxt_file_path, caffe_model_path)

    # initialize the video stream
    vid = Vision()
    udp_send = udp.UdpPacket(udp_ip=config.IP, udp_port=config.PORT)

    # loop over the frames from the video stream
    while vid.isCameraConnected():

        ret, frame = vid.getVideo()

        frame = vid.resize_frame(frame)

        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                     0.007843, (300, 300), 127.5)

        # pass the blob through the network and obtain the detections and
        # predictions
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > 0.2:
                # extract the index of the class label from the
                # `detections`, then compute the (x, y)-coordinates of
                # the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(CLASSES[idx],
                                             confidence * 100)

                if CLASSES[idx] == config.recog_object_name:
                    cv2.rectangle(frame, (startX, startY), (endX, endY),
                                  COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15

                    cv2.putText(frame, label, (startX, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                    udp_send.udp_packet_send(x=startX, y=y, frame=frame)

        if config.VID_FRAME_INDEX == 0:

            frame = frame

        elif config.VID_FRAME_INDEX == 1:

            frame = frame

        else:
            # opencv understand BGR, in order to display we need to convert image  form   BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # for display
            # TASK_INFO = "Colored Frame  " + TASK_INFO
        # Display the frame
        display.display_render(screen, frame, disply_obj, TASK_INFO)

        image_title.Render(to=screen, pos=TASK_TITLE_POS)

        # check if TASK_INDEX is not 3 then it means another buttons has pressed
        if not config.TASK_INDEX == 3:
            log.info("TASK_INDEX is not 1 but {}".format(config.TASK_INDEX))
            break

        if not config.CAM_START or config.EXIT:
            # print(f"face_recog config.CAM_START {config.CAM_START}")
            break

        # show the output frame
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    vid.videoCleanUp()
    log.info("object_recog_pygm closing ")


# ----------------------------------------------------------------------------------------------------------------------
# """ main """
# ----------------------------------------------------------------------------------------------------------------------
def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--prototxt", required=True,
                    help="path to Caffe 'deploy' prototxt file")
    ap.add_argument("-m", "--model", required=True,
                    help="path to Caffe pre-trained model")
    ap.add_argument("-c", "--confidence", type=float, default=0.2,
                    help="minimum probability to filter weak detections")
    args = vars(ap.parse_args())

    # initialize the list of class labels MobileNet SSD was trained to
    # detect, then generate a set of bounding box colors for each class
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    # load our serialized model from disk
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

    # initialize the video stream, allow the cammera sensor to warmup,
    # and initialize the FPS counter
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    # vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)
    fps = FPS().start()

    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                     0.007843, (300, 300), 127.5)

        # pass the blob through the network and obtain the detections and
        # predictions
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > args["confidence"]:
                # extract the index of the class label from the
                # `detections`, then compute the (x, y)-coordinates of
                # the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(CLASSES[idx],
                                             confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

        # update the FPS counter
        fps.update()

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()


if __name__ == "__main__":
    main()
