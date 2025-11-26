import sys

def is_consistent(var, color, assignment, neighbors):
    """
    Checks if assigning 'color' to 'var' conflicts with any already assigned neighbors.
    """
    if var in neighbors:
        for neighbor in neighbors[var]:
            if neighbor in assignment and assignment[neighbor] == color:
                return False
    return True

def forward_check(var, color, domains, assignment, removed, neighbors):
    """
    Reduces the domains of unassigned neighbors.
    Returns False if any domain becomes empty (DWO - Domain Wipe Out).
    """
    if var in neighbors:
        for neighbor in neighbors[var]:
            if neighbor not in assignment:
                if color in domains[neighbor]:
                    # Initialize the set for this neighbor in 'removed' if needed
                    if neighbor not in removed:
                        removed[neighbor] = set()
                    
                    # Remove color from neighbor's domain and track it
                    removed[neighbor].add(color)
                    domains[neighbor].remove(color)
                    
                    # If domain becomes empty, this path is invalid
                    if not domains[neighbor]:
                        return False
    return True

def restore_domains(domains, removed):
    """
    Adds back the colors removed during the forward check step (Backtracking).
    """
    for var, colors in removed.items():
        for color in colors:
            domains[var].add(color)

def backtrack(index, variables, domains, assignment, neighbors):
    """
    Recursive backtracking function.
    """
    # Base case: All variables assigned
    if index == len(variables):
        return True

    var = variables[index]

    # Iterate over available colors in the domain.
    # sorted() is used to mimic C++ std::set behavior (alphabetical order)
    # ensuring the solution path is identical.
    current_domain = sorted(list(domains[var]))

    for color in current_domain:
        if is_consistent(var, color, assignment, neighbors):
            assignment[var] = color
            
            # 'removed' maps variable_name -> set of colors removed from its domain
            removed = {} 

            if forward_check(var, color, domains, assignment, removed, neighbors):
                if backtrack(index + 1, variables, domains, assignment, neighbors):
                    return True
            
            # Backtrack: Restore domains and remove assignment
            restore_domains(domains, removed)
            del assignment[var]

    return False

def get_input_tokens(prompt):
    """
    Helper to emulate C++ cin >> behavior.
    Reads lines until it gets enough tokens to satisfy the need.
    """
    tokens = []
    print(prompt, end="")
    sys.stdout.flush() # Ensure prompt shows up
    
    while not tokens:
        try:
            line = input()
            tokens = line.split()
        except EOFError:
            return None
    return tokens

def main():
    # 1. Read Number of Regions
    try:
        tokens = get_input_tokens("Enter number of regions: ")
        if not tokens: return
        num_regions = int(tokens[0])
    except ValueError:
        print("Invalid number.")
        return

    variables = []
    neighbors = {}
    domains = {}

    # 2. Read Region Names
    print("Enter region names:")
    collected_regions = 0
    buffer = []
    
    while collected_regions < num_regions:
        if not buffer:
            try:
                line = input()
                buffer = line.split()
            except EOFError:
                break
        
        if buffer:
            region = buffer.pop(0)
            variables.append(region)
            neighbors[region] = []
            collected_regions += 1

    # 3. Read Number of Edges
    try:
        tokens = get_input_tokens("Enter number of adjacency relations (edges): ")
        if not tokens: return
        num_edges = int(tokens[0])
    except ValueError:
        return

    # 4. Read Edges
    print(f"Enter {num_edges} pairs of adjacent regions:")
    collected_edges = 0
    buffer = []
    
    while collected_edges < num_edges:
        # We need pairs (2 tokens)
        while len(buffer) < 2:
            try:
                line = input()
                buffer.extend(line.split())
            except EOFError:
                break
        
        if len(buffer) >= 2:
            u = buffer.pop(0)
            v = buffer.pop(0)
            
            if u not in neighbors: neighbors[u] = []
            if v not in neighbors: neighbors[v] = []
            
            neighbors[u].append(v)
            neighbors[v].append(u)
            collected_edges += 1

    # 5. Read Number of Colors
    try:
        tokens = get_input_tokens("Enter number of colors: ")
        if not tokens: return
        num_colors = int(tokens[0])
    except ValueError:
        return

    # 6. Read Color Names
    print("Enter color names:")
    color_list = []
    collected_colors = 0
    buffer = []
    
    while collected_colors < num_colors:
        if not buffer:
            try:
                line = input()
                buffer = line.split()
            except EOFError:
                break
        
        if buffer:
            color = buffer.pop(0)
            color_list.append(color)
            collected_colors += 1

    # Initialize Domains
    for var in variables:
        domains[var] = set(color_list)

    assignment = {}

    # Solve
    success = backtrack(0, variables, domains, assignment, neighbors)

    if success:
        print("\nFinal Answer:")
        for var in variables:
            print(f"{var} = {assignment[var]}")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()