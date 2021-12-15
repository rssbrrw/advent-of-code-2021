import heapq
import sys
from typing import Optional

ip = [[int(i) for i in line.strip()] for line in sys.stdin.readlines()]


class Node:

    parent: Optional["Node"]
    score: int
    pos: tuple[int, int]

    def __init__(self, parent: Optional["Node"], score: int, pos: tuple[int, int]):
        self.parent = parent
        self.g = score
        self.pos = pos

    def __lt__(self, n: "Node"):
        return True


def get_adjacent(grid: list[list[int]], x: int, y: int):
    return (
        (x1, y1)
        for x1 in range(max(0, x - 1), min(x + 2, len(grid)))
        for y1 in range(max(0, y - 1), min(y + 2, len(grid[0])))
        if (x1, y1) != (x, y) and (x1 == x or y1 == y)
    )


def find_path(grid: list[list[int]]) -> Optional[Node]:

    start = (0, 0)
    end = (len(grid) - 1, len(grid[0]) - 1)
    open_list = [(0, Node(None, 0, start))]
    heapq.heapify(open_list)
    closed_list = set()

    while open_list:
        current = heapq.heappop(open_list)[1]
        closed_list.add(current.pos)

        if current.pos == end:
            return current

        for adj in get_adjacent(grid, current.pos[0], current.pos[1]):
            child = Node(current, current.g + grid[adj[1]][adj[0]], adj)
            if child.pos in closed_list:
                continue

            existing = [n for n in open_list if n[1].pos == child.pos]

            if existing and child.g > existing[0][1].g:
                continue

            h = -(child.pos[0] + child.pos[1])
            heapq.heappush(open_list, (child.g + h, child))
    return None


def full_map(grid: list[list[int]]) -> list[list[int]]:
    new = []
    for _ in range(5):
        for row in grid.copy():
            new.append(row * 5)
    for x in range(0, len(new)):
        for y in range(0, len(new[0])):
            new[x][y] = new[x][y] + (x // len(grid)) + (y // len(grid[0]))
            if new[x][y] > 9:
                new[x][y] -= 9
    return new


def part_one(grid: list[list[int]]) -> int:
    n = find_path(grid)
    return n.g if n else 0


def part_two(grid: list[list[int]]) -> int:
    n = find_path(full_map(grid))
    return n.g if n else 0


print(part_one(ip.copy()))
print(part_two(ip.copy()))
