#include <iostream>
#include <vector>
#include <limits>
using namespace std;

const char HUMAN = 'O';
const char AI = 'X';
const char EMPTY = '_';

// Function to print the board
void printBoard(const vector<vector<char>>& board) {
    cout << "\n";
    for (auto& row : board) {
        for (auto& cell : row)
            cout << cell << " ";
        cout << endl;
    }
    cout << "\n";
}

// Check if moves are left on the board
bool isMovesLeft(const vector<vector<char>>& board) {
    for (auto& row : board)
        for (auto& cell : row)
            if (cell == EMPTY) return true;
    return false;
}

// Evaluate the board (return +10, -10, or 0)
int evaluate(const vector<vector<char>>& b) {
    // Check rows
    for (int row = 0; row < 3; row++) {
        if (b[row][0] == b[row][1] && b[row][1] == b[row][2] && b[row][0] != EMPTY) {
            return (b[row][0] == AI) ? +10 : -10;
        }
    }
    // Check columns
    for (int col = 0; col < 3; col++) {
        if (b[0][col] == b[1][col] && b[1][col] == b[2][col] && b[0][col] != EMPTY) {
            return (b[0][col] == AI) ? +10 : -10;
        }
    }
    // Check diagonals
    if (b[0][0] == b[1][1] && b[1][1] == b[2][2] && b[0][0] != EMPTY)
        return (b[0][0] == AI) ? +10 : -10;
    if (b[0][2] == b[1][1] && b[1][1] == b[2][0] && b[0][2] != EMPTY)
        return (b[0][2] == AI) ? +10 : -10;

    return 0;
}

// Minimax function
int minimax(vector<vector<char>>& board, int depth, bool isMax) {
    int score = evaluate(board);

    // Terminal conditions
    if (score == 10) return score - depth;
    if (score == -10) return score + depth;
    if (!isMovesLeft(board)) return 0;

    if (isMax) {
        int best = numeric_limits<int>::min();
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[i][j] == EMPTY) {
                    board[i][j] = AI;
                    best = max(best, minimax(board, depth + 1, false));
                    board[i][j] = EMPTY;
                }
            }
        }
        return best;
    } else {
        int best = numeric_limits<int>::max();
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[i][j] == EMPTY) {
                    board[i][j] = HUMAN;
                    best = min(best, minimax(board, depth + 1, true));
                    board[i][j] = EMPTY;
                }
            }
        }
        return best;
    }
}

// Find the best move for AI
pair<int, int> findBestMove(vector<vector<char>>& board) {
    int bestVal = numeric_limits<int>::min();
    pair<int, int> bestMove = {-1, -1};

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i][j] == EMPTY) {
                board[i][j] = AI;
                int moveVal = minimax(board, 0, false);
                board[i][j] = EMPTY;

                if (moveVal > bestVal) {
                    bestMove = {i, j};
                    bestVal = moveVal;
                }
            }
        }
    }
    return bestMove;
}

// Check if game is over
bool isGameOver(vector<vector<char>>& board) {
    int score = evaluate(board);
    if (score == 10) {
        printBoard(board);
        cout << "AI wins! \n";
        return true;
    } else if (score == -10) {
        printBoard(board);
        cout << "You win! \n";
        return true;
    } else if (!isMovesLeft(board)) {
        printBoard(board);
        cout << "It's a draw! \n";
        return true;
    }
    return false;
}

// Main Game Loop
int main() {
    vector<vector<char>> board(3, vector<char>(3, EMPTY));
    cout << "Welcome to Tic-Tac-Toe using Minimax!\n";
    cout << "You are 'O' and AI is 'X'\n";
    cout << "Enter your move as row and column (0-2)\n";

    printBoard(board);

    while (true) {
        int row, col;
        cout << "Your Move (row col): ";
        cin >> row >> col;

        // Validate move
        if (row < 0 || row > 2 || col < 0 || col > 2 || board[row][col] != EMPTY) {
            cout << "Invalid move! Try again.\n";
            continue;
        }

        // Human move
        board[row][col] = HUMAN;
        printBoard(board);
        if (isGameOver(board)) break;

        // AI move
        cout << "AI is thinking...\n";
        pair<int, int> bestMove = findBestMove(board);
        board[bestMove.first][bestMove.second] = AI;
        printBoard(board);
        if (isGameOver(board)) break;
    }

    cout << "Game Over. Thanks for playing!\n";
    return 0;
}
