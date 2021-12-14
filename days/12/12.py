import sys
from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple

pairs: List[Tuple[str, ...]] = [
    tuple(line.strip().split("-")) for line in sys.stdin.readlines()
]

START, END = "start", "end"


def map_caves(pairs: List[Tuple[str, ...]]) -> Dict[str, Set[str]]:
    cave_map = defaultdict(set)
    for n1, n2 in pairs:
        if n1 == END or n2 == START:
            cave_map[n2].add(n1)
        elif n1 == START or n2 == END:
            cave_map[n1].add(n2)
        else:
            cave_map[n1].add(n2)
            cave_map[n2].add(n1)

    return cave_map


def count_paths(pairs: List[Tuple[str, ...]], visit_small_twice: bool = False) -> int:
    cave_map = map_caves(pairs)
    paths: Dict[str, bool] = {}
    visited = [START]
    available = set(cave_map) | {END}
    # If we pop START off the visited stack, we have exhausted our options
    while visited:
        current = visited[-1]
        for destination in cave_map[current]:
            if destination not in available:
                # This is a small cave we've already visited
                continue
            if "".join(visited + [destination]) in paths:
                # This is a big cave all of whose paths we've explored
                continue
            if destination.islower():
                if visit_small_twice:
                    small_cave_counts = Counter(visited)
                    # We can only visit one small cave twice, and we did already
                    if any(
                        v > 1
                        for k, v in small_cave_counts.items()
                        if k.islower() and small_cave_counts[destination] > 0
                    ):
                        continue
                else:
                    available.remove(destination)
            current = destination
            visited.append(current)
            break
        else:
            # No available cave, store this path and backtrack
            paths["".join(visited)] = True
            available.add(visited.pop())
    return len([path for path in paths if path.endswith(END)])


def part_one(pairs: List[Tuple[str, ...]]) -> int:
    return count_paths(pairs)


def part_two(pairs: List[Tuple[str, ...]]) -> int:
    return count_paths(pairs, True)


print(part_one(pairs))
print(part_two(pairs))
