from core.pieces import (
    Pawn, Rook, Knight, Bishop, Queen, King
)
from core.move import Move

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

    def setup_board(self):
        for col in range(8):
            self.board[1][col] = Pawn('black', (1, col))
            self.board[6][col] = Pawn('white', (6, col))

        self.board[0][0] = Rook('black', (0, 0))
        self.board[0][7] = Rook('black', (0, 7))
        self.board[7][0] = Rook('white', (7, 0))
        self.board[7][7] = Rook('white', (7, 7))

        self.board[0][1] = Knight('black', (0, 1))
        self.board[0][6] = Knight('black', (0, 6))
        self.board[7][1] = Knight('white', (7, 1))
        self.board[7][6] = Knight('white', (7, 6))

        self.board[0][2] = Bishop('black', (0, 2))
        self.board[0][5] = Bishop('black', (0, 5))
        self.board[7][2] = Bishop('white', (7, 2))
        self.board[7][5] = Bishop('white', (7, 5))

        self.board[0][3] = Queen('black', (0, 3))
        self.board[7][3] = Queen('white', (7, 3))

        self.board[0][4] = King('black', (0, 4))
        self.board[7][4] = King('white', (7, 4))

    def get_piece(self, pos):
        row, col = pos
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None

    def move_piece(self, move: Move):
        start_row, start_col = move.start_pos
        end_row, end_col = move.end_pos

        piece = self.board[start_row][start_col]
        captured = self.board[end_row][end_col]

        # Gérer le roque : déplace aussi la tour
        if move.is_castling and isinstance(piece, King):
            if end_col == 6:  # Petit roque
                self.board[end_row][5] = self.board[end_row][7]
                self.board[end_row][7] = None
                self.board[end_row][5].pos = (end_row, 5)
            elif end_col == 2:  # Grand roque
                self.board[end_row][3] = self.board[end_row][0]
                self.board[end_row][0] = None
                self.board[end_row][3].pos = (end_row, 3)

        # Déplacement normal
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = None
        piece.pos = (end_row, end_col)

        if hasattr(piece, 'has_moved'):
            piece.has_moved = True
        if isinstance(piece, Pawn):
            piece.first_move = False

        if isinstance(piece, King):
            if piece.color == 'white':
                self.white_king_pos = (end_row, end_col)
            else:
                self.black_king_pos = (end_row, end_col)

        move.piece_captured = captured
        self.move_history.append(move)

        self.turn = 'black' if self.turn == 'white' else 'white'

    def get_all_pieces(self, color):
        return [p for row in self.board for p in row if p and p.color == color]

    def get_valid_moves(self, piece):
        legal_moves = piece.get_legal_moves(self)
        valid = []
        for move in legal_moves:
            temp = self.copy()
            temp.move_piece(move)
            if not temp.is_in_check(piece.color):
                valid.append(move)
        return valid

    def is_in_check(self, color):
        king_pos = self.white_king_pos if color == 'white' else self.black_king_pos
        enemy_color = 'black' if color == 'white' else 'white'
        for piece in self.get_all_pieces(enemy_color):
            for move in piece.get_legal_moves(self):
                if move.end_pos == king_pos:
                    return True
        return False

    def square_under_attack(self, pos, color):
        enemy_color = 'black' if color == 'white' else 'white'
        for piece in self.get_all_pieces(enemy_color):
            for move in piece.get_legal_moves(self):
                if move.end_pos == pos:
                    return True
        return False

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False
        for piece in self.get_all_pieces(color):
            if self.get_valid_moves(piece):
                return False
        return True

    def is_stalemate(self, color):
        if self.is_in_check(color):
            return False
        for piece in self.get_all_pieces(color):
            if self.get_valid_moves(piece):
                return False
        return True

    def copy(self):
        import copy
        return copy.deepcopy(self)

    def __str__(self):
        rows = []
        for row in self.board:
            line = []
            for piece in row:
                if piece:
                    line.append(piece.symbol)
                else:
                    line.append('.')
            rows.append(" ".join(line))
        return "\n".join(rows)
