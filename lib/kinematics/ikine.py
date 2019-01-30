# Created by viv at 26.01.19
import collections
import math
import sys

import numpy as np

# -----------------------------------------------
from lib.kinematics import fkine
import constants as const


# ------------------------------------------------------------------------------
# """ FUNCTION: To make input value in given range """
# ------------------------------------------------------------------------------
def make_val_in_range(val, min_range=-1, max_range=1):
    if val < min_range:
        return -1
    elif val > max_range:
        return 1
    else:
        return val


# ------------------------------------------------------------------------------
# """ FUNCTION: To Calculate 3 degrees of freedom (using Trigonometry) """
# ------------------------------------------------------------------------------
def ik_3dof(x_axis=0, y_axis=0, z_axis=0):
    """
    Calculate 3 degrees of freedom using Trigonometry
    Note: only for 3 revolute joints
         __   __
       |__| |__|
      _
    |_|

    Desired X Y Z position of the end effector in cm

    :param x_axis: cm
    :param y_axis: cm
    :param z_axis: cm
    :return:  values of thetas in radians
    """

    # length of each joint
    joint_len_1 = 33.  # mm 3.3cm
    joint_len_2 = 105.  # mm 10.5cm
    joint_len_3 = 98.  # mm 9.8cm

    theta_1 = math.atan(y_axis / x_axis)  # eq1
    r1 = np.sqrt(x_axis ** 2 + y_axis ** 2)  # eq2
    r2 = z_axis - joint_len_1  # eq3
    phi_2 = math.atan(r2 / r1)  # eq4
    r3 = np.sqrt(r1 ** 2 + r2 ** 2)  # eq5

    phi_1_eq = (((joint_len_3 ** 2) - (joint_len_2 ** 2) - (r3 ** 2)) / (-2.0 * joint_len_2 * r3))

    phi_1 = np.arccos(make_val_in_range(phi_1_eq, min_range=-1, max_range=1))  # eq6

    theta_2 = phi_2 - phi_1  # eq7

    phi_3_eq = (((r3 ** 2) - (joint_len_2 ** 2) - (joint_len_3 ** 2)) / (-2.0 * joint_len_2 * joint_len_3))
    phi_3 = np.arccos(make_val_in_range(phi_3_eq, min_range=-1, max_range=1))  # eq8
    theta_3 = np.pi - phi_3  # eq9

    return theta_1, theta_2, theta_3


# ------------------------------------------------------------------------------
# """ FUNCTION: To Check if the matrix is valid rotation matrix  """
# ------------------------------------------------------------------------------
def is_correct_rotation_mat(matrix):
    """
    Check if the matrix is valid rotation matrix
    :param matrix:
    :return: valid rotation matrix
    """
    mat = np.matrix(matrix)

    #  check whether matrix is 3x3 or not
    if not mat.shape == (3, 3):
        print("[ERROR] matrix must be 3x3")

    # checking if the matrix is a rotation matrix or not
    #  step #1 Square of each element of row
    #  step #2 adding the the output of all the squares
    #  step #3 calculating square root of total
    #  step #4 it must be 1 then and then matrix said to be valid rotation matrix
    for row in range(np.shape(mat)[1]):
        vector_len = 0

        for column in range(np.shape(mat)[0]):
            vector_len += mat[column, row] ** 2

        if not np.sqrt(vector_len) == 1:
            print("[ERROR] matrix is not a valid rotation matrix")
            sys.exit(1)
    return mat


# ------------------------------------------------------------------------------
# """ FUNCTION: To Calculate 5 degrees of freedom  """
# ------------------------------------------------------------------------------
def ik_5dof(end_eff_direction_mat, *axis):
    """
    Calculate 5 degrees of freedom

    :param end_eff_direction_mat: end effector matrix (valid rotation matrix)
    :param *axis: x, y, z
    :return: namedtuple 5 thetas
    """
    """
    step #1 : find R3_6 = inv R0_3 * R0_6
    step #2 : find R3_6 by Denavit Hartenberg or other methods
    step #3 : R0_6 depends on the requirement
             suppose gripper will be on facing on Z direction thus, the R0_6 matrix will be comparison with R0_1

                  _         _
                 | -1.  0  0 |
         R0_5 =  |  0  -1  0 |
                 |  1   0  1 |
                  -         -
         for example (will make Z axis up)         
         R0_5 = np.matrix([
              [-1., 0., 0.],
              [0., -1., 0.],
              [0., 0., 1.]
         ])         

    """
    end_eff_direction_mat = is_correct_rotation_mat(end_eff_direction_mat)

    theta_1, theta_2, theta_3 = ik_3dof(axis[0], axis[1], axis[2])

    fk_3dof = fkine.Fkine(const.PT_3dof)

    # removing last row and last column to get only rotation matrix
    R0_3 = fk_3dof.fk()[:, :-1][:-1]

    invR0_3 = np.linalg.inv(R0_3)

    R3_5 = invR0_3.dot(end_eff_direction_mat)

    theta_4 = np.arcsin(R3_5[1, 2])  # [row][column]
    theta_5 = np.arccos(R3_5[2, 1])

    Thetas = collections.namedtuple('thetas', ['theta_1',
                                               'theta_2',
                                               'theta_3',
                                               'theta_4',
                                               'theta_5'
                                               ])

    thetas = Thetas(theta_1=theta_1,
                    theta_2=theta_2,
                    theta_3=theta_3,
                    theta_4=theta_4,
                    theta_5=theta_5
                    )
    return thetas


if __name__ == "__main__":
    ik_3dof(50.0, 60.0, 60.0)
