import sys
from collections import defaultdict
from typing import DefaultDict, Dict

start = sys.stdin.readline().strip()
rules: Dict[str, str] = {
    w[0]: w[1]
    for w in map(
        lambda l: l.strip().split(" -> "), sys.stdin.read().strip().split("\n")
    )
}


def insert(start: str, rules: Dict, rounds: int) -> int:
    pair_counts: DefaultDict = defaultdict(int)
    for p1, p2 in zip(start, start[1:]):
        pair_counts[p1 + p2] += 1

    for _ in range(rounds):
        for (first, second), count in pair_counts.copy().items():
            pair_counts[first + second] -= count
            pair_counts[first + rules[first + second]] += count
            pair_counts[rules[first + second] + second] += count

    char_counts = defaultdict(int, {start[0]: 1})
    for (_, second), count in pair_counts.items():
        char_counts[second] += count
    return max(char_counts.values()) - min(char_counts.values())


def part_one(start, rules):
    return insert(start, rules, 10)


def part_two(start, rules):
    return insert(start, rules, 40)


print(part_one(start, rules))
print(part_two(start, rules))
