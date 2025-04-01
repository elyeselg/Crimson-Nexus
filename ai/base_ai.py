import random

def get_random_move(board_obj):
    """Renvoie un coup aléatoire, mais favorise les captures de pièces ennemies."""
    all_moves = []

    pieces = board_obj.get_all_pieces("black")
    for piece in pieces:
        moves = board_obj.get_valid_moves(piece)
        if moves:
            all_moves.extend(moves)

    # Si possible, favorise les captures
    capturing_moves = [m for m in all_moves if m.piece_captured]
    if capturing_moves:
        return random.choice(capturing_moves)

    # Sinon, joue un coup au hasard
    return random.choice(all_moves) if all_moves else None
