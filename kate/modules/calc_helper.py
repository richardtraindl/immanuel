from kate.models import Match, Move
from kate.modules import rules, debug, helper


def eval_contacts(match):
    supported_whites = 0
    attacked_whites = 0
    supported_blacks = 0
    attacked_blacks = 0
    color = match.next_color()

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(Match.color_of_piece(piece) == Match.COLORS['undefined']):
                continue
            elif(Match.color_of_piece(piece) == Match.COLORS['white']):
                if(rules.attacked(match, x, y, Match.COLORS['white'])):
                    #if(rules.attacked(match, x, y, Match.COLORS['black'])):
                        #supported_whites += 2
                    #else:
                    supported_whites += 1
                if(rules.attacked(match, x, y, Match.COLORS['black'])):
                    attacked_whites += 1
            else:
                if(rules.attacked(match, x, y, Match.COLORS['black'])):
                    #if(rules.attacked(match, x, y, Match.COLORS['white'])):
                        #supported_blacks += 2
                    #else:
                    supported_blacks += 1
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
        
    if(piece == Match.PIECES['wQu'] or piece == Match.PIECES['bQu']):
        dirs = [ [0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1] ]
        dircnt = 8
        stepcnt = 7
    elif(piece == Match.PIECES['wRk'] or piece == Match.PIECES['bRk']):
        dirs = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]
        dircnt = 4
        stepcnt = 7
    elif(piece == Match.PIECES['wBp'] or piece == Match.PIECES['bBp']):
        dirs = [ [1, 1], [-1, -1], [-1, 1], [1, -1] ]
        dircnt = 4
        stepcnt = 7
    elif(piece == Match.PIECES['wKn'] or piece == Match.PIECES['bKn']):
        dirs =  [ [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2] ]
        dircnt = 8
        stepcnt = 1
    else:
        return movecnt

    for j in range(dircnt):
        stepx = dirs[j][0]
        stepy = dirs[j][1]
        dstx = srcx
        dsty = srcy
        for i in range(stepcnt):
            dstx += stepx
            dsty += stepy
            flag,errcode = rules.is_move_valid(match, srcx, srcy, dstx, dsty, Match.PIECES['blk'])
            if(flag):
                movecnt += 1
            elif(errcode == rules.ERROR_CODES['out-of-bounds']):
                break

    return movecnt


def eval_move_cnt(match):
    movecnt = 0

    for y1 in range(8):
        for x1 in range(8):
            movecnt += eval_piece_moves(match, x1, y1)

    return movecnt



def eval_developments(match):
    developed_whites = 0
    developed_blacks = 0

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(Match.color_of_piece(piece) == Match.COLORS['undefined']):
                continue
            elif(Match.color_of_piece(piece) == Match.COLORS['white']):
                if(piece == Match.PIECES['wKn'] or piece == Match.PIECES['wBp'] or piece == Match.PIECES['wQu']):
                    if(y > 0):
                        developed_whites += 1
            else:
                if(piece == Match.PIECES['bKn'] or piece == Match.PIECES['bBp'] or piece == Match.PIECES['bQu']):
                    if(y < 7):
                        developed_blacks += 1

    return developed_whites + (developed_blacks * -1)


def eval_pos(match):
    movecnt = eval_move_cnt(match)
    print("movecnts: " + str(movecnt))

    contacts = eval_contacts(match)
    print("contacts: " + str(contacts))

    if(match.count < 12):
        developments = eval_developments(match)
        print("developments: " + str(developments))
    else:
        developments = 0

    print("****************************")

    if(match.next_color() == Match.COLORS['white']):
        return (movecnt + contacts + developments)
    else:
        return (movecnt + contacts + developments)

