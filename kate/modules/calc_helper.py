from kate.models import Match, Move
from kate.modules import rules, pawn, debug, helper


def is_capture(match, move):
    dstpiece = match.readfield(move.dstx, move.dsty)
    if(dstpiece != Match.PIECES['blk']):
        return True
    else:
        piece = match.readfield(move.srcx, move.srcy)
        if(piece == Match.PIECES['wPw'] or piece == Match.PIECES['bPw']):
            if(move.srcx != move.dstx and dstpiece == Match.PIECES['blk']):
                return True

    return False
        
def is_promotion(match, move):
    if(move.prom_piece != None):
        return True
    else:
        return False

def is_castling(match, move):
    piece = match.readfield(move.srcx, move.srcy)
    if(piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
        if(move.srcx - move.dstx == 2 or move.srcx - move.dstx == -2):
            return True

    return False

def does_attack(match, move):
    piece = match.readfield(move.srcx, move.srcy)

    if(piece == Match.PIECES['wPw']):
        if(is_move_inbounds(move.dstx + pawn.WHITE_1N1E_X, move.dsty + pawn.WHITE_1N1E_Y)):
            att_piece1 = match.readfield(move.dstx + pawn.WHITE_1N1E_X, move.dsty + pawn.WHITE_1N1E_Y)
            if(color_of_piece(att_piece1) == Match.COLORS['black']):
                return True
        if(is_move_inbounds(move.dstx + pawn.WHITE_1N1W_X, move.dsty + pawn.WHITE_1N1W_Y)):
            att_piece2 = match.readfield(move.dstx + pawn.WHITE_1N1W_X, move.dsty + pawn.WHITE_1N1W_Y)
            if(color_of_piece(att_piece2) == Match.COLORS['black']):
                return True

        return False
    elif(piece == Match.PIECES['bPw']):
        if(is_move_inbounds(move.dstx + pawn.BLACK_1S1E_X, move.dsty + pawn.BLACK_1S1E_Y)):
            att_piece1 = match.readfield(move.dstx + pawn.BLACK_1S1E_X, move.dsty + pawn.BLACK_1S1E_Y)
            if(color_of_piece(att_piece1) == Match.COLORS['white']):
                return True
        if(is_move_inbounds(move.dstx + pawn.BLACK_1S1W_X, move.dsty + pawn.BLACK_1S1W_Y)):
            att_piece2 = match.readfield(move.dstx + pawn.BLACK_1S1W_X, move.dsty + pawn.BLACK_1S1W_Y)
            if(color_of_piece(att_piece2) == Match.COLORS['white']):
                return True

        return False
    elif(piece == Match.PIECES['wRk'] or piece == Match.PIECES['bRk']):
        rkdir = rk_dir(move.srcx, move.srcy, move.dstx, move.dsty)
        if(rkdir == rules.DIRS['north'] or rkdir == rules.DIRS['south']):
            RK_STEPS = [ [[1, 0], [-1, 0] ]
        else:
            RK_STEPS = [ [0, 1], [0, -1] ]
        for i in range(2):
            stepx = RK_STEPS[i][0]
            stepy = RK_STEPS[i][1]
            x1, y1 = search(match, move.srcx, move.srcy, stepx, stepy)
            if(x1 != UNDEF_X):
                att_piece = match.readfield(x1, y1)
                if(color_of_piece(piece) != color_of_piece(att_piece) and color_of_piece(att_piece) != Match.COLORS['undefined']):
                    return True
        return False
    elif(piece == Match.PIECES['wBp'] or piece == Match.PIECES['bBp']):
        bpdir = rk_dir(move.srcx, move.srcy, move.dstx, move.dsty)
        if(bpdir == rules.DIRS['north-east'] or bpdir == rules.DIRS['south-west']):
            BP_STEPS = [ [-1, 1], [1, -1] ]
        else:
            BP_STEPS = [ [1, 1], [-1, -1] ]
        for i in range(2):
            stepx = BP_STEPS[i][0]
            stepy = BP_STEPS[i][1]
            x1, y1 = search(match, move.srcx, move.srcy, stepx, stepy)
            if(x1 != UNDEF_X):
                att_piece = match.readfield(x1, y1)
                if(color_of_piece(piece) != color_of_piece(att_piece) and color_of_piece(att_piece) != Match.COLORS['undefined']):
                    return True
        return False
    elif(piece == Match.PIECES['wKn'] or piece == Match.PIECES['bKn']):
        KN_STEPS = [ [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2] ]
        for i in range(8):
            x1 = move.srcx + KN_STEPS[i][0]
            y2 = move.srcy + KN_STEPS[i][1]
            if(is_inbounds(x1, y1)):
                att_piece = match.readfield(x1, y1)
                if(color_of_piece(piece) != color_of_piece(att_piece) and color_of_piece(att_piece) != Match.COLORS['undefined']):
                    return True
    elif(piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
        KG_STEPS = [ [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1] ]
        for i in range(8):
            x1 = move.srcx + KG_STEPS[i][0]
            y1 = move.srcy + KG_STEPS[i][1]
            if(is_inbounds(x1, y1)):
                att_piece = match.readfield(x1, y1)
                if(color_of_piece(piece) != color_of_piece(att_piece) and color_of_piece(att_piece) != Match.COLORS['undefined']):
                    return True
    else:
        return False


def pieces_attacked(match, color):
    if(color == Match.COLORS['white']):
        opp_color = Match.COLORS['black']
    else:
        opp_color = Match.COLORS['white']
    
    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(Match.color_of_piece(piece) == opp_color):
                if(rules.attacked(match, x, y, opp_color)):
                    return True
            else:
                continue

    return False


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
                        developed_blacks += 20
                    elif(y == 7 and x == 2 and match.readfield(x, y-1) == Match.PIECES['bPw'] and match.readfield(x-1, y-1) == Match.PIECES['bPw'] and match.readfield(x-2, y-1) == Match.PIECES['bPw']):
                        developed_blacks += 20

    return developed_whites - developed_blacks


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

