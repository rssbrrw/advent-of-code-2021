import sys

[(min_x, max_x), (min_y, max_y)] = list(
    map(
        lambda w: (int(w[2:].split("..")[0]), int(w[2:].split("..")[1])),
        sys.stdin.read().strip("\n").replace(",", "").split(" ")[-2:],
    )
)


def step(
    current: tuple[int, int], x_vel: int, y_vel: int
) -> tuple[tuple[int, int], int, int]:
    next_x = current[0] + x_vel
    next_y = current[1] + y_vel
    new_x_vel = x_vel - 1 if x_vel > 0 else min(0, x_vel + 1)
    new_y_vel = y_vel - 1
    return (next_x, next_y), new_x_vel, new_y_vel


global_max_y = 0
vels = set()
for start_y_vel in range(1000, min_y - 1, -1):
    for start_x_vel in range(max_x + 1, 0, -1):
        pos = 0, 0
        local_max_y = 0
        x_vel, y_vel = start_x_vel, start_y_vel
        while pos[0] < max_x and pos[1] > min_y:
            pos, x_vel, y_vel = step(pos, x_vel, y_vel)
            if pos[1] > local_max_y:
                local_max_y = pos[1]
            if (min_x <= pos[0] <= max_x) and (min_y <= pos[1] <= max_y):
                vels.add((start_x_vel, start_y_vel))
                print(start_x_vel, start_y_vel)
                if local_max_y > global_max_y:
                    global_max_y = local_max_y


print(global_max_y)
print(len(vels))
