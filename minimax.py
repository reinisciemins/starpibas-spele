import random


class MinimaxALG:
    def __init__(self):
        self.nodes_visited = 0  # skaitītājs apmeklētajiem mezgliem

    def evaluate(self, player_score, ai_score, remaining_moves):
        score_diff = ai_score - player_score
        # izvēlas gājienu kas atstāj pretiniekam mazāk iespēju
        return score_diff * 10 - remaining_moves

    def get_minimax_choice(self, game_data, player_score, ai_score, depth=4):
        self.nodes_visited = 0
        sequence = list(game_data.values())

        # iegūst visus derīgos gājienus (no mazākā uz lielāko)
        valid_moves = [i for i in range(len(sequence)) if sequence[i] <= ai_score]
        valid_moves.sort(key=lambda i: sequence[i])  # priekšroka mazākiem skaitļiem

        if not valid_moves:
            return None

        best_move_index = None
        best_value = float('-inf')

        for move_index in valid_moves:
            num = sequence[move_index]
            new_seq = sequence[:move_index] + sequence[move_index + 1:]
            new_ai_score = ai_score - num

            # aprēķina pretinieka atlikušos gājienus
            opp_valid_moves = sum(1 for x in new_seq if x <= player_score)

            _, current_value = self._minimax(
                new_seq,
                player_score,
                new_ai_score,
                depth - 1,
                False,
                opp_valid_moves,
                float('-inf'),
                float('inf')
            )

            # izvēlas labāko gājienu, ja vienādi - mazāko skaitli
            if current_value > best_value or (
                    current_value == best_value and sequence[move_index] < sequence[best_move_index]
            ):
                best_value = current_value
                best_move_index = move_index

        return sequence[best_move_index] if best_move_index is not None else random.choice(sequence)

    def _minimax(self, sequence, p_score, ai_score, depth, is_maximizing, remaining_moves, alpha, beta):
        self.nodes_visited += 1

        # terminālos stāvokļu pārbaude
        if depth == 0 or not sequence:
            return None, self.evaluate(p_score, ai_score, remaining_moves)

        valid_moves = [i for i in range(len(sequence)) if sequence[i] <= (ai_score if is_maximizing else p_score)]
        valid_moves.sort(key=lambda i: sequence[i])  # mazākie skaitļi vispirms

        if not valid_moves:
            return None, self.evaluate(p_score, ai_score, 0)

        best_index = None
        best_value = float('-inf') if is_maximizing else float('inf')

        for move_index in valid_moves:
            num = sequence[move_index]
            new_seq = sequence[:move_index] + sequence[move_index + 1:]

            if is_maximizing:  # datora gājiens
                new_ai_score = ai_score - num
                opp_moves = sum(1 for x in new_seq if x <= p_score)
                _, value = self._minimax(new_seq, p_score, new_ai_score, depth - 1, False, opp_moves, alpha, beta)

                if value > best_value:
                    best_value = value
                    best_index = move_index
                    alpha = max(alpha, value)
            else:  # spēlētāja gājiens
                new_p_score = p_score - num
                opp_moves = sum(1 for x in new_seq if x <= ai_score)
                _, value = self._minimax(new_seq, new_p_score, ai_score, depth - 1, True, opp_moves, alpha, beta)

                if value < best_value:
                    best_value = value
                    best_index = move_index
                    beta = min(beta, value)

            if alpha >= beta:
                break

        return best_index, best_value