import random
from core.move import Move

def get_random_move(board_obj):
    """Renvoie un coup aléatoire pour l'IA noire"""
    all_moves = []

    # On récupère toutes les pièces de la couleur à jouer
    pieces = board_obj.get_all_pieces(board_obj.turn)

    for piece in pieces:
        moves = piece.get_legal_moves(board_obj)
        if moves:
            all_moves.extend(moves)

    # Choisir un coup au hasard parmi tous les coups légaux
    if all_moves:
        return random.choice(all_moves)

    # Aucun coup possible (échec et mat ou pat)
    return None
