# Created by viv at 12.02.19
import numpy as np


def coord_transformed():
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
    return H0_C
