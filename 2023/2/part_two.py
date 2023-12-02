from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import repeat
from pathlib import Path
from typing import Iterable, Iterator, Literal, TypeGuard, get_args

parser = argparse.ArgumentParser()
parser.add_argument("file_path", help="File path to read input from.")
parser.add_argument("--debug", action="store_true", default=False)
args = parser.parse_args()


def get_input_lines(input_file: Path) -> list[str]:
    with Path(input_file).open() as f:
        return f.readlines()


def parse_input_line(line: str) -> str:
    return line.strip()


input_lines = (parse_input_line(line) for line in get_input_lines(args.file_path))

Color = Literal["red", "green", "blue"]


def is_color(s: str) -> TypeGuard[Color]:
    return s in get_args(Color)


@dataclass
class Cube:
    color: Color


class Set(list):
    def _count_cubes(self, color: Color) -> int:
        return len([cube for cube in self if cube.color == color])

    @property
    def number_of_red_cubes(self) -> int:
        return self._count_cubes("red")

    @property
    def number_of_green_cubes(self) -> int:
        return self._count_cubes("green")

    @property
    def number_of_blue_cubes(self) -> int:
        return self._count_cubes("blue")

    @property
    def power(self) -> int:
        return (
            self.number_of_red_cubes
            * self.number_of_green_cubes
            * self.number_of_blue_cubes
        )


@dataclass
class Game:
    number: int
    sets: list[Set]

    @property
    def number_of_red_cubes(self) -> int:
        return sum(s.number_of_red_cubes for s in self.sets)

    @property
    def number_of_green_cubes(self) -> int:
        return sum(s.number_of_green_cubes for s in self.sets)

    @property
    def number_of_blue_cubes(self) -> int:
        return sum(s.number_of_blue_cubes for s in self.sets)


games: list[Game] = []


def parse_cubes(cubes: str) -> Iterator[Cube]:
    for cube in cubes.split(","):
        times, color = cube.strip().split(" ")
        assert is_color(color)
        yield from repeat(Cube(color=color), times=int(times))


def parse_games(games: Iterable[tuple[str, str]]) -> Iterator[Game]:
    for game_id, sets in games:
        yield Game(
            number=int(game_id.split()[-1]),
            sets=[Set(parse_cubes(s.strip())) for s in sets.split(";")],
        )


def find_minimum_set(sets: Iterable[Set]) -> Set:
    max_red, max_green, max_blue = 0, 0, 0
    for s in sets:
        if s.number_of_red_cubes > max_red:
            max_red = s.number_of_red_cubes
        if s.number_of_green_cubes > max_green:
            max_green = s.number_of_green_cubes
        if s.number_of_blue_cubes > max_blue:
            max_blue = s.number_of_blue_cubes
    return Set([
        *repeat(Cube(color="red"), times=max_red),
        *repeat(Cube(color="green"), times=max_green),
        *repeat(Cube(color="blue"), times=max_blue),
    ])

def get_minimum_sets(games: Iterable[Game]) -> Iterator[Set]:
    for game in games:
        yield find_minimum_set(game.sets)


all_games = parse_games(line.strip().split(":") for line in input_lines)  # type: ignore

print(sum(s.power for s in get_minimum_sets(all_games)))
