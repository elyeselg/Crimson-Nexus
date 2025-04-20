from core.move import Move

# === RÈGLE 50 COUPS ===
def is_fifty_move_rule(board_obj):
    count = 0
    for move in reversed(board_obj.move_history):
        if isinstance(move.piece_moved, board_obj.piece_classes["Pawn"]) or move.piece_captured:
            break
        count += 1
        if count >= 50:
            return True
    return False

def get_legal_moves(piece, board_obj):
    if piece is None:
        return []

    name = piece.__class__.__name__
    if name == "Pawn":
        return get_pawn_moves(piece, board_obj)
    elif name == "Rook":
        return get_rook_moves(piece, board_obj)
    elif name == "Knight":
        return get_knight_moves(piece, board_obj)
    elif name == "Bishop":
        return get_bishop_moves(piece, board_obj)
    elif name == "Queen":
        return get_queen_moves(piece, board_obj)
    elif name == "King":
        safe = getattr(board_obj, "_checking_check", False)
        return get_king_moves(piece, board_obj, safe_mode=safe)
    return []

# === Pièces linéaires ===

def get_linear_moves(piece, board_obj, directions):
    moves = []
    row, col = piece.pos
    board = board_obj.board

    for d_row, d_col in directions:
        r, c = row + d_row, col + d_col
        while 0 <= r < 8 and 0 <= c < 8:
            target = board[r][c]
            if target is None:
                moves.append(Move((row, col), (r, c), piece))
            elif target.color != piece.color:
                moves.append(Move((row, col), (r, c), piece, target))
                break
            else:
                break
            r += d_row
            c += d_col
    return moves

def get_rook_moves(piece, board_obj):
    return get_linear_moves(piece, board_obj, [(1, 0), (-1, 0), (0, 1), (0, -1)])

def get_bishop_moves(piece, board_obj):
    return get_linear_moves(piece, board_obj, [(1, 1), (-1, -1), (1, -1), (-1, 1)])

def get_queen_moves(piece, board_obj):
    return get_linear_moves(piece, board_obj, [
        (1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (-1, -1), (1, -1), (-1, 1)
    ])

# === Cavalier ===

def get_knight_moves(knight, board_obj):
    moves = []
    row, col = knight.pos
    board = board_obj.board
    directions = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            target = board[r][c]
            if target is None or target.color != knight.color:
                moves.append(Move((row, col), (r, c), knight, target))
    return moves

# === Pion ===

def get_pawn_moves(pawn, board_obj):
    moves = []
    row, col = pawn.pos
    direction = -1 if pawn.color == 'white' else 1
    board = board_obj.board
    promotion_row = 0 if pawn.color == 'white' else 7

    # Avancer d'une case
    next_row = row + direction
    if 0 <= next_row < 8 and board[next_row][col] is None:
        if next_row == promotion_row:
            moves.append(Move((row, col), (next_row, col), pawn, promotion="Queen"))
        else:
            moves.append(Move((row, col), (next_row, col), pawn))

        # Double avancée si premier coup
        double_row = row + 2 * direction
        if pawn.first_move and 0 <= double_row < 8 and board[double_row][col] is None:
            moves.append(Move((row, col), (double_row, col), pawn))

    # Captures diagonales
    for dcol in [-1, 1]:
        new_col = col + dcol
        new_row = row + direction
        if 0 <= new_col < 8 and 0 <= new_row < 8:
            target = board[new_row][new_col]
            if target and target.color != pawn.color:
                if new_row == promotion_row:
                    moves.append(Move((row, col), (new_row, new_col), pawn, target, promotion="Queen"))
                else:
                    moves.append(Move((row, col), (new_row, new_col), pawn, target))

    # Prise en passant
    if board_obj.move_history:
        last_move = board_obj.move_history[-1]
        if last_move and isinstance(last_move.piece_moved, type(pawn)) \
           and abs(last_move.start_pos[0] - last_move.end_pos[0]) == 2:
            if last_move.end_pos[0] == row and abs(last_move.end_pos[1] - col) == 1:
                if last_move.piece_moved.color != pawn.color:
                    capture_col = last_move.end_pos[1]
                    capture_piece = board[row][capture_col]
                    end_pos = (row + direction, capture_col)
                    if capture_piece and capture_piece.color != pawn.color:
                        moves.append(Move((row, col), end_pos, pawn, capture_piece, is_en_passant=True))
    return moves

# === Roi ===

def get_king_moves(king, board_obj, safe_mode=False):
    moves = []
    row, col = king.pos
    board = board_obj.board
    directions = [
        (1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (-1, -1), (1, -1), (-1, 1)
    ]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            target = board[r][c]
            if target is None or target.color != king.color:
                moves.append(Move((row, col), (r, c), king, target))

    if safe_mode:
        return moves

    if not king.has_moved and not board_obj.is_in_check(king.color):
        back_row = 7 if king.color == "white" else 0

        # Petit roque
        rook_k = board[back_row][7]
        if isinstance(rook_k, board_obj.piece_classes["Rook"]) and not rook_k.has_moved:
            if all(board[back_row][col] is None for col in [5, 6]):
                if not board_obj.square_under_attack((back_row, 5), king.color) and \
                   not board_obj.square_under_attack((back_row, 6), king.color):
                    moves.append(Move((row, col), (back_row, 6), king, is_castling=True))

        # Grand roque
        rook_q = board[back_row][0]
        if isinstance(rook_q, board_obj.piece_classes["Rook"]) and not rook_q.has_moved:
            if all(board[back_row][col] is None for col in [1, 2, 3]):
                if not board_obj.square_under_attack((back_row, 2), king.color) and \
                   not board_obj.square_under_attack((back_row, 3), king.color):
                    moves.append(Move((row, col), (back_row, 2), king, is_castling=True))
    return moves
