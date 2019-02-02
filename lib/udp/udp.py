# Created by viv at 30.01.19

import socket
import pickle
import sys

UDP_IP = "192.168.1.103"
UDP_PORT = 47777


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
        self.sock = sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # ------------------------------------------------------------------------------
    # """ FUNCTION: To send UDP packets """
    # ------------------------------------------------------------------------------
    def udp_packet_send(self, data):
        """
        This function sent data via udp packets
        :param data: send data
        :return:
        """
        self.sock.sendto(data, (self.udp_ip, self.udp_port))

    # ------------------------------------------------------------------------------
    # """ FUNCTION: To receive UDP packets """
    # ------------------------------------------------------------------------------
    def udp_packet_receive(self):

        self.sock.bind((self.udp_ip, self.udp_port))

        while True:
            data, _ = self.sock.recvfrom(1024)
            return pickle.loads(data)


if __name__ == '__main__':
    udp_pack = UdpPacket(udp_ip=UDP_IP, udp_port=UDP_PORT)
    udp_pack.udp_packet_send(b"hello, world!")
