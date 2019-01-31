# Created by viv at 30.01.19

import socket

UDP_IP = "255.255.255.255"
UDP_PORT = 47777

def udp_receive():
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
    sock.bind((UDP_IP,UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024)
        return data
if __name__ == '__main__':
    udp_receive()