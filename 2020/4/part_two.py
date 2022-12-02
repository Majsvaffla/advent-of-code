import re

valid_eye_colors = (
    "amb",
    "blu",
    "brn",
    "gry",
    "grn",
    "hzl",
    "oth",
)
required_fields = (
    ("byr", lambda byr: len(byr) == 4 and byr.isnumeric() and 1920 <= int(byr) <= 2002),
    ("iyr", lambda iyr: len(iyr) == 4 and iyr.isnumeric() and 2010 <= int(iyr) <= 2020),
    ("eyr", lambda eyr: len(eyr) == 4 and eyr.isnumeric() and 2020 <= int(eyr) <= 2030),
    ("hgt", lambda hgt: (
        (
            len(hgt) == 5 and
            hgt.endswith("cm") and
            hgt[:3].isnumeric() and
            150 <= int(hgt[:3]) <= 193
        )
        or
        (
            len(hgt) == 4 and
            hgt.endswith("in") and
            hgt[:2].isnumeric() and
            59 <= int(hgt[:2]) <= 76
        )
    )),
    ("hcl", lambda hcl: re.match(r"#[0-9a-f]{6}", hcl)),
    ("ecl", lambda ecl: ecl in valid_eye_colors),
    ("pid", lambda pid: len(pid) == 9 and pid.isnumeric()),
)
number_of_valid_passports = 0
with open("input.txt") as f:
    passports = f.read().split("\n\n")
    for passport in passports:
        lines = passport.split()
        items = (line.split(":") for line in lines)
        fields = {k: v for k, v in items}
        for field_name, validator in required_fields:
            if field_name not in fields or not validator(fields[field_name]):
                break
        else:
            number_of_valid_passports += 1
print(number_of_valid_passports)
