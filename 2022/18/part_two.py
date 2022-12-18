from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("file_path", help="File path to read input from.")
parser.add_argument("--debug", action="store_true", default=False)
args = parser.parse_args()


def get_input_lines(input_file: Path) -> list[str]:
    with Path(input_file).open() as f:
        return f.readlines()


def parse_input_line(line: str) -> str:
    return tuple(int(s) for s in line.strip().split(","))


input_lines = (parse_input_line(line) for line in get_input_lines(args.file_path))


@dataclass
class Cube:
    x: int
    y: int
    z: int

    def __eq__(self, other: Cube) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self) -> tuple[int]:
        return int("".join(str(c) for c in [self.x, self.y, self.z]))

    def is_adjacent(self, other: Cube) -> bool:
        return any(other == neighbor for neighbor in self.neighbors)

    @property
    def neighbors(self) -> list[Cube]:
        return [
            self.top_neighbor,
            self.right_neighbor,
            self.bottom_neighbor,
            self.left_neighbor,
            self.front_neighbor,
            self.back_neighbor,
        ]

    @property
    def top_neighbor(self) -> Cube:
        return Cube(self.x, self.y + 1, self.z)

    @property
    def right_neighbor(self) -> Cube:
        return Cube(self.x + 1, self.y, self.z)

    @property
    def bottom_neighbor(self) -> Cube:
        return Cube(self.x, self.y - 1, self.z)

    @property
    def left_neighbor(self) -> Cube:
        return Cube(self.x - 1, self.y, self.z)

    @property
    def front_neighbor(self) -> Cube:
        return Cube(self.x, self.y, self.z - 1)

    @property
    def back_neighbor(self) -> Cube:
        return Cube(self.x, self.y, self.z + 1)


cubes: list[Cube] = [Cube(x, y, z) for x, y, z in input_lines]

number_of_sides = 4456
number_of_sides = 64
number_of_enclosed_cubes = 0


def get_all_cubes():
    for cube in cubes:
        yield cube
        for neighbor in cube.neighbors:
            yield neighbor


for cube in get_all_cubes():
    if cube not in cubes and all(neighbor in cubes for neighbor in cube.neighbors):
        number_of_enclosed_cubes += 1

print(number_of_sides - number_of_enclosed_cubes)
