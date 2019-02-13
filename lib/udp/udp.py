# Created by viv at 30.01.19

import socket
import pickle
import sys
import numpy as np

import config


# UDP_IP = "192.168.1.103"
# UDP_PORT = 47777


# ------------------------------------------------------------------------------
# """ class: To send and receive UDP packets """
# ------------------------------------------------------------------------------
class UdpPacket:
    def __init__(self, udp_ip, udp_port):

        if not isinstance(udp_ip, str):
            print("[ERROR] udp ip must be string ")
            sys.exit(1)

        if not isinstance(udp_port, int):
            print("[ERROR] udp port must be string ")
            sys.exit(1)

        for num in udp_ip.split('.'):  # check for correct ip address
            try:
                num = int(num)
            except Exception as error:
                print(error)
                sys.exit(1)
            if not num >= 0 or not num <= 255:
                print("[ERROR] udp ip is incorrect ")
                sys.exit(1)

        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # ------------------------------------------------------------------------------
    # """ FUNCTION: To send UDP packets """
    # ------------------------------------------------------------------------------
    def udp_packet_send(self, data=None, x=0, y=0, frame=None):
        """
        This function sent data via udp packets
        :param data: transformed coordinate values (x, y, z)  list
        :param x:  untransformed value
        :param y:  untransformed value
        :param frame: captured frame
        :return:
        """
        if data is None:
            if x != 0 or y != 0 or frame is not None:
                cm_to_pixel = config.frame_physical_area / frame.shape[0]
                # displacement vector of camera
                cam_point = np.mat([[x],
                                    [y],
                                    [90.0],  # distance between camera to person in cm
                                    [1.]],
                                   dtype=float
                                   )
                face_coordinates = np.dot(config.H0_C, cam_point)

                # origin of frame is at the left up side, setting in to right down side
                new_x = face_coordinates[0] * cm_to_pixel
                new_y = (frame.shape[0] - face_coordinates[1]) * cm_to_pixel
                new_z = face_coordinates[2] * cm_to_pixel

                data = [new_x, new_y, new_z]
                print(data)
            else:
                print("[ERROR] invalid input values")
        self.sock.sendto(pickle.dumps(data), (self.udp_ip, self.udp_port))

    # ------------------------------------------------------------------------------
    # """ FUNCTION: To receive UDP packets """
    # ------------------------------------------------------------------------------
    def udp_packet_receive(self):

        self.sock.bind((self.udp_ip, self.udp_port))

        while True:
            data, _ = self.sock.recvfrom(1024)
            return pickle.loads(data)

    def __exit__(self):
        self.sock.close()


if __name__ == '__main__':
    udp_pack = UdpPacket(udp_ip=config.UDP_IP, udp_port=config.UDP_PORT)
    for i in range(10):
        udp_pack.udp_packet_send(pickle.dumps([0, 0, 0]))
