from __future__ import annotations

import argparse
import functools
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("file_path", help="File path to read input from.")
args = parser.parse_args()


def get_input_lines(input_file: Path):
    with Path(input_file).open() as f:
        return f.readlines()


input_lines = (line.strip() for line in get_input_lines(args.file_path))

packets = [json.loads(line) for line in input_lines if line]


class OrderException(Exception):
    pass


class InRightOrderException(OrderException):
    pass


class NotInRightOrderException(OrderException):
    pass


def is_in_right_order(left: int | list, right: int | list) -> bool:
    print(f"Compare {left} vs {right}")
    if isinstance(left, int) and isinstance(right, int):
        """
        If both values are integers, the lower integer should come first.
        If the left integer is lower than the right integer, the inputs are in the right order.
        If the left integer is higher than the right integer, the inputs are not in the right order.
        Otherwise, the inputs are the same integer; continue checking the next part of the input.
        """
        if left < right:
            raise InRightOrderException(
                "Left side is smaller, so inputs are in the right order"
            )
        elif right < left:
            raise NotInRightOrderException(
                "Right side is smaller, so inputs are not in the right order"
            )
        raise InRightOrderException("Left and right are the same")
    elif isinstance(left, list) and isinstance(right, list):
        """
        If both values are lists, compare the first value of each list, then the second value, and so on.
        If the left list runs out of items first, the inputs are in the right order.
        If the right list runs out of items first, the inputs are not in the right order.
        If the lists are the same length and no comparison makes a decision about the order, continue checking the next part of the input.
        """
        while left and right:
            is_in_right_order(left.pop(0), right.pop(0))
        if not left:
            raise InRightOrderException(
                "Left side ran out of items, so inputs are in the right order"
            )
        if not right:
            raise NotInRightOrderException(
                "Right side ran out of items, so inputs are not in the right order"
            )
    elif isinstance(left, int):
        """
        If exactly one value is an integer, convert the integer to a list which contains that integer as its only value,
        then retry the comparison. For example, if comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2);
        the result is then found by instead comparing [0,0,0] and [2].
        """
        print(f"Mixed types; convert left to [{left}] and retry comparison")
        return is_in_right_order([left], right)
    elif isinstance(right, int):
        """
        If exactly one value is an integer, convert the integer to a list which contains that integer as its only value,
        then retry the comparison. For example, if comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2);
        the result is then found by instead comparing [0,0,0] and [2].
        """
        print(f"Mixed types; convert right to [{right}] and retry comparison")
        return is_in_right_order(left, [right])
    raise AssertionError("Unexpected condition was met.")


DIVIDER_PACKET_1 = [[2]]
DIVIDER_PACKET_2 = [[6]]
DIVIDER_PACKETS = [DIVIDER_PACKET_1, DIVIDER_PACKET_2]


def order_pairs(left: int | list, right: int | list) -> bool:
    try:
        if is_in_right_order(left, right):
            return True
    except InRightOrderException:
        return True
    except NotInRightOrderException:
        return False
    return False


ordered_packets = sorted(
    packets + DIVIDER_PACKETS, key=functools.cmp_to_key(order_pairs)
)
print(ordered_packets)
print(
    (ordered_packets.index(DIVIDER_PACKET_1) + 1)
    * (ordered_packets.index(DIVIDER_PACKET_2) + 1)
)
