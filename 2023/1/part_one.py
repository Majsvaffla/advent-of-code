from __future__ import annotations

import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("file_path", help="File path to read input from.")
parser.add_argument("--debug", action="store_true", default=False)
args = parser.parse_args()


def get_input_lines(input_file: Path) -> list[str]:
    with Path(input_file).open() as f:
        return f.readlines()


def parse_input_line(line: str) -> str:
    return line.strip()


input_lines = (parse_input_line(line) for line in get_input_lines(args.file_path))

total_calibration_value = 0

for line in input_lines:
    digits = [digit for digit in line.strip() if digit.isnumeric()]
    first_digit, last_digit = digits[0], digits[-1]
    calibration_value = int(f"{first_digit}{last_digit}")
    if args.debug:
        print(first_digit, last_digit, calibration_value)
    total_calibration_value += calibration_value

print(total_calibration_value)