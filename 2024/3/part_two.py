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

pattern = re.compile(r"(mul)\(([\d]+),([\d]+)\)|(do)\(\)|(don't)\(\)")

total_sum = 0
enabled = True

for line in input_lines:
    matches = re.finditer(pattern, line)
    operations = (match.groups() for match in matches)
    for operation in operations:
        match operation:
            case ("mul", x, y, None, None) if enabled:
                total_sum += int(x) * int(y)
                if args.debug:
                    print(f"mul({x},{y})")
            case (None, None, None, "do", None):
                enabled = True
                if args.debug:
                    print("do()")
            case (None, None, None, None, "don't"):
                enabled = False
                if args.debug:
                    print("don't()")

print(total_sum)
