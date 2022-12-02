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

for instruction in instructions:
    direction, value = instruction.split()
    match direction, value:
        case "forward", value:
            horizontal_position += int(value)
        case "up", value:
            depth -= int(value)
        case "down", value:
            depth += int(value)

print(horizontal_position, depth, horizontal_position * depth)
