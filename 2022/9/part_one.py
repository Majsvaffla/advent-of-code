from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable, Iterable

parser = argparse.ArgumentParser()
parser.add_argument("file_path", help="File path to read input from.")
args = parser.parse_args()


def get_input_lines(input_file: Path):
    with Path(input_file).open() as f:
        return f.readlines()


input_lines = get_input_lines(args.file_path)

Movement = Callable[["Position"], None]


def get_movement(direction: str) -> Movement:
    if direction == "U":
        return Position.move_up
    elif direction == "R":
        return Position.move_right
    elif direction == "D":
        return Position.move_down
    elif direction == "L":
        return Position.move_left
    raise AssertionError(f"Invalid direction {direction}.")


instructions: Iterable[tuple[Movement, int]] = (
    (get_movement(direction), int(amount))
    for direction, amount in (line.split() for line in input_lines)
)


class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    def __repr__(self) -> str:
        return self.as_tuple()

    def __str__(self) -> str:
        return f"<Position x={self.x} y={self.y}>"

    def __eq__(self, rhs: Position) -> bool:
        return self.x == rhs.x and self.y == rhs.y

    def as_tuple(self) -> tuple[int, int]:
        return self.x, self.y

    def move_up(self) -> None:
        self.y -= 1

    def move_right(self) -> None:
        self.x += 1

    def move_down(self) -> None:
        self.y += 1

    def move_left(self) -> None:
        self.x -= 1

    def move(self, movement: Movement) -> None:
        movement(self)

    def is_touching(self, other: Position) -> bool:
        return any(
            [
                self == other,
                self.is_in_same_column(other) and self.is_vertically_adjacent(other),
                self.is_horizontally_adjacent(other) and self.is_in_same_row(other),
                self.is_diagonally_adjacent(other),
            ]
        )

    def is_in_same_column(self, other: Position) -> bool:
        return self.x == other.x

    def is_in_same_row(self, other: Position) -> bool:
        return self.y == other.y

    def is_vertically_adjacent(self, other: Position) -> bool:
        return self.y - other.y == 1

    def is_horizontally_adjacent(self, other: Position) -> bool:
        return self.x - other.x == 1

    def is_diagonally_adjacent(self, other: Position) -> bool:
        return self.is_vertically_adjacent(other) and self.is_horizontally_adjacent(
            other
        )

    def is_vertically_apart(self, other: Position) -> bool:
        return self.y - other.y == 2

    def is_horizontally_apart(self, other: Position) -> bool:
        return self.x - other.x == 2

    def is_diagonally_apart(self, other: Position) -> bool:
        return self.is_vertically_apart(other) or self.is_horizontally_apart(other)


positions_visited_by_the_tail: set[Position] = set()
head_position = Position(0, 0)
tail_position = Position(0, 0)


for movement, amount in instructions:
    for step in range(1, amount + 1):
        print("head", head_position)
        head_position.move(movement)
        if head_position.is_horizontally_apart(tail_position):
            if head_position.is_in_same_row(tail_position):
                tail_position.move(movement)
            elif head_position.is_vertically_adjacent(tail_position):
                if head_position.is_to_the_right(tail_position):
                    tail_position.move_right()
                else:
                    tail_position.move_left()

        elif head_position.is_vertically_apart(tail_position):
            if head_position.is_in_same_column(tail_position):
                tail_position.move(movement)
            elif head_position.is_horizontally_adjacent(tail_position):
                if head_position.is_above(tail_position):
                    tail_position.move_up()
                else:
                    tail_position.move_down()

        print("tail", tail_position)
        positions_visited_by_the_tail.add(tail_position.as_tuple())
        print()

print(len(positions_visited_by_the_tail))
