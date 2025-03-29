class MinimaxALG:
    def __init__(self):
        self.nodes_visited = 0

    def evaluate(self, player_score, ai_score):
        return ai_score - player_score

    def get_minimax_choice(self, game_data, player_score, ai_score, depth=4):
        self.nodes_visited = 0
        sequence = list(game_data.values())

        # iegūst visus derīgus gājienus
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

            _, current_value = self._minimax(
                new_seq,
                player_score,
                new_ai_score,
                depth - 1,
                False,
                alpha,
                beta
            )

            # labākā gadījuma izvēle
            if current_value > best_value or (
                    current_value == best_value and sequence[move_index] < sequence[best_move_index]
            ):
                best_value = current_value
                best_move_index = move_index
                alpha = max(alpha, best_value)

        return sequence[best_move_index] if best_move_index is not None else None

    def _minimax(self, sequence, p_score, ai_score, depth, is_maximizing, alpha, beta):
        self.nodes_visited += 1


        if depth == 0 or not sequence:
            return None, self.evaluate(p_score, ai_score)

        # gājiena izvēle
        valid_moves = [i for i in range(len(sequence)) if sequence[i] <= (ai_score if is_maximizing else p_score)]
        valid_moves.sort(key=lambda i: sequence[i])

        if not valid_moves:
            return None, self.evaluate(p_score, ai_score)

        best_index = None
        best_value = float('-inf') if is_maximizing else float('inf')

        for move_index in valid_moves:
            num = sequence[move_index]
            new_seq = sequence[:move_index] + sequence[move_index + 1:]

            if is_maximizing:  # dators
                new_ai_score = ai_score - num
                _, value = self._minimax(new_seq, p_score, new_ai_score, depth - 1, False, alpha, beta)

                if value > best_value:
                    best_value = value
                    best_index = move_index
                    alpha = max(alpha, best_value)
            else:  # spēlētājs
                new_p_score = p_score - num
                _, value = self._minimax(new_seq, new_p_score, ai_score, depth - 1, True, alpha, beta)

                if value < best_value:
                    best_value = value
                    best_index = move_index
                    beta = min(beta, best_value)

            if alpha >= beta:
                break

        return best_index, best_value