import sys

class Rule:
    def __init__(self):
        self.antecedents = []
        self.consequent = ""
        self.used = False

def can_fire(rule, facts):
    """
    Checks if all antecedents of a rule are present in the facts list.
    """
    for ant in rule.antecedents:
        if ant not in facts:
            return False # one antecedent missing
    return True

def forward_chaining(rules, facts, query):
    derived = False
    
    print("\nInitial facts:", end=" ")
    print(" ".join(facts))
    
    # Loop until no new facts are added or query is derived
    while True:
        added_new = False
        
        for rule in rules:
            if not rule.used and can_fire(rule, facts):
                # Fire the rule
                print("Rule fired:", end=" ")
                print(" ".join(rule.antecedents), end=" ")
                print(f"=> {rule.consequent}")
                
                facts.append(rule.consequent)
                rule.used = True
                added_new = True
                
                if rule.consequent == query:
                    derived = True
                    break # Break out of for-loop to re-evaluate or finish
        
        if derived:
            break
        
        if not added_new:
            break

    print("\nFinal facts:", end=" ")
    print(" ".join(facts))
    print()

    return derived

def main():
    try:
        num_rules_str = input("Enter number of rules: ")
        if not num_rules_str: return
        num_rules = int(num_rules_str)
    except ValueError:
        print("Invalid input")
        return

    rules = []

    for i in range(num_rules):
        r = Rule()
        print(f"Rule {i + 1}:")
        
        try:
            num_ant_str = input("Enter number of antecedents: ")
            num_ant = int(num_ant_str)
            
            # Handling antecedents input
            print("Enter antecedents (space separated): ", end="")
            ants_input = input().split()
            # Ensure we take exactly num_ant inputs if user typed more
            r.antecedents = ants_input[:num_ant]
            
            # Handling consequent input
            r.consequent = input("Enter consequent: ").strip()
            
            rules.append(r)
        except ValueError:
            print("Invalid input during rule creation")
            return

    try:
        num_facts_str = input("Enter number of initial facts: ")
        num_facts = int(num_facts_str)
        
        print("Enter initial facts (space separated): ", end="")
        facts_input = input().split()
        facts = facts_input[:num_facts]
        
        query = input("Enter query (goal): ").strip()
    except ValueError:
        print("Invalid input")
        return

    result = forward_chaining(rules, facts, query)

    if result:
        print(f"SUCCESS: Query {query} is derived!")
    else:
        print(f"FAIL: Query {query} cannot be derived.")

if __name__ == "__main__":
    main()