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
        self.start_pos = start_pos                # (row, col)
        self.end_pos = end_pos                    # (row, col)
        self.piece_moved = piece_moved            # Objet Piece
        self.piece_captured = piece_captured      # Objet Piece ou None
        self.promotion = promotion                # str (ex: 'Queen') ou None
        self.is_castling = is_castling
        self.is_en_passant = is_en_passant

    def __repr__(self):
        start = f"{chr(self.start_pos[1] + ord('a'))}{8 - self.start_pos[0]}"
        end = f"{chr(self.end_pos[1] + ord('a'))}{8 - self.end_pos[0]}"
        promo = f"={self.promotion}" if self.promotion else ""
        return f"{self.piece_moved.__class__.__name__} {start}->{end}{promo}"
