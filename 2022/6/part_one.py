from __future__ import annotations

import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("file_path", help="File path to read input from.")
args = parser.parse_args()


def get_input_lines(input_file: Path):
    with Path(input_file).open() as f:
        return f.readlines()


input_lines = get_input_lines(args.file_path)

MARKER_LENGTH = 4

for buffer in input_lines:
    for marker_start in range(len(buffer)):
        marker_end = marker_start + MARKER_LENGTH
        marker = buffer[marker_start:marker_end]
        if len(set(marker)) == MARKER_LENGTH:
            break

    print(marker_end)
