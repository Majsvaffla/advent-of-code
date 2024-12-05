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

RULES: list[tuple[int, int]] = []
UPDATES: list[tuple[int, ...]] = []

for line in input_lines:
    if "|" in line:
        first, second = line.strip().split("|")
        RULES.append((int(first), int(second)))
    if "," in line:
        UPDATES.append(tuple(int(n) for n in line.strip().split(",")))

ordered_updates: list[tuple[int, ...]] = []


def is_ordered(update: tuple[int, ...]) -> bool:
    for i in range(len(update)):
        if i + 1 == len(update):
            continue
        if not any((update[i], update[i + 1]) == rule for rule in RULES):
            return False
    return True


def order_page(page: int, update: tuple[int, ...]) -> int:
    order = 0
    for first, second in RULES:
        if first not in update or second not in update:
            continue
        if page == first:
            order -= 1
        elif page == second:
            order += 1
    return order


for update in UPDATES:
    if not is_ordered(update):
        debug(update)
        ordered_update = tuple(sorted(update, key=lambda p: order_page(p, update)))
        debug(ordered_update)
        ordered_updates.append(tuple(ordered_update))


print(sum(update[len(update) // 2] for update in ordered_updates))
