from __future__ import annotations

import argparse
from pathlib import Path
import re

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

DIGITS_PATTERN = r"(zero|one|two|three|four|five|six|seven|eight|nine|\d)"


def letters_to_int(letters: str) -> int:
    if letters.isnumeric():
        return int(letters)
    return {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }[letters]


total_calibration_value = 0

for line in input_lines:
    digits = re.findall(DIGITS_PATTERN, line.strip())
    if args.debug:
        print(line, digits)
    first_digit, last_digit = letters_to_int(digits[0]), letters_to_int(digits[-1])
    calibration_value = int(f"{first_digit}{last_digit}")
    if args.debug:
        print(first_digit, last_digit, calibration_value)
    total_calibration_value += calibration_value

print(total_calibration_value)
