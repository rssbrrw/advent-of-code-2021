from functools import cache
from typing import Callable, List

crabs = list(map(int, input().split(",")))


@cache
def triangle(n: int) -> int:
    return sum(range(n + 1))


def min_cost(crabs: List[int], cost_fn: Callable) -> int:
    return min(sum(cost_fn(crab, i) for crab in crabs) for i in range(max(crabs)))


def task_one(crabs: List[int]) -> int:
    return min_cost(crabs, lambda crab, i: abs(crab - i))


def task_two(crabs: List[int]) -> int:
    return min_cost(crabs, lambda crab, i: triangle(abs(crab - i)))


print(task_one(crabs))
print(task_two(crabs))
