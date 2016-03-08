from kate.modules import rook, bishop


def is_move_ok(match, srcx, srcy, dstx, dsty, piece):
    if(rook.is_move_ok(match, srcx, srcy, dstx, dsty, piece)):
        return True
    else:
        return bishop.is_move_ok(match, srcx, srcy, dstx, dsty, piece)

