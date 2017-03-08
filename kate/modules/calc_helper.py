from kate.models import Match, Move
from kate.modules import rules, debug, helper


def evaluate_contacts(match):
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
                supported_whites += rules.count_attacks(match, x, y, Match.COLORS['white'])
                attacked_whites += rules.eval_attacks(match, x, y, Match.COLORS['black'])
                # attacked_whites += rules.count_attacks(match, x, y, Match.COLORS['black'])
            else:
                supported_blacks += rules.count_attacks(match, x, y, Match.COLORS['black'])
                attacked_blacks += rules.eval_attacks(match, x, y, Match.COLORS['white'])
                #attacked_blacks += rules.count_attacks(match, x, y, Match.COLORS['white'])

    return (supported_whites - attacked_whites) - (supported_blacks - attacked_blacks)


def evaluate_piece_moves(match, srcx, srcy):
    color = match.next_color()
    piece = match.readfield(srcx, srcy)
    movecnt = 0

    if(Match.color_of_piece(piece) != color):
        return movecnt
        
    if(piece == Match.PIECES['wQu'] or piece == Match.PIECES['bQu']):
        dirs = [ [0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1] ]
        dircnt = 8
        stepcnt = 7
        value = 2
    elif(piece == Match.PIECES['wRk'] or piece == Match.PIECES['bRk']):
        dirs = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]
        dircnt = 4
        stepcnt = 7
        value = 4
    elif(piece == Match.PIECES['wBp'] or piece == Match.PIECES['bBp']):
        dirs = [ [1, 1], [-1, -1], [-1, 1], [1, -1] ]
        dircnt = 4
        stepcnt = 7
        value = 6
    elif(piece == Match.PIECES['wKn'] or piece == Match.PIECES['bKn']):
        dirs =  [ [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2] ]
        dircnt = 8
        stepcnt = 1
        value = 6
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
                movecnt += value
            elif(errcode == rules.ERROR_CODES['out-of-bounds']):
                break

    return (movecnt)


def evaluate_movecnt(match):
    movecnt = 0

    for y1 in range(8):
        for x1 in range(8):
            movecnt += evaluate_piece_moves(match, x1, y1)

    if(match.next_color() == Match.COLORS['white']):
        return movecnt
    else:
        return (movecnt * -1)


def evaluate_developments(match):
    developed_whites = 0
    developed_blacks = 0

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(Match.color_of_piece(piece) == Match.COLORS['undefined']):
                continue
            elif(Match.color_of_piece(piece) == Match.COLORS['white']):
                """
                if(piece == Match.PIECES['wKn']):
                    if(y > 0):
                        developed_whites += 3
                elif(piece == Match.PIECES['wBp']):
                    if(y > 0):
                        developed_whites += 2
                elif(piece == Match.PIECES['wQu']):
                    if(y > 0):
                        developed_whites += 1
                """
                if(piece == Match.PIECES['wKg']):
                    if(y == 0 and x == 6 and match.readfield(x-1, y+1) == Match.PIECES['wPw'] and match.readfield(x, y+1) == Match.PIECES['wPw']):
                        developed_whites += 20
                    elif(y == 0 and x == 2 and match.readfield(x, y+1) == Match.PIECES['wPw'] and match.readfield(x-1, y+1) == Match.PIECES['wPw'] and match.readfield(x-2, y+1) == Match.PIECES['wPw']):
                        developed_whites += 20
            else:
                """
                if(piece == Match.PIECES['bKn']):
                    if(y < 7):
                        developed_blacks += -3
                elif(piece == Match.PIECES['bBp']):
                    if(y < 7):
                        developed_blacks += -2
                elif(piece == Match.PIECES['bQu']):
                    if(y < 7):
                        developed_blacks += -1
                """
                if(piece == Match.PIECES['bKg']):
                    if(y == 7 and x == 6 and match.readfield(x-1, y-1) == Match.PIECES['bPw'] and match.readfield(x, y-1) == Match.PIECES['bPw']):
                        developed_blacks += -20
                    elif(y == 7 and x == 2 and match.readfield(x, y-1) == Match.PIECES['bPw'] and match.readfield(x-1, y-1) == Match.PIECES['bPw'] and match.readfield(x-2, y-1) == Match.PIECES['bPw']):
                        developed_blacks += -20

    return developed_whites + developed_blacks


def evaluate_position(match):
    contacts = evaluate_contacts(match)

    movecnt = evaluate_movecnt(match)

    if(match.count < 24):
        developments = evaluate_developments(match)
    else:
        developments = 0

    # print("contacts: " + str(contacts))
    # print("movecnts: " + str(movecnt))
    # print("developments: " + str(developments))
    # print("****************************")

    return (movecnt + contacts + developments)

