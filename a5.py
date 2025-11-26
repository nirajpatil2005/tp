import sys

# Constants
HUMAN = 'O'
AI = 'X'
EMPTY = '_'

def print_board(board):
    print("\n")
    for row in board:
        for cell in row:
            print(f"{cell} ", end="")
        print()
    print("\n")

def is_moves_left(board):
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return True
    return False

def evaluate(b):
    """
    Returns +10 if AI wins, -10 if Human wins, 0 otherwise.
    """
    # Check rows
    for row in range(3):
        if b[row][0] == b[row][1] and b[row][1] == b[row][2]:
            if b[row][0] == AI:
                return 10
            elif b[row][0] == HUMAN:
                return -10

    # Check columns
    for col in range(3):
        if b[0][col] == b[1][col] and b[1][col] == b[2][col]:
            if b[0][col] == AI:
                return 10
            elif b[0][col] == HUMAN:
                return -10

    # Check diagonals
    if b[0][0] == b[1][1] and b[1][1] == b[2][2]:
        if b[0][0] == AI:
            return 10
        elif b[0][0] == HUMAN:
            return -10

    if b[0][2] == b[1][1] and b[1][1] == b[2][0]:
        if b[0][2] == AI:
            return 10
        elif b[0][2] == HUMAN:
            return -10

    return 0

def minimax(board, depth, is_max):
    score = evaluate(board)

    # Terminal conditions
    # If AI wins
    if score == 10:
        return score - depth
    # If Human wins
    if score == -10:
        return score + depth
    # If tie
    if not is_moves_left(board):
        return 0

    if is_max:
        best = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = AI
                    best = max(best, minimax(board, depth + 1, False))
                    board[i][j] = EMPTY
        return best
    else:
        best = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = HUMAN
                    best = min(best, minimax(board, depth + 1, True))
                    board[i][j] = EMPTY
        return best

def find_best_move(board):
    best_val = float('-inf')
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                move_val = minimax(board, 0, False)
                board[i][j] = EMPTY

                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    return best_move

def is_game_over(board):
    score = evaluate(board)
    if score == 10:
        print_board(board)
        print("AI wins! \n")
        return True
    elif score == -10:
        print_board(board)
        print("You win! \n")
        return True
    elif not is_moves_left(board):
        print_board(board)
        print("It's a draw! \n")
        return True
    return False

def main():
    board = [[EMPTY for _ in range(3)] for _ in range(3)]
    
    print("Welcome to Tic-Tac-Toe using Minimax!")
    print("You are 'O' and AI is 'X'")
    print("Enter your move as row and column (0-2)")

    print_board(board)

    while True:
        # Human Move Loop
        valid_move = False
        while not valid_move:
            try:
                user_input = input("Your Move (row col): ").split()
                if len(user_input) != 2:
                    print("Please enter two numbers separated by space.")
                    continue
                    
                row, col = map(int, user_input)

                if 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] == EMPTY:
                    board[row][col] = HUMAN
                    valid_move = True
                else:
                    print("Invalid move! Try again.")
            except ValueError:
                print("Invalid input. Please enter integers.")

        print_board(board)
        if is_game_over(board):
            break

        # AI Move
        print("AI is thinking...")
        best_move_row, best_move_col = find_best_move(board)
        
        # Check valid AI move (should always be valid unless board full)
        if best_move_row != -1 and best_move_col != -1:
            board[best_move_row][best_move_col] = AI
            print_board(board)
            if is_game_over(board):
                break
        else:
            # Fallback for draw detection in case loop logic misses it
            if is_game_over(board):
                break

    print("Game Over. Thanks for playing!")

if __name__ == "__main__":
    main()