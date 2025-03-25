# ai/minimax.py

from core.move import Move
import copy

PIECE_VALUES = {
    "Pawn": 1,
    "Knight": 3,
    "Bishop": 3,
    "Rook": 5,
    "Queen": 9,
    "King": 1000  # Élevé car la perte du roi = fin de partie
}

def evaluate_board(board):
    score = 0
    for row in board.board:
        for piece in row:
            if piece:
                value = PIECE_VALUES.get(piece.__class__.__name__, 0)
                score += value if piece.color == "black" else -value
    return score

def minimax(board, depth, maximizing_player):
    if depth == 0:
        return evaluate_board(board), None

    possible_moves = []

    for piece in board.get_all_pieces(board.turn):
        for move in piece.get_legal_moves(board):
            possible_moves.append(move)

    if not possible_moves:
        return evaluate_board(board), None

    best_move = None

    if maximizing_player:
        max_eval = float("-inf")
        for move in possible_moves:
            temp_board = copy.deepcopy(board)
            temp_board.move_piece(move)
            eval_score, _ = minimax(temp_board, depth - 1, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move

    else:
        min_eval = float("inf")
        for move in possible_moves:
            temp_board = copy.deepcopy(board)
            temp_board.move_piece(move)
            eval_score, _ = minimax(temp_board, depth - 1, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return min_eval, best_move


def get_minimax_move(board, depth=2):
    """Renvoie le meilleur coup trouvé par minimax pour l'IA noire"""
    _, best_move = minimax(board, depth, True)
    return best_move
