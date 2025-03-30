import random

# Class representing a single node in the game tree
class Node:
    def __init__(self, id, sequence, p1, p2, level):
        self.id = id
        self.sequence = sequence
        self.p1 = p1
        self.p2 = p2
        self.level = level

# Class representing the game tree structure        
class GameTree:
    def __init__(self):
        self.nodes = []
        self.edges = dict()
    def add_node(self, node):
        self.nodes.append(node)
    def add_edge(self, start_node_id, end_node_id):
        self.edges[start_node_id] = self.edges.get(start_node_id, []) + [end_node_id]

# Function that generates a random digit sequence of a given length
def generate_sequence(length):
    sequence = ""
    for _ in range(length):
        sequence += str(random.randint(1, 3))
    return sequence

# Recursive function to generate a partial game tree from a given state up to max_depth
def generate_partial_game_tree_rec(current_state, max_depth):
    if current_state[4] >= max_depth or current_state[1] == "":
        return
    for i in range(len(current_state[1])):
        digit = current_state[1][i]
        new_sequence = current_state[1][:i] + current_state[1][i + 1:]
        if current_state[4] % 2 == 1:
            new_p1 = current_state[2] - int(digit)
            new_p2 = current_state[3]
        else:
            new_p1 = current_state[2]
            new_p2 = current_state[3] - int(digit)
        new_level = current_state[4] + 1
        
        global j
        new_id = 'A' + str(j)
        j += 1
        new_state = [new_id, new_sequence, new_p1, new_p2, new_level]
        
        # Check if this state already exists in the game tree
        exists = False
        for v in game_tree.nodes:
            if (v.sequence == new_state[1] and v.p1 == new_state[2] and 
                v.p2 == new_state[3] and v.level == new_state[4]):
                exists = True
                break
        if exists:
            game_tree.add_edge(current_state[0], new_id)
        else:
            game_tree.add_node(Node(new_id, new_sequence, new_p1, new_p2, new_level))
            game_tree.add_edge(current_state[0], new_id)
            generate_partial_game_tree_rec(new_state, max_depth)

def main():
    print("Game Tree Generation!")
    # Get sequence length from user (between 15 and 25)
    while True:
        try:
            length = int(input("Enter the sequence length (15-25): "))
            if 15 <= length <= 25:
                break
            else:
                print("The length must be between 15 and 25. Please try again.")
        except ValueError:
            print("Please enter an integer.")
    
    starting_sequence = generate_sequence(length)
    print(f"Generated sequence: {starting_sequence}")
    p1 = 80
    p2 = 80
    
    # Initialize game tree with the initial state
    global game_tree, j
    game_tree = GameTree()
    initial_state = ['A1', starting_sequence, p1, p2, 1]
    game_tree.add_node(Node(initial_state[0], starting_sequence, p1, p2, 1))
    j = 2
    
    # Get maximum depth for tree generation
    while True:
        try:
            max_depth = int(input("Enter the maximum depth for tree generation: "))
            if max_depth >= 1:
                break
            else:
                print("Depth must be at least 1.")
        except ValueError:
            print("Please enter an integer.")
    
    # Generate the partial game tree from the initial state
    generate_partial_game_tree_rec(initial_state, max_depth)
    
    # Print the game tree (nodes and edges)
    print("\nPartial game tree (depth", max_depth, "):")
    print("\nNodes:")
    for v in game_tree.nodes:
        print(f"ID: {v.id}, Sequence: {v.sequence}, P1: {v.p1}, P2: {v.p2}, Level: {v.level}")
    print("\nEdges:")
    for start, end in game_tree.edges.items():
        print(f"{start} -> {end}")

if __name__ == "__main__":
    main()
