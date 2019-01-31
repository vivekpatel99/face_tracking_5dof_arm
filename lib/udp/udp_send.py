# Created by viv at 30.01.19

import socket

UDP_IP = "255.255.255.255"
UDP_PORT = 47777


def udp_send(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data, (UDP_IP, UDP_PORT))


if __name__ == '__main__':
    udp_send("hello, world!")