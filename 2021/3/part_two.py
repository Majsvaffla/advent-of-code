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

def find_oxygen_generator_rating(numbers, start_position):
    bits_by_position = defaultdict(str)

    for number in numbers:
        for position in range(len(number)):
            bits_by_position[position] += number[position]

    def get_numbers_at_position(position):
        most_common_bit = get_most_common_bit(bits_by_position[position])
        numbers_with_most_common_bit_at_position = [number for number in numbers if number[position] == most_common_bit]
        if len(numbers_with_most_common_bit_at_position) == 1:
            return numbers_with_most_common_bit_at_position[0]
        return find_oxygen_generator_rating(numbers_with_most_common_bit_at_position, position + 1)

    return get_numbers_at_position(start_position)

def find_co2_scrubber_rating(numbers, start_position):
    bits_by_position = defaultdict(str)

    for number in numbers:
        for position in range(len(number)):
            bits_by_position[position] += number[position]

    def get_numbers_at_position(position):
        least_common_bit = get_least_common_bit(bits_by_position[position])
        numbers_with_least_common_bit_at_position = [number for number in numbers if number[position] == least_common_bit]
        if len(numbers_with_least_common_bit_at_position) == 1:
            return numbers_with_least_common_bit_at_position[0]
        return find_co2_scrubber_rating(numbers_with_least_common_bit_at_position, position + 1)

    return get_numbers_at_position(start_position)


oxygen_generator_rating = int(find_oxygen_generator_rating(numbers, 0), 2)
co2_scrubber_rating = int(find_co2_scrubber_rating(numbers, 0), 2)

print(oxygen_generator_rating, co2_scrubber_rating, oxygen_generator_rating * co2_scrubber_rating)
