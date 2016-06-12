from kate.models import Match, Move
from kate.modules import values, rules, debug


def eval_contacts(match):
    supported_whites = 0
    attacked_whites = 0
    supported_blacks = 0
    attacked_blacks = 0
    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(Match.color_of_piece(piece) == Match.COLORS['undefined']):
                continue
            elif(Match.color_of_piece(piece) == Match.COLORS['white']):
                if(rules.attacked(match, x, y, Match.COLORS['white'])):
                    supported_whites += 2
                if(rules.attacked(match, x, y, Match.COLORS['black'])):
                    attacked_whites += 1
            else:
                if(rules.attacked(match, x, y, Match.COLORS['black'])):
                    supported_blacks += 2
                if(rules.attacked(match, x, y, Match.COLORS['white'])):
                    attacked_blacks += 1
        
    rate_white = (supported_whites - attacked_whites)
    rate_black = (supported_blacks - attacked_blacks) * -1
    return rate_white + rate_black


def count_piece_moves(match, srcx, srcy):
    color = match.next_color()
    piece = match.readfield(srcx, srcy)
    movecnt = 0

    if(Match.color_of_piece(piece) != color):
        return movecnt
        
    if(piece == Match.PIECES['wQu'] or piece == Match.PIECES['bQu']):
        steps = [ [0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1] ]
        rangecnt = 8
    elif(piece == Match.PIECES['wRk'] or piece == Match.PIECES['bRk']):
        steps = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]
        rangecnt = 4
    elif(piece == Match.PIECES['wBp'] or piece == Match.PIECES['bBp']):
        steps = [ [1, 1], [-1, -1], [-1, 1], [1, -1] ]
        rangecnt = 4
    elif(piece == Match.PIECES['wKn'] or piece == Match.PIECES['bKn']):
        steps =  [ [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2] ]
        rangecnt = 8
    else:
        return movecnt

    for i in range(rangecnt):
        dstx = srcx + steps[i][0]
        dsty = srcx + steps[i][1]
        if(rules.is_move_valid(match, srcx, srcy, dstx, dsty, Match.PIECES['blk'])):
            movecnt += 1

    return movecnt


def count_moves(match):
    movecnt = 0

    for y1 in range(8):
        for x1 in range(8):
            movecnt += count_piece_moves(match, x1, y1)

    return movecnt

