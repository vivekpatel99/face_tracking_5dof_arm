# Created by viv at 08.12.18

import numpy as np
import constants as const


# ------------------------------------------------------------------------------
# """ CLASS: for Forward Kinematics"""
# ------------------------------------------------------------------------------

class Fkine:
    def __init__(self, PT):
        """ Initialize the DH parameters for forward kinematics
            DH parameters columns should be DH = [theta alpha  r  d]
        """
        if not isinstance(PT, list):
            print("[ERROR] dh parameter should be matrix {}".format(PT))
        if not np.shape(PT)[1] == 4:
            print("[ERROR] enter proper dh parameter {}".format(PT))

        self.PT = np.array(PT)

    # ------------------------------------------------------------------------------
    # """ FUNCTION: to calculate homogeneous matrix """
    # ------------------------------------------------------------------------------

    def homog_trans_matrix(self, row_num):
        """
        """
        """
         homogeneous Transformation matrix
               _                                                                                                     _
              |                                                                                                       |
              | cos(theta_n),    -sin(theta_n) * cos(alpha_n),     sin(theta_n) * sin(alpha_n),    r_n * cos(theta_n) |
              | sin(theta_n),     cos(theta_n) * cos(alpha_n),    -cos(theta_n) * sin(alpha_n),    r_n * sin(theta_n) |
        H_n = |       0     ,            sin(alpha_n)        ,             cos(alpha_n)       ,           d_n         |
              |       0     ,                  0             ,                  0             ,            1          |
              |_                                                                                                     _|
        """
        cos_theta_n = np.cos(self.PT[row_num][0])
        sin_theta_n = np.sin(self.PT[row_num][0])

        cos_alpha_n = np.cos(self.PT[row_num][1])
        sin_alpha_n = np.sin(self.PT[row_num][1])

        r_n = self.PT[row_num][2]
        d_n = self.PT[row_num][3]

        homog_trans_matrix = [
            [cos_theta_n, -sin_theta_n * cos_alpha_n, sin_theta_n * sin_alpha_n, r_n * cos_theta_n],
            [sin_theta_n, cos_theta_n * cos_alpha_n, -cos_theta_n * sin_alpha_n, r_n * sin_theta_n],
            [0, sin_alpha_n, cos_alpha_n, d_n],
            [0, 0, 0, 1],
        ]
        return np.matrix(homog_trans_matrix)

    # ------------------------------------------------------------------------------
    # """ FUNCTION: to Calculate forward kinematics """
    # ------------------------------------------------------------------------------

    def fk(self):
        """ function to generate forward kinematic from DH parameters
            by multiplying homogeneous transformation matrix Hn = H_0 * H_1 * ....H_n-1
        """
        Hn = []
        # taking the number of rows from the DH parameters
        for i in range(np.shape(self.PT)[0]):
            H = self.homog_trans_matrix(i)
            if i == 0:
                Hn = H
            else:
                Hn = np.dot(Hn, H)

        return Hn


# ------------------------------------------------------------------------------
# """ FUNCTION: to Calculate Rotation matrix """
# ------------------------------------------------------------------------------
def rotation_mat(theta):
    """ function will generate rotation matrix by implementing
    theta value in the rotation matrix """
    rotation_matrix = [
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ]

    return rotation_matrix


# ------------------------------------------------------------------------------
# """ FUNCTION: to Calculate forward kinematics """
# ------------------------------------------------------------------------------

def fkine_3dof():
    """
    """
    fk_m = Fkine(const.PT_3dof)
    Hn = fk_m.fk()
    # print(np.matrix(Hn))
    return Hn


# ------------------------------------------------------------------------------
# """ FUNCTION: to Test forward kinematics """
# ------------------------------------------------------------------------------
def test_3dof_fk():
    R0_1 = [
        [np.cos(const.THETA_1), 0., -np.sin(const.THETA_1)],
        [np.sin(const.THETA_1), 0., np.cos(const.THETA_1)],
        [0., 0., 1.]
    ]
    R1_2 = [
        [np.cos(const.THETA_2), -np.sin(const.THETA_2), 0.],
        [np.sin(const.THETA_2), np.cos(const.THETA_2), 0.],
        [0., 0., 1.]
    ]
    R2_3 = [
        [np.cos(const.THETA_3), -np.sin(const.THETA_3), 0.],
        [np.sin(const.THETA_3), np.cos(const.THETA_3), 0.],
        [0., 0., 1.]
    ]

    R0_2 = np.dot(R0_1, R1_2)
    R0_3 = np.dot(R0_2, R2_3)

    print(np.matrix(R0_3))
    # print(np.matrix(R0_2))


# ------------------------------------------------------------------------------
# """ FUNCTION: to Test forward kinematics """
# ------------------------------------------------------------------------------

def test_fkine(theta_1=const.THETA_1, theta_2=const.THETA_2, theta_3=const.THETA_3, theta_4=const.THETA_4,
               theta_5=const.THETA_5):
    """ manual calculation of forward kinematics to test"""

    """ Rotation matrix """

    R0_1 = [
        [1., 0., 0.],
        [0., 0., -1.],
        [0., 1., 0.]
    ]
    R1_2 = [
        [1., 0., 0.],
        [0., 1., 0.],
        [0., 0., 1.]
    ]
    R2_3 = [
        [1., 0., 0.],
        [0., 1., 0.],
        [0., 0., 1.]
    ]
    R3_4 = [
        [0., 0., 1.],
        [1., 0., 0.],
        [0., 1., 0.]
    ]
    R4_5 = [
        [1., 0., 0.],
        [0., 1., 0.],
        [0., 0., 1.]
    ]

    """ displacement vectors """
    d0_1 = [
        [0.],
        [0.],
        [const.L_1]
    ]
    d1_2 = [
        [const.L_2 * np.cos(theta_2)],
        [const.L_2 * np.sin(theta_2)],
        [0]
    ]
    d2_3 = [
        [const.L_3 * np.cos(theta_3)],
        [const.L_3 * np.sin(theta_3)],
        [0]
    ]
    d3_4 = [
        [const.L_4 * np.cos(theta_4)],
        [const.L_4 * np.sin(theta_4)],
        [0]
    ]
    d4_5 = [
        [0],
        [0.],
        [const.L_5]
    ]

    R0_1 = np.dot(rotation_mat(theta_1), R0_1)

    R1_2 = np.dot(rotation_mat(theta_2), R1_2)

    R2_3 = np.dot(rotation_mat(theta_3), R2_3)

    R3_4 = np.dot(rotation_mat(theta_4), R3_4)

    R4_5 = np.dot(rotation_mat(theta_5), R4_5)

    # R0_2 = np.dot(R0_1,R1_2)
    # R0_3 = np.dot(R0_2,R2_3)
    # R0_4 = np.dot(R0_3,R3_4)
    # R0_5 = np.dot(R0_4,R4_5)

    all_mat = [
        [R0_1, d0_1],
        [R1_2, d1_2],
        [R2_3, d2_3],
        [R3_4, d3_4],
        [R4_5, d4_5]
    ]

    Hn = []
    for i in range(len(all_mat)):

        H = np.concatenate((all_mat[i][0], all_mat[i][1]), 1)
        H = np.concatenate((H, [[0., 0., 0., 1.]]), 0)

        if i == 0:
            Hn = H

        else:
            Hn = np.dot(Hn, H)

    print("Rot_R0_5 ")
    print(Hn)


# ------------------------------------------------------------------------------
# """ FUNCTION: MAIN """
# ------------------------------------------------------------------------------

def main():
    fk_m = Fkine(const.PT_5dof)
    Hn = fk_m.fk()

    print(Hn)
    test_fkine()


if __name__ == "__main__":
    # test_fkine()
    # print()

    fk_m = Fkine(const.PT_5dof)
    Hn = fk_m.fk()
    print(np.matrix(Hn))
