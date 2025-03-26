# ai/evaluator.py

import copy

PIECE_VALUES = {
    "Pawn": 1,
    "Knight": 3.2,
    "Bishop": 3.3,
    "Rook": 5,
    "Queen": 9,
    "King": 1000  # On n'autorise pas de perdre le roi
}

CENTER_SQUARES = [(3, 3), (3, 4), (4, 3), (4, 4)]

def evaluate_board(board):
    score = 0

    for row in range(8):
        for col in range(8):
            piece = board.board[row][col]
            if piece:
                value = PIECE_VALUES.get(piece.__class__.__name__, 0)
                color = piece.color

                # Contrôle du centre
                center_bonus = 0.3 if (row, col) in CENTER_SQUARES else 0

                # Mobilité
                mobility = len(board.get_valid_moves(piece)) * 0.04

                # Activité : pièce avancée = mieux (hors pion)
                activity_bonus = 0
                if piece.__class__.__name__ != "Pawn":
                    activity_bonus = (7 - row if color == "black" else row) * 0.02

                piece_score = value + center_bonus + mobility + activity_bonus
                score += piece_score if color == "black" else -piece_score

    return score


def alphabeta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_checkmate(board.turn) or board.is_stalemate(board.turn):
        return evaluate_board(board), None

    best_move = None
    pieces = board.get_all_pieces(board.turn)

    if maximizing_player:
        max_eval = float('-inf')
        for piece in pieces:
            for move in board.get_valid_moves(piece):
                temp = board.copy()
                temp.move_piece(move)
                eval_score, _ = alphabeta(temp, depth - 1, alpha, beta, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
        return max_eval, best_move

    else:
        min_eval = float('inf')
        for piece in pieces:
            for move in board.get_valid_moves(piece):
                temp = board.copy()
                temp.move_piece(move)
                eval_score, _ = alphabeta(temp, depth - 1, alpha, beta, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
        return min_eval, best_move


def get_best_move_alphabeta(board, depth=3):
    _, best_move = alphabeta(board, depth, float("-inf"), float("inf"), True)
    return best_move
