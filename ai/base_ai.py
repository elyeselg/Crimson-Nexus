import random

# Valeur de chaque pièce pour l’IA basique
PIECE_VALUE = {
    "Queen": 9,
    "Rook": 5,
    "Bishop": 3,
    "Knight": 3,
    "Pawn": 1,
    "King": 0  # Pas de valeur car non capturable
}

def get_random_move_smart(board_obj):
    """Renvoie un coup instantané pour les noirs, avec logique simple :
    - Favorise les captures les plus précieuses
    - Évite les suicides inutiles
    """
    all_moves = []

    # Récupère toutes les pièces noires
    pieces = board_obj.get_all_pieces("black")

    for piece in pieces:
        valid_moves = board_obj.get_valid_moves(piece)
        all_moves.extend(valid_moves)

    if not all_moves:
        return None

    # 1. Cherche les meilleures captures possibles
    capturing_moves = [m for m in all_moves if m.piece_captured]
    if capturing_moves:
        # Trie les captures par valeur décroissante
        capturing_moves.sort(
            key=lambda m: PIECE_VALUE.get(m.piece_captured.__class__.__name__, 0),
            reverse=True
        )
        return capturing_moves[0]  # capture la meilleure cible dispo

    # 2. Sinon, cherche un coup safe aléatoire
    safe_moves = []
    for move in all_moves:
        temp_board = board_obj.copy()
        temp_board.move_piece(move)

        # Si après le coup, la pièce n'est pas immédiatement prise, c’est safe
        after_piece = temp_board.get_piece(move.end_pos)
        if not temp_board.square_under_attack(move.end_pos, after_piece.color):
            safe_moves.append(move)

    if safe_moves:
        return random.choice(safe_moves)

    # 3. Sinon, pas le choix : joue n'importe quoi
    return random.choice(all_moves)
