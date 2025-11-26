#include <iostream>
#include <vector>
using namespace std;

const int N = 8;

// Function to print the chessboard
void printBoard(const vector<int>& board) {
    for (int row = 0; row < N; ++row) {
        for (int col = 0; col < N; ++col) {
            if (board[row] == col)
                cout << "Q ";
            else
                cout << ". ";
        }
        cout << endl;
    }
    cout << endl;
}

// Check if a queen can be placed at board[row] = col
bool isSafe(const vector<int>& board, int row, int col) {
    for (int i = 0; i < row; ++i) {
        if (board[i] == col || abs(board[i] - col) == abs(i - row))
            return false; // same column or diagonal
    }
    return true;
}

// Backtracking function to solve 8-Queens
bool solveNQueens(vector<int>& board, int row) {
    if (row == N) {
        printBoard(board);
        return true; // Found a solution
    }

    bool foundSolution = false;
    for (int col = 0; col < N; ++col) {
        if (isSafe(board, row, col)) {
            board[row] = col; // Place queen
            foundSolution |= solveNQueens(board, row + 1);
            board[row] = -1; // Backtrack
        }
    }
    return foundSolution;
}

int main() {
    vector<int> board(N, -1); // board[i] = column of queen in row i
    if (!solveNQueens(board, 0)) {
        cout << "No solution exists." << endl;
    }
    return 0;
}
