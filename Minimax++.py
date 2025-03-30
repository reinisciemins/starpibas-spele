import speles_koka_gen

def generate_partial_tree(p1, p2, max_depth, length=15):
    """
    Generates a partial game tree using speles_koka_gen.
    A random sequence of digits is generated automatically.
    """
    global j, game_tree
    sequence = speles_koka_gen.generate_sequence(length)
    game_tree = speles_koka_gen.GameTree()
    initial_state = ['A1', sequence, p1, p2, 1]
    game_tree.add_node(speles_koka_gen.Node(initial_state[0], sequence, p1, p2, 1))
    j = 2
    speles_koka_gen.generate_partial_game_tree_rec(initial_state, max_depth)
    return game_tree

def get_children(tree, node):
    """
    Returns the children of a node using the tree's edges.
    """
    children_ids = tree.edges.get(node.id, [])
    return [n for n in tree.nodes if n.id in children_ids]

class MinimaxALG:
    def __init__(self):
        self.nodes_visited = 0
        self.game_tree = None

    def evaluate(self, node):
        # Evaluation function: AI score minus player's score.
        return node.p2 - node.p1

    def minimax(self, node, depth, is_maximizing):
        self.nodes_visited += 1
        children = get_children(self.game_tree, node)
        if depth == 0 or not children:
            node.value = self.evaluate(node)
            return node.value

        if is_maximizing:
            maxEval = float('-inf')
            for child in children:
                eval = self.minimax(child, depth - 1, False)
                maxEval = max(maxEval, eval)
            node.value = maxEval
            return maxEval
        else:
            minEval = float('inf')
            for child in children:
                eval = self.minimax(child, depth - 1, True)
                minEval = min(minEval, eval)
            node.value = minEval
            return minEval

    def get_best_value(self, p1, p2, max_depth, search_depth, is_maximizing=True, length=15):
        """
        Generates the partial tree and runs the minimax algorithm.
          - p1, p2: initial scores (integers)
          - max_depth: depth for tree generation
          - search_depth: search depth for minimax
          - is_maximizing: flag for starting with maximizing (default True)
          - length: length of the generated sequence (default 15)
        Returns the evaluated best value.
        """
        self.game_tree = generate_partial_tree(p1, p2, max_depth, length)
        best_val = self.minimax(self.game_tree.nodes[0], search_depth, is_maximizing)
        return best_val

if __name__ == "__main__":
    # Example parameters for testing
    p1 = 80
    p2 = 80
    max_depth = 3      # Maximum depth for generating the tree
    search_depth = 3   # Depth for minimax search
    alg = MinimaxALG()
    best_value = alg.get_best_value(p1, p2, max_depth, search_depth, True)
    print("Best value (Minimax):", best_value)
    print("Nodes visited:", alg.nodes_visited)
