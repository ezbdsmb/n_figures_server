def format_dict(dict):
    msg = ''

    for item in dict.items():
        label = item[0]
        params = item[1]

        msg += f'({label}'

        for param in params:
            msg += f' {param}'

        msg += ')'

    return msg
