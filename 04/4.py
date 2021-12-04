import re
import sys
from typing import List


def transpose(matrix: List[List]) -> List[List]:
    return [*zip(*matrix)]


class CardNumber:

    value: int
    marked: bool = False

    def __init__(self, value: int):
        self.value = value

    def __str__(self):
        s = f"{self.value}{'*' if self.marked else ''}"
        return f"{s:<4}"


class BingoCard:

    numbers: List[List[dict]]

    def __str__(self):
        rows = [" ".join(map(str, row)) for row in self.numbers]
        return "\n".join(rows)

    def __init__(self, numbers: List[List[int]]):
        self.numbers = [[CardNumber(int(number)) for number in row] for row in numbers]
        self.size = len(self.numbers)

    def mark(self, n: int) -> None:
        for row in self.numbers:
            for number in row:
                if number.value == n:
                    number.marked = True

    @property
    def score(self) -> int:
        return sum(n.value for row in self.numbers for n in row if not n.marked)

    def is_winner(self) -> bool:
        return (
            # Horizontal
            any(all(n.marked for n in numbers) for numbers in self.numbers)
            # Vertical
            or any(
                all(n.marked for n in numbers) for numbers in transpose(self.numbers)
            )
        )


draw = (int(n) for n in sys.stdin.readline().split(","))
sys.stdin.readline()
cards = [
    BingoCard([re.split(r"\s+", line.strip()) for line in grid.split("\n")])
    for grid in sys.stdin.read().strip().split("\n\n")
]
total_cards = len(cards)

for number in draw:
    winners = []
    for card in cards:
        card.mark(number)
        if card.is_winner():
            winners.append(card)

    for winner in winners:
        if len(cards) in (1, total_cards):
            print(winner.score * number)
        cards.remove(winner)
