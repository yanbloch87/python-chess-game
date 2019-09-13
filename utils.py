def position_to_row(position):
    return int(position / 8)


def position_to_column(position):
    return position % 8


def col_to_number(col):
    return ord(col) - ord('A') + 1


def is_same_row(position_a, position_b):
    return int(position_a / 8) == int(position_b / 8)


def is_same_column(position_a, position_b):
    return position_a % 8 == position_b % 8


def col_row_to_position(col, row):
    return (ord(col) - ord('A')) + 8 * (row - 1)
