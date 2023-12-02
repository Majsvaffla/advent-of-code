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


@dataclass
class Bag:
    number_of_red_cubes: int
    number_of_green_cubes: int
    number_of_blue_cubes: int


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


def get_impossible_sets(sets: Iterable[Set], bag: Bag) -> Iterator[Set]:
    for s in sets:
        if s.number_of_red_cubes > bag.number_of_red_cubes:
            yield s
        elif s.number_of_green_cubes > bag.number_of_green_cubes:
            yield s
        elif s.number_of_blue_cubes > bag.number_of_blue_cubes:
            yield s


def get_possible_games(games: Iterable[Game], bag: Bag) -> Iterator[Game]:
    for game in games:
        impossible_sets = get_impossible_sets(game.sets, bag)
        if not any(impossible_sets):
            yield game


all_games = parse_games(line.strip().split(":") for line in input_lines)  # type: ignore
possible_games = get_possible_games(
    all_games,
    Bag(
        number_of_red_cubes=12,
        number_of_green_cubes=13,
        number_of_blue_cubes=14,
    ),
)

print(sum(game.number for game in possible_games))
