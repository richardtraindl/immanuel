from kate.models import Match, Move
from kate.modules import pawn, rook, knight, bishop, queen, king, generic


def do_move(match, srcx, srcy, dstx, dsty, prom_piece):
    move = Move(match=match, 
                count=match.count+1, 
                move_type=Move.TYPES['standard'], 
                srcx=srcx, 
                srcy=srcy, 
                dstx=dstx, 
                dsty=dsty, 
                e_p_fieldx=None,
                e_p_fieldy=None,
                captured_piece=Match.PIECES['blk'], 
                prom_piece=prom_piece, 
                fifty_moves_count=match.fifty_moves_count)

    srcpiece = match.readfield(srcx, srcy)
    dstpiece = match.readfield(dstx, dsty)

    if(srcpiece == Match.PIECES['wPw'] or srcpiece == Match.PIECES['bPw']):
        return pawn.do_move(match, move, srcpiece, dstpiece)
    elif(srcpiece == Match.PIECES['wKg'] or srcpiece == Match.PIECES['bKg']):
        return king.do_move(match, move, srcpiece, dstpiece)
    else:
        return generic.do_move(match, move, srcpiece, dstpiece)


def undo_move(match, calc):
    if(calc == False):
        move = Move.objects.filter(match_id=match.id).order_by("count").last()
        if(move == None):
            return None
    else:
        if(len(match.move_list) > 0):
            move = match.move_list.pop()
        else:
            return None

    if(move.move_type == Move.TYPES['standard']):
        return generic.undo_move(match, move)
    elif(move.move_type == Move.TYPES['short_castling']):
        return king.undo_short_castling(match, move)
    elif(move.move_type == Move.TYPES['long_castling']):
        return king.undo_long_castling(match, move)
    elif(move.move_type == Move.TYPES['promotion']):
        return pawn.undo_promotion(match, move)
    else:
        return pawn.undo_en_passant(match, move)

