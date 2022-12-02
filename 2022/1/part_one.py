with open("input.txt") as f:
    input_lines = f.readlines()

max_calories = 0
current_elf_sum = 0

for line in input_lines:
    if line == "\n":
        max_calories = max(max_calories, current_elf_sum)
        current_elf_sum = 0
    else:
        current_elf_sum += int(line)

print(max_calories)
