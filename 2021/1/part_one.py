with open("input.txt") as f:
    measurements = [int(x) for x in f.readlines()]

# measurements = [
#     199,
#     200,
#     208,
#     210,
#     200,
#     207,
#     240,
#     269,
#     260,
#     263,
# ]

increments = 0
last_measurement = None
for measurement in measurements:
    if last_measurement and measurement > last_measurement:
        increments += 1
    last_measurement = measurement
print(increments)
