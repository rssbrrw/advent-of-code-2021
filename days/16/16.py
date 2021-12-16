import sys
from dataclasses import dataclass
from functools import reduce
from itertools import takewhile
from operator import mul

from boltons.iterutils import chunked_iter

BIT_MAP = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def hex2bin(digits: str) -> str:
    return "".join(BIT_MAP[d] for d in digits)


def bin2dec(digits: str) -> int:
    return int(digits, 2)


def bin2hex(digits: str) -> str:
    return hex(bin2dec(digits))[2:].upper()


@dataclass
class Packet:
    version: int

    def get_version(self):
        return self.version


@dataclass
class Literal(Packet):
    value: int

    def get_value(self):
        return self.value


@dataclass
class Operator(Packet):
    sub: list[Packet]
    type: int

    def get_version(self):
        return self.version + sum(p.get_version() for p in self.sub)

    def get_value(self):
        if self.type == 0:
            return sum(p.get_value() for p in self.sub)
        elif self.type == 1:
            return reduce((mul), (p.get_value() for p in self.sub))
        elif self.type == 2:
            return min(p.get_value() for p in self.sub)
        elif self.type == 3:
            return max(p.get_value() for p in self.sub)
        elif self.type == 5:
            return self.sub[0].get_value() > self.sub[1].get_value()
        elif self.type == 6:
            return self.sub[0].get_value() < self.sub[1].get_value()
        elif self.type == 7:
            return self.sub[0].get_value() == self.sub[1].get_value()


class PacketReader:
    @classmethod
    def read(
        cls,
        binary: str,
        max_: int = None,
        packets: list[Packet] = None,
        length: int = 0,
    ) -> tuple[list[Packet], int]:
        packets = packets or []
        if len(binary) == 0 or all(b == "0" for b in binary):
            return packets, length
        p_version = bin2dec(binary[:3])
        p_type = bin2dec(binary[3:6])
        if p_type == 4:
            packet, bit_length = cls.read_literal(p_version, binary[6:])
        else:
            packet, bit_length = cls.read_operator(p_version, p_type, binary[6:])

        if max_ is None:
            return cls.read(
                binary[6 + bit_length :],
                packets=packets + [packet],
                length=6 + bit_length + length,
            )
        elif max_ > 1:
            return cls.read(
                binary[6 + bit_length :],
                packets=packets + [packet],
                max_=max_ - 1,
                length=6 + bit_length + length,
            )
        else:
            return packets + [packet], 6 + bit_length + length

    @classmethod
    def read_operator(
        cls, version: int, type_: int, binary: str
    ) -> tuple[Operator, int]:
        length_id = binary[0]
        if length_id == "0":
            bit_length = bin2dec(binary[1:16])
            p = Operator(
                version=version,
                type=type_,
                sub=cls.read(binary[16 : 16 + bit_length])[0],
            )
            return p, bit_length + 16
        else:
            num_packets = bin2dec(binary[1:12])
            sub, bit_length = cls.read(binary[12:], max_=num_packets)
            p = Operator(version=version, type=type_, sub=sub)
            return p, bit_length + 12

    @staticmethod
    def read_literal(version: int, binary: str) -> tuple[Literal, int]:
        num = ""
        length = 0
        for bit in takewhile(lambda c: c[0] == "1", chunked_iter(binary, 5)):
            num += bit[1:]
            length += 5
        num += binary[length + 1 : length + 5]
        return Literal(version=version, value=bin2dec(num)), length + 5


ip = hex2bin(sys.stdin.read().strip())


def part_one(data: str) -> int:
    packets = PacketReader.read(data)[0]
    return sum(p.get_version() for p in packets)


def part_two(data: str) -> int:
    packets = PacketReader.read(data)[0]
    return packets[0].get_value()


print(part_one(ip))
print(part_two(ip))
