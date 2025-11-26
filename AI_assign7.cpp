#include <iostream>
#include <vector>
#include <string>
using namespace std;

// Rule structure: IF antecedents => THEN consequent
struct Rule {
    vector<string> antecedents;
    string consequent;
    bool used = false; // to prevent reusing once fired
};

// Function to check if all antecedents of a rule are in facts
bool canFire(const Rule &rule, const vector<string> &facts) {
    for (auto &ant : rule.antecedents) {
        bool found = false;
        for (auto &f : facts) {
            if (f == ant) { found = true; break; }
        }
        if (!found) return false; // one antecedent missing
    }
    return true;
}

// Forward Chaining Function
bool forwardChaining(vector<Rule> &rules, vector<string> &facts, const string &query) {
    bool derived = false;
    bool addedNew;

    cout << "\nInitial facts: ";
    for (auto &f : facts) cout << f << " ";
    cout << "\n";

    do {
        addedNew = false;
        for (auto &rule : rules) {
            if (!rule.used && canFire(rule, facts)) {
                // fire the rule
                cout << "Rule fired: ";
                for (auto &a : rule.antecedents) cout << a << " ";
                cout << "=> " << rule.consequent << "\n";

                facts.push_back(rule.consequent);
                rule.used = true;
                addedNew = true;

                if (rule.consequent == query) {
                    derived = true;
                    break;
                }
            }
        }
    } while (addedNew && !derived);

    cout << "\nFinal facts: ";
    for (auto &f : facts) cout << f << " ";
    cout << "\n";

    return derived;
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
        for (int j = 0; j < numAntecedents; j++) {
            cin >> r.antecedents[j];
        }

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

    bool result = forwardChaining(rules, facts, query);

    if (result)
        cout << "SUCCESS: Query " << query << " is derived!\n";
    else
        cout << "FAIL: Query " << query << " cannot be derived.\n";

    return 0;
}
