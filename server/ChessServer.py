from server.UDPServer import UDPServer
from server.msg_parser import parse_command
from server.msg_formatter import format_dict
from chess.game import *


class ChessServer(UDPServer):
    def __init__(self, host, port):
        super().__init__(host, port)

        self.game = Game()

        self.agent_addresses = dict()
        self.judge_address = None
        self.monitor_adresses = []

    def exec_loop(self):
        while True:
            while not self.msg_queue.empty():
                cmd, addr = self.msg_queue.get()
                type, params = parse_command(cmd)

                self.response(type, params, addr)

                print('parsed msg: ', type, params, addr)

    def response(self, type, params, addr):
        if type == 'invalid' or params == 'invalid':
            self.send(bytes(f'bad_language {type}', encoding='utf-8'), addr)
            return

        if type == 'init_monitor':
            self.monitor_adresses.append(addr)
            self.send(bytes(f'{type} ok', encoding='utf-8'), addr)

            if self.game.state != PRE:
                for adresse in self.monitor_adresses:
                    self.send(bytes(f'board {format_dict(self.game.figure_positions())}', encoding='utf-8'), adresse)
                    self.send(bytes(f'board_size {str(self.game.board_size())}', encoding='utf-8'), adresse)

            return


        if self.game.state == PRE:
            if type == 'init':
                name = self.game.add_figure(params)
                self.agent_addresses[name] = addr
                self.send(bytes(f'{type} ok {name}', encoding='utf-8'), addr)

            elif type == 'init_judge':
                self.game.set_judge()
                self.judge_address = addr
                self.send(bytes(f'{type} ok', encoding='utf-8'), addr)

            elif type == 'set_params':
                self.game.set_board_size(params)
                self.send(bytes(f'{type} {str(self.game.board_size())}', encoding='utf-8'), addr)

            elif type == 'get_params':
                self.send(bytes(f'{type} {str(self.game.board_size())}', encoding='utf-8'), addr)

            elif type == 'start_solving':
                self.game.start()

                self.send(bytes(f'{type} ok', encoding='utf-8'), addr)

                self.send(bytes(f'board_size {str(self.game.board_size())}', encoding='utf-8'), self.judge_address)
                self.send(bytes(f'agents {format_dict(self.agent_addresses)}', encoding='utf-8'), self.judge_address)

                for adresse in self.monitor_adresses:
                    self.send(bytes(f'board_size {str(self.game.board_size())}', encoding='utf-8'), adresse)

            else:
                self.send(bytes(f'{type} failure', encoding='utf-8'), addr)

        elif self.game.state == SOLVING:
            if type == 'change_pos':
                self.game.update_positions(params)

                print(str(self.game.figure_positions()))

                for adresse in self.agent_addresses.values():
                    self.send(bytes(f'board {format_dict(self.game.figure_positions())}', encoding='utf-8'), adresse)

                for adresse in self.monitor_adresses:
                    self.send(bytes(f'board {format_dict(self.game.figure_positions())}', encoding='utf-8'), adresse)

            else:
                self.send(bytes(f'{type} failure', encoding='utf-8'), addr)



    def start(self):
        self._start_recv()
        self.exec_loop()
