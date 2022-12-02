number_of_valid_passwords = 0
with open("input.txt") as f:
    for line in f.readlines():
        policy, password = line.strip().split(": ")
        positions, letter = policy.split()
        pos_1, pos_2 = positions.split("-")
        if password[int(pos_1) - 1] == letter:
            if password[int(pos_2) - 1] == letter:
                continue
            number_of_valid_passwords += 1
        elif password[int(pos_2) - 1] == letter:
            number_of_valid_passwords += 1
print(number_of_valid_passwords)
