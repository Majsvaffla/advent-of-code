with open("input.txt") as f:
    instructions = [x for x in f.readlines()]

# instructions = [
#     "forward 5",
#     "down 5",
#     "forward 8",
#     "up 3",
#     "down 8",
#     "forward 2",
# ]

horizontal_position = 0
depth = 0
aim = 0

for instruction in instructions:
    direction, amount = instruction.split()
    match direction, amount:
        case "forward", amount:
            horizontal_position += int(amount)
            if aim > 0:
                depth += int(amount) * aim
        case "up", amount:
            aim -= int(amount)
        case "down", amount:
            aim += int(amount)

print(horizontal_position, depth, horizontal_position * depth)
