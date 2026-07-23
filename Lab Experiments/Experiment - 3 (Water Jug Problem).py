from collections import deque

# Capacities of the two jugs
jug1 = 4
jug2 = 1

# Target amount of water
target = 2


def water_jug():
    queue = deque()
    visited = set()

    # Initial state (0,0)
    queue.append((0, 0, []))

    while queue:

        x, y, path = queue.popleft()

        if (x, y) in visited:
            continue

        visited.add((x, y))

        path = path + [(x, y)]

        # Goal condition
        if x == target or y == target:
            return path

        # Possible operations
        next_states = [

            (jug1, y),          # Fill Jug1
            (x, jug2),          # Fill Jug2
            (0, y),             # Empty Jug1
            (x, 0),             # Empty Jug2

            # Pour Jug1 -> Jug2
            (x - min(x, jug2 - y),
             y + min(x, jug2 - y)),

            # Pour Jug2 -> Jug1
            (x + min(y, jug1 - x),
             y - min(y, jug1 - x))
        ]

        for state in next_states:
            if state not in visited:
                queue.append((state[0], state[1], path))

    return None


solution = water_jug()

if solution:
    print("Solution Found\n")
    step = 0
    for state in solution:
        print("Step", step, ":", state)
        step += 1
else:
    print("No Solution")

