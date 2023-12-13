from __future__ import annotations

import argparse
import re
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

GroupLengths = tuple[int, ...]
Record = tuple[list[str], GroupLengths]

records: list[Record] = []

for line in input_lines:
    springs, numbers = line.split()
    records.append((list(springs), tuple(int(n) for n in numbers.split(","))))


def get_variants(springs: list[str]) -> list[list[str]]:
    if "?" not in springs:
        return [springs]
    question_mark_index = springs.index("?")
    a = [*springs]
    b = [*springs]
    a[question_mark_index] = "#"
    b[question_mark_index] = "."
    return get_variants(a) + get_variants(b)


count: int = 0 

for springs, group_lengths in records:  # type: ignore
    number_of_groups_lengths = len(group_lengths)
    group_lengths_pattern = r"\.+".join(
        rf"#{{{group_length}}}" for group_length in group_lengths
    )
    pattern = r"\.*" + group_lengths_pattern + r"\.*$"
    debug(pattern)
    for variant in get_variants(springs):  # type: ignore
        debug("".join(variant))
        if re.match(pattern, "".join(variant)):
            count += 1

print(count)
