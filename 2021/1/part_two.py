with open("input.txt") as f:
    measurements = [int(x) for x in f.readlines()]

# measurements = [
#     199,  # A      
#     200,  # A B    
#     208,  # A B C  
#     210,  #   B C D
#     200,  # E   C D
#     207,  # E F   D
#     240,  # E F G  
#     269,  #   F G H
#     260,  #     G H
#     263,  #       H
# ]

increments = 0
last_window = None

while len(measurements) >= 3:
    window, measurements = measurements[:3], measurements[1:]
    if last_window and sum(window) > sum(last_window):
        increments += 1
    last_window = window

print(increments)
