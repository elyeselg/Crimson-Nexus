import copy

PIECE_VALUES = {
    "Pawn": 1,
    "Knight": 3,
    "Bishop": 3,
    "Rook": 5,
    "Queen": 9,
    "King": 0  # Le roi ne compte pas dans l'évaluation brute
}

def evaluate_board(board):
    score = 0
    for row in range(8):
        for col in range(8):
            piece = board.board[row][col]
            if piece:
                value = PIECE_VALUES.get(piece.__class__.__name__, 0)
                score += value if piece.color == "black" else -value
    return score

def negamax(board, depth):
    if depth == 0 or board.is_checkmate(board.turn) or board.is_stalemate(board.turn):
        return evaluate_board(board), None

    max_eval = float('-inf')
    best_move = None

    for piece in board.get_all_pieces(board.turn):
        for move in board.get_valid_moves(piece):
            temp = board.copy()
            temp.move_piece(move)
            score, _ = negamax(temp, depth - 1)
            score = -score
            if score > max_eval:
                max_eval = score
                best_move = move

    return max_eval, best_move

def get_negamax_move(board, depth=2):
    _, best_move = negamax(board, depth)
    return best_move
