class AlphaBetaALG:
    def __init__(self):
        self.nodes_visited = 0

    def evaluate(self, ai_points, human_points):
        # Pārbauda, vai kāds spēlētājs ir zaudējis, ja viņa punkti ir 0 vai mazāk
        if ai_points <= 0 and human_points <= 0:
            return 0  # Neizšķirts
        elif ai_points <= 0:
            return float('-inf')  # Ļoti slikts AI
        elif human_points <= 0:
            return float('inf')  # Ļoti labs AI
        # Heuristiska vērtēšana parasti
        return ai_points - human_points

    def get_best_move(self, sequence, ai_points, human_points, depth=4):
        self.nodes_visited = 0
        best_move = None
        best_value = float('-inf')
        moves = sorted(sequence)
        last_move = None
        for move in moves:
            if move == last_move:
                continue
            last_move = move
            if move > ai_points:
                continue
            new_sequence = sequence.copy()
            new_sequence.remove(move)
            new_ai_points = ai_points - move
            value = self._alpha_beta(new_sequence, new_ai_points, human_points, depth - 1, float('-inf'), float('inf'), False)
            if value > best_value:
                best_value = value
                best_move = move
        return best_move

    def _alpha_beta(self, sequence, ai_points, human_points, depth, alpha, beta, maximizing):
        self.nodes_visited += 1
        if depth == 0 or not sequence or ai_points <= 0 or human_points <= 0:
            return self.evaluate(ai_points, human_points)
        if maximizing:
            max_eval = float('-inf')
            for move in sorted(sequence):
                if move > ai_points:
                    continue
                new_sequence = sequence.copy()
                new_sequence.remove(move)
                new_ai_points = ai_points - move
                eval_val = self._alpha_beta(new_sequence, new_ai_points, human_points, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_val)
                alpha = max(alpha, eval_val)
                if alpha >= beta:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in sorted(sequence):
                if move > human_points:
                    continue
                new_sequence = sequence.copy()
                new_sequence.remove(move)
                new_human_points = human_points - move
                eval_val = self._alpha_beta(new_sequence, ai_points, new_human_points, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_val)
                beta = min(beta, eval_val)
                if beta <= alpha:
                    break
            return min_eval
