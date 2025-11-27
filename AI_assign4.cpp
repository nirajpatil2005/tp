#include <iostream>
#include <map>
#include <vector>
#include <queue>
#include <string>
#include <limits>
#include <climits>

using namespace std;

struct Edge {
    string neighbor;
    int cost; // actual distance
};

struct Node {
    string city;
    int g; // cost so far
    int h; // heuristic to goal
    int f; // total estimated cost
    string parent;

    bool operator>(const Node &other) const {
        return f > other.f;
    }
};

// --- A* Search Function ---
void aStarSearch(map<string, vector<Edge>> &graph, map<string, int> &heuristic,
                 string start, string goal) {

    priority_queue<Node, vector<Node>, greater<Node>> openList;
    map<string, bool> closedList;
    map<string, int> gScore;
    map<string, string> parent;

    for (auto &pair : graph)
        gScore[pair.first] = INT_MAX;

    gScore[start] = 0;

    openList.push({start, 0, heuristic[start], heuristic[start], ""});

    cout << "\n--- A* Search Steps ---\n";

    while (!openList.empty()) {
        Node current = openList.top();
        openList.pop();

        if (closedList[current.city])
            continue;
        closedList[current.city] = true;

        cout << "Expanding: " << current.city << " (f=" << current.f
             << ", g=" << current.g << ", h=" << current.h << ")\n";

        if (current.city == goal) {
            cout << "\nGoal Reached: " << goal << "\n";
            cout << "Total Cost = " << current.g << " km\n";

            // Reconstruct path
            vector<string> path;
            string city = goal;
            while (city != "") {
                path.push_back(city);
                city = parent[city];
            }
            cout << "\nPath: ";
            for (int i = path.size() - 1; i >= 0; i--)
                cout << path[i] << (i ? "----" : "\n");
            return;
        }

        for (auto &edge : graph[current.city]) {
            if (!closedList[edge.neighbor]) {
                int new_g = current.g + edge.cost;
                int new_f = new_g + heuristic[edge.neighbor];

                if (new_g < gScore[edge.neighbor]) {
                    gScore[edge.neighbor] = new_g;
                    parent[edge.neighbor] = current.city;
                    openList.push({edge.neighbor, new_g, heuristic[edge.neighbor], new_f, current.city});
                }
            }
        }
    }

    cout << "No path found!\n";
}

int main() {
    map<string, vector<Edge>> graph;
    map<string, int> heuristic;
    int n;

    cout << "Enter number of cities: ";
    cin >> n;

    cout << "\nEnter city names:\n";
    vector<string> cities(n);
    for (int i = 0; i < n; i++)
        cin >> cities[i];

    cout << "\nEnter heuristic values (estimated distance to goal city):\n";
    for (auto &city : cities) {
        cout << "h(" << city << ") = ";
        cin >> heuristic[city];
    }

    int e;
    cout << "\nEnter number of routes (edges): ";
    cin >> e;

    cout << "\nEnter routes in format: Source Destination Distance\n";
    for (int i = 0; i < e; i++) {
        string u, v;
        int cost;
        cin >> u >> v >> cost;
        graph[u].push_back({v, cost});
        // if roads are two-way
        graph[v].push_back({u, cost});
    }

    string start, goal;
    cout << "\nEnter start city: ";
    cin >> start;
    cout << "Enter goal city: ";
    cin >> goal;

    aStarSearch(graph, heuristic, start, goal);

    return 0;
}
// # Enter number of cities: 4

// # Enter city names:
// # s a b g

// # Enter heuristic values (estimated distance to goal city):
// # h(s) = 7 
// # h(a) = 6
// # h(b) = 2
// # h(g) = 0

// # Enter number of routes (edges): 5

// # Enter routes in format: Source Destination Distance
// # s a 1
// # s b 4
// # a b 2
// # a g 12
// # b g 3

// # Enter start city: s
// # Enter goal city: g

// # --- A* Search Steps ---
// # Expanding: s (f=7, g=0, h=7)
// # Expanding: b (f=6, g=4, h=2)
// # Expanding: a (f=7, g=1, h=6)
// # Expanding: g (f=7, g=7, h=0)

// # Goal Reached: g
// # Total Cost = 7 km

// # Path: s----b----g