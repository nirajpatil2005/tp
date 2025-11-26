import sys

# Rule structure: IF antecedents => THEN consequent
class Rule:
    def __init__(self):
        self.antecedents = []
        self.consequent = ""

def is_fact(goal, facts):
    """
    Checks if a specific goal is present in the list of known facts.
    """
    return goal in facts

def backward_chaining(goal, rules, facts):
    """
    Recursive function to verify if a goal can be derived.
    """
    # Check if goal is already a known fact
    if is_fact(goal, facts):
        print(f"Goal {goal} is already known.")
        return True

    # Try to find a rule that can derive the goal
    for rule in rules:
        if rule.consequent == goal:
            print(f"Trying to satisfy goal: {goal} using rule: ", end="")
            print(" ".join(rule.antecedents), end="")
            print(f" => {rule.consequent}")

            all_antecedents_true = True
            
            # Recursively check all antecedents
            for ant in rule.antecedents:
                # To prevent infinite loops in cyclic rules, complex systems use a 'visited' set.
                # For this specific translation, we stick to the simple recursion of the C++ code.
                if not backward_chaining(ant, rules, facts):
                    all_antecedents_true = False
                    break
            
            if all_antecedents_true:
                print(f"Goal {goal} is derived!")
                return True

    print(f"Goal {goal} cannot be derived.")
    return False

def main():
    try:
        num_rules_str = input("Enter number of rules: ")
        if not num_rules_str: return
        num_rules = int(num_rules_str)
    except ValueError:
        print("Invalid input.")
        return

    rules = []

    for i in range(num_rules):
        r = Rule()
        print(f"Rule {i + 1}:")
        
        try:
            num_ant = int(input("Enter number of antecedents: "))
            
            print("Enter antecedents (space separated): ", end="")
            ants_input = input().split()
            r.antecedents = ants_input[:num_ant]
            
            r.consequent = input("Enter consequent: ").strip()
            
            rules.append(r)
        except ValueError:
            print("Invalid input during rule entry.")
            return

    try:
        num_facts_str = input("Enter number of initial facts: ")
        num_facts = int(num_facts_str)
        
        print("Enter initial facts (space separated): ", end="")
        facts_input = input().split()
        facts = facts_input[:num_facts]
        
        query = input("Enter query (goal): ").strip()
    except ValueError:
        print("Invalid input.")
        return

    print("\nStarting Backward Chaining...")
    result = backward_chaining(query, rules, facts)

    if result:
        print(f"\nSUCCESS: Query {query} is derived!")
    else:
        print(f"\nFAIL: Query {query} cannot be derived.")

if __name__ == "__main__":
    main()