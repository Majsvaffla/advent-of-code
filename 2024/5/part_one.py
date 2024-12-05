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

RULES = []
UPDATES = []

for line in input_lines:
    if "|" in line:
        RULES.append(tuple(line.strip().split("|")))
    if "," in line:
        UPDATES.append(tuple(line.strip().split(",")))

debug(RULES)
debug(UPDATES)

ordered_updates = []


def is_ordered(update: tuple[str, ...]) -> bool:
    for i in range(len(update)):
        if i + 1 == len(update):
            continue
        if not any((update[i], update[i + 1]) == rule for rule in RULES):
            return False
    return True


for update in UPDATES:
    if is_ordered(update):
        debug(update)
        ordered_updates.append(update)

print(sum(int(update[len(update) // 2]) for update in ordered_updates))
