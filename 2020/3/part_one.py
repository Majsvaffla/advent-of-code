tree_count = 0
with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]
    x, y = 0, 0
    for line in lines[1:]:
        x += 3
        while x > len(line) - 1:
            line += line
        if line[x] == "#":
            tree_count += 1
print(tree_count)
