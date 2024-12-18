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
pairs = [tuple(int(n) for n in line.split("   ")) for line in input_lines]
left_numbers = [pair[0] for pair in pairs]
right_numbers = [pair[-1] for pair in pairs]
similarity_score = 0

for left_number in left_numbers:
    similarity_score += left_number * len(
        [right_number for right_number in right_numbers if right_number == left_number]
    )

print(similarity_score)
