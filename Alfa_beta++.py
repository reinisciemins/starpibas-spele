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
    Returns a list of child nodes for a given node based on the tree's edges.
    """
    children_ids = tree.edges.get(node.id, [])
    return [n for n in tree.nodes if n.id in children_ids]

class AlphaBetaALG:
    def __init__(self):
        self.nodes_visited = 0
        self.game_tree = None

    def evaluate(self, node):
        # Evaluation: AI score minus player's score.
        return node.p2 - node.p1

    def alfabeta(self, node, depth, alpha, beta):
        self.nodes_visited += 1
        children = get_children(self.game_tree, node)
        if depth == 0 or not children:
            node.value = self.evaluate(node)
            return node.value

        # Using node level to determine maximizing/minimizing (odd levels maximize)
        if node.level % 2 == 1:
            maxEval = float('-inf')
            for child in children:
                eval = self.alfabeta(child, depth - 1, alpha, beta)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            node.value = maxEval
            return maxEval
        else:
            minEval = float('inf')
            for child in children:
                eval = self.alfabeta(child, depth - 1, alpha, beta)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            node.value = minEval
            return minEval

    def get_best_value(self, p1, p2, max_depth, search_depth, length=15):
        """
        Generates the partial tree and runs alpha-beta search.
          - p1, p2: initial scores (integers)
          - max_depth: depth for tree generation
          - search_depth: search depth for the algorithm
          - length: length of the generated sequence (default 15)
        Returns the evaluated best value.
        """
        self.game_tree = generate_partial_tree(p1, p2, max_depth, length)
        best_val = self.alfabeta(self.game_tree.nodes[0], search_depth, float('-inf'), float('inf'))
        return best_val

if __name__ == "__main__":
    # Example parameters for testing
    p1 = 80
    p2 = 80
    max_depth = 3      # Maximum depth for generating the tree
    search_depth = 3   # Depth for alpha-beta search
    alg = AlphaBetaALG()
    best_value = alg.get_best_value(p1, p2, max_depth, search_depth)
    print("Best value (AlphaBeta):", best_value)
    print("Nodes visited:", alg.nodes_visited)
