with open("input.txt") as f:
    input_lines = f.readlines()

calories_sums = []
current_elf_sum = 0

for line in input_lines:
    if line == "\n":
        calories_sums.append(current_elf_sum)
        current_elf_sum = 0
    else:
        current_elf_sum += int(line)

print(sum(sorted(calories_sums,reverse=True)[:3]))
