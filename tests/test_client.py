import socket
import sys

HOST, PORT = "localhost", 9998
data = "collision queen2"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


reqs = ['init queen', 'init queen', 'get_params', 'init_judge', 'start_solving', 'change_pos (q1 2 4)(q2 3 4)', 'change_pos (q1 2 4)(q2 3 4)']

for req in reqs:
    sock.sendto(bytes(req, "utf-8"), (HOST, PORT))
    received = str(sock.recv(1024), "utf-8")

    print("Sent:     {}".format(req))
    print("Received: {}".format(received))
    print()