from __future__ import annotations

import argparse
from dataclasses import dataclass
import itertools
from pathlib import Path
import math
import re
from typing import Any, Iterable, Literal


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


input_lines = list(parse_input_line(line) for line in get_input_lines(args.file_path))

Direction = Literal["L", "R"]


@dataclass
class Node:
    head: str
    left: str
    right: str


class Network(dict):
    def get_next_node(self, node: Node, direction: Direction) -> Node:
        if direction == "L":
            return self[node.left]
        if direction == "R":
            return self[node.right]
        raise AssertionError("Invalid direction")


def parse_nodes(network: Iterable[str]):
    for node in network:
        match = re.match(r"([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)", node)
        assert match is not None
        head, left, right = match.groups()
        yield head, left, right


directions = re.findall(r"([L|R])", input_lines[0])
network = Network(
    {
        head: Node(head, left, right)
        for head, left, right in parse_nodes(input_lines[2:])
    }
)
start_nodes = [node for node in network.values() if node.head.endswith("A")]


def count_steps(current_node: Node, directions: Iterable[Direction]) -> int:
    for count, direction in enumerate(itertools.cycle(directions), start=1):
        current_node = network.get_next_node(current_node, direction)
        if current_node.head.endswith("Z"):
            break
    return count


print(math.lcm(*(count_steps(node, directions) for node in start_nodes)))
