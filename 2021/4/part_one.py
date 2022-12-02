from pathlib import Path

root = Path(__file__).parent
input_path = root / "input.txt"
input_path = root / "example.txt"

boards = []

class Board(list):
    def mark(self, target):
        for row_index, row in enumerate(self):
            for column_index, column in enumerate(row):
                if column == target:
                    self[row_index][column_index] = f"X{target}X"

    @property
    def has_bingo(self):
        for row_index, row in enumerate(self):
            if all(number == f"X{number}X" for number in row):
                return True
        return False


with open(input_path) as f:
    numbers = [number for number in f.readline().split(",")]
    lines = [line.strip() for line in f.readlines()]
    for index, line in enumerate(lines):
        if line:
            continue
        board = []
        for row in lines[index + 1 : index + 6]:
            board.append([number for number in row.split() if number])
        boards.append(Board(board))

for drawn_number in numbers:
    for board in boards:
        board.mark(drawn_number)
        if board.has_bingo:
            print("Bingo!")

print(boards)
