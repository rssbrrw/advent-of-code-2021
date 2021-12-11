import sys
import time
from functools import cached_property
from itertools import count
from typing import Iterator, List, Optional, Tuple

import click
import pygame

SPEED = 0.1
FLASH_TTL = 20


class Octopus:

    MAX_ENERGY = 10

    energy: int
    flashed: bool = False

    def __init__(self, energy: int):
        self.energy = energy

    def __repr__(self):
        return f"{self.energy}"

    @property
    def alpha(self) -> int:
        return min(self.energy * (255 // self.MAX_ENERGY), 255)

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
    _window: Optional[pygame.Surface] = None
    _flashes: Optional[List[dict]] = None

    def __init__(self, octopi: List[List[Octopus]], window=None):
        self.octopi = octopi
        self._window = window
        self._flashes = []

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

        self.render()
        flashes = len([octo for row in self.octopi for octo in row if octo.reset()])
        return flashes if count == 1 else flashes + self.step(count - 1)

    def cascade_flash(self, x: int, y: int) -> None:
        for (x2, y2) in get_adjacent_coords(x, y, max_=len(self.octopi)):
            if self.octopi[x2][y2].charge():
                self.cascade_flash(x2, y2)

    def render(self) -> None:
        if self._window is None:
            return
        self._window.fill((0, 0, 0))
        for x, row in enumerate(self.octopi):
            for y, octo in enumerate(row):
                pygame.gfxdraw.aacircle(
                    self._window,
                    (x + 1) * 50,
                    (y + 1) * 50,
                    20,
                    (255, 255, 0, octo.alpha),
                )
                pygame.gfxdraw.filled_circle(
                    self._window,
                    (x + 1) * 50,
                    (y + 1) * 50,
                    20,
                    (255, 255, 0, octo.alpha),
                )
                if octo.flashed:
                    self._flashes.append(
                        {
                            "pos": (
                                (x + 1) * 50,
                                (y + 1) * 50,
                                (y + 1) * 50,
                                (y + 1) * 50,
                            ),
                            "ttl": FLASH_TTL,
                        }
                    )
        for flash in self._flashes:
            pygame.gfxdraw.aacircle(
                self._window,
                flash["pos"][0],
                flash["pos"][1],
                20 + (20 - flash["ttl"]),
                (255, 255, 255, min(50, flash["ttl"] * 10)),
            )
            pygame.gfxdraw.filled_circle(
                self._window,
                flash["pos"][0],
                flash["pos"][1],
                20 + (20 - flash["ttl"]),
                (255, 255, 255, min(50, flash["ttl"] * 10)),
            )
            flash["ttl"] -= 1
            if flash["ttl"] == 0:
                self._flashes.remove(flash)
        pygame.event.get()
        pygame.display.update()
        time.sleep(SPEED)


def get_adjacent_coords(x: int, y: int, max_: int) -> Iterator[Tuple[int, int]]:
    return (
        (x1, y1)
        for x1 in range(max(0, x - 1), min(x + 2, max_))
        for y1 in range(max(0, y - 1), min(y + 2, max_))
        if (x1, y1) != (x, y)
    )


def init_window():
    window = pygame.display.set_mode((550, 550))
    window.fill((0, 0, 0))
    pygame.display.set_caption("Dumbo Octopus")
    return window


def part_one(data: List[List[int]], window=None) -> int:
    return Consortium(
        [[Octopus(i) for i in line] for line in data], window=window
    ).step(100)


def part_two(data: List[List[int]], window=None) -> Optional[int]:
    cons = Consortium([[Octopus(i) for i in line] for line in data], window)
    for i in count(start=1):
        if cons.step() == cons.population:
            return i
    return None


@click.command()
@click.option("--visualise", is_flag=True, default=False)
def main(visualise: bool):
    ip = [[int(i) for i in line.strip()] for line in sys.stdin.readlines()]
    window = init_window() if visualise else None
    print(part_one(ip, window))
    print(part_two(ip, window))


if __name__ == "__main__":
    main()
