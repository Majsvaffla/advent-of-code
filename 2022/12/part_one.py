from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("file_path", help="File path to read input from.")
args = parser.parse_args()


def get_input_lines(input_file: Path):
    with Path(input_file).open() as f:
        return (line.strip("\n") for line in f.readlines())


input_lines = get_input_lines(args.file_path)

# 1. GENERATE A LIST of all possible next steps
#    towards goal from current position

# 2. STORE CHILDREN in priority queue
#    based on distance to goal, closest first

# 3. SELECT CLOSEST child and REPEAT until goal reached or no more children


class Day12Error(Exception):
    pass


class OutOfBoundsError(Day12Error):
    pass


@dataclass
class Point:
    x: int
    y: int

    @classmethod
    def from_coordinates(cls, x: int, y: int) -> Point:
        if y < 0 or len(rows) - 1 < y:
            raise OutOfBoundsError(f"Row {y} isn't within the bounds.")
        if x < 0 or len(rows) - 1 < x:
            raise OutOfBoundsError(f"Column {x} isn't within the bounds.")
        return cls(x, y)


rows = [line for line in input_lines]


def get_starting_point():
    for y, row in enumerate(rows):
        for x, cell_value in enumerate(row):
            if cell_value == "S":
                return Point.from_coordinates(x, y)


starting_point = get_starting_point()
neighbors = [starting_point]


def get_neighbors(point: Point):
    def get_neighbor(x: int, y: int) -> Point | None:
        try:
            return Point.from_coordinates(x, y)
        except OutOfBoundsError:
            return None

    return [
        n
        for n in (
            get_neighbor(point.x + 1, point.y),
            get_neighbor(point.x - 1, point.y),
            get_neighbor(point.x, point.y + 1),
            get_neighbor(point.x, point.y - 1),
        )
        if n and get_elevation(point) - get_elevation(n) == 1
    ]


ALPHABET = [chr(i) for i in range(97, 123)]


def get_ascii_number(letter: str) -> int:
    assert len(letter) == 1
    return ALPHABET.index(letter) + 1


def get_elevation(point: str) -> int:
    letter = rows[point.y][point.x]
    if letter == "S":
        return get_ascii_number("a")
    if letter == "E":
        return get_ascii_number("z")
    return get_ascii_number(letter)


for neighbor in neighbors:
    neighbors = get_neighbors(neighbor)
