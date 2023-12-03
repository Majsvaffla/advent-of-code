from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Literal, TypeGuard, Any


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


Numeric = Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
Blank = Literal["."]
Gear = Literal["*"]


def is_numeric(char: str) -> TypeGuard[Numeric]:
    return len(char) == 1 and char.isnumeric()


def is_blank(char: str) -> TypeGuard[Blank]:
    return char == "."


def is_symbol(char: str | Char) -> bool:
    if isinstance(char, Char):
        return is_symbol(str(char))
    return len(char) == 1 and not is_blank(char) and not char.isnumeric()


def is_gear(char: Char) -> TypeGuard[Gear]:
    return str(char) == "*"


@dataclass
class Char:
    char: str
    x: int
    y: int

    @classmethod
    def from_schematic(cls, schematic: list[str], x: int, y: int) -> Char:
        return cls(
            char=schematic[y][x],
            x=x,
            y=y,
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.char,
                self.x,
                self.y,
            )
        )

    def __str__(self) -> str:
        return self.char


input_lines = (parse_input_line(line) for line in get_input_lines(args.file_path))


def find_adjacent_symbols(
    schematic: list[str], digit: Numeric, x: int, y: int
) -> Iterator[Char]:
    char = Char(char=digit, x=x, y=y)
    line_length = len(schematic[0])
    number_of_lines = len(schematic)
    MIN_X, MAX_X = 0, line_length - 1
    MIN_Y, MAX_Y = 0, number_of_lines - 1
    TO_THE_LEFT = max(MIN_X, char.x - 1)
    ABOVE = max(MIN_Y, char.y - 1)
    TO_THE_RIGHT = min(MAX_X, char.x + 1)
    BELOW = min(MAX_Y, char.y + 1)
    adjacent_chars = [
        # to the left
        Char.from_schematic(schematic, TO_THE_LEFT, char.y),
        # diagonally to the left
        Char.from_schematic(schematic, TO_THE_LEFT, ABOVE),
        # above
        Char.from_schematic(schematic, char.x, ABOVE),
        # diagonally to the right
        Char.from_schematic(schematic, TO_THE_RIGHT, ABOVE),
        # to the right
        Char.from_schematic(schematic, TO_THE_RIGHT, char.y),
        # diagonally to the right
        Char.from_schematic(schematic, TO_THE_RIGHT, BELOW),
        # below
        Char.from_schematic(schematic, char.x, BELOW),
        # diagonally to the left
        Char.from_schematic(schematic, TO_THE_LEFT, BELOW),
    ]
    for adjacent_char in adjacent_chars:
        if is_symbol(adjacent_char) and adjacent_char is not char:
            debug(f"Found {adjacent_char} adjacent to {char} at ({char.x}, {char.y})")
            yield adjacent_char


def parse_part_number(consecutive_digits: list[Numeric]) -> int:
    part_number = int("".join(consecutive_digits))
    debug("Found part number:", part_number)
    return part_number


def find_gear_ratios(schematic: list[str]) -> Iterator[int]:
    possible_gears: dict[Char, set[int]] = defaultdict(set)
    for line_number, line in enumerate(schematic):
        consecutive_digits: list[Numeric] = []
        adjacent_symbols: list[Char] = []
        for position, char in enumerate(line):
            if is_numeric(char):
                consecutive_digits.append(char)
                adjacent_symbols.extend(
                    find_adjacent_symbols(
                        schematic,
                        char,
                        x=position,
                        y=line_number,
                    )
                )
            elif consecutive_digits:
                for adjacent_symbol in adjacent_symbols:
                    if str(adjacent_symbol) == "*":
                        part_number = parse_part_number(consecutive_digits)
                        possible_gears[adjacent_symbol].add(part_number)

                adjacent_symbols = []
                consecutive_digits = []

        if consecutive_digits:
            for adjacent_symbol in adjacent_symbols:
                if str(adjacent_symbol) == "*":
                    part_number = parse_part_number(consecutive_digits)
                    possible_gears[adjacent_symbol].add(part_number)

            adjacent_symbols = []
            consecutive_digits = []
    
    for gear, (first, second) in ((k, v) for k, v in possible_gears.items() if len(v) == 2):
        yield first * second


gear_ratios = find_gear_ratios(list(input_lines))

print(sum(gear_ratios))
