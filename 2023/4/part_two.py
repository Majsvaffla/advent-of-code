from __future__ import annotations

import argparse
from pathlib import Path
import re
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    Card = tuple[int, set[int], set[int]]

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


def parse_numbers(s: str) -> set[int]:
    return {int(numeric) for numeric in re.findall(r"(\d+)(?: |\n|$)", s)}


input_lines = (parse_input_line(line) for line in get_input_lines(args.file_path))
split_input_lines = (
    [parse_numbers(s) for s in line.split("|")] for line in input_lines
)
cards: list[Card] = [
    (card_number, card_numbers, winning_numbers)
    for card_number, (card_numbers, winning_numbers) in enumerate(
        split_input_lines, start=1
    )
]


def calculate_points(card_numbers: set[int], winning_numbers: set[int]) -> int:
    point_numbers = [number for number in card_numbers if number in winning_numbers]
    number_of_point_numbers = len(point_numbers)
    if number_of_point_numbers == 0:
        return 0
    exponent = number_of_point_numbers - 1
    return 2**exponent


def count_winning_scratchcards(card: Card) -> int:
    card_number, card_numbers, winning_numbers = card
    points = calculate_points(card_numbers, winning_numbers)
    if points == 0:
        return 0
    card_index = card_number - 1
    last_copy_index_end = min(len(cards) - 1, card_number + points)
    copies = cards[card_index + 1:last_copy_index_end]
    debug(f"Card number {card_number} wins", [copy[0] for copy in copies])
    return sum(count_winning_scratchcards(copy) for copy in copies)

print(sum(count_winning_scratchcards(card) for card in cards))
