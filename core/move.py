class Move:
    def __init__(
        self,
        start_pos,
        end_pos,
        piece_moved,
        piece_captured=None,
        promotion=None,
        is_castling=False,
        is_en_passant=False
    ):
        self.start_pos = start_pos              # Tuple (row, col)
        self.end_pos = end_pos                  # Tuple (row, col)
        self.piece_moved = piece_moved          # Objet de type Piece
        self.piece_captured = piece_captured    # Objet de type Piece ou None
        self.promotion = promotion              # Type de pièce en cas de promotion
        self.is_castling = is_castling
        self.is_en_passant = is_en_passant

    def __repr__(self):
        piece_name = self.piece_moved.__class__.__name__
        return f"{piece_name} from {self.start_pos} to {self.end_pos}"
