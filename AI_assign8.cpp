#include <iostream>
#include <vector>
#include <string>
using namespace std;

// Rule structure: IF antecedents => THEN consequent
struct Rule {
    vector<string> antecedents;
    string consequent;
};

// Function to check if a fact is in the known facts
bool isFact(const string &goal, const vector<string> &facts) {
    for (auto &f : facts) {
        if (f == goal) return true;
    }
    return false;
}

// Backward Chaining Function
bool backwardChaining(const string &goal, const vector<Rule> &rules, const vector<string> &facts) {
    // Check if goal is already a known fact
    if (isFact(goal, facts)) {
        cout << "Goal " << goal << " is already known.\n";
        return true;
    }

    // Try to find a rule that can derive the goal
    for (auto &rule : rules) {
        if (rule.consequent == goal) {
            cout << "Trying to satisfy goal: " << goal << " using rule: ";
            for (auto &ant : rule.antecedents) cout << ant << " ";
            cout << "=> " << rule.consequent << "\n";

            bool allAntecedentsTrue = true;
            for (auto &ant : rule.antecedents) {
                if (!backwardChaining(ant, rules, facts)) {
                    allAntecedentsTrue = false;
                    break;
                }
            }

            if (allAntecedentsTrue) {
                cout << "Goal " << goal << " is derived!\n";
                return true;
            }
        }
    }

    cout << "Goal " << goal << " cannot be derived.\n";
    return false;
}

int main() {
    int numRules, numAntecedents;
    cout << "Enter number of rules: ";
    cin >> numRules;

    vector<Rule> rules;

    for (int i = 0; i < numRules; i++) {
        Rule r;
        cout << "Rule " << i + 1 << ":\n";
        cout << "Enter number of antecedents: ";
        cin >> numAntecedents;

        r.antecedents.resize(numAntecedents);
        cout << "Enter antecedents (space separated): ";
        for (int j = 0; j < numAntecedents; j++) cin >> r.antecedents[j];

        cout << "Enter consequent: ";
        cin >> r.consequent;

        rules.push_back(r);
    }

    int numFacts;
    cout << "Enter number of initial facts: ";
    cin >> numFacts;

    vector<string> facts(numFacts);
    cout << "Enter initial facts (space separated): ";
    for (int i = 0; i < numFacts; i++) cin >> facts[i];

    string query;
    cout << "Enter query (goal): ";
    cin >> query;

    cout << "\nStarting Backward Chaining...\n";
    bool result = backwardChaining(query, rules, facts);

    if (result)
        cout << "\nSUCCESS: Query " << query << " is derived!\n";
    else
        cout << "\nFAIL: Query " << query << " cannot be derived.\n";

    return 0;
}