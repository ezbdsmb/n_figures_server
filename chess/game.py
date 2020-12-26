import queue

from chess.board import Board
from chess.figure import Figure


PRE = 0
SOLVING = 1


class Game:
    def __init__(self, board_size=(8, 8)):
        self.board = Board(board_size)
        self.state = PRE
        self.judge = False

        self.pre_solve_figures_queue = queue.Queue()

    def start(self):
        if self.state != PRE:
            return False

        self.state = SOLVING

    def set_board_size(self, size):
        self.board.set_size(size)

    def board_size(self):
        return self.board.size()

    def end(self):
        self.state = PRE

    def add_figure(self, type):
        name = f'{type[0]}{str(self.pre_solve_figures_queue.qsize())}'
        self.pre_solve_figures_queue.put(Figure(name, type))
        return name

    def set_judge(self):
        self.judge = True

    def update_positions(self, new_positions):
        self.board.update_positions(new_positions)

    def figure_positions(self):
        return self.board.figures_positions





