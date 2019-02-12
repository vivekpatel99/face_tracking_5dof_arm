# Created by viv at 29.01.19

import cv2
import os
import sys
import numpy as np

# sys.path.append("/media/sf_linux_shared/python_projects/face_detect/face_tracking_5dof_arm/lib/vision")
from lib.vision.vision import Vision
from lib.udp import udp
import config as const


# ------------------------------------------------------------------------------
# """ FUNCTION: send coordinates via udp packets """
# ------------------------------------------------------------------------------
def face_detect_coords_udpsend():
    """
    This function will detect face and get the x, y coordinates from the face. It will change coordinates system of
    robotic arm into camera coordinates system and then send those coordinates via udp packets
    :return:
    """
    if not os.path.exists(const.cascade_path):
        print("[ERROR] path not found {}".format(const.cascade_path))
        sys.exit(1)

    face_cascade = cv2.CascadeClassifier(const.cascade_path)

    vid = Vision()

    ip = "192.168.1.103"
    port = 47777
    udp_send = udp.UdpPacket(udp_ip=ip, udp_port=port)

    cm_to_pixel = const.frame_physical_area / vid.getFrameSize()[0]

    # transformation from robotic arm frame coordinate to camera coordinate
    # assume that camera is on the exactly above the origin of arm
    R0_C = np.mat([[1, 0, 0],
                   [0, 1, 0],
                   [0, 0, 1]
                   ],
                  dtype=float
                  )
    d0_C = np.mat([[0.],
                   [8.],  # assumed that the camera just at y axis  on arm's origin
                   [0.]],
                  dtype=float
                  )

    # creating Homogeneous transformation matrix
    H0_C = np.concatenate((R0_C, d0_C), 1)  # concatenate column
    H0_C = np.concatenate((H0_C, [[0., 0., 0., 1.]]), 0)  # concatenate row

    while vid.isCameraConnected():
        _, frame = vid.getVideo()
        # frame = cv2.flip(frame, 1)

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # the detected objects are returned as a list of rectangles.
        faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + w), (255, 0, 0), 2)
            # displacement vector of camera
            cam_point = np.mat([[x],
                                [y],
                                [90.0],  # distance between camera to person in cm
                                [1.]],
                               dtype=float
                               )
            face_coordinates = np.dot(H0_C, cam_point)

            # origin of frame is at the left up side, setting in to right down side
            new_x = face_coordinates[0] * cm_to_pixel
            # new_x = (frame.shape[1] - face_coordinates[0]) * cm_to_pixel
            new_y = (frame.shape[0] - face_coordinates[1]) * cm_to_pixel
            # new_y = (frame.shape[0] - face_coordinates[1]) * cm_to_pixel
            new_z = face_coordinates[2] * cm_to_pixel

            udp_send.udp_packet_send([new_x, new_y, new_z])

            print('x=', x, 'y=', y, 'new_x=', face_coordinates[0], 'new_y=', face_coordinates[1], 'new_z=', new_z)

        vid.display('Video Frame', cv2.flip(frame, 1))

        if cv2.waitKey(30) & 0xFF == ord("q"):
            break

    vid.videoCleanUp()


# ------------------------------------------------------------------------------
# """ FUNCTION: MAIN """
# ------------------------------------------------------------------------------
def main():
    if not os.path.exists(const.cascade_path):
        print("[ERROR] path not found {}".format(const.cascade_path))
        sys.exit(1)

    face_cascade = cv2.CascadeClassifier(const.cascade_path)
    vid = Vision()

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

    while vid.isCameraConnected():
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


if __name__ == '__main__':
    main()
