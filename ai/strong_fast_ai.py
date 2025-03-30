import copy

PIECE_VALUES = {
    "Pawn": 1,
    "Knight": 3.2,
    "Bishop": 3.3,
    "Rook": 5,
    "Queen": 9,
    "King": 1000
}

CENTER_SQUARES = {(3, 3), (3, 4), (4, 3), (4, 4)}

def evaluate_board(board):
    score = 0
    for row in range(8):
        for col in range(8):
            piece = board.board[row][col]
            if piece:
                val = PIECE_VALUES.get(piece.__class__.__name__, 0)
                color = piece.color
                center_bonus = 0.3 if (row, col) in CENTER_SQUARES else 0
                activity = (7 - row if color == "black" else row) * 0.01 if piece.__class__.__name__ != "Pawn" else 0
                score += (val + center_bonus + activity) * (1 if color == "black" else -1)
    return score

def order_moves(moves, maximizing):
    def move_score(move):
        captured = move.piece_captured
        return PIECE_VALUES.get(captured.__class__.__name__, 0) if captured else 0
    return sorted(moves, key=move_score, reverse=maximizing)

def fast_alphabeta(board, depth, alpha, beta, maximizing):
    if depth == 0 or board.is_checkmate(board.turn) or board.is_stalemate(board.turn):
        return evaluate_board(board), None

    best_move = None
    all_moves = []
    for piece in board.get_all_pieces(board.turn):
        all_moves.extend(board.get_valid_moves(piece))

    ordered_moves = order_moves(all_moves, maximizing)

    if maximizing:
        max_eval = float('-inf')
        for move in ordered_moves:
            temp = board.copy()
            temp.move_piece(move)
            eval_score, _ = fast_alphabeta(temp, depth - 1, alpha, beta, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in ordered_moves:
            temp = board.copy()
            temp.move_piece(move)
            eval_score, _ = fast_alphabeta(temp, depth - 1, alpha, beta, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def get_fast_strong_ai_move(board, depth=3):
    _, best = fast_alphabeta(board, depth, float("-inf"), float("inf"), True)
    return best
