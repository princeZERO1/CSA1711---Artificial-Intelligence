# Number of Queens (Change this value: 4, 5, 6, 8...)
N = 8

# Create an N x N board
board = [[0 for i in range(N)] for j in range(N)]


# Function to print Matrix and Chessboard
def print_board():

    # Matrix Representation
    print("\nMatrix Representation:\n")

    for row in board:
        print(row)

    # Chessboard Representation
    print("\nChessboard Representation:\n")

    print("    A  B  C  D  E  F  G  H")

    for i in range(8):

        print(i + 1, end="  ")

        for j in range(8):

            if i < N and j < N:

                if board[i][j] == 1:
                    print("Q ", end=" ")
                else:
                    print(". ", end=" ")

            else:
                print(". ", end=" ")

        print()

# Check whether queen placement is safe
def is_safe(row, col):

    # Check left side of current row
    for i in range(col):
        if board[row][i] == 1:
            return False

    # Check upper-left diagonal
    i = row
    j = col
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1

    # Check lower-left diagonal
    i = row
    j = col
    while i < N and j >= 0:
        if board[i][j] == 1:
            return False
        i += 1
        j -= 1

    return True


# Backtracking function
def solve(col):

    # If all queens are placed
    if col >= N:
        return True

    # Try every row
    for row in range(N):

        if is_safe(row, col):

            board[row][col] = 1

            if solve(col + 1):
                return True

            # Backtrack
            board[row][col] = 0

    return False


# Main Program
if solve(0):
    print("Solution Found!")
    print_board()
else:
    print("No Solution")
