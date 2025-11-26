import heapq
import sys

class Node:
    def __init__(self, city, g, h, f, parent):
        self.city = city
        self.g = g  # Cost so far
        self.h = h  # Heuristic to goal
        self.f = f  # Total estimated cost
        self.parent = parent

    # Comparison operator for Priority Queue (Min-Heap)
    # Allows heapq to sort Nodes based on 'f' value
    def __lt__(self, other):
        return self.f < other.f

def a_star_search(graph, heuristic, start, goal):
    # Priority Queue stores Node objects
    open_list = []
    
    # Push start node
    start_node = Node(start, 0, heuristic[start], heuristic[start], "")
    heapq.heappush(open_list, start_node)
    
    closed_list = set()
    parent_map = {}
    
    # Initialize g_score with infinity for all known cities
    g_score = {city: float('inf') for city in heuristic}
    g_score[start] = 0

    print("\n--- A* Search Steps ---")

    while open_list:
        # Pop node with lowest f score
        current = heapq.heappop(open_list)

        if current.city in closed_list:
            continue
        
        closed_list.add(current.city)

        print(f"Expanding: {current.city} (f={current.f}, g={current.g}, h={current.h})")

        if current.city == goal:
            print(f"\nGoal Reached: {goal}")
            print(f"Total Cost = {current.g} km")

            # Reconstruct path
            path = []
            curr = goal
            while curr:
                path.append(curr)
                curr = parent_map.get(curr, "")
            
            print("\nPath: ", end="")
            # Reverse list to get Start -> Goal
            print("----".join(reversed(path)))
            return

        # Check neighbors
        if current.city in graph:
            for neighbor, cost in graph[current.city]:
                if neighbor not in closed_list:
                    new_g = current.g + cost
                    new_f = new_g + heuristic[neighbor]

                    # If we found a cheaper path to this neighbor, update it
                    if new_g < g_score[neighbor]:
                        g_score[neighbor] = new_g
                        parent_map[neighbor] = current.city
                        new_node = Node(neighbor, new_g, heuristic[neighbor], new_f, current.city)
                        heapq.heappush(open_list, new_node)

    print("No path found!")

def main():
    try:
        n = int(input("Enter number of cities: "))
    except ValueError:
        return

    print("\nEnter city names:")
    cities = []
    # Read n cities (handling potentially multi-line or single-line input)
    while len(cities) < n:
        line = input().split()
        cities.extend(line)

    heuristic = {}
    print("\nEnter heuristic values (estimated distance to goal city):")
    for city in cities:
        val = int(input(f"h({city}) = "))
        heuristic[city] = val

    e = int(input("\nEnter number of routes (edges): "))
    
    graph = {city: [] for city in cities}
    
    print("\nEnter routes in format: Source Destination Distance")
    for _ in range(e):
        u, v, cost = input().split()
        cost = int(cost)
        graph[u].append((v, cost))
        # Assuming two-way roads (undirected graph)
        graph[v].append((u, cost))

    print("\nEnter start city: ", end="")
    start = input().strip()
    print("Enter goal city: ", end="")
    goal = input().strip()

    a_star_search(graph, heuristic, start, goal)

if __name__ == "__main__":
    main()
    
# (base) PS D:\TRY\AI practical\AI_4> python a4.py
# Enter number of cities: 4

# Enter city names:
# s a b g

# Enter heuristic values (estimated distance to goal city):
# h(s) = 7 
# h(a) = 6
# h(b) = 2
# h(g) = 0

# Enter number of routes (edges): 5

# Enter routes in format: Source Destination Distance
# s a 1
# s b 4
# a b 2
# a g 12
# b g 3

# Enter start city: s
# Enter goal city: g

# --- A* Search Steps ---
# Expanding: s (f=7, g=0, h=7)
# Expanding: b (f=6, g=4, h=2)
# Expanding: a (f=7, g=1, h=6)
# Expanding: g (f=7, g=7, h=0)

# Goal Reached: g
# Total Cost = 7 km

# Path: s----b----g