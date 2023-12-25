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


def is_good_variant(springs: list[str], group_lengths: GroupLengths) -> bool:
    group_lengths_pattern = r"(\.|\?)+".join(
        rf"(#|\?){{{group_length}}}" for group_length in group_lengths
    )
    pattern = r"(\.|\?)*" + group_lengths_pattern + r"(\.|\?)*$"
    debug(f"^{pattern}")
    return re.match(pattern, "".join(springs)) is not None


def get_variants(springs: list[str], group_lengths: GroupLengths) -> list[list[str]]:
    if "?" not in springs:
        return [springs]

    question_mark_index = springs.index("?")
    a = [*springs]
    b = [*springs]
    a[question_mark_index] = "#"
    b[question_mark_index] = "."

    a_is_good = is_good_variant(a, group_lengths)
    b_is_good = is_good_variant(b, group_lengths)

    return get_variants(a, group_lengths) if a_is_good else [] + get_variants(b, group_lengths) if b_is_good else []


count: int = 0

for springs, group_lengths in records:  # type: ignore
    variants = get_variants(springs, group_lengths)  # type: ignore
    count += len(variants)

print(count)
