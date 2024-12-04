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
MAS_X_LIST = list("MASMAS")

number_of_exes = 0


def char_at_position(x: int, y: int) -> str:
    if 0 <= x < NUMBER_OF_COLUMNS and 0 <= y < NUMBER_OF_ROWS:
        return GRID[y][x]
    return "KRYSSMAS"


for y, row in enumerate(GRID):
    for x, char in enumerate(row):
        if char != "A":
            continue
        debug((x, y))
        if any(
            [
                all(
                    [
                        char_at_position(x - 1, y - 1) == "M",
                        char_at_position(x + 1, y + 1) == "S",
                        char_at_position(x - 1, y + 1) == "M",
                        char_at_position(x + 1, y - 1) == "S",
                    ]
                ),
                all(
                    [
                        char_at_position(x - 1, y - 1) == "M",
                        char_at_position(x + 1, y + 1) == "S",
                        char_at_position(x - 1, y + 1) == "S",
                        char_at_position(x + 1, y - 1) == "M",
                    ]
                ),
                all(
                    [
                        char_at_position(x - 1, y - 1) == "S",
                        char_at_position(x + 1, y + 1) == "M",
                        char_at_position(x - 1, y + 1) == "S",
                        char_at_position(x + 1, y - 1) == "M",
                    ]
                ),
                all(
                    [
                        char_at_position(x - 1, y - 1) == "S",
                        char_at_position(x + 1, y + 1) == "M",
                        char_at_position(x - 1, y + 1) == "M",
                        char_at_position(x + 1, y - 1) == "S",
                    ]
                ),
            ]
        ):
            number_of_exes += 1
        if args.debug:
            breakpoint()

print(number_of_exes)
