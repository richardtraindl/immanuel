from kate.models import Match, Move
from kate.modules import rules, pawn, debug, helper


"""
def analyse(match):
    analyses = []
    qu_analyses = []
    rk_analyses = []
    bp_analyses = []
    kn_analyses = []
    pw_analyses = []
    
    color = match.next_color()
    opp_color = Match.REVERSED_COLORS[color]

    for y1 in range(8):
        for x1 in range(8):
            piece = match.readfield(x1, y1)
            if(color == Match.color_of_piece(piece)):
                if(piece == Match.PIECES['wPw'] or Match.PIECES['bPw']):
                    if( rules.is_field_attacked(match, opp_color, x1, y1) ):
                        pw_analyses.append("pw")
                elif(piece == Match.PIECES['wRk'] or piece == Match.PIECES['bRk']):
                    if( rules.is_field_attacked(match, opp_color, x1, y1) ):
                        rk_analyses.append("rk")
                elif(piece == Match.PIECES['wBp'] or piece == Match.PIECES['bBp']):
                    if( rules.is_field_attacked(match, opp_color, x1, y1) ):
                        bp_analyses.append("bp")
                elif(piece == Match.PIECES['wKn'] or piece == Match.PIECES['bKn']):
                    if( rules.is_field_attacked(match, opp_color, x1, y1) ):
                        kn_analyses.append("kn")
                elif(piece == Match.PIECES['wQu'] or piece == Match.PIECES['bQu']):
                    if( rules.is_field_attacked(match, opp_color, x1, y1) ):
                        qu_analyses.append("qu")
                else:
                    if( rules.is_field_attacked(match, opp_color, x1, y1) ):
                        analyses.append("kg")

    analyses.extend(qu_analyses)
    analyses.extend(rk_analyses)
    analyses.extend(bp_analyses)
    analyses.extend(kn_analyses)
    analyses.extend(pw_manalyses)
    return analyses
"""


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
    if(move.prom_piece == Match.PIECES['blk']):
        return False
    else:
        return True


def is_castling(match, move):
    piece = match.readfield(move.srcx, move.srcy)
    if(piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
        if(move.srcx - move.dstx == 2 or move.srcx - move.dstx == -2):
            return True

    return False


def does_attack(match, move):
    return rules.does_attack(match, move.srcx, move.srcy, move.dstx, move.dsty)


def does_support_attacked(match, move):
    return rules.does_support_attacked(match, move.srcx, move.srcy, move.dstx, move.dsty)


def does_attacked_flee(match, move):
    opp_color = Match.REVERSED_COLORS[match.next_color()]
    
    if( rules.is_field_attacked(match, opp_color, move.srcx, move.srcy) ):
        piece = match.readfield(move.srcx, move.srcy)
        if(piece == Match.PIECES['wQu'] or piece == Match.PIECES['bQu']):
            return True, 2
        else:
            return True, 1

    return False, 0


def is_endgame_move(match, move):
    if(match.count > 60):
        piece = match.readfield(move.srcx, move.srcy)
        if(piece == Match.PIECES['wPw'] or piece == Match.PIECES['bPw'] or piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
            return True

    return False


"""
def is_king_attacked(match, move):
    return rules.is_king_attacked(match, move.srcx, move.srcy)
"""


"""
def pieces_attacked(match, color):
    if(color == Match.COLORS['white']):
        opp_color = Match.COLORS['black']
    else:
        opp_color = Match.COLORS['white']
    
    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(Match.color_of_piece(piece) == opp_color):
                if(rules.is_field_attacked(match, opp_color, x, y)):
                    return True
            else:
                continue

    return False
"""


def evaluate_contacts(match):
    supporter = 0
    attacked = 0

    color = match.next_color()

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(Match.color_of_piece(piece) == Match.COLORS['undefined']):
                continue

            supporter += rules.score_supports_of_attacked(match, x, y)
            attacked += rules.score_attacks(match, x, y)

    return (supporter + attacked)


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
            elif(errcode == rules.RETURN_CODES['out-of-bounds']):
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
    if(match.wKg_first_movecnt > 0 and (match.wRk_a1_first_movecnt > 0 or match.wRk_h1_first_movecnt > 0) ):
        developed_whites = 20
    else:
        developed_whites = 0

    if(match.bKg_first_movecnt > 0 and (match.bRk_a8_first_movecnt > 0 or match.bRk_h8_first_movecnt > 0) ):
        developed_blacks = -20
    else:
        developed_blacks = 0

    return developed_whites + developed_blacks


def evaluate_position(match):
    value = evaluate_contacts(match)

    if(match.count < 30):
        value += evaluate_movecnt(match)
        value += evaluate_developments(match)

    return value

