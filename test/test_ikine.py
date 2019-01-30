# Created by viv at 26.01.19

# R3_6_check = np.matrix([
#                 [-np.sin(theta_4) * np.cos(theta_5), np.sin(theta_4) * np.sin(theta_5),     np.cos(theta_4)],
#                 [ np.cos(theta_4) * np.cos(theta_5), np.cos(theta_4) * (-np.sin(theta_5)),  np.sin(theta_4)],
#                 [          np.sin(theta_5),                  np.cos(theta_5),                 0       ]
#               ])

# print(np.matrix(R3_6_check))

# L_1 = 33.  # mm 3.3cm
# L_2 = 105.  # mm 10.5cm
# L_3 = 98.  # mm 9.8cm
# L_4 = 27.  # mm 2.7cm
# L_5 = 65.  # mm 6.5cm
#
# PT_5dof = [
#     [theta_1, math.radians(90.0), 0, L_1],
#     [theta_2, 0, L_2, 0],
#     [theta_3, 0, L_3, 0],
#     [theta_4 + math.radians(90.0), math.radians(90.0), 0, 0],
#     [theta_5, 0, 0, L_4 + L_5]
# ]
# # fk.test_fkine(theta_1, theta_2, theta_3, theta_4, theta_5)
# fk_5dof = fk.Fkine(PT_5dof)
# # removing last row and last column to get only rotation matrix
# print(fk_5dof.fk())
# if __name__ == '__main__':
#         pass