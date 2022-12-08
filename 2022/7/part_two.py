from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("file_path", help="File path to read input from.")
args = parser.parse_args()


def get_input_lines(input_file: Path):
    with Path(input_file).open() as f:
        return f.readlines()


input_lines = get_input_lines(args.file_path)

filesystem = {"/": {}}
current_working_directory = []
file_sizes_by_directory = defaultdict(int)


def _add_filesystem_entry(entry_name, entry_value) -> None:
    current_level = filesystem
    for level in current_working_directory:
        current_level = current_level[level]
    if entry_name not in current_level:
        current_level[entry_name] = entry_value


def add_directory(directory_name: str) -> None:
    _add_filesystem_entry(directory_name, {})


def add_file(file_name: str, file_size: int) -> None:
    _add_filesystem_entry(file_name, file_size)


for line in input_lines:
    if line.startswith("$"):
        cmd, *args = line.split()[1:]
        if cmd == "cd":
            path = args[0]
            if path == "..":
                current_working_directory.pop()
            else:
                # if current_working_directory and path == current_working_directory[-1]:
                #     continue
                current_working_directory.append(path)
        elif cmd == "ls":
            continue
    elif line.startswith("dir"):
        new_directory = line.split()[1]
        add_directory(new_directory)
    else:
        file_size, file_name = line.split()
        add_file(file_name, int(file_size))
        for level in reversed(current_working_directory):
            file_sizes_by_directory[level] += int(file_size)

MAX_DIRECTORY_SIZE = 100_000
TOTAL_DISK_SPACE = 70_000_000
REQUIRED_DISK_SPACE = 30_000_000


def sum_directory_file_size(directory):
    directory_sum = 0
    for entry in directory.values():
        if isinstance(entry, int):
            directory_sum += entry
        else:
            directory_sum += sum_directory_file_size(entry)
    return directory_sum


USED_DISK_SPACE = sum_directory_file_size(filesystem)
FREE_DISK_SPACE = TOTAL_DISK_SPACE - USED_DISK_SPACE
smallest_deletion_size = TOTAL_DISK_SPACE


def find_smallest_deletion_candidate(directory):
    global smallest_deletion_size
    directory_sum = 0
    for entry in directory.values():
        if isinstance(entry, int):
            directory_sum += entry
        else:
            directory_sum += sum_directory_file_size(entry)
    if (
        FREE_DISK_SPACE + directory_sum >= REQUIRED_DISK_SPACE
        and directory_sum < smallest_deletion_size
    ):
        smallest_deletion_size = directory_sum
    return directory_sum


find_smallest_deletion_candidate(filesystem)
print(smallest_deletion_size)
