from core.rules import get_legal_moves

class Piece:
    def __init__(self, color, pos):
        self.color = color              # 'white' ou 'black'
        self.pos = pos                  # (row, col)
        self.symbol = ''                # Unicode pour affichage
        self.name = ''                  # Nom court : ex "P", "K", etc.

    def get_legal_moves(self, board):
        return get_legal_moves(self, board)

    def __repr__(self):
        return f"{self.name}({self.color}, {self.pos})"

# ♟♜♞♝♛♚ — Noir
# ♙♖♘♗♕♔ — Blanc

class Pawn(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.first_move = True
        self.name = 'P'
        self.symbol = '♙' if color == 'white' else '♟'

class Rook(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.has_moved = False
        self.name = 'R'
        self.symbol = '♖' if color == 'white' else '♜'

class Knight(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.name = 'N'  # 'N' pour knight (car 'K' = King)
        self.symbol = '♘' if color == 'white' else '♞'

class Bishop(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.name = 'B'
        self.symbol = '♗' if color == 'white' else '♝'

class Queen(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.name = 'Q'
        self.symbol = '♕' if color == 'white' else '♛'

class King(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.has_moved = False
        self.name = 'K'
        self.symbol = '♔' if color == 'white' else '♚'
