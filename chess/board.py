from chess.figure import Figure



class Board:
    def __init__(self, size):
        self.width, self.height = self._size = size
        self.figures = []
        self.figures_positions = dict()

    def add_figure(self, figure):
        self.figures.append(figure)

    def set_size(self, size):
        self._size = size

    def size(self):
        return self._size

    def update_positions(self, new_positions):
        self.figures_positions.update(new_positions)





