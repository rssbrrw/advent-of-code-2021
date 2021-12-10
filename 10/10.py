import sys
from collections import defaultdict
from functools import reduce
from typing import DefaultDict, List, Optional, Tuple

ip = [line.strip() for line in sys.stdin.readlines()]

BRACKET_MAP = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}

CORRUPTED_SCORES = {
    "(": 3,
    "[": 57,
    "{": 1197,
    "<": 25137,
}


def get_error(line: str) -> Tuple[Optional[str], List[str]]:
    stack = []
    for char in line:
        if char in BRACKET_MAP.values():
            stack.append(char)
        elif char in BRACKET_MAP:
            if stack.pop() != BRACKET_MAP[char]:
                return char, stack
    return None, stack


def get_autocomplete_score(leftovers: List[str]) -> int:
    return reduce(lambda score, c: 5 * score + "_([{<".index(c), reversed(leftovers), 0)


def part_one(data: List[str]) -> int:
    counts: DefaultDict[Optional[str], int] = defaultdict(int)
    for line in data:
        counts[get_error(line)[0]] += 1
    return sum(
        counts[char] * CORRUPTED_SCORES[BRACKET_MAP[char]]
        for char in BRACKET_MAP.keys()
    )


def part_two(data: List[str]) -> int:
    incompletes = filter(lambda x: x[0] is None, map(get_error, data))
    scores = [get_autocomplete_score(x[1]) for x in incompletes]
    return sorted(scores)[len(scores) // 2]


print(part_one(ip))
print(part_two(ip))
