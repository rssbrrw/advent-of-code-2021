import json
import sys
from math import ceil
from typing import Optional, Union


class Node:

    left: Union[int, "Node"]
    right: Union[int, "Node"]
    parent: Optional["Node"] = None
    depth: int = 0

    def __init__(
        self,
        left: Union[int, list, "Node"],
        right: Union[int, list, "Node"],
        parent: Optional["Node"] = None,
    ):
        if parent:
            self.parent = parent
            self.depth = parent.depth + 1
        if type(left) in (int, Node):
            if type(left) == Node:
                left.parent = self
                left.depth = self.depth + 1
            self.left = left
        else:
            self.left = Node(*left, parent=self)

        if type(right) in (int, Node):
            if type(right) == Node:
                right.parent = self
                right.depth = self.depth + 1
            self.right = right
        else:
            self.right = Node(*right, parent=self)

    def __repr__(self):
        return f"[{self.left},{self.right}]"

    def __rshift__(self, val: int) -> "Node":
        if isinstance(self.right, int):
            return Node(self.left, self.right + val, parent=self.parent)
        else:
            return Node(self.left, self.right >> val, parent=self.parent)

    def __lshift__(self, val: int) -> "Node":
        if isinstance(self.left, int):
            return Node(self.left + val, self.right, parent=self.parent)
        else:
            return Node(self.left << val, self.right, parent=self.parent)

    @property
    def magnitude(self):
        return 3 * self.left_mag + 2 * self.right_mag

    @property
    def left_mag(self):
        return self.left if isinstance(self.left, int) else self.left.magnitude

    @property
    def right_mag(self):
        return self.right if isinstance(self.right, int) else self.right.magnitude

    def explode(self):
        # Does my left need to be exploded?
        if self.depth > 2 and isinstance(self.left, Node):
            to_shift = self.parent
            prev = self
            while to_shift.left is prev and to_shift.parent:
                prev = to_shift
                to_shift = to_shift.parent
            if to_shift.left != prev:
                if isinstance(to_shift.left, int):
                    to_shift.left += self.left.left
                else:
                    to_shift.left >>= self.left.left
            if isinstance(self.right, int):
                self.right += self.left.right
            else:
                self.right <<= self.left.right
            self.left = 0
            return True
        elif isinstance(self.left, Node) and self.left.explode():
            return True
        # Else does my right need to be exploded?
        elif self.depth > 2 and isinstance(self.right, Node):
            to_shift = self.parent
            prev = self
            while to_shift.right is prev and to_shift.parent:
                prev = to_shift
                to_shift = to_shift.parent
            if to_shift.right != prev:
                if isinstance(to_shift.right, int):
                    to_shift.right += self.right.right
                else:
                    to_shift.right <<= self.right.right
            if isinstance(self.left, int):
                self.left += self.right.left
            else:
                self.left >>= self.right.left
            self.right = 0
            return True
        elif isinstance(self.right, Node) and self.right.explode():
            return True
        return False

    def split(self):
        # Else Does my left need to be split?
        if isinstance(self.left, int) and self.left > 9:
            self.left = Node(self.left // 2, int(ceil(self.left / 2)), parent=self)
            return True
        elif isinstance(self.left, Node) and self.left.split():
            return True
        # Else does my right need to be split?
        elif isinstance(self.right, int) and self.right > 9:
            self.right = Node(self.right // 2, int(ceil(self.right / 2)), parent=self)
            return True
        elif isinstance(self.right, Node) and self.right.split():
            return True
        return False

    def reduce(self):
        while self.explode() or self.split():
            pass
        return self


numbers = [json.loads(line.strip()) for line in sys.stdin.readlines()]


def part_one(numbers):
    it = iter(numbers)
    current = Node(next(it), next(it))
    current.reduce()
    while nxt := next(it, None):
        current = Node(json.loads(str(current)), nxt)
        current.reduce()
    return current.magnitude


def part_two(numbers):
    max_ = 0
    for x in numbers:
        for y in numbers:
            if x == y:
                continue
            candidate = Node(x, y).reduce().magnitude
            if candidate > max_:
                max_ = candidate
            candidate = Node(y, x).reduce().magnitude
            if candidate > max_:
                max_ = candidate
    return max_


print(part_one(numbers.copy()))
print(part_two(numbers.copy()))
