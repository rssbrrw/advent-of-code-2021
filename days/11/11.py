import sys
from functools import cached_property
from itertools import count
from typing import Iterator, List, Optional, Tuple

ip = [[int(i) for i in line.strip()] for line in sys.stdin.readlines()]


class Octopus:

    MAX_ENERGY = 10

    energy: int
    flashed: bool = False

    def __init__(self, energy: int):
        self.energy = energy

    def __repr__(self):
        return f"{self.energy}"

    def charge(self) -> bool:
        """
        Increment the energy level of this octopus by 1
        return True if the increase caused the octopus to flash, False otherwise
        """
        prev = self.energy
        self.energy += 1
        if prev < self.MAX_ENERGY <= self.energy:
            self.flash()
            return True
        return False

    def flash(self) -> None:
        self.flashed = True

    def reset(self) -> bool:
        if self.flashed:
            self.flashed = False
            self.energy = 0
            return True
        return False


class Consortium:
    """
    Group of octopi partaking in octopus business
    """

    octopi: List[List[Octopus]]

    def __init__(self, octopi: List[List[Octopus]]):
        self.octopi = octopi

    def __repr__(self):
        return "\n".join("".join(str(octo) for octo in row) for row in self.octopi)

    @cached_property
    def population(self) -> int:
        return len(self.octopi) * len(self.octopi[0])

    def step(self, count: int = 1) -> int:
        """
        Charge all octopi count number of times
        Return the total number of flashes that happen in all steps
        """
        for x, row in enumerate(self.octopi):
            for y, octo in enumerate(row):
                if octo.charge():
                    self.cascade_flash(x, y)

        flashes = len([octo for row in self.octopi for octo in row if octo.reset()])
        return flashes if count == 1 else flashes + self.step(count - 1)

    def cascade_flash(self, x: int, y: int) -> None:
        for (x2, y2) in get_adjacent_coords(x, y, max_=len(self.octopi)):
            if self.octopi[x2][y2].charge():
                self.cascade_flash(x2, y2)


def get_adjacent_coords(x: int, y: int, max_: int) -> Iterator[Tuple[int, int]]:
    return (
        (x1, y1)
        for x1 in range(max(0, x - 1), min(x + 2, max_))
        for y1 in range(max(0, y - 1), min(y + 2, max_))
        if (x1, y1) != (x, y)
    )


def part_one(data: List[List[int]]) -> int:
    cons = Consortium([[Octopus(i) for i in line] for line in data])
    return cons.step(100)


def part_two(data: List[List[int]]) -> Optional[int]:
    cons = Consortium([[Octopus(i) for i in line] for line in data])
    for i in count(start=1):
        if cons.step() == cons.population:
            return i
    return None


print(part_one(ip))
print(part_two(ip))
