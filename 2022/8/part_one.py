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

visible_trees = set()


def add_visible_tree(row, column, height):
    tree = (row, column, height)
    # if tree == (3, 1, 3):
    #     breakpoint()
    # if tree not in visible_trees:
    #     if 0 < row < 4 and 0 < column < 4:
    #         print(tree)
    visible_trees.add(tree)


tallest_tree_by_column = defaultdict(tuple)

for y, row in ((i, line.strip()) for i, line in enumerate(input_lines)):
    tallest_tree_by_column = defaultdict(tuple)
    trees = list(enumerate(int(r) for r in row))
    number_of_trees_in_row = len(trees)
    tallest_tree = ()

    for tree in trees:
        tree_position, tree_height = tree
        if tree_position == 0:
            # First tree in row is counted here.
            add_visible_tree(y, *tree)
        elif y == 0:
            # All other trees in the first row is counted here.
            add_visible_tree(y, *tree)
        elif tree_position == number_of_trees_in_row - 1:
            # Last tree in row is counted here.
            add_visible_tree(y, *tree)

        if tallest_tree == ():
            tallest_tree = tree
        else:
            tallest_tree_position, tallest_tree_height = tallest_tree
            if tree_height >= tallest_tree_height:
                if tree_height > tallest_tree_height:
                    add_visible_tree(y, *tree)
                tallest_tree = tree
            else:
                add_visible_tree(y, *tree)

        tallest_tree_in_column = tallest_tree_by_column[tree_position]
        if tallest_tree_in_column == ():
            tallest_tree_by_column[tree_position] = tree
        else:
            (
                tallest_tree_in_column_position,
                tallest_tree_in_column_height,
            ) = tallest_tree_in_column
            if tree_height >= tallest_tree_in_column_height:
                if tree_height > tallest_tree_in_column_height:
                    add_visible_tree(y, *tree)
                tallest_tree_by_column[tree_position] = tree
            else:
                add_visible_tree(y, *tree)

    tallest_tree = ()
    tallest_tree_by_column = defaultdict(tuple)

    for tree in reversed(trees):
        tree_position, tree_height = tree

        if tallest_tree == ():
            tallest_tree = tree
        else:
            tallest_tree_position, tallest_tree_height = tallest_tree
            if tree_height >= tallest_tree_height:
                if tree_height > tallest_tree_height:
                    add_visible_tree(y, *tree)
                tallest_tree = tree
            else:
                add_visible_tree(y, *tree)

        tallest_tree_in_column = tallest_tree_by_column[tree_position]
        if tallest_tree_in_column == ():
            tallest_tree_by_column[tree_position] = tree
        else:
            (
                tallest_tree_in_column_position,
                tallest_tree_in_column_height,
            ) = tallest_tree_in_column
            if tree_height >= tallest_tree_in_column_height:
                if tree_height > tallest_tree_in_column_height:
                    add_visible_tree(y, *tree)
                tallest_tree_by_column[tree_position] = tree
            else:
                add_visible_tree(y, *tree)
else:
    for tree in trees[1:-1]:
        add_visible_tree(y, *tree)

print(len(visible_trees))
