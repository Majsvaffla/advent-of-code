required_fields = (
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
)
number_of_valid_passports = 0
invalid = 0
with open("input.txt") as f:
    passports = f.read().split("\n\n")
    for passport in passports:
        lines = passport.split()
        items = (line.split(":") for line in lines)
        fields = {k: v for k, v in items}
        if all(field_name in fields for field_name in required_fields):
            number_of_valid_passports += 1
print(number_of_valid_passports)
