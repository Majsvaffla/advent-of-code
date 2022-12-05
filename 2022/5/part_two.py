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

STACK_LINES = []
INSTRUCTION_LINES = []

while input_lines:
    line = input_lines.pop(0).strip("\n")
    if "[" in line:
        STACK_LINES.append(line)
    elif line.startswith("move"):
        INSTRUCTION_LINES.append(line)
    elif len(line) > 1:
        NUMBER_OF_STACKS = int(line.split().pop())


class Stack:
    def __init__(self, items: list[str] | None = None) -> None:
        self._items = items or []

    def __len__(self):
        return len(self._items)

    def __repr__(self) -> str:
        return repr(self._items)

    def pop(self):
        return self._items.pop()

    def push(self, item: str):
        self._items.append(item)


STACK_SIZE = len(STACK_LINES)
STACK_LEVELS = list(reversed(STACK_LINES))
stacks = []

for i in range(NUMBER_OF_STACKS):
    stack = Stack()
    for stack_level in STACK_LEVELS:
        item = stack_level[i * 4 : i * 4 + 3].strip("[ ]")
        if item:
            stack.push(item)
    stacks.append(stack)


class Instruction:
    @classmethod
    def from_string(cls, s: str) -> Instruction:
        parts = s.split()
        return cls(
            amount=int(parts[1]),
            source=int(parts[3]),
            destination=int(parts[5]),
        )

    def __init__(self, source: int, destination: int, amount: int) -> None:
        self.source = source
        self.destination = destination
        self.amount = amount


instructions = (Instruction.from_string(line.strip()) for line in INSTRUCTION_LINES)
for instruction in instructions:
    source_stack = stacks[instruction.source - 1]
    destination_stack = stacks[instruction.destination - 1]
    crates = [source_stack.pop() for _ in range(1, instruction.amount + 1)]
    for crate in reversed(crates):
        destination_stack.push(crate)

print("".join(stack.pop() for stack in stacks))
