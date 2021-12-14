import sys
from functools import reduce
from typing import List, Optional, Set, Tuple

ip = [[int(x) for x in row.strip()] for row in sys.stdin.readlines()]


def get_safe_points(data: List[List[int]]):
    safe_points = []
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            comparators = set()
            if x > 0:
                comparators.add(row[x - 1])
            if x < len(row) - 1:
                comparators.add(row[x + 1])
            if y > 0:
                comparators.add(data[y - 1][x])
            if y < len(data) - 1:
                comparators.add(data[y + 1][x])

            if all(cell < comp for comp in comparators):
                safe_points.append((cell, (y, x)))
    return safe_points


def part_one(data: List[List[int]]) -> int:
    return sum(p + 1 for p, _ in get_safe_points(data))


known_points = set()


def get_basin(
    data: List[List[int]],
    y: int,
    x: int,
    current_basin: Optional[Set[Tuple[int, int]]] = None,
) -> Set[Tuple[int, int]]:
    """
    For each low point
    Search outwards in the row and column until we hit a 9
    Recursively do the same for all points we find
    """

    current_basin = current_basin or set()
    new_basin = set(current_basin)
    for i in range(x, -1, -1):
        if data[y][i] == 9:
            break
        new_basin.add((y, i))
    for i in range(x, len(data[y])):
        if data[y][i] == 9:
            break
        new_basin.add((y, i))
    for i in range(y, -1, -1):
        if data[i][x] == 9:
            break
        new_basin.add((i, x))
    for i in range(y, len(data)):
        if data[i][x] == 9:
            break
        new_basin.add((i, x))

    if new_basin == current_basin or (y, x) in known_points:
        return set()
    else:
        known_points.add((y, x))
        return new_basin.union(
            *[get_basin(data, y, x, new_basin | current_basin) for y, x in new_basin]
        )


def part_two(data: List[List[int]]) -> int:
    safe_points = get_safe_points(data)
    basins = [get_basin(data, y, x) for (_, (y, x)) in safe_points]
    return reduce(lambda x, y: x * y, sorted([len(basin) for basin in basins])[-3:], 1)


print(part_one(ip))
print(part_two(ip))
