import sys
from collections import defaultdict
from typing import List

fishies = list(map(int, sys.stdin.readline().split(",")))


def days_fishy_created(from_day: int, fish_value: int = 8) -> List[int]:
    return range(from_day - fish_value - 1, -1, -7)


def how_many_fishies(starting_fishies: List[int], after_days: int) -> int:
    fishies_created_per_day = defaultdict(int)

    for fishy in starting_fishies:
        for i in days_fishy_created(after_days, fishy):
            fishies_created_per_day[i] += 1

    for day in range(after_days, -1, -1):
        if not fishies_created_per_day[day]:
            continue
        for i in days_fishy_created(day):
            fishies_created_per_day[i] += fishies_created_per_day[day]

    return len(starting_fishies) + sum(fishies_created_per_day.values())


print(how_many_fishies(fishies, 80))
print(how_many_fishies(fishies, 256))
