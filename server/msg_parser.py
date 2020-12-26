import re

cmd_types = ['init', 'init_judge', 'init_monitor', 'start_solving', 'set_params', 'get_params', 'change_pos']
cmd_types_without_params = ['init_judge', 'start_solving', 'get_params', 'init_monitor']
figure_names = ['queen', 'pawn', 'bishop', 'king', 'knight', 'rook']


def parse_type(cmd):
    parsed_cmd = cmd.split(' ', 1)
    type = parsed_cmd[0]

    if not (type in cmd_types):
        return 'invalid'

    return type


def parse_params(cmd, type):
    if type in cmd_types_without_params:
        return None

    parsed_cmd = cmd.split(' ', 1)

    if len(parsed_cmd) < 2:
        return 'invalid'

    params = parsed_cmd[1]

    if type == 'init':
        if params in figure_names:
            return params
        else:
            return 'invalid'

    elif type == 'set_params':
        board_size = params.split(' ')

        if len(board_size) != 2:
            return 'invalid'

        if not board_size[0].isnumeric() or not board_size[1].isnumeric():
            return 'invalid'

        board_width = int(board_size[0])
        board_height = int(board_size[1])

        if board_width <= 0 and board_height <= 0:
            return 'invalid'

        return (board_width, board_height)

    elif type == 'change_pos':
        figure_positions = re.findall(r'\([a-zA-Z]*\d* \d* \d*\)', params)

        if len(figure_positions) < 1:
            return 'invalid'

        new_positions = dict()

        for figure_position in figure_positions:
            info = figure_position.strip('()').split()
            name = info[0]
            x = info[1]
            y = info[2]

            new_positions[name] = (x, y)

        return new_positions


def parse_command(cmd):
    type = parse_type(cmd)

    if type == 'invalid':
        return 'invalid', 'invalid'

    params = parse_params(cmd, type)

    return type, params
