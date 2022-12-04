from __future__ import annotations

import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("file_path", help="File path to read input from.")
args = parser.parse_args()


def get_input_lines(input_file: Path):
    with Path(input_file).open() as f:
        return [line.strip() for line in f.readlines()]


input_lines = get_input_lines(args.file_path)


class SectionAssignment:
    @classmethod
    def from_string(cls, s: str) -> SectionAssignment:
        lower, upper = s.split("-")
        return cls(int(lower), int(upper))

    def __init__(self, lower: int, upper: int) -> None:
        self.lower, self.upper = lower, upper

    def contains(self, other: SectionAssignment) -> bool:
        return self.lower <= other.lower <= other.upper <= self.upper


pairs = (tuple(line.split(",")) for line in input_lines)
number_of_contains = 0
for first, second in (
    tuple(SectionAssignment.from_string(assignment) for assignment in pair)
    for pair in pairs
):
    if first.contains(second) or second.contains(first):
        number_of_contains += 1

print(number_of_contains)
