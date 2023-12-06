from __future__ import annotations

import argparse
from dataclasses import dataclass
import itertools
import math
import operator
from pathlib import Path
import re
from typing import Any, Iterator


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


input_lines = list(parse_input_line(line) for line in get_input_lines(args.file_path))

durations = (int(number) for number in re.findall(r"(\d+)", input_lines[0]))
distances = (int(number) for number in re.findall(r"(\d+)", input_lines[1]))


@dataclass
class Race:
    maximum_duration: int
    distance_record: int


races = (
    Race(
        maximum_duration=duration,
        distance_record=distance,
    ) 
    for duration, distance in zip(durations, distances)
)


def jespers_algorithm(t: int, x: int) -> int:
    return (t - x) * x


def get_solutions(race: Race) -> Iterator[int]:
    debug(race)
    for i in range(10_000):
        result = jespers_algorithm(race.maximum_duration, i)
        if result > race.distance_record:
            debug(i)
            yield i

print(math.prod(len(list(get_solutions(race))) for race in races))
