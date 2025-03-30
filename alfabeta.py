class Node:
    def __init__(self, sequence, player_score, ai_score, move=None, level=0, is_max=True, value=None):
        self.sequence = sequence
        self.player_score = player_score
        self.ai_score = ai_score
        self.move = move
        self.level = level
        self.is_max = is_max
        self.value = value
        self.children = []

class GameTree:
    def __init__(self):
        self.root = None
        self.nodes = []

    def add_node(self, parent, sequence, player_score, ai_score, move, level, is_max):
        node = Node(sequence, player_score, ai_score, move, level, is_max)
        if parent:
            parent.children.append(node)
        else:
            self.root = node
        self.nodes.append(node)
        return node

class AlphaBetaALG:
    def __init__(self):
        self.nodes_visited = 0
        self.game_tree = GameTree()

    def evaluate(self, player_score, ai_score):
        return ai_score - player_score

    def get_best_move(self, sequence, player_score, ai_score, depth=4):
        self.nodes_visited = 0
        root_node = self.game_tree.add_node(None, sequence, player_score, ai_score, None, 0, True)
        best_value = float('-inf')
        best_move = None

        for move in sorted(sequence):
            if move > ai_score:
                continue

            new_sequence = sequence[:]
            new_sequence.remove(move)
            new_ai_score = ai_score - move

            _, value = self._alpha_beta(new_sequence, player_score, new_ai_score, depth - 1, False, float('-inf'), float('inf'), root_node, move)

            if value > best_value:
                best_value = value
                best_move = move

        root_node.value = best_value  # Set the value at root after all children are evaluated
        return best_move

    def _alpha_beta(self, sequence, p_score, ai_score, depth, is_maximizing, alpha, beta, parent_node, move):
        current_node = self.game_tree.add_node(parent_node, sequence, p_score, ai_score, move, parent_node.level + 1, is_maximizing)
        self.nodes_visited += 1

        if depth == 0 or not sequence:
            current_node.value = self.evaluate(p_score, ai_score)
            return None, current_node.value

        if is_maximizing:
            max_eval = float('-inf')
            for move in sorted(sequence):
                if move > ai_score:
                    continue
                new_sequence = sequence[:]
                new_sequence.remove(move)
                _, eval = self._alpha_beta(new_sequence, p_score, ai_score - move, depth - 1, False, alpha, beta, current_node, move)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if alpha >= beta:
                    break
            current_node.value = max_eval
            return None, max_eval
        else:
            min_eval = float('inf')
            for move in sorted(sequence):
                if move > p_score:
                    continue
                new_sequence = sequence[:]
                new_sequence.remove(move)
                _, eval = self._alpha_beta(new_sequence, p_score - move, ai_score, depth - 1, True, alpha, beta, current_node, move)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            current_node.value = min_eval
            return None, min_eval

    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.game_tree.root
        print('  ' * level + f'Node({node.move}): Seq={node.sequence}, P={node.player_score}, AI={node.ai_score}, Val={node.value}')
        for child in node.children:
            self.print_tree(child, level + 1)

# Example usage
if __name__ == "__main__":
    alg = AlphaBetaALG()
    game_data = [1, 2, 3]
    player_score = 5
    ai_score = 5
    best_move = alg.get_best_move(game_data, player_score, ai_score)
    print("Best move:", best_move)
    print("Game tree:")
    alg.print_tree()

