from __future__ import annotations

import argparse
from itertools import repeat
from pathlib import Path
from typing import Iterator, Literal, Sequence

parser = argparse.ArgumentParser()
parser.add_argument("file_path", help="File path to read input from.")
parser.add_argument("--debug", action="store_true", default=False)
args = parser.parse_args()


def get_input_lines(input_file: Path):
    with Path(input_file).open() as f:
        return f.readlines()


input_lines = get_input_lines(args.file_path)

CAVE_INNER_WIDTH = 7
CAVE_OUTER_WIDTH = CAVE_INNER_WIDTH + 2


class Rock(list):
    def __init__(self, *levels: str) -> None:
        levels_list = list(levels)
        for level in levels_list:
            assert len(level) == CAVE_OUTER_WIDTH
        super().__init__(levels_list)

    def __contains__(self, s: str) -> bool:
        return any(s in level for level in self)

    def __repr__(self) -> str:
        return "\n".join(str(level) for level in self)

    @property
    def height(self):
        return len(self)


class Cave(Rock):
    def __repr__(self) -> str:
        return "\n".join(str(level) for level in reversed(self))


ROCKS = (
    Rock(
        "|..@@@@.|",
    ),
    Rock(
        "|...@...|",
        "|..@@@..|",
        "|...@...|",
    ),
    Rock(
        "|....@..|",
        "|....@..|",
        "|..@@@..|",
    ),
    Rock(
        "|..@....|",
        "|..@....|",
        "|..@....|",
        "|..@....|",
    ),
    Rock(
        "|..@@...|",
        "|..@@...|",
    ),
)

[JET_PATTERNS] = (line.strip() for line in input_lines)

EMPTY_SPACE = "."
FALLING_ROCK_SPACE = "@"
RESTING_ROCK_SPACE = "#"
BOTTOM_CAVE_LEVEL_SPACE = "-"

EMPTY_CAVE_LEVEL = "|.......|"
BOTTOM_CAVE_LEVEL = "+-------+"

assert len(EMPTY_CAVE_LEVEL) == CAVE_OUTER_WIDTH
assert len(BOTTOM_CAVE_LEVEL) == CAVE_OUTER_WIDTH

cave = Cave(str(BOTTOM_CAVE_LEVEL))


def get_rocks() -> Iterator[Rock]:
    while True:
        yield from ROCKS


endless_rocks = get_rocks()


def get_next_rock() -> Rock:
    return next(endless_rocks)


def get_jet_directions() -> Iterator[str]:
    while True:
        yield from JET_PATTERNS


endless_jet_directions = get_jet_directions()


def get_next_jet_direction():
    return next(endless_jet_directions)


def get_lower_edges(rock: tuple[str]) -> Iterator[int]:
    for level in rock:
        yield get_lower_edge(level)


def get_upper_edges(rock: tuple[str]) -> Iterator[int]:
    for level in rock:
        yield get_lower_edge(tuple(reversed(level)))


def get_lower_edge(level: str) -> int:
    return level.index(FALLING_ROCK_SPACE)


JetDirection = Literal["<", ">"]


def push_inner_level_left(inner_level: str) -> str:
    edge_index = inner_level.index(FALLING_ROCK_SPACE)
    if edge_index == 0:
        return inner_level
    return inner_level[1:] + EMPTY_SPACE


def push_inner_level_right(inner_level: str) -> str:
    return "".join(reversed(push_inner_level_left("".join(reversed(inner_level)))))


def push_inner_level(inner_level: str, direction: JetDirection) -> str:
    if direction == "<":
        return push_inner_level_left(inner_level)
    elif direction == ">":
        return push_inner_level_right(inner_level)
    else:
        raise AssertionError(f"Unknown jet direction {direction}.")


def push_levels(levels: Sequence[str], direction: JetDirection) -> Iterator[str]:
    for level in levels:
        pushed = f"|{push_inner_level(level[1:-1], direction)}|"
        print(level, pushed)
        yield pushed


def push_rock(rock: Rock, direction: JetDirection) -> Rock:
    return Rock(*push_levels(rock, direction))


def put_levels_to_rest(levels: Sequence[str]) -> Iterator[str]:
    for level in levels:
        yield level.replace(FALLING_ROCK_SPACE, RESTING_ROCK_SPACE)


def put_rock_to_rest(rock: Rock) -> Rock:
    return Rock(*put_levels_to_rest(rock))


class CollisionDetected(Exception):
    spaces = (
        RESTING_ROCK_SPACE,
        BOTTOM_CAVE_LEVEL_SPACE,
    )

    def __init__(self, upper_space: str, lower_space: str) -> None:
        assert upper_space == FALLING_ROCK_SPACE
        assert lower_space in self.spaces
        super().__init__(f"{upper_space} fell on {lower_space}.")


def merge_inner_levels(lower_level: str, upper_level: str) -> Iterator[str]:
    for lower_space, upper_space in zip(lower_level, upper_level, strict=True):
        if bottom_rock_level == "|@@@....|" and top_cave_level == "|...#...|":
            breakpoint()
        if (
            upper_space == FALLING_ROCK_SPACE
            and lower_space in CollisionDetected.spaces
        ):
            raise CollisionDetected(upper_space, lower_space)
        if lower_space == EMPTY_SPACE:
            yield upper_space
        else:
            assert lower_space != EMPTY_SPACE


def merge_levels(lower_level: str, upper_level: str) -> str:
    inner_level = "".join(merge_inner_levels(lower_level[1:-1], upper_level[1:-1]))
    return f"|{inner_level}|"


for i in range(2022):
    cave.extend(repeat(EMPTY_CAVE_LEVEL, 3))
    rock = get_next_rock()
    while FALLING_ROCK_SPACE in rock:
        if args.debug:
            print("falling")
            print(rock)
            print(cave)
            breakpoint()
        jet_direction = get_next_jet_direction()
        rock = push_rock(rock, jet_direction)
        if args.debug:
            print("pushed")
            print(rock)
            print(cave)
            breakpoint()
        bottom_rock_level = rock.pop()
        top_cave_level = cave.pop()
        try:
            merged = merge_levels(top_cave_level, bottom_rock_level)
            rock.append(merged)
        except CollisionDetected:
            rock.append(bottom_rock_level)
        if args.debug:
            print("merged")
            print(rock)
            print(top_cave_level)
            print(cave)
            breakpoint()
        if top_cave_level == EMPTY_CAVE_LEVEL:
            continue
        if top_cave_level == BOTTOM_CAVE_LEVEL:
            cave.append(top_cave_level)
            rock = put_rock_to_rest(rock)
            cave.extend(reversed(rock))
            if args.debug:
                print("put to rest")
                print(cave)
                breakpoint()
            break
        bottom_rock_level = rock.pop()
        if len(top_cave_level) != len(bottom_rock_level):
            breakpoint()
        for lower_space, upper_space in zip(
            top_cave_level, bottom_rock_level, strict=True
        ):
            if upper_space == FALLING_ROCK_SPACE and lower_space == RESTING_ROCK_SPACE:
                rock.append(bottom_rock_level)
                rock = put_rock_to_rest(rock)
                cave.append(top_cave_level)
                cave.extend(reversed(rock))
                if args.debug:
                    print("put to rest")
                    print(cave)
                    breakpoint()
                break
        else:
            rock.append(merge_levels(top_cave_level, bottom_rock_level))

print(cave.height)
