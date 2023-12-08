from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import re
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


@dataclass
class Converter:
    destination_range_start: int
    source_range_start: int
    range_length: int


@dataclass
class Map(list):
    source: str
    destination: str


input_lines = list(parse_input_line(line) for line in get_input_lines(args.file_path))

seeds: list[int] = [
    int(match.group()) for match in re.finditer(r" (\d+)", input_lines[0]) if match
]
maps: list[Map] = []

for line in input_lines[2:]:
    if match := re.match(r"([a-z]+)-to-([a-z]+)", line):
        maps.append(
            Map(
                source=match.group(1),
                destination=match.group(2),
            )
        )
    elif numbers := [int(number) for number in re.findall(r"(\d+)", line)]:
        assert maps != []
        assert len(numbers) == 3
        maps[-1].append(
            Converter(
                destination_range_start=numbers[0],
                source_range_start=numbers[1],
                range_length=numbers[2],
            )
        )

for seed in seeds:
    pass
