import sys
from collections import defaultdict

# --- Knowledge Base ---
# Using defaultdict to automatically handle empty lists for new keys
father = defaultdict(list)
mother = defaultdict(list)

# --- Add Facts ---
def add_father(f, c):
    father[f].append(c)

def add_mother(m, c):
    mother[m].append(c)

# --- Rules ---

# Parent Rule
def get_children(p):
    # Combine lists from both father and mother maps.
    # Returns an empty list if p is not found.
    return father.get(p, []) + mother.get(p, [])

# Sibling Rule
def get_siblings(name):
    result = []
    
    # Check in father map
    for p, children in father.items():
        if name in children:
            for c in children:
                if c != name:
                    result.append(c)

    # Check in mother map
    for p, children in mother.items():
        if name in children:
            for c in children:
                if c != name:
                    result.append(c)
    
    # Note: This logic (like the C++ version) might include duplicates
    # if siblings share both parents. To remove duplicates, we could use set().
    # Keeping it as list to match C++ 'vector' behavior exactly.
    return result

# Grandparent Rule
def get_grandchildren(gp):
    result = []
    
    # Get immediate children from both maps
    immediate_children = get_children(gp)
    
    # For every child, get their children (grandchildren of gp)
    for child in immediate_children:
        gkids = get_children(child)
        result.extend(gkids)
        
    return result

# --- Main ---
def main():
    print("Family Tree Knowledge Base Parser")
    print("----------------------------------")

    print("Enter family facts (type 'done' when finished):")
    print("Use format:")
    print("  father <FatherName> <ChildName>")
    print("  mother <MotherName> <ChildName>")

    while True:
        try:
            # Emulating cin >> behavior by reading a line and splitting
            line = input("Enter fact: ").strip()
            if not line: continue # Skip empty lines
            
            parts = line.split()
            relation = parts[0]
            
            if relation == "done":
                break
            
            if len(parts) < 3:
                print("Invalid format. Usage: <relation> <parent> <child>")
                continue
                
            parent = parts[1]
            child = parts[2]

            if relation == "father":
                add_father(parent, child)
            elif relation == "mother":
                add_mother(parent, child)
            else:
                print("Unknown relation type! Use 'father' or 'mother'.")
                
        except EOFError:
            break

    print("\nKnowledge base created successfully!\n")
    print("Queries Supported:")
    print("1. children <name>")
    print("2. siblings <name>")
    print("3. grandchildren <name>")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            line = input("Enter query: ").strip()
            if not line: continue
            
            parts = line.split()
            query = parts[0]
            
            if query == "exit":
                break
            
            if len(parts) < 2:
                print("Invalid format. Usage: <query> <name>")
                continue
                
            name = parts[1]

            if query == "children":
                res = get_children(name)
                if not res:
                    print(f"{name} has no children.")
                else:
                    print(f"Children of {name}:", end=" ")
                    print(*res)
                    
            elif query == "siblings":
                res = get_siblings(name)
                if not res:
                    print(f"{name} has no siblings.")
                else:
                    print(f"Siblings of {name}:", end=" ")
                    print(*res)
                    
            elif query == "grandchildren":
                res = get_grandchildren(name)
                if not res:
                    print(f"{name} has no grandchildren.")
                else:
                    print(f"Grandchildren of {name}:", end=" ")
                    print(*res)
            else:
                print("Unknown query type!")
                
        except EOFError:
            break

    print("\nThank you for using the Family Tree Parser!")

if __name__ == "__main__":
    main()