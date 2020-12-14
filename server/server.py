import socket
import queue
import threading


class UDPServer():
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.msg_queue = queue.Queue()

        self.server_thread = threading.Thread(target=self.recv_loop)
        self.server_thread.daemon = True


    def exec_loop(self):
        while True:
            while not self.msg_queue.empty():
                data, addr = self.msg_queue.get()
                type, params = self.parse_command(data)

                self.response(type, params, addr)

                print('type:', type, 'params:', params, 'addr:', addr)


    def recv_loop(self):
        while True:
            msg = self.sock.recvfrom(1024)

            if msg is not None:
                self.msg_queue.put((msg[0].strip().decode('utf-8'), msg[1]))


    def send(self, data, addr):
        self.sock.sendto(data, addr)


    def run(self):
        self.server_thread.start()
        self.exec_loop()

    def parse_command(self, data):
        parsed_msg = data.split(' ', 1)

        type = parsed_msg[0]
        params = []

        if len(parsed_msg) != 1:
            params = parsed_msg[1]

        return type, params


    def response(self, type, params, addr):
        if type == 'init':
            # TODO: а можно ли его инициализировать
            self.send(bytes('init_ok ' + params[0], encoding='utf-8'), addr)






if __name__ == "__main__":
    server = UDPServer("localhost", 9999)

    server.run()
