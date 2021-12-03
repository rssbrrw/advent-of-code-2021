import sys
from collections import Counter
from copy import copy
from typing import Iterable, List

nums = [list(x.strip()) for x in sys.stdin]


def transpose(matrix: List[List]) -> List[List]:
    return [*zip(*matrix)]


def bin2dec(x: Iterable[str]) -> int:
    return int("".join(x), 2)


nums_t = transpose(nums)

gamma = bin2dec(max(set(bits), key=list(bits).count) for bits in nums_t)
epsilon = bin2dec(min(set(bits), key=list(bits).count) for bits in nums_t)

print(f"Power consumption = {gamma * epsilon}")


# Oxygen
filtered_nums = copy(nums)
for idx in range(len(nums_t)):
    bit_counts = Counter(transpose(filtered_nums)[idx])
    most_common_bit = "1" if bit_counts["1"] >= bit_counts["0"] else "0"

    filtered_nums = [num for num in filtered_nums if num[idx] != most_common_bit]

    if len(filtered_nums) == 1:
        break

oxygen = bin2dec(filtered_nums[0])

# CO2
filtered_nums = copy(nums)
for idx in range(len(nums_t)):
    bit_counts = Counter(transpose(filtered_nums)[idx])
    least_common_bit = "1" if bit_counts["1"] < bit_counts["0"] else "0"

    filtered_nums = [num for num in filtered_nums if num[idx] != least_common_bit]

    if len(filtered_nums) == 1:
        break

co2 = bin2dec(filtered_nums[0])

print(f"Life support rating = {oxygen * co2}")
