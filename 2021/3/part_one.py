from collections import defaultdict

with open("input.txt") as f:
    numbers = [x.strip() for x in f.readlines()]

# numbers = [
#     "00100",
#     "11110",
#     "10110",
#     "10111",
#     "10101",
#     "01111",
#     "00111",
#     "11100",
#     "10000",
#     "11001",
#     "00010",
#     "01010",
# ]

def get_most_common_bit(bits):
    zeroes = 0
    ones = 0
    for bit in bits:
        if bit == "0":
            zeroes += 1 
        elif bit == "1":
            ones += 1
    if zeroes > ones:
        return "0"
    return "1"


def get_least_common_bit(bits):
    zeroes = 0
    ones = 0
    for bit in bits:
        if bit == "0":
            zeroes += 1 
        elif bit == "1":
            ones += 1
    if zeroes > ones:
        return "1"
    return "0"

bits_by_position = defaultdict(str)

for number in numbers:
    for position, bit in enumerate(number):
        bits_by_position[position] += bit

most_common_bits = ""
least_common_bits = ""

for position in sorted(bits_by_position.keys()):
    bits = bits_by_position[position]
    most_common_bits += get_most_common_bit(bits)
    least_common_bits += get_least_common_bit(bits)

gamma_rate = int(most_common_bits, 2)
epsilon_rate = int(least_common_bits, 2)

print(gamma_rate, epsilon_rate, gamma_rate * epsilon_rate)
