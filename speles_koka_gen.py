import random

# Klase, kas atbilst vienai virsotnei spēles kokā
class Node:
    def __init__(self, id, sequence, p1, p2, level):
        self.id = id
        self.sequence = sequence
        self.p1 = p1
        self.p2 = p2
        self.level = level

# Klase, kas atbilst spēles kokam        
class GameTree:
    def __init__(self):
        self.nodes = []
        self.edges = dict()
    def add_node(self, node):
        self.nodes.append(node)
    def add_edge(self, start_node_id, end_node_id):
        self.edges[start_node_id] = self.edges.get(start_node_id, []) + [end_node_id]

# Funkcija, kas ģenerē gadījuma skaitļu virkni noteiktam garumam
def generate_sequence(length):
    sequence = ""
    for _ in range(length):
        sequence += str(random.randint(1, 3))
    return sequence

# Funkcija, kas ļauj lietotājam ievadīt virknes garumu
def input_sequence_length():
    while True:
        try:
            length = int(input("Enter the sequence length (15-25): "))
            if 15 <= length <= 25:
                return length
            else:
                print("The length must be between 15 and 25. Please try again.")
        except ValueError:
            print("Please enter an integer.")

# Funkcija, kas attēlo spēles stāvokli
def display_game_state(sequence, p1, p2, level):
    print("\n" + "=" * 40)
    print(f"Turn: {level}")
    print(f"Sequence: {sequence}")
    print(f"Player 1 points: {p1}")
    print(f"Player 2 points: {p2}")
    print("=" * 40)

# Funkcija, lai spēlētājs izvēlētos gājiena pozīciju
def choose_move(sequence, player_number):
    while True:
        print(f"\nPlayer {player_number}, choose a digit from the sequence:")
        pos = input(f"Enter a position (1-{len(sequence)}): ")
        try:
            pos = int(pos)
            if 1 <= pos <= len(sequence):
                return sequence[pos - 1]
            else:
                print(f"Position must be between 1 and {len(sequence)}.")
        except ValueError:
            print("Please enter an integer.")

# Funkcija, kas veic gājiena pārbaudi un atjauno spēles stāvokli
def validate_move(chosen_digit, generated_states, current_state):
    if chosen_digit in current_state[1]:
        global j
        new_id = 'A' + str(j)
        j += 1
        # Izveidojam jaunu virkni, izņemot izvēlēto skaitli (atrodot pirmo atrasto)
        pos = current_state[1].find(chosen_digit)
        new_sequence = current_state[1][:pos] + current_state[1][pos + 1:]
        # Punktu atjaunošana: ja pašreizējais līmenis ir nepāra – pirmā spēlētāja zaudē, citādi otrā
        if current_state[4] % 2 == 1:
            new_p1 = current_state[2] - int(chosen_digit)
            new_p2 = current_state[3]
        else:
            new_p1 = current_state[2]
            new_p2 = current_state[3] - int(chosen_digit)
        new_level = current_state[4] + 1
        new_node = Node(new_id, new_sequence, new_p1, new_p2, new_level)
        
        # Pārbaudām, vai šāds stāvoklis jau eksistē spēles kokā
        already_exists = False
        i = 0
        while (not already_exists) and (i < len(game_tree.nodes)):
            if (game_tree.nodes[i].sequence == new_node.sequence and
                game_tree.nodes[i].p1 == new_node.p1 and
                game_tree.nodes[i].p2 == new_node.p2 and
                game_tree.nodes[i].level == new_node.level):
                already_exists = True
            else:
                i += 1
                
        if not already_exists:
            game_tree.add_node(new_node)
            generated_states.append([new_id, new_sequence, new_p1, new_p2, new_level])
            game_tree.add_edge(current_state[0], new_id)
        else:
            j -= 1
            game_tree.add_edge(current_state[0], game_tree.nodes[i].id)

# ---------------------------------------------------------------------
# Rekurzīvā funkcija, kas ģenerē daļējo spēles koku līdz noteiktam (maksimālajam) dziļumam
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
        
        # Pārbaudām, vai šāds stāvoklis jau ir koka virsotnēs
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
# ---------------------------------------------------------------------

# Interaktīvā spēles funkcija – spēle tiek izspēlēta no sākuma līdz brīdim,
# kad virknes vērtība kļūst tukša (spēle beidzas)
def play_game():
    length = input_sequence_length()
    starting_sequence = generate_sequence(length)
    print(f"Generated sequence: {starting_sequence}")
    p1 = 80
    p2 = 80
    global game_tree, j
    game_tree = GameTree()
    # Saglabājam sākuma stāvokli, kurš tiks izmantots arī vēlāk koka ģenerēšanai
    initial_state = ['A1', starting_sequence, p1, p2, 1]
    game_tree.add_node(Node('A1', starting_sequence, p1, p2, 1))
    generated_states = [initial_state]
    j = 2
    current_state = initial_state
    
    while current_state[1]:
        display_game_state(current_state[1], current_state[2], current_state[3], current_state[4])
        player_number = 1 if current_state[4] % 2 == 1 else 2
        chosen = choose_move(current_state[1], player_number)
        validate_move(chosen, generated_states, current_state)
        current_state = generated_states[0]
        generated_states.pop(0)
        
    display_game_state(current_state[1], current_state[2], current_state[3], current_state[4])
    print("\nGame over!")
    if current_state[2] > current_state[3]:
        print("Winner: Player 1")
    elif current_state[2] < current_state[3]:
        print("Winner: Player 2")
    else:
        print("Draw!")
    
    # Pēc spēles beigām paprasām maksimālo dziļumu un izvadām daļējo spēles koku,
    # kas ģenerēts no sākuma stāvokļa (initial_state)
    while True:
        try:
            max_depth = int(input("Enter the maximum depth for tree generation: "))
            if max_depth >= 1:
                break
            else:
                print("Depth must be at least 1.")
        except ValueError:
            print("Please enter an integer.")
    
    # Atjaunojam koka struktūru, sākot no sākuma stāvokļa
    game_tree = GameTree()
    game_tree.add_node(Node(initial_state[0], initial_state[1], initial_state[2], initial_state[3], initial_state[4]))
    j = 2
    generate_partial_game_tree_rec(initial_state, max_depth)
    
    print("\nPartial game tree (depth", max_depth, "):")
    print("\nNodes:")
    for v in game_tree.nodes:
        print(f"ID: {v.id}, Sequence: {v.sequence}, P1: {v.p1}, P2: {v.p2}, Level: {v.level}")
    print("\nEdges:")
    for start, end in game_tree.edges.items():
        print(f"{start} -> {end}")

def main():
    print("Game starts!")
    play_game()

if __name__ == "__main__":
    main()
