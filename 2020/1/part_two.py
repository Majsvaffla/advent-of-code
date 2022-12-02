with open("input.txt") as f:
    numbers = [int(x) for x in f.readlines()]
answer = ()
for n in numbers:
    for m in numbers:
        for k in numbers:
            if n + m + k == 2020:
                answer = (n, m, k)
                break
        if answer:
            break
    if answer:
        break

print(f"{n} + {m} + {k} = 2020 and {n} * {m} * {k} = {n*m*k}")
