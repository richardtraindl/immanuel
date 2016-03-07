from kate.models import Match, Move
from kate.modules import values, pawn, rook, knight, bishop, queen, king


REVERSE_DIRS = {
    'north' : rook.DIRS['south'],
    'south' : rook.DIRS['north'],
    'east' : rook.DIRS['west'],
    'west' : rook.DIRS['east'],
    'north-east' : bishop.DIRS['south-west'],
    'south-west' : bishop.DIRS['north-east'],
    'north-west' : bishop.DIRS['south-east'],
    'south-east' : bishop.DIRS['north-west'],
    'undefined' : 10 }


def is_move_color_ok(piece, count):
    color = Match.color_of_piece(piece)
    if(count % 2 == 0 and color == Match.COLORS['white']):
        return True
    elif(count % 2 == 1 and color == Match.COLORS['black']):
        return True
    else:
        return False


def is_move_inbounds(srcx, srcy, dstx, dsty):
    if(srcx < 0 or srcx > 7 or srcy < 0 or srcy > 7 or
       dstx < 0 or dstx > 7 or dsty < 0 or dsty > 7):
        return False
    else:
        return True

def search(match, srcx, srcy, stepx, stepy):
    x = srcx + stepx
    y = srcy + stepy
    while(x >= 0 and x <= 7 and y >= 0 and y <= 7):
        field = match.readfield(x, y)
        if(field != Match.PIECES['blk']):
            return x, y

        x += stepx
        y += stepy
    return 8, 8


def pinned(match, color, scrx, srcy, kgx, kgy):
    direction = rook.direction(scrx, srcy, kgx, kgy)
    if(direction != rook.DIRS['undefined']):
        stepx, stepy = rook.step(direction, None, None, None, None)
        dstx, dsty = search(match, scrx, srcy, stepx, stepy)
        piece = match.readfield(dstx, dsty)
        if( (color == Match.COLORS['white'] and piece == Match.PIECES['wKg']) or
            (color == Match.COLORS['black'] and piece == Match.PIECES['bKg']) ):
            reverse_direction = rook.REVERSE_DIRS[direction]
            stepx, stepy = rook.step(reverse_direction, None, None, None, None)
            dstx, dsty = search(match, scrx, srcy, stepx, stepy)
            if(dstx != 8):
                piece = match.readfield(dstx, dsty)
                if(color == Match.COLORS['white']):
                    if(piece == Match.PIECES['bQu'] or piece == Match.PIECES['bRk']):
                        return direction
                    else:
                        return rook.DIRS['undefined']
                else:
                    if(piece == Match.PIECES['wQu'] or piece == Match.PIECES['wRk']):
                        return direction
                    else:
                        return rook.DIRS['undefined']

    direction = bishop.direction(scrx, srcy, kgx, kgy)
    if(direction != bishop.DIRS['undefined']):
        stepx, stepy = bishop.step(direction, None, None, None, None)
        dstx, dsty = search(match, scrx, srcy, stepx, stepy)
        piece = match.readfield(dstx, dsty)
        if( (color == Match.COLORS['white'] and piece == Match.PIECES['wKg']) or
            (color == Match.COLORS['black'] and piece == Match.PIECES['bKg']) ):
            reverse_direction = bishop.REVERSE_DIRS[direction]
            stepx, stepy = bishop.step(reverse_direction, None, None, None, None)
            dstx, dsty = search(scrx, srcy, stepx, stepy)
            if(dstx != 8):
                piece = match.readfield(dstx, dsty)
                if(color == Match.COLORS['white']):
                    if(piece == Match.PIECES['bQu'] or piece == Match.PIECES['bBp']):
                        return direction
                    else:
                        return bishop.DIRS['undefined']
                else:
                    if(piece == Match.PIECES['wQu'] or piece == Match.PIECES['wBp']):
                        return direction
                    else:
                        return bishop.DIRS['undefined']
        
    return rook.DIRS['undefined']


def is_move_valid(match, srcx, srcy, dstx, dsty, prom_piece):
    piece = match.readfield(srcx, srcy)

    if(not is_move_inbounds(srcx, srcy, dstx, dsty)):
        return False

    if(not is_move_color_ok(piece, match.count)):
        return False

    if(piece == Match.PIECES['wPw'] or piece == Match.PIECES['bPw']):
        if(not pawn.is_move_ok(match, srcx, srcy, dstx, dsty, piece, prom_piece)):
            return False
        else:
            return True
    elif(piece == Match.PIECES['wRk'] or piece == Match.PIECES['bRk']):
        if(not rook.is_move_ok(match, srcx, srcy, dstx, dsty, piece)):
            return False
        else:
            return True
    elif(piece == Match.PIECES['wKn'] or piece == Match.PIECES['bKn']):
        if(not knight.is_move_ok(match, srcx, srcy, dstx, dsty, piece)):
            return False
        else:
            return True
    elif(piece == Match.PIECES['wBp'] or piece == Match.PIECES['bBp']):
        if(not bishop.is_move_ok(match, srcx, srcy, dstx, dsty, piece)):
            return False
        else:
            return True
    elif(piece == Match.PIECES['wQu'] or piece == Match.PIECES['bQu']):
        if(not queen.is_move_ok(match, srcx, srcy, dstx, dsty, piece)):
            return False
        else:
            return True
    elif(piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
        if(not king.is_move_ok(match, srcx, srcy, dstx, dsty, piece)):
            return False
        else:
            return True
    else:
        return False
