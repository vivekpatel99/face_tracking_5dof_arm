# Created by viv at 29.01.19

import cv2
import os
import sys
import numpy as np

sys.path.append("/media/sf_linux_shared/python_projects/lib")
from vision.vision import Vision

cascade_path = "/media/sf_linux_shared/python_projects/face_detect/cascades/haarcascade_frontalface_default.xml"
if not os.path.exists(cascade_path):
    print("[ERROR] path not found {}".format(cascade_path))

face_cascade = cv2.CascadeClassifier(cascade_path)


def main():
    vid = Vision()
    vid.isCameraConnected()
    # transformation from robotic arm frame coordinate to camera coordinate
    # assume that camera is on the exactly above the origin of arm
    R0_C = np.mat([[1, 0, 0],
                   [0, np.cos(np.pi / 2), -np.sin(np.pi / 2)],
                   [0, np.sin(np.pi / 2), np.cos(np.pi / 2)]
                   ],
                  dtype=float
                  )
    d0_C = np.mat([[0.],
                   [80.],
                   [0.]],
                  dtype=float
                  )
    # creating Homogeneous transformation matrix
    H0_C = np.concatenate((R0_C, d0_C), 1)  # concatenate column
    H0_C = np.concatenate((H0_C, [[0, 0, 0, 1]]), 0)  # concatenate row

    while True:
        ret, frame = vid.getVideo()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # the detected objects are returned as a list of rectangles.
        faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + w), (255, 0, 0), 2)

            cam_point = np.mat([[x],
                                [y],
                                [0],
                                [1]],
                               dtype=float
                               )
            p0 = np.dot(H0_C, cam_point)
            print(p0[0], p0[1], p0[0])
            # roi_gray = gray_frame[y:y + h, x:x + w]
            # roi_color = img[y:y + h, x:x + w]

        vid.display('img', cv2.flip(frame, 1))

        if cv2.waitKey(30) & 0xFF == ord("q"):
            break

    vid.videoCleanUp()


if __name__ == '__main__':
    main()
