class AlphaBetaALG:
    def __init__(self):
        # Iekšējs skaitītājs, cik mezgli (stāvokļi) pārmeklēti
        self.nodes_visited = 0

    def get_best_move(self, ai_score, opp_score, depth, is_ai_turn=True):
        # Inicializē mezglu skaitītāju un alfa-beta sākumvērtības
        self.nodes_visited = 0
        alpha = float('-inf')
        beta = float('inf')
        best_move = None
        best_value = float('-inf') if is_ai_turn else float('inf')

        # Ģenerējam visus iespējamos gājienus no dotā stāvokļa
        moves = [m for m in [1, 2, 3] if (ai_score if is_ai_turn else opp_score) - m >= 0]
        for move in moves:
            new_ai = ai_score - move if is_ai_turn else ai_score
            new_opp = opp_score - move if not is_ai_turn else opp_score
            value = self._alpha_beta(new_ai, new_opp, depth - 1, alpha, beta, not is_ai_turn)
            if is_ai_turn and value > best_value:
                best_value = value
                best_move = move
                alpha = max(alpha, value)
            if not is_ai_turn and value < best_value:
                best_value = value
                best_move = move
                beta = min(beta, value)
            if beta <= alpha:
                break
        return best_move, best_value

    def _alpha_beta(self, ai_score, opp_score, depth, alpha, beta, is_ai_turn):
        self.nodes_visited += 1
        if depth == 0 or ai_score == 0 or opp_score == 0:
            return self._evaluate(ai_score, opp_score)

        moves = [m for m in [1, 2, 3] if (ai_score if is_ai_turn else opp_score) - m >= 0]
        if is_ai_turn:
            max_eval = float('-inf')
            for move in moves:
                new_ai = ai_score - move
                new_opp = opp_score
                eval_val = self._alpha_beta(new_ai, new_opp, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_val)
                alpha = max(alpha, eval_val)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                new_ai = ai_score
                new_opp = opp_score - move
                eval_val = self._alpha_beta(new_ai, new_opp, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_val)
                beta = min(beta, eval_val)
                if beta <= alpha:
                    break
            return min_eval

    def _evaluate(self, ai_score, opp_score):
        if ai_score == 0 or opp_score == 0:
            if ai_score > opp_score:
                return float('inf')
            elif ai_score < opp_score:
                return float('-inf')
            else:
                return 0
        point_diff = ai_score - opp_score
        opp_moves = 3 - min(3, opp_score)
        return point_diff + (3 - opp_moves)
