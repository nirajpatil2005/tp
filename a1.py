import sys
from collections import deque

# Constants
GOAL = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
# Directions: Up, Down, Left, Right
DX = [-1, 1, 0, 0]
DY = [0, 0, -1, 1]

class State:
    def __init__(self, mat, path, depth=0):
        self.mat = mat
        self.path = path
        self.depth = depth

def serialize(mat):
    """Flattens matrix to string for visited set checks."""
    s = ""
    for row in mat:
        for val in row:
            s += str(val)
    return s

def is_goal(mat):
    return mat == GOAL

def get_neighbours(mat, path):
    neighbours = []
    x, y = -1, -1

    # Find 0 position
    for i in range(3):
        for j in range(3):
            if mat[i][j] == 0:
                x = i
                y = j
                break
    
    for direction in range(4):
        nx = x + DX[direction]
        ny = y + DY[direction]

        if 0 <= nx < 3 and 0 <= ny < 3:
            # Create a deep copy of the matrix manually for performance
            new_mat = [row[:] for row in mat]
            
            # Swap
            new_mat[x][y], new_mat[nx][ny] = new_mat[nx][ny], new_mat[x][y]
            
            # The value we swapped into the empty space
            moved_val = new_mat[x][y] 
            
            move_desc = f" -> move {moved_val}"
            neighbours.append(State(new_mat, path + move_desc))
            
    return neighbours

def bfs(start_mat):
    q = deque()
    visited = set()

    q.append(State(start_mat, "Start"))
    visited.add(serialize(start_mat))

    while q:
        current = q.popleft() # Dequeue

        if is_goal(current.mat):
            print("Reached Goal using BFS!")
            print(f"Path: {current.path}")
            return

        for next_state in get_neighbours(current.mat, current.path):
            key = serialize(next_state.mat)
            if key not in visited:
                visited.add(key)
                q.append(next_state)
    
    print("Goal not reachable using BFS.")

def dfs(start_mat):
    st = [] # List used as Stack
    visited = set()

    # Initial depth is 0
    st.append(State(start_mat, "Start", 0))
    visited.add(serialize(start_mat))

    MAX_DEPTH = 20

    while st:
        current = st.pop() # Pop from top (LIFO)

        if is_goal(current.mat):
            print("Reached Goal using DFS!")
            print(f"Path: {current.path}")
            return

        if current.depth >= MAX_DEPTH:
            continue

        # In C++, getNeighbours is called and iterated. 
        # C++ pushes to stack in order of directions (Up, Down, Left, Right).
        # We do the same here.
        for next_state in get_neighbours(current.mat, current.path):
            key = serialize(next_state.mat)
            if key not in visited:
                visited.add(key)
                # Update depth for next state
                next_state.depth = current.depth + 1
                st.append(next_state)

    print("Goal not reachable using DFS within depth limit.")

def main():
    initial = []
    print("Enter initial 3x3 puzzle state (0 is blank):")
    
    # Logic to read 9 integers from input (handles newlines or single line input)
    inputs = []
    while len(inputs) < 9:
        try:
            line = input().split()
            inputs.extend(map(int, line))
        except EOFError:
            break
            
    # Construct 3x3 matrix
    k = 0
    for i in range(3):
        row = []
        for j in range(3):
            row.append(inputs[k])
            k += 1
        initial.append(row)

    print("\n--- BFS ---")
    bfs(initial)

    print("\n--- DFS ---")
    dfs(initial)

if __name__ == "__main__":
    main()