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

reports = [[int(n) for n in line.split()] for line in input_lines]

number_of_safe_reports = 0


def is_safe(report: list[int]) -> bool:
    if report != sorted(report) and report != sorted(report, reverse=True):
        return False
    last_level = report[0]
    for level in report[1:]:
        if level == last_level:
            return False
        if abs(last_level - level) > 3:
            return False
        last_level = level
    return True


for original_report in reports:
    dampened_reports: list[list[int]] = []
    for i in range(len(original_report)):
        dampened_report = [*original_report]
        dampened_report.pop(i)
        dampened_reports.append(dampened_report)
    for report in [original_report, *dampened_reports]:
        if is_safe(report):
            if args.debug:
                print(report)
            number_of_safe_reports += 1
            break

print(number_of_safe_reports)
