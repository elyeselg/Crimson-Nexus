from core.move import Move


def get_legal_moves(piece, board_obj):
    """Router : redirige vers la bonne fonction selon la pièce"""
    if piece is None:
        return []

    if piece.__class__.__name__ == "Pawn":
        return get_pawn_moves(piece, board_obj)
    elif piece.__class__.__name__ == "Rook":
        return get_rook_moves(piece, board_obj)
    elif piece.__class__.__name__ == "Knight":
        return get_knight_moves(piece, board_obj)
    elif piece.__class__.__name__ == "Bishop":
        return get_bishop_moves(piece, board_obj)
    elif piece.__class__.__name__ == "Queen":
        return get_queen_moves(piece, board_obj)
    elif piece.__class__.__name__ == "King":
        return get_king_moves(piece, board_obj)
    else:
        return []


def get_pawn_moves(pawn, board_obj):
    moves = []
    row, col = pawn.pos
    direction = -1 if pawn.color == 'white' else 1
    board = board_obj.board

    # Avancer de 1
    if board[row + direction][col] is None:
        moves.append(Move((row, col), (row + direction, col), pawn))

        # Avancer de 2 si première fois
        if pawn.first_move and board[row + 2 * direction][col] is None:
            moves.append(Move((row, col), (row + 2 * direction, col), pawn))

    # Captures diagonales
    for dcol in [-1, 1]:
        new_col = col + dcol
        new_row = row + direction
        if 0 <= new_col < 8 and 0 <= new_row < 8:
            target = board[new_row][new_col]
            if target and target.color != pawn.color:
                moves.append(Move((row, col), (new_row, new_col), pawn, target))

    # TODO : prise en passant (plus tard)
    return moves


def get_rook_moves(rook, board_obj):
    return get_linear_moves(rook, board_obj, directions=[(1, 0), (-1, 0), (0, 1), (0, -1)])


def get_bishop_moves(bishop, board_obj):
    return get_linear_moves(bishop, board_obj, directions=[(1, 1), (-1, -1), (1, -1), (-1, 1)])


def get_queen_moves(queen, board_obj):
    return get_linear_moves(queen, board_obj, directions=[
        (1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (-1, -1), (1, -1), (-1, 1)
    ])


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


def get_king_moves(king, board_obj):
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

    # === Roque (petit et grand) ===
    if not king.has_moved and not board_obj.is_in_check(king.color):
        back_row = 7 if king.color == "white" else 0

        # Petit roque (côté roi)
        rook = board[back_row][7]
        if isinstance(rook, board_obj.piece_classes["Rook"]) and not rook.has_moved:
            if board[back_row][5] is None and board[back_row][6] is None:
                if not board_obj.square_under_attack((back_row, 5), king.color) and \
                   not board_obj.square_under_attack((back_row, 6), king.color):
                    moves.append(Move((row, col), (back_row, 6), king, is_castling=True))

        # Grand roque (côté dame)
        rook = board[back_row][0]
        if isinstance(rook, board_obj.piece_classes["Rook"]) and not rook.has_moved:
            if board[back_row][1] is None and board[back_row][2] is None and board[back_row][3] is None:
                if not board_obj.square_under_attack((back_row, 2), king.color) and \
                   not board_obj.square_under_attack((back_row, 3), king.color):
                    moves.append(Move((row, col), (back_row, 2), king, is_castling=True))

    return moves
