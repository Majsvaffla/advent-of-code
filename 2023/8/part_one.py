from __future__ import annotations

import argparse
from collections import UserList
from dataclasses import dataclass
import itertools
from pathlib import Path
import re
from typing import Any, Iterable, Iterator, Literal


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
        match = re.match(
            r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)", node
        )
        assert match is not None
        head, left, right = match.groups()
        debug(head, left, right)
        yield head, left, right


def count_steps(network: Network, directions: Iterable[Direction]) -> int:
    current_node: Node = network["AAA"]
    for count, direction in enumerate(itertools.cycle(directions), start=1):
        current_node = network.get_next_node(current_node, direction)
        if current_node.head == "ZZZ":
            break
    return count


print(count_steps(
    network=Network({
        head: Node(head, left, right)
        for head, left, right in parse_nodes(input_lines[2:])
    }),
    directions=re.findall(r"([L|R])", input_lines[0]),
))
