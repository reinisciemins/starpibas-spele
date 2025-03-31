from dataStructure import Node, GameTree

class MinimaxALG:
    def __init__(self):
        self.nodes_visited = 0
        self.game_tree = GameTree()
        self.current_id = 0

    def evaluate(self, player_score, ai_score):
        return (ai_score - player_score) * 10

    def get_minimax_choice(self, game_data, player_score, ai_score, depth=4):
        self.nodes_visited = 0
        sequence = list(game_data.values())
        root_node = self.game_tree.add_node(None, sequence, player_score, ai_score, 0)

        valid_moves = [i for i in range(len(sequence)) if sequence[i] <= ai_score]
        valid_moves.sort(key=lambda i: sequence[i])

        if not valid_moves:
            return None

        best_move_index = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for move_index in valid_moves:
            num = sequence[move_index]
            new_seq = sequence[:move_index] + sequence[move_index + 1:]
            new_ai_score = ai_score - num

            # rekursivi veido koku
            _, current_value = self._minimax(
                new_seq,
                player_score,
                new_ai_score,
                depth - 1,
                False,
                alpha,
                beta,
                root_node
            )

            if current_value > best_value or (
                    current_value == best_value and sequence[move_index] < sequence[best_move_index]
            ):
                best_value = current_value
                best_move_index = move_index
                alpha = max(alpha, best_value)

        # atjauno sakni ar labako vertibu
        root_node.value = best_value
        return sequence[best_move_index] if best_move_index is not None else None

    def _minimax(self, sequence, p_score, ai_score, depth, is_maximizing, alpha, beta, parent_node=None):
        self.nodes_visited += 1

        # izveido jaunu node
        current_node = self.game_tree.add_node(
            parent_node,
            sequence,
            p_score,
            ai_score,
            depth,
            self.evaluate(p_score, ai_score)
        )

        if depth == 0 or not sequence:
            return None, self.evaluate(p_score, ai_score)

        valid_moves = [i for i in range(len(sequence)) if sequence[i] <= (ai_score if is_maximizing else p_score)]
        valid_moves.sort(key=lambda i: sequence[i])

        if not valid_moves:
            return None, self.evaluate(p_score, ai_score)

        best_index = None
        best_value = float('-inf') if is_maximizing else float('inf')

        for move_index in valid_moves:
            num = sequence[move_index]
            new_seq = sequence[:move_index] + sequence[move_index + 1:]

            if is_maximizing:  # datora gajiens
                new_ai_score = ai_score - num
                _, value = self._minimax(new_seq, p_score, new_ai_score, depth - 1, False, alpha, beta, current_node)

                if value > best_value:
                    best_value = value
                    best_index = move_index
                    alpha = max(alpha, best_value)
            else:  # speletaja gajiens
                new_p_score = p_score - num
                _, value = self._minimax(new_seq, new_p_score, ai_score, depth - 1, True, alpha, beta, current_node)

                if value < best_value:
                    best_value = value
                    best_index = move_index
                    beta = min(beta, best_value)

            if alpha >= beta:
                break

        # atjauno node vertibu
        current_node.value = best_value
        return best_index, best_value

    def print_tree(self, node=None, indent=0):
        if node is None:
            node = self.game_tree.root

        print(
            " " * indent + f"{node.id}: Seq={node.sequence}, P={node.player_score}, AI={node.ai_score}, Val={node.value}")
        for child in node.children:
            self.print_tree(child, indent + 2)


# ja vajag parbaudit vai tiek generets dalejs koks
if __name__ == "__main__":
    minimax = MinimaxALG()
    game_data = {0: 1, 1: 2, 2: 3}
    player_score = 5
    ai_score = 5

    best_move = minimax.get_minimax_choice(game_data, player_score, ai_score)
    print(f"Best move: {best_move}")
    print("Game tree:")
    minimax.print_tree()