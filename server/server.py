import socketserver
import threading


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


class ThreadedUDPRequestHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        msgRecvd = self.rfile.readline().strip()
        self.server.queue.add(msgRecvd)


class Queue:
    def __init__(self, ip, port):
        self.server = ThreadedUDPServer((ip, port), ThreadedUDPRequestHandler)
        self.server.queue = self
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.messages = []

    def start_server(self):
        self.server_thread.start()
        print("Server loop running in thread:", self.server_thread.name)

    def stop_server(self):
        self.server.shutdown()
        self.server.server_close()

    def add(self, message):
        self.messages.append(message)

    def view(self):
        return self.messages

    def get(self):
        return self.messages.pop()

    def exists(self):
        return len(self.messages)


import socket
import time

class Server:
    def __init__(self, ip, port):
        self.queue = Queue(ip, port)

    def start_server(self):
        self.queue.start_server()

    def stop_server(self):
        self.queue.stop_server()

    def loop(self):
        while True:
            time.sleep(1)
            while self.queue.exists():
                self.handle(self.queue.get())

    def handle(self, message):
        print(message)
        pass

    def send(self, ip, port, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        try:
            sock.sendall(bytes(message, 'utf-8'))
        finally:
            sock.close()


class Alice(Server):
    def handle(self, message):
        try:
            print("Got: {}".format(message))
        except Exception as e:
            print("Error: {}".format(e))

if __name__ == "__main__":
    print("Alice started.")
    app = Alice("localhost", 8889)
    app.start_server()
    app.loop()
    app.stop_server()