from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

parser = argparse.ArgumentParser()
parser.add_argument("file_path", help="File path to read input from.")
parser.add_argument("--debug", action="store_true", default=False)
args = parser.parse_args()


def debug(*print_args: Any, **print_kwargs: Any) -> None:
    if args.debug:
        print(*print_args, **print_kwargs)


def get_input_lines(input_file: Path) -> list[str]:
    with Path(input_file).open() as f:
        return f.readlines()


def parse_input_line(line: str) -> str:
    return line.strip()


input_lines = (parse_input_line(line) for line in get_input_lines(args.file_path))

GRID = tuple(input_lines)
NUMBER_OF_ROWS = len(GRID)
NUMBER_OF_COLUMNS = len(GRID[0])
XMAS_LIST = list("XMAS")

number_of_exes = 0


def char_at_position(x: int, y: int) -> str:
    if 0 <= x < NUMBER_OF_COLUMNS and 0 <= y < NUMBER_OF_ROWS:
        return GRID[y][x]
    return "KRYSSMAS"


for y, row in enumerate(GRID):
    for x, char in enumerate(row):
        if char != "X":
            continue
        debug((x, y))
        if [
            # horizontal forward
            char_at_position(x, y),
            char_at_position(x + 1, y),
            char_at_position(x + 2, y),
            char_at_position(x + 3, y),
        ] == XMAS_LIST:
            number_of_exes += 1
            debug("""XMAS
....
....
....""")
        if [
            # horizontal backward
            char_at_position(x, y),
            char_at_position(x - 1, y),
            char_at_position(x - 2, y),
            char_at_position(x - 3, y),
        ] == XMAS_LIST:
            number_of_exes += 1
            debug("""SAMX
....
....
....""")
        if [
            # vertical downward
            char_at_position(x, y),
            char_at_position(x, y + 1),
            char_at_position(x, y + 2),
            char_at_position(x, y + 3),
        ] == XMAS_LIST:
            number_of_exes += 1
            debug("""X...
M...
A...
S...""")
        if [
            # vertical upward
            char_at_position(x, y),
            char_at_position(x, y - 1),
            char_at_position(x, y - 2),
            char_at_position(x, y - 3),
        ] == XMAS_LIST:
            number_of_exes += 1
            debug("""S...
A...
M...
X...""")
        if [
            # diagonal upward forward
            char_at_position(x, y),
            char_at_position(x + 1, y - 1),
            char_at_position(x + 2, y - 2),
            char_at_position(x + 3, y - 3),
        ] == XMAS_LIST:
            number_of_exes += 1
            debug("""...S
..A.
.M..
X...""")
        if [
            # diagonal downward forward
            char_at_position(x, y),
            char_at_position(x + 1, y + 1),
            char_at_position(x + 2, y + 2),
            char_at_position(x + 3, y + 3),
        ] == XMAS_LIST:
            number_of_exes += 1
            debug("""X...
.M..
..A.
...S""")
        if [
            # diagonal downward backward
            char_at_position(x, y),
            char_at_position(x - 1, y + 1),
            char_at_position(x - 2, y + 2),
            char_at_position(x - 3, y + 3),
        ] == XMAS_LIST:
            number_of_exes += 1
            debug("""...X
..M.
.A..
S...""")
        if [
            # diagonal upward backward
            char_at_position(x, y),
            char_at_position(x - 1, y - 1),
            char_at_position(x - 2, y - 2),
            char_at_position(x - 3, y - 3),
        ] == XMAS_LIST:
            number_of_exes += 1
            debug("""S...
.A..
..M.
...X""")
        if args.debug:
            breakpoint()

print(number_of_exes)
