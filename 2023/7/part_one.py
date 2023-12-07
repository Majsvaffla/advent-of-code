from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path
from typing import Any, Generic, Literal, TypeGuard, TypeVar, get_args


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

T = TypeVar("T")


@dataclass
class Sortable(Generic[T]):
    value: T
    # ALPHABET: tuple[T]

    def __eq__(self, __value: object) -> bool:
        assert isinstance(__value, Sortable)
        return self.ALPHABET.index(self.value) == self.ALPHABET.index(__value.value)

    def __lt__(self, __value: object) -> bool:
        assert isinstance(__value, Sortable)
        return self.ALPHABET.index(self.value) > self.ALPHABET.index(__value.value)

    def __gt__(self, __value: object) -> bool:
        assert isinstance(__value, Sortable)
        return self.ALPHABET.index(self.value) < self.ALPHABET.index(__value.value)

    def __hash__(self) -> int:
        return hash(self.value)


Letter = Literal["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]


def is_letter(s: str) -> TypeGuard[Letter]:
    return s in Card.ALPHABET


class Card(Sortable[Letter]):
    ALPHABET: tuple[Letter] = get_args(Letter)  # type: ignore


@dataclass
class Hand:
    cards: list[Card]
    bid: int

    def __lt__(self, __value: object) -> bool:
        assert isinstance(__value, Hand)
        for m, n in zip(self.cards, __value.cards):
            if m == n:
                continue
            return m < n
        return False

    @property
    def counter(self) -> Counter:
        return Counter(self.cards)


def is_high_card(hand: Hand) -> bool:
    return len(set(hand.cards)) == 5


def _is_pair(hand: Hand, number_of_pairs: int) -> bool:
    pairs = [card for card, count in hand.counter.items() if count == 2]
    return len(pairs) == number_of_pairs


def is_one_pair(hand: Hand) -> bool:
    return _is_pair(hand, 1)


def is_two_pair(hand: Hand) -> bool:
    return _is_pair(hand, 2)


def _is_of_a_kind(hand: Hand, number_of_kind: int) -> bool:
    return any(count == number_of_kind for count in hand.counter.values())


def is_three_of_a_kind(hand: Hand) -> bool:
    return _is_of_a_kind(hand, 3)


def is_full_house(hand: Hand) -> bool:
    return is_one_pair(hand) and is_three_of_a_kind(hand)


def is_four_of_a_kind(hand: Hand) -> bool:
    return _is_of_a_kind(hand, 4)


def is_five_of_a_kind(hand: Hand) -> bool:
    return _is_of_a_kind(hand, 5)


rounds: list[Hand] = [
    Hand(
        cards=[Card(letter) for letter in hand if is_letter(letter)],
        bid=int(bid),
    )
    for hand, bid in (line.split() for line in input_lines)
]


Combination = Literal[
    "five_of_a_kind",
    "four_of_a_kind",
    "full_house",
    "three_of_a_kind",
    "two_pair",
    "one_pair",
    "high_card",
]


def is_kind(s: str) -> TypeGuard[Kind]:
    return s in Kind.ALPHABET


class Kind(Sortable[Combination]):
    ALPHABET: tuple[Combination] = get_args(Combination)  # type: ignore


def get_kind_of_hand(hand: Hand) -> Kind:
    if is_five_of_a_kind(hand):
        return Kind("five_of_a_kind")
    if is_four_of_a_kind(hand):
        return Kind("four_of_a_kind")
    if is_full_house(hand):
        return Kind("full_house")
    if is_three_of_a_kind(hand):
        return Kind("three_of_a_kind")
    if is_two_pair(hand):
        return Kind("two_pair")
    if is_one_pair(hand):
        return Kind("one_pair")
    if is_high_card(hand):
        return Kind("high_card")
    raise AssertionError("wat", hand)


hands_by_kind: dict[Kind, list[Hand]] = defaultdict(list)

for hand in rounds:
    hands_by_kind[get_kind_of_hand(hand)].append(hand)

sorted_kinds = sorted(hands_by_kind.keys())

all_hands: list[Hand] = []

for kind in sorted_kinds:
    all_hands.extend(sorted(hands_by_kind[kind]))

print(sum(hand.bid * rank for rank, hand in enumerate(all_hands, start=1)))
