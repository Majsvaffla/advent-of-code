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


def group_rucksacks(rucksacks: list[str]) -> list[tuple[str]]:
    if len(rucksacks) == 3:
        return [tuple(rucksacks)]
    return [*group_rucksacks(rucksacks[:3]), *group_rucksacks(rucksacks[3:])]


priorities_sum = 0
grouped_rucksacks = group_rucksacks([line for line in input_lines])
for group in grouped_rucksacks:
    print(group)

for first_rucksack, second_rucksack, third_rucksack in grouped_rucksacks:
    for item in first_rucksack:
        if item in second_rucksack and item in third_rucksack:
            item_priority = get_priority(item)
            priorities_sum += item_priority
            print(item, item_priority)
            break

print(priorities_sum)
