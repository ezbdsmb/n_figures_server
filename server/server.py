import socket


class UDPServer():
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))

    def run(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            print("received message:", data, "from", addr)

            self.sock.sendto(b"ok", addr)


if __name__ == "__main__":
    server = UDPServer("localhost", 9999)
    server.run()
