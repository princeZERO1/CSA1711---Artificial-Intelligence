from collections import deque

# Goal state
goal = [1, 2, 4,
        3, 5, 6,
        0, 8, 7]

# Initial state
start = [5, 4, 7,
         6, 1, 8,
         0, 3, 2]


# Function to print the puzzle
def print_board(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()


# Function to find blank tile (0)
def find_zero(state):
    return state.index(0)


# Generate all possible moves
def get_neighbors(state):

    neighbors = []

    zero = find_zero(state)

    # Row and column of blank tile
    row = zero // 3
    col = zero % 3

    # Possible movements
    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    for dr, dc in directions:

        new_row = row + dr
        new_col = col + dc

        # Check boundary
        if 0 <= new_row < 3 and 0 <= new_col < 3:

            new_zero = new_row * 3 + new_col

            new_state = state[:]

            # Swap blank with adjacent tile
            new_state[zero], new_state[new_zero] = new_state[new_zero], new_state[zero]

            neighbors.append(new_state)

    return neighbors


# Breadth First Search
def bfs(start):

    queue = deque()

    queue.append((start, []))

    visited = set()

    visited.add(tuple(start))

    while queue:

        current, path = queue.popleft()

        if current == goal:
            return path + [current]

        for neighbor in get_neighbors(current):

            if tuple(neighbor) not in visited:

                visited.add(tuple(neighbor))

                queue.append((neighbor, path + [current]))

    return None
 


# Solve puzzle
solution = bfs(start)

# Print solution
if solution:

    print("Solution Found!\n")

    step = 0

    for state in solution:

        print("Step", step)

        print_board(state)

        step += 1

else:

    print("No Solution")

