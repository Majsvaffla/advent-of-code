number_of_valid_passwords = 0
with open("input.txt") as f:
    for line in f.readlines():
        policy, password = line.split(":")
        counts, letter = policy.split()
        min_count, max_count = counts.split("-")
        char_count = 0
        for char in password:
            if letter == char:
                char_count += 1
        if int(min_count) <= char_count <= int(max_count):
            number_of_valid_passwords +=1
print(number_of_valid_passwords)
  