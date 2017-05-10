


TYPES = { 'standard' : 1, 
          'short_castling' : 2,
          'long_castling' : 3,
          'promotion' : 4,
          'en_passant' : 5 }


class Move:
    def __init__(self, match=None, count=None, move_type=None, srcx=None, srcy=None, dstx=None, dsty=None, e_p_fieldx=None, e_p_fieldy=None, captured_piece=None, prom_piece=None, fifty_moves_count=None):
        self.match = match
        self.count = count
        self.move_type = move_type
        self.srcx = srcx
        self.srcy = srcy
        self.dstx = dstx
        self.dsty = dsty
        self.e_p_fieldx = e_p_fieldx
        self.e_p_fieldy = e_p_fieldy
        self.captured_piece = captured_piece
        self.prom_piece = prom_piece
        self.fifty_moves_count = fifty_moves_count

