#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <set>
using namespace std;

const vector<vector<int>> goal = {{1,2,3},{4,5,6},{7,8,0}};
const int dx[] = {-1, 1, 0, 0}; // up, down
const int dy[] = {0, 0, -1, 1}; // left, right

struct State {
    vector<vector<int>> mat;
    string path;
    int depth;
};

string serialize(const vector<vector<int>> &mat) {
    string s;
    for (auto &row : mat)
        for (int val : row)
            s += to_string(val);
    return s;
}

bool isGoal(const vector<vector<int>> &mat) {
    return mat == goal;
}

vector<State> getNeighbours(const vector<vector<int>> &mat, const string &path) {
    vector<State> neighbours;
    int x, y;
    
    // find 0 position
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            if (mat[i][j] == 0) {
                x = i;
                y = j;
            }

    for (int dir = 0; dir < 4; dir++) {
        int nx = x + dx[dir];
        int ny = y + dy[dir];

        if (nx >= 0 && nx < 3 && ny >= 0 && ny < 3) {
            vector<vector<int>> newMat = mat;
            swap(newMat[x][y], newMat[nx][ny]);
            string moveDesc = " -> move " + to_string(newMat[x][y]);
            neighbours.push_back({newMat, path + moveDesc});
        }
    }
    return neighbours;
}

void bfs(vector<vector<int>> start) {
    queue<State> q;
    set<string> visited;

    q.push({start, "Start"});
    visited.insert(serialize(start));

    while (!q.empty()) {
        State current = q.front(); q.pop();

        if (isGoal(current.mat)) {
            cout << "Reached Goal using BFS!\n";
            cout << "Path: " << current.path << "\n";
            return;
        }

        for (auto &next : getNeighbours(current.mat, current.path)) {
            string key = serialize(next.mat);
            if (!visited.count(key)) {
                visited.insert(key);
                q.push(next);
            }
        }
    }
    cout << "Goal not reachable using BFS.\n";
}

void dfs(vector<vector<int>> start) {
    stack<State> st;
    set<string> visited;

    st.push({start, "Start", 0});
    visited.insert(serialize(start));

    const int MAX_DEPTH = 20;

    while (!st.empty()) {
        State current = st.top(); st.pop();

        if (isGoal(current.mat)) {
            cout << "Reached Goal using DFS!\n";
            cout << "Path: " << current.path << "\n";
            return;
        }

        if (current.depth >= MAX_DEPTH) continue;

        for (auto &next : getNeighbours(current.mat, current.path)) {
            string key = serialize(next.mat);
            if (!visited.count(key)) {
                visited.insert(key);
                st.push({next.mat, next.path, current.depth + 1});
            }
        }
    }

    cout << "Goal not reachable using DFS within depth limit.\n";
}


int main() {
    vector<vector<int>> initial(3, vector<int>(3));
    cout << "Enter initial 3x3 puzzle state (0 is blank):\n";
    for (auto &row : initial)
        for (int &val : row)
            cin >> val;

    cout << "\n--- BFS ---\n";
    bfs(initial);

    cout << "\n--- DFS ---\n";
    dfs(initial);

    return 0;
}
