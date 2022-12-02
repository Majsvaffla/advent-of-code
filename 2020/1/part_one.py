with open("input.txt") as f:
    numbers = [int(x) for x in f.readlines()]
answer = ()
for n in numbers:
    for m in numbers:
        if n + m == 2020:
            answer = (n, m)
            break
    if answer:
        break

print(f"{n} + {m} = 2020 and {n} * {m} = {n*m}")
