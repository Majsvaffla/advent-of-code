MAX_ROW_NUMBER = 127
MAX_COLUMN_NUMBER = 7
ROW_NUMBERS = range(MAX_ROW_NUMBER + 1)
COLUMN_NUMBERS = range(MAX_COLUMN_NUMBER + 1)
FRONT = "F"
BACK = "B"
LEFT = "L"
RIGHT = "R"
NUMBER_OF_ROW_CHARS = 7
NUMBER_OF_COLUMN_CHARS = 3

def decode_seat(seat):
    def binary_space_partition(spaces, scheme, lower, upper):
        for char in scheme:
            split = len(spaces) / 2
            assert split == 1 or split % 2 == 0
            if char == lower:
                spaces = spaces[:int(split)]
            elif char == upper:
                spaces = spaces[int(split):]
        assert len(spaces) == 1
        return int(spaces[0])

    rows = [*ROW_NUMBERS]
    row_chars = seat[:NUMBER_OF_ROW_CHARS]
    columns = [*COLUMN_NUMBERS]
    column_chars = seat[-NUMBER_OF_COLUMN_CHARS:]

    assert len(row_chars) == 7
    assert len(column_chars) == 3

    row = binary_space_partition(rows, row_chars, FRONT, BACK)
    column = binary_space_partition(columns, column_chars, LEFT, RIGHT)
    seat_id = int(row) * 8 + int(column)

    return row, column, seat_id


if __name__ == '__main__':
    with open("input.txt") as f:
        print(sorted(seat_id for *_, seat_id in map(decode_seat, (line.strip() for line in f.readlines())))[-1])

