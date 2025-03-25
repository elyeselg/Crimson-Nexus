class Piece:
    def __init__(self, color, pos):
        self.color = color          # 'white' ou 'black'
        self.pos = pos              # (row, col)
        self.symbol = ''            # Pour affichage éventuel

    def get_legal_moves(self, board):
        from core.rules import get_legal_moves
        return get_legal_moves(self, board)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.color}, {self.pos})"


class Pawn(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.first_move = True
        self.symbol = '♙' if color == 'white' else '♟'


class Rook(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.has_moved = False
        self.symbol = '♖' if color == 'white' else '♜'


class Knight(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = '♘' if color == 'white' else '♞'


class Bishop(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = '♗' if color == 'white' else '♝'


class Queen(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.symbol = '♕' if color == 'white' else '♛'


class King(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.has_moved = False
        self.symbol = '♔' if color == 'white' else '♚'
