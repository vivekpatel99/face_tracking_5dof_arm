# Created by viv at 30.01.19

import socket
import pickle

UDP_IP = "192.168.1.103"
UDP_PORT = 47777


def udp_receive():
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024)
        return pickle.loads(data)


if __name__ == '__main__':
    udp_receive()
