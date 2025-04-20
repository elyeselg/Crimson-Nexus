from core.pieces import Pawn, Rook, Knight, Bishop, Queen, King
from core.move import Move
from core.rules import is_fifty_move_rule
import copy

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.turn = 'white'
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
        self.move_history = []
        self.board_states = {}  # Pour la répétition
        self.piece_classes = {
            "Rook": Rook,
            "Pawn": Pawn,
            "Knight": Knight,
            "Bishop": Bishop,
            "Queen": Queen,
            "King": King
        }
        self.setup_board()
        self._checking_check = False

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

        self.record_board_state()

    def record_board_state(self):
        key = self._board_state_key()
        self.board_states[key] = self.board_states.get(key, 0) + 1

    def _board_state_key(self):
        flat = []
        for row in self.board:
            for piece in row:
                if piece:
                    flat.append((piece.__class__.__name__, piece.color, piece.pos))
                else:
                    flat.append(None)
        return tuple(flat + [self.turn])

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

        # Roque
        if move.is_castling and isinstance(piece, King):
            if end_col == 6:
                self.board[end_row][5] = self.board[end_row][7]
                self.board[end_row][7] = None
                self.board[end_row][5].pos = (end_row, 5)
            elif end_col == 2:
                self.board[end_row][3] = self.board[end_row][0]
                self.board[end_row][0] = None
                self.board[end_row][3].pos = (end_row, 3)

        # Prise en passant
        if move.is_en_passant and isinstance(piece, Pawn):
            capture_row = start_row
            capture_col = end_col
            captured = self.board[capture_row][capture_col]
            self.board[capture_row][capture_col] = None

        # Promotion
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

        self.record_board_state()

    def get_all_pieces(self, color):
        return [p for row in self.board for p in row if p and p.color == color]

    def get_valid_moves(self, piece):
        valid_moves = []
        if piece is None:
            return valid_moves

        for move in piece.get_legal_moves(self):
            temp_board = self.copy()
            temp_board.move_piece(move)
            if not temp_board.is_in_check(piece.color):
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

    def is_fifty_move_draw(self):
        return is_fifty_move_rule(self)

    def is_threefold_repetition(self):
        key = self._board_state_key()
        return self.board_states.get(key, 0) >= 3

    def is_insufficient_material(self):
        all_pieces = [p for row in self.board for p in row if p]
        if len(all_pieces) == 2:
            return True  # Roi vs Roi
        if len(all_pieces) == 3:
            types = {type(p).__name__ for p in all_pieces}
            if "Bishop" in types or "Knight" in types:
                return True  # Roi + fou/cavalier vs roi
        return False

    def is_draw(self, color):
        return (
            self.is_stalemate(color)
            or self.is_fifty_move_draw()
            or self.is_threefold_repetition()
            or self.is_insufficient_material()
        )

    def copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        return "\n".join(
            " ".join(piece.symbol if piece else "." for piece in row)
            for row in self.board
        )

    def get_end_message(self):
        """
        Retourne (winner, message) si la partie est terminée, sinon (None, None).
        """
        if self.is_checkmate(self.turn):
            winner = "Blancs" if self.turn == "black" else "Noirs"
            return winner, f"{winner} gagnent par échec et mat"
        elif self.is_stalemate(self.turn):
            return "Aucun", "Match nul par pat"
        elif self.is_fifty_move_draw():
            return "Aucun", "Match nul (règle des 50 coups)"
        elif self.is_threefold_repetition():
            return "Aucun", "Match nul (répétition de position)"
        elif self.is_insufficient_material():
            return "Aucun", "Match nul (matériel insuffisant)"
        return None, None
