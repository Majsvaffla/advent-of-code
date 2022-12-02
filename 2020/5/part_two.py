from part_one import decode_seat

with open("input.txt") as f:
    seats = sorted(seat_id for * _, seat_id in map(decode_seat, (line.strip() for line in f.readlines())))
    for index, seat in enumerate(seats):
        preceeding_index, following_index = (
            max(0, index - 1),
            min(len(seats) - 1, index + 1),
        )
        if seat - seats[preceeding_index] == 2:
            print(seat - 1)
            break
        elif seats[following_index] - seat == 2:
            print(seat + 1)
            break
