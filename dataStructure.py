class Node:
    def __init__(self, sequence, player_score, ai_score, level, node_id=None, move=None, is_max=None, value=None):
        self.id = node_id  # Unikāls ID, ja nepieciešams
        self.sequence = sequence
        self.player_score = player_score
        self.ai_score = ai_score
        self.level = level
        self.move = move  # Pēdējā veikta kustība (ja piemērojams)
        self.is_max = is_max  # Vai tas ir maksimizācijas mezgls (ja nepieciešams)
        self.value = value  # Novērtējuma funkcijas vērtība
        self.children = []  # Saraksts ar bērnu mezgliem


class GameTree:
    def __init__(self):
        self.root = None
        self.node_count = 0
        self.nodes = []  # Saglabā visus mezglus, ja nepieciešams

    def add_node(self, parent, sequence, player_score, ai_score, level, move=None, is_max=None, value=None):
        """Pievieno mezglu, pielāgojoties dažādiem algoritmiem."""
        node_id = f"N{self.node_count}"  # Automātisks ID
        new_node = Node(sequence, player_score, ai_score, level, node_id, move, is_max, value)
        self.node_count += 1

        if parent:
            parent.children.append(new_node)
        else:
            self.root = new_node

        self.nodes.append(new_node)  # Ja nepieciešams sekot visiem mezgliem
        return new_node