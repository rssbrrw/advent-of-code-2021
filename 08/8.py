import sys
from typing import List, Tuple

ip = [
    (digits.strip().split(" "), output.strip().split(" "))
    for digits, output in map(lambda l: l.strip().split("|"), sys.stdin.readlines())
]


def taskOne(data: Tuple[List[str]]) -> int:
    return len([d for (_, o) in data for d in o if len(d) in (2, 3, 4, 7)])


def get_mapping(digits: List[str]) -> List[str]:
    mapping = {}
    ambiguous = []
    for digit in digits:
        ds = set(digit)
        match (len(digit)):
            case 2:
                mapping[1] = ds
            case 3:
                mapping[7] = ds
            case 4:
                mapping[4] = ds
            case 7:
                mapping[8] = ds
            case _:
                ambiguous.append(digit)

    for digit in ambiguous:
        ds = set(digit)
        if len(digit) == 5:
            if len(ds - mapping[4]) == 3:
                mapping[2] = ds
            elif len(ds - mapping[7]) == 2:
                mapping[3] = ds
            else:
                mapping[5] = ds
        else:
            if len(ds - mapping[4]) == 2:
                mapping[9] = ds
            elif len(ds - mapping[7]) == 3:
                mapping[0] = ds
            else:
                mapping[6] = ds
    return {"".join(sorted(v)): k for k, v in mapping.items()}


def taskTwo(data: List[Tuple[str]]) -> int:
    """
    Mapping is a mapping from sorted strings of wire
    identifiers to the digit that they correspond to e.g.

    {
        'be': 1,
        'bde' : 7,
        ...
    }

    To decode the output we just sort each word to get the key to look up in the mapping

    """
    return sum(
        int(
            "".join(
                str(get_mapping(line[0])["".join(sorted(digit))]) for digit in line[1]
            )
        )
        for line in data
    )


print(taskOne(ip))
print(taskTwo(ip))
