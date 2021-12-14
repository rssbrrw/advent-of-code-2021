import sys

from boltons.iterutils import pairwise, windowed

ip = [int(x) for x in sys.stdin]

print(sum(y > x for x, y in pairwise(ip)))
print(sum(sum(ys) > sum(xs) for xs, ys in pairwise(windowed(ip, 3))))
