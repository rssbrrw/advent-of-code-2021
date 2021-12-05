import sys
from collections import defaultdict
from itertools import cycle
from typing import DefaultDict, List, NewType, Tuple

Map = NewType("Map", DefaultDict[int, DefaultDict[int, int]])
Point = NewType("Point", Tuple[int, int])


def parse_input(ip: str) -> List[Tuple[Point, Point]]:
    pairs = []
    for line in ip.strip().split("\n"):
        start_str, end_str = line.split(" -> ")
        start = tuple(map(int, start_str.split(",")))
        end = tuple(map(int, end_str.split(",")))
        pairs.append((start, end))
    return pairs


def draw_line(
    grid: Map,
    p1: Point,
    p2: Point,
    include_diagonals: bool = True,
) -> None:
    (x1, y1), (x2, y2) = (p1, p2) if p1[0] < p2[0] else (p2, p1)

    # Add/subtract 1 from end of range and set direction
    # depending on whether y is going up or down
    y_step = y2 > y1 or -1
    y_end = y2 + y_step

    x_range = range(x1, x2 + 1)
    y_range = range(y1, y_end, y_step)

    # For horizontal/vertical lines, repeat the shared coordinate
    if x1 == x2:
        x_range = cycle(x_range)
    elif y1 == y2:
        y_range = cycle(y_range)
    elif not include_diagonals:
        return

    for (x, y) in zip(x_range, y_range):
        grid[x][y] += 1


def count_dangerous_points(grid: Map) -> int:
    return sum(y > 1 for x in grid.values() for y in x.values())


def map_vents(pairs: List[Tuple[Point, Point]], include_diagonals=True):
    vent_counts: Map = defaultdict(lambda: defaultdict(lambda: 0))
    for pair in pairs:
        draw_line(vent_counts, pair[0], pair[1], include_diagonals)
    return vent_counts


pairs = parse_input(sys.stdin.read())

# Part one
vent_map = map_vents(pairs, include_diagonals=False)
print(count_dangerous_points(vent_map))

# Part two:
# Consider not working out the horizontal/vertical lines twice
vent_map = map_vents(pairs)
print(count_dangerous_points(vent_map))
