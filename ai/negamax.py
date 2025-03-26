import copy
from core.move import Move

PIECE_VALUES = {
    "Pawn": 1,
    "Knight": 3,
    "Bishop": 3.2,
    "Rook": 5,
    "Queen": 9,
    "King": 0  # Le roi n'est pas compté dans la valeur brute
}

CENTER_SQUARES = [(3, 3), (3, 4), (4, 3), (4, 4)]

def evaluate_board(board):
    score = 0

    for row in range(8):
        for col in range(8):
            piece = board.board[row][col]
            if piece:
                value = PIECE_VALUES.get(piece.__class__.__name__, 0)

                # Contrôle du centre
                center_bonus = 0.2 if (row, col) in CENTER_SQUARES else 0

                # Mobilité
                mobility = len(board.get_valid_moves(piece)) * 0.05

                # Défense du roi (éviter qu’il soit seul)
                if piece.__class__.__name__ == "King":
                    neighbors = get_king_safety_score(board, piece.pos)
                    mobility -= 0.05 * neighbors  # moins bon s’il est isolé

                total = value + center_bonus + mobility
                score += total if piece.color == "black" else -total

    return score


def get_king_safety_score(board, king_pos):
    """Renvoie le nombre de pièces alliées autour du roi"""
    row, col = king_pos
    allies = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board.get_piece((r, c))
                if piece and piece.color == board.get_piece(king_pos).color:
                    allies += 1
    return allies


def negamax(board, depth):
    if depth == 0 or board.is_checkmate(board.turn) or board.is_stalemate(board.turn):
        return evaluate_board(board), None

    max_eval = float('-inf')
    best_move = None

    pieces = board.get_all_pieces(board.turn)
    for piece in pieces:
        for move in board.get_valid_moves(piece):
            temp = board.copy()
            temp.move_piece(move)
            score, _ = negamax(temp, depth - 1)
            score = -score  # inversion pour Negamax

            if score > max_eval:
                max_eval = score
                best_move = move

    return max_eval, best_move


def get_negamax_move(board, depth=2):
    _, best_move = negamax(board, depth)
    return best_move
