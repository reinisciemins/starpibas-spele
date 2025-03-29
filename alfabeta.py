import math

def alphabeta_best_move(sequence, ai_points, player_points, depth):
    # Iekšējā funkcija alfa-beta vērtību aprēķinam
    def alphabeta(seq, ai_score, player_score, d, alpha, beta, is_ai_turn):
        if d == 0 or not seq:
            return ai_score - player_score  # Atgriež punktu starpību
        
        if is_ai_turn:
            max_eval = -math.inf
            for idx, value in list(seq.items()):
                new_ai_score = ai_score - value
                new_seq = {k: v for k, v in seq.items() if k != idx}
                eval = alphabeta(new_seq, new_ai_score, player_score, d-1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for idx, value in list(seq.items()):
                new_player_score = player_score - value
                new_seq = {k: v for k, v in seq.items() if k != idx}
                eval = alphabeta(new_seq, ai_score, new_player_score, d-1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    # Algoritma galvenā daļa, kas atgriež labāko gājienu
    best_move = None
    best_value = -math.inf
    for idx, value in list(sequence.items()):
        new_ai_points = ai_points - value
        new_seq = {k: v for k, v in sequence.items() if k != idx}
        value = alphabeta(new_seq, new_ai_points, player_points, depth-1, -math.inf, math.inf, False)
        if value > best_value:
            best_value = value
            best_move = value

    return best_move
