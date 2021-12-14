import sys

ip = [x for x in sys.stdin]

depth = 0
hor = 0
for i in ip:
    direction, distance = i.split(" ")
    if direction == "forward":
        hor += int(distance)
    elif direction == "down":
        depth += int(distance)
    elif direction == "up":
        depth -= int(distance)

print(depth * hor)


depth = 0
hor = 0
aim = 0
for i in ip:
    direction, distance = i.split(" ")
    if direction == "forward":
        hor += int(distance)
        depth += aim * int(distance)
    elif direction == "down":
        aim += int(distance)
    elif direction == "up":
        aim -= int(distance)

print(depth * hor)
