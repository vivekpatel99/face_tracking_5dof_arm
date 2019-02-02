# Created by viv at 29.01.19

import cv2
import os
import sys
import numpy as np
import math
import pickle
import matplotlib.pyplot as plt

# sys.path.append("/media/sf_linux_shared/python_projects/face_detect/face_tracking_5dof_arm/lib/vision")
from vision.vision import Vision
from lib.udp import udp_send
import constants as const


def main():
  cascade_path = "/media/sf_linux_shared/python_projects/face_detect/face_tracking_5dof_arm/cascades/haarcascade_frontalface_default.xml"

  if not os.path.exists(cascade_path):
    print("[ERROR] path not found {}".format(cascade_path))
    sys.exit(1)

  face_cascade = cv2.CascadeClassifier(cascade_path)
  vid = Vision()
  vid.isCameraConnected()

  # transformation from robotic arm frame coordinate to camera coordinate
  # assume that camera is on the exactly above the origin of arm
  R0_C = np.mat([[1, 0, 0],
                 [0, np.cos(-np.pi / 2), -np.sin(-np.pi / 2)],
                 [0, np.sin(-np.pi / 2), np.cos(-np.pi / 2)]
                 ],
                dtype=float
                )

  d0_C = np.mat([[0.],
                 [8.],
                 [0.]],
                dtype=float
                )
  # creating Homogeneous transformation matrix
  H0_C = np.concatenate((R0_C, d0_C), 1)  # concatenate column
  H0_C = np.concatenate((H0_C, [[0, 0, 0, 1]]), 0)  # concatenate row

  while True:
    ret, frame = vid.getVideo()
    frame = cv2.flip(frame, 1)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # the detected objects are returned as a list of rectangles.
    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

    for (x, y, w, h) in faces:
      frame = cv2.rectangle(frame, (x, y), (x + w, y + w), (255, 0, 0), 2)

      cam_point = np.mat([[x],
                          [y],
                          [200.0],
                          [1]],
                         dtype=float
                         )
      p0 = np.dot(H0_C, cam_point)
      print(x, y, p0[0], p0[1], p0[0])

    vid.display('img', frame)
    # vid.display('img', cv2.flip(frame, 1))

    if cv2.waitKey(30) & 0xFF == ord("q"):
      break

  vid.videoCleanUp()


def coordinate_udpsend():

  cascade_path = "/media/sf_linux_shared/python_projects/face_detect/face_tracking_5dof_arm/cascades/haarcascade_frontalface_default.xml"

  if not os.path.exists(cascade_path):
    print("[ERROR] path not found {}".format(cascade_path))
    sys.exit(1)

  face_cascade = cv2.CascadeClassifier(cascade_path)

  vid = Vision()

  # the values here is assumed
  cm_to_pixel = const.frame_physical_area / vid.getFrameSize()[0]

  # transformation from robotic arm frame coordinate to camera coordinate
  # assume that camera is on the exactly above the origin of arm
  R_min90_x = np.mat([[1, 0, 0],
                      [0, np.cos(-np.pi / 2), -np.sin(-np.pi / 2)],
                      [0, np.sin(-np.pi / 2), np.cos(-np.pi / 2)]
                      ],
                     dtype=float
                     )

  R0_C = R_min90_x
  d0_C = np.mat([[0.],
                 [8.],
                 [0.]],
                dtype=float
                )
  # creating Homogeneous transformation matrix
  H0_C = np.concatenate((R0_C, d0_C), 1)  # concatenate column
  H0_C = np.concatenate((H0_C, [[0., 0., 0., 1.]]), 0)  # concatenate row

  while True:
    _, frame = vid.getVideo()
    # frame = cv2.flip(frame, 1)

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # the detected objects are returned as a list of rectangles.
    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

    for (x, y, w, h) in faces:
      frame = cv2.rectangle(frame, (x, y), (x + w, y + w), (255, 0, 0), 2)

      cam_point = np.mat([[x],
                          [y],
                          [90.0],
                          [1.]],
                         dtype=float
                         )
      p0 = np.dot(H0_C, cam_point)
      nx = (frame.shape[1] - abs(p0[0])) * cm_to_pixel
      ny = (frame.shape[0] - abs(p0[1])) * cm_to_pixel
      nz = p0[2] * cm_to_pixel
      cord_data = pickle.dumps([nx, ny, nz])
      udp_send.udp_send(cord_data)
      print(x, y, nx, ny, nz)

    vid.display('img', frame)

    if cv2.waitKey(30) & 0xFF == ord("q"):
      break

  vid.videoCleanUp()


if __name__ == '__main__':
  main()
