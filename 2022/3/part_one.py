from pathlib import Path

with Path("input.txt").open() as f:
    input_lines = f.readlines()

# input_lines = [
#     "vJrwpWtwJgWrhcsFMMfFFhFp",
#     "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
#     "PmmdzqPrVvPwwTWBwg",
#     "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
#     "ttgJtRGJQctTZtZT",
#     "CrZsJsPPZsGzwwsLwLmpwMDw",
# ]

ALPHABET_LOWER = [chr(i) for i in range(97, 123)]
ALPHABET_UPPER = [chr(i) for i in range(65, 91)]
ALPHABET = ALPHABET_LOWER + ALPHABET_UPPER


def get_priority(item: str) -> int:
    return ALPHABET.index(item) + 1


rucksacks = (line for line in input_lines)
priorities_sum = 0

for rucksack in rucksacks:
    number_of_items = len(rucksack)
    split_index = number_of_items // 2
    first_compartment = rucksack[: split_index]
    second_compartment = rucksack[split_index :]
    for item in first_compartment:
        if item in second_compartment:
            item_priority = get_priority(item)
            priorities_sum += item_priority
            print(item, item_priority)
            break

print(priorities_sum)