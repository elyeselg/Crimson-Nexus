from core.pieces import Pawn, Rook, Knight, Bishop, Queen, King
from core.move import Move
import copy


class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.turn = 'white'
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
        self.move_history = []
        self.piece_classes = {
            "Rook": Rook,
            "Pawn": Pawn,
            "Knight": Knight,
            "Bishop": Bishop,
            "Queen": Queen,
            "King": King
        }
        self.setup_board()
        self._checking_check = False  # Pour bloquer le roque quand on vérifie l'échec

    def setup_board(self):
        for col in range(8):
            self.board[1][col] = Pawn('black', (1, col))
            self.board[6][col] = Pawn('white', (6, col))

        placements = [
            (Rook, [0, 7]),
            (Knight, [1, 6]),
            (Bishop, [2, 5]),
            (Queen, [3]),
            (King, [4]),
        ]

        for cls, cols in placements:
            for col in cols:
                self.board[0][col] = cls('black', (0, col))
                self.board[7][col] = cls('white', (7, col))

    def get_piece(self, pos):
        row, col = pos
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None

    def move_piece(self, move: Move):
        start_row, start_col = move.start_pos
        end_row, end_col = move.end_pos

        piece = self.board[start_row][start_col]
        captured = move.piece_captured

        # === Roque ===
        if move.is_castling and isinstance(piece, King):
            if end_col == 6:  # Petit roque
                self.board[end_row][5] = self.board[end_row][7]
                self.board[end_row][7] = None
                self.board[end_row][5].pos = (end_row, 5)
            elif end_col == 2:  # Grand roque
                self.board[end_row][3] = self.board[end_row][0]
                self.board[end_row][0] = None
                self.board[end_row][3].pos = (end_row, 3)

        # === Prise en passant ===
        if move.is_en_passant and isinstance(piece, Pawn):
            capture_row = start_row
            capture_col = end_col
            captured = self.board[capture_row][capture_col]
            self.board[capture_row][capture_col] = None

        # === Promotion ===
        if move.promotion and isinstance(piece, Pawn):
            promoted_piece = self.piece_classes[move.promotion](piece.color, (end_row, end_col))
            self.board[end_row][end_col] = promoted_piece
        else:
            self.board[end_row][end_col] = piece
            piece.pos = (end_row, end_col)

        self.board[start_row][start_col] = None

        if hasattr(piece, "has_moved"):
            piece.has_moved = True
        if isinstance(piece, Pawn):
            piece.first_move = False

        if isinstance(piece, King):
            if piece.color == "white":
                self.white_king_pos = (end_row, end_col)
            else:
                self.black_king_pos = (end_row, end_col)

        move.piece_captured = captured
        self.move_history.append(move)
        self.turn = 'black' if self.turn == 'white' else 'white'

    def get_all_pieces(self, color):
        return [p for row in self.board for p in row if p and p.color == color]

    def get_valid_moves(self, piece):
        valid_moves = []
        for move in piece.get_legal_moves(self):
            temp = self.copy()
            temp.move_piece(copy.deepcopy(move))
            if not temp.is_in_check(piece.color):
                valid_moves.append(move)
        return valid_moves

    def is_in_check(self, color):
        self._checking_check = True
        king_pos = self.white_king_pos if color == 'white' else self.black_king_pos
        enemy_color = 'black' if color == 'white' else 'white'

        try:
            for piece in self.get_all_pieces(enemy_color):
                for move in piece.get_legal_moves(self):
                    if move.end_pos == king_pos:
                        return True
            return False
        finally:
            self._checking_check = False

    def square_under_attack(self, pos, color):
        enemy_color = 'black' if color == 'white' else 'white'
        for enemy in self.get_all_pieces(enemy_color):
            for move in enemy.get_legal_moves(self):
                if move.end_pos == pos:
                    return True
        return False

    def is_checkmate(self, color):
        return self.is_in_check(color) and all(
            not self.get_valid_moves(piece) for piece in self.get_all_pieces(color)
        )

    def is_stalemate(self, color):
        return not self.is_in_check(color) and all(
            not self.get_valid_moves(piece) for piece in self.get_all_pieces(color)
        )

    def copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        return "\n".join(
            " ".join(piece.symbol if piece else "." for piece in row)
            for row in self.board
        )
