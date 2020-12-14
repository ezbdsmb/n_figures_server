from UDPServer import UDPServer

class ChessServer(UDPServer):
    def exec_loop(self):
        while True:
            while not self.msg_queue.empty():
                data, addr = self.msg_queue.get()
                type, params = self.parse_command(data)

                self.response(type, params, addr)

                print('type:', type, 'params:', params, 'addr:', addr)

    def response(self, type, params, addr):
        if type == 'init':
            # TODO: а можно ли его инициализировать
            self.send(bytes('init_ok ' + params[0], encoding='utf-8'), addr)


    def parse_command(self, data):
        parsed_msg = data.split(' ', 1)

        type = parsed_msg[0]
        params = []

        if len(parsed_msg) != 1:
            params = parsed_msg[1]

        return type, params

    def start(self):
        self._start_recv()
        self.exec_loop()

if __name__ == "__main__":
    server = ChessServer("localhost", 9999)

    server.start()
