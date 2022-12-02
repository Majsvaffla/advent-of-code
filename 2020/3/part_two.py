with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]
    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
    total_tree_count = 1
    for x_offset, y_offset in slopes:
        tree_count = 0
        x, y = 0, 0
        for i in range(y_offset, len(lines), y_offset):
            line = lines[i]
            x += x_offset
            while x > len(line) - 1:
                line += line
            if line[x] == "#":
                tree_count += 1
        total_tree_count *= tree_count
    print(total_tree_count)
