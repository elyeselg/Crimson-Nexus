import uuid

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
        self.id = uuid.uuid4()  # identifiant unique pour tracer les coups
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.piece_moved = piece_moved
        self.piece_captured = piece_captured
        self.promotion = promotion
        self.is_castling = is_castling
        self.is_en_passant = is_en_passant
        self.notation = None  
        self.is_check = False  # tu peux la renseigner après coup si besoin

    def __repr__(self):
        start = f"{chr(self.start_pos[1] + ord('a'))}{8 - self.start_pos[0]}"
        end = f"{chr(self.end_pos[1] + ord('a'))}{8 - self.end_pos[0]}"
        promo = f"={self.promotion}" if self.promotion else ""
        return f"{self.piece_moved.__class__.__name__} {start}->{end}{promo}"

    def __str__(self):
        return self.__repr__()
