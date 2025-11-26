import sys

# Constants
N = 8

def print_board(board):
    """
    Prints the chessboard with 'Q' and '.'
    """
    for row in range(N):
        line = ""
        for col in range(N):
            if board[row] == col:
                line += "Q "
            else:
                line += ". "
        print(line)
    print()

def is_safe(board, row, col):
    """
    Check if a queen can be placed at board[row] = col
    """
    for i in range(row):
        # Check if same column or same diagonal
        # diagonal check: |x1 - x2| == |y1 - y2|
        if board[i] == col or abs(board[i] - col) == abs(i - row):
            return False
    return True

def solve_n_queens(board, row):
    """
    Backtracking function to solve 8-Queens
    Returns True if at least one solution is found
    """
    # Base case: If all queens are placed
    if row == N:
        print_board(board)
        return True

    found_solution = False
    
    for col in range(N):
        if is_safe(board, row, col):
            board[row] = col  # Place queen
            
            # Recurse and accumulate result (matches C++ |= operator logic)
            if solve_n_queens(board, row + 1):
                found_solution = True
            
            board[row] = -1   # Backtrack
            
    return found_solution

def main():
    # board[i] = column of queen in row i
    # Initialize with -1 to indicate no queen placed
    board = [-1] * N
    
    if not solve_n_queens(board, 0):
        print("No solution exists.")

if __name__ == "__main__":
    main()