from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Iterator, Literal, Sequence, TypeVar

parser = argparse.ArgumentParser()
parser.add_argument("file_path", help="File path to read input from.")
parser.add_argument("--debug", action="store_true", default=False)
args = parser.parse_args()


def get_input_lines(input_file: Path) -> list[str]:
    with Path(input_file).open() as f:
        return f.readlines()


T = TypeVar("T")


@dataclass
class Number:
    _digits: Sequence[T]

    def __str__(self) -> str:
        return "".join(self._digits)

    def __repr__(self) -> str:
        return str(self)

    def __len__(self) -> int:
        return len(self._digits)


DecimalDigit = Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
SnafuDigit = Literal["2", "1", "0", "-", "="]


@dataclass
class DecimalNumber(Number):
    _digits: Sequence[DecimalDigit]

    @classmethod
    def from_int(cls, number: int) -> DecimalNumber:
        return cls(str(number))

    def __iter__(self) -> Generator[DecimalDigit, None, None]:
        yield from self._digits

    def __reversed__(self) -> Iterator[DecimalDigit]:
        return reversed(self._digits)

    def __add__(self, other: DecimalNumber | int) -> DecimalNumber:
        return DecimalNumber.from_int(int(self) + int(other))

    def __sub__(self, other: DecimalNumber | int) -> DecimalNumber:
        return DecimalNumber.from_int(int(self) - int(other))

    def __int__(self) -> int:
        return int(str(self))

    def __mod__(self, other: DecimalNumber) -> DecimalNumber:
        return DecimalNumber.from_int(int(self) % int(other))

    def __floordiv__(self, other: DecimalNumber | int) -> DecimalNumber:
        return DecimalNumber.from_int(int(self) // int(other))


@dataclass
class SnafuNumber(Number):
    _digits: Sequence[SnafuDigit]

    def __iter__(self) -> Generator[SnafuDigit, None, None]:
        yield from self._digits

    def __reversed__(self) -> Iterator[SnafuDigit]:
        return reversed(self._digits)


def parse_input_line(line: str) -> str:
    return SnafuNumber(line.strip())


input_lines = (parse_input_line(line) for line in get_input_lines(args.file_path))
snafu_numbers = list(input_lines)


SNAFU_TO_DECIMAL_CONVERSION_TABLE: dict[SnafuDigit, DecimalDigit] = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}


def from_decimal_to_snafu(number: DecimalNumber) -> SnafuNumber:
    if number == DecimalNumber("-2"):
        return SnafuNumber("=")
    elif number == DecimalNumber("-1"):
        return SnafuNumber("-")
    elif number == DecimalNumber("0"):
        return SnafuNumber("0")
    elif number == DecimalNumber("1"):
        return SnafuNumber("1")
    elif number == DecimalNumber("2"):
        return SnafuNumber("2")

    remainder = (number + 2) % 5 - 2
    snafu_digit = from_decimal_to_snafu(remainder)
    if args.debug:
        print(number)
        print(snafu_digit)
        breakpoint()
    diff = number - remainder
    five_on_the_floor = diff // 5
    return SnafuNumber(
        [
            *str(from_decimal_to_snafu(five_on_the_floor)),
            str(snafu_digit),
        ]
    )


def from_snafu_to_decimal(number: SnafuNumber) -> DecimalNumber:
    decimal_number = 0
    for power, digit in enumerate(reversed(number)):
        decimal_number += SNAFU_TO_DECIMAL_CONVERSION_TABLE[digit] * 5**power
    return DecimalNumber(str(decimal_number))


decimal_numbers = (from_snafu_to_decimal(number) for number in snafu_numbers)
decimal_sum = sum(decimal_numbers, DecimalNumber("0"))
snafu_sum = from_decimal_to_snafu(decimal_sum)
print(snafu_sum)
