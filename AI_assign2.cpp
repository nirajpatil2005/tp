#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>
#include <set>

using namespace std;

bool isConsistent(string var, string color, unordered_map<string, string> &assignment,
                  unordered_map<string, vector<string>> &neighbors)
{
    for (const string &neighbor : neighbors[var])
    {
        if (assignment.find(neighbor) != assignment.end() && assignment[neighbor] == color)
        {
            return false;
        }
    }
    return true;
}

bool forwardCheck(string var, string color,
                  unordered_map<string, set<string>> &domains,
                  unordered_map<string, string> &assignment,
                  unordered_map<string, set<string>> &removed,
                  unordered_map<string, vector<string>> &neighbors)
{
    for (const string &neighbor : neighbors[var])
    {
        if (assignment.find(neighbor) == assignment.end())
        {
            if (domains[neighbor].count(color))
            {
                removed[neighbor].insert(color);
                domains[neighbor].erase(color);
                if (domains[neighbor].empty())
                    return false;
            }
        }
    }
    return true;
}

void restoreDomains(unordered_map<string, set<string>> &domains,
                    unordered_map<string, set<string>> &removed)
{
    for (const auto &entry : removed)
    {
        for (const string &val : entry.second)
        {
            domains[entry.first].insert(val);
        }
    }
}

bool backtrack(int index, vector<string> &variables,
               unordered_map<string, set<string>> &domains,
               unordered_map<string, string> &assignment,
               unordered_map<string, vector<string>> &neighbors)
{
    if (index == variables.size())
        return true;

    string var = variables[index];

    for (const string &color : domains[var])
    {
        if (isConsistent(var, color, assignment, neighbors))
        {
            assignment[var] = color;
            unordered_map<string, set<string>> removed;

            if (forwardCheck(var, color, domains, assignment, removed, neighbors))
            {
                if (backtrack(index + 1, variables, domains, assignment, neighbors))
                {
                    return true;
                }
            }

            restoreDomains(domains, removed);
            assignment.erase(var);
        }
    }

    return false;
}

int main()
{
    int numRegions, numEdges, numColors;

    cout << "Enter number of regions: ";
    cin >> numRegions;

    vector<string> variables;
    unordered_map<string, vector<string>> neighbors;
    unordered_map<string, set<string>> domains;

    cout << "Enter region names:\n";
    for (int i = 0; i < numRegions; ++i)
    {
        string region;
        cin >> region;
        variables.push_back(region);
        neighbors[region] = {};
    }

    cout << "Enter number of adjacency relations (edges): ";
    cin >> numEdges;
    cout << "Enter " << numEdges << " pairs of adjacent regions:\n";
    for (int i = 0; i < numEdges; ++i)
    {
        string a, b;
        cin >> a >> b;
        neighbors[a].push_back(b);
        neighbors[b].push_back(a);
    }

    cout << "Enter number of colors: ";
    cin >> numColors;
    vector<string> colorList(numColors);
    cout << "Enter color names:\n";
    for (int i = 0; i < numColors; ++i)
    {
        cin >> colorList[i];
    }

    for (const string &var : variables)
    {
        domains[var] = set<string>(colorList.begin(), colorList.end());
    }

    unordered_map<string, string> assignment;

    bool success = backtrack(0, variables, domains, assignment, neighbors);

    if (success)
    {
        cout << "\nFinal Answer:\n";
        for (const string &var : variables)
        {
            cout << var << " = " << assignment[var] << "\n";
        }
    }
    else
    {
        cout << "No solution found.\n";
    }

    return 0;
}
