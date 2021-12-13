import sys
from functools import reduce
from typing import NewType, Set, Tuple

ip = sys.stdin.read().strip()
coord_str, fold_str = ip.split("\n\n")
coords = set(
    (int(w[0]), int(w[1])) for w in map(lambda l: l.split(","), coord_str.split("\n"))
)
folds = [
    (w[0], int(w[1]))
    for w in map(lambda l: l.split(" ")[-1].split("="), fold_str.split("\n"))
]

Coord = NewType("Coord", Tuple[int, int])

paper = set(coords)


def fold(coords: Set[Coord], fold_: Tuple[str, int]) -> Set[Coord]:
    if fold_[0] == "y":
        to_remove = {c for c in coords if c[1] > fold_[1]}
        to_add = {Coord((c[0], fold_[1] - (c[1] - fold_[1]))) for c in to_remove}
    else:
        to_remove = {c for c in coords if c[0] > fold_[1]}
        to_add = {Coord((fold_[1] - (c[0] - fold_[1]), c[1])) for c in to_remove}
    return (coords - to_remove) | to_add


def part_one(coords, folds):
    return len(fold(coords, folds[0]))


def part_two(coords, folds):
    return reduce(fold, folds, coords)


def print_paper(coords):
    height = max(c[1] for c in coords)
    width = max(c[0] for c in coords)
    for y in range(height + 1):
        print("".join(["#" if (x, y) in coords else " " for x in range(width + 1)]))


print(part_one(coords, folds))
print_paper(part_two(coords, folds))
