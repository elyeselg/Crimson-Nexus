# ai/base_ai.py

import random

def get_random_move(board_obj):
    """Renvoie un coup aléatoire légal pour l'IA noire"""
    all_moves = []

    pieces = board_obj.get_all_pieces("black")

    for piece in pieces:
        moves = board_obj.get_valid_moves(piece)
        if moves:
            all_moves.extend(moves)

    if all_moves:
        return random.choice(all_moves)

    return None  # Aucun coup possible (mat ou pat)
