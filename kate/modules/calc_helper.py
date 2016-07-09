from kate.models import Match, Move
from kate.modules import rules, debug


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
        
    eval_white = (supported_whites - attacked_whites)
    eval_black = (supported_blacks - attacked_blacks) * -1
    return eval_white + eval_black


def eval_piece_moves(match, srcx, srcy):
    color = match.next_color()
    piece = match.readfield(srcx, srcy)
    movecnt = 0

    if(Match.color_of_piece(piece) != color):
        return movecnt
        
    #if(piece == Match.PIECES['wQu'] or piece == Match.PIECES['bQu']):
    #    steps = [ [0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1] ]
    #    rangecnt = 8
    if(piece == Match.PIECES['wRk'] or piece == Match.PIECES['bRk']):
        steps = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]
        dircnt = 4
        stepcnt = 7
    elif(piece == Match.PIECES['wBp'] or piece == Match.PIECES['bBp']):
        steps = [ [1, 1], [-1, -1], [-1, 1], [1, -1] ]
        dircnt = 4
        stepcnt = 7
    elif(piece == Match.PIECES['wKn'] or piece == Match.PIECES['bKn']):
        steps =  [ [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2] ]
        dircnt = 8
        stepcnt = 1
    else:
        return movecnt

    for i in range(dircnt):
        for j in range(stepcnt):
            dstx = srcx + steps[i][0]
            dsty = srcx + steps[i][1]
            if(rules.is_move_inbounds(srcx, srcy, dstx, dsty)):
                if(rules.is_move_valid(match, srcx, srcy, dstx, dsty, Match.PIECES['blk'])):
                    movecnt += 1
                dstx = dstx + steps[i][0]
                dsty = dsty + steps[i][1]
            else:
                break

    return movecnt


def eval_move_cnt(match):
    movecnt = 0

    for y1 in range(8):
        for x1 in range(8):
            movecnt += eval_piece_moves(match, x1, y1)

    return movecnt


def eval_pos(match):
    movecnt = eval_move_cnt(match)
    # print("movecnts: " + str(movecnt))

    contacts = eval_contacts(match)
    # print("contacts: " + str(contacts))

    if(match.next_color() == Match.COLORS['white']):
        return movecnt * 2 + contacts
    else:
        return movecnt * -2 + contacts
