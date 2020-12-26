import socket
import queue
import threading


class UDPServer:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))

        self.msg_queue = queue.Queue()

        self.server_thread = threading.Thread(target=self.__recv_loop)
        self.server_thread.daemon = True

    def __recv_loop(self):
        while True:
            msg = self.sock.recvfrom(1024)

            if msg is not None:
                self.msg_queue.put((msg[0].strip().decode('utf-8'), msg[1]))

    def send(self, data, addr):
        self.sock.sendto(data, addr)

    def _start_recv(self):
        self.server_thread.start()
