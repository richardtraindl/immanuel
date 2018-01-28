from .match import *
from . import rules # RETURN_CODES, status, is_move_inbounds
from .pieces import pawn, knight, bishop, rook, king 
from .pieces.generic_piece import cTouch
from .analyze_helper import field_touches_beyond, field_touches
from .cvalues import *


def score_supports(match, color):
    score = 0

    for y in range(8):
        for x in range(8):
            piece = match.readfield(x, y)

            if(piece == PIECES['blk']):
                continue
            elif(Match.color_of_piece(piece) != color):
                continue
            elif(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                score += pawn.score_supports(match, x, y)
            elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                score += knight.score_supports(match, x, y)
            elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
                score += bishop.score_supports(match, x, y)
            elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
                score += rook.score_supports(match, x, y)
            elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                score += bishop.score_supports(match, x, y)
                score += rook.score_supports(match, x, y)
            else:
                score += king.score_supports(match, x, y)

    return score


def score_attacks(match, color):
    score = 0

    for y in range(8):
        for x in range(8):
            piece = match.readfield(x, y)

            if(piece == PIECES['blk']):
                continue
            elif(Match.color_of_piece(piece) != color):
                continue
            elif(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                score += pawn.score_attacks(match, x, y)
            elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                score += knight.score_attacks(match, x, y)
            elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
                score += bishop.score_attacks(match, x, y)
            elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
                score += rook.score_attacks(match, x, y)    
            elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                score += bishop.score_attacks(match, x, y)
                score += rook.score_attacks(match, x, y)
            else:
                score += king.score_attacks(match, x, y)

    return score


def score_controled_horizontal_files(match):
    score = 0

    whiterate = ATTACKED_SCORES[PIECES['bKn']]
    
    blackrate = ATTACKED_SCORES[PIECES['wKn']]

    for y in range(0, 2, 1):
        wcnt = 0
        bcnt = 0
        for x in range(8):
            piece = match.readfield(x, y)
            if(piece == PIECES['wRk'] or piece == PIECES['wQu']):
                wcnt += 1
            elif(piece == PIECES['bRk'] or piece == PIECES['bQu']):
                bcnt += 1
            else:
                continue

        if(bcnt > wcnt):
            score += blackrate

    for y in range(6, 8, 1):
        wcnt = 0
        bcnt = 0
        for x in range(8):
            piece = match.readfield(x, y)
            if(piece == PIECES['bRk'] or piece == PIECES['bQu']):
                bcnt += 1
            elif(piece == PIECES['wRk'] or piece == PIECES['wQu']):
                wcnt += 1
            else:
                continue

        if(wcnt > bcnt):
            score += whiterate

    return score


def score_controled_vertical_files(match):
    score = 0

    whiterate = ATTACKED_SCORES[PIECES['bKn']]
    
    blackrate = ATTACKED_SCORES[PIECES['wKn']]

    for x in range(8):
        wcnt = 0
        bcnt = 0
        wpwcnt = 0
        bpwcnt = 0
        for y in range(8):
            piece = match.readfield(x, y)
            if(piece == PIECES['blk']):
                continue
            elif(piece == PIECES['wPw']):
                wpwcnt += 1
                continue
            elif(piece == PIECES['bPw']):
                bpwcnt += 1
                continue
            elif(piece == PIECES['wRk'] or piece == PIECES['wQu']):
                wcnt += 1
                continue
            elif(piece == PIECES['bRk'] or piece == PIECES['bQu']):
                bcnt += 1
                continue
            else:
                continue

        if(wpwcnt == 0 and bpwcnt == 0):
            if(wcnt > bcnt):
                score += whiterate
            elif(bcnt > wcnt):
                score += blackrate

    return score



"""def check_mobility_move(match, srcx, srcy, dstx, dsty, prom_piece):
    if(not is_move_inbounds(srcx, srcy, dstx, dsty)):
        return False

    piece = match.readfield(srcx, srcy)

    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        if(pawn.is_move_valid(match, srcx, srcy, dstx, dsty, piece, prom_piece)):
            return True
        else:
            return False
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        if(rook.is_move_valid(match, srcx, srcy, dstx, dsty, piece)):
            return True
        else:
            return False
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        if(knight.is_move_valid(match, srcx, srcy, dstx, dsty, piece)):
            return True
        else:
            return False
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        if(bishop.is_move_valid(match, srcx, srcy, dstx, dsty, piece)):
            return True
        else:
            return False
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        if(queen.is_move_valid(match, srcx, srcy, dstx, dsty, piece)):
            return True
        else:
            return False
    else:
        return False

def count_mobility(match, srcx, srcy, excludedpieces):
    piece = match.readfield(srcx, srcy)
    movecnt = 0

    for expiece in excludedpieces:
        if(piece == expiece):
            return movecnt

    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        dirs = [ [0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1] ]
        dircnt = 8
        stepcnt = 1
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        dirs = [ [0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1] ]
        dircnt = 8
        stepcnt = 7
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        dirs = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]
        dircnt = 4
        stepcnt = 7
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        dirs = [ [1, 1], [-1, -1], [-1, 1], [1, -1] ]
        dircnt = 4
        stepcnt = 7
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
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
            if(check_mobility_move(match, srcx, srcy, dstx, dsty, PIECES['blk'])):
                movecnt += 1
            else:
                break

    return movecnt"""


def is_opening(match):
    return match.count < 30


def is_endgame(match):
    return match.count >= 30


def is_king_defended_by_pawns(match, color):
    if(color == COLORS['white']):
        y = 1
        Kg_x = match.wKg_x
        Kg_y = match.wKg_y
        pawn = PIECES['wPw']
    else:
        y= 6
        Kg_x = match.bKg_x
        Kg_y = match.bKg_y
        pawn = PIECES['bPw']
    
    count = 0
    for x in range(8):
        if(x == Kg_x or x - 1 == Kg_x or x + 1 == Kg_x):
            if(match.readfield(x, y) == pawn):
                count += 1

    if(count >= 2):
        return True
    else:
        return False

def is_king_centered(match, color):
    if(color == COLORS['white']):
        if(wKg_y >= 2):
            return True

        x = match.wKg_x
    else:
        if(bKg_y <= 5):
            return True

        x = match.bKg_x

    if(x == 3 or x == 4 or x == 5):
        return True
    
    return False

def is_rook_trapped(match, color):
    if(color == COLORS['white']):
        y = 0
        Kg_x = match.wKg_x
        Kg_y = match.wKg_y
        rook = PIECES['wRk']
    else:
        y= 7
        Kg_x = match.bKg_x
        Kg_y = match.bKg_y
        rook = PIECES['bRk']

    rook_leftcnt = 0
    piece_leftcnt = 0
    rook_rightcnt = 0
    piece_rightcnt = 0

    if(Kg_x > 0):
        for x in range(0, Kg_x, 1):
            piece = match.readfield(x, y)

            if(piece == PIECES['blk']):
                continue
            elif(piece == rook):
                rook_leftcnt += 1
            else:
                piece_leftcnt += 1

    if(Kg_x < 7):
        for x in range(Kg_x + 1, 8, 1):
            piece = match.readfield(x, y)

            if(piece == PIECES['blk']):
                continue
            elif(piece == rook):
                rook_rightcnt += 1
            else:
                piece_rightcnt += 1

    if((rook_leftcnt == 0 and piece_leftcnt == 0) or 
       (rook_rightcnt == 0 and piece_rightcnt == 0)):
        return False
    else:
        return True

def score_opening(match):
    value = 0

    whiterate = ATTACKED_SCORES[PIECES['bPw']]
    
    blackrate = ATTACKED_SCORES[PIECES['wPw']]

    # white position
    y = 0
    cnt = 0
    for x in range(8):
        piece = match.readfield(x, y)
        if(piece == PIECES['wKn'] or piece == PIECES['wBp']):
            cnt += 1

    value += cnt * blackrate

    y = 1
    cnt = 0
    for x in range(8):
        piece = match.readfield(x, y)
        if(piece == PIECES['wPw']):
            cnt += 1
    
    if(cnt <= 6): 
        value += whiterate

    # black position
    y = 7
    cnt = 0
    for x in range(8):
        piece = match.readfield(x, y)
        if(piece == PIECES['bKn'] or piece == PIECES['bBp']):
            cnt += 1

    value += cnt * whiterate

    y = 6
    cnt = 0
    for x in range(8):
        piece = match.readfield(x, y)
        if(piece == PIECES['bPw']):
            cnt += 1
    
    if(cnt <= 6): 
        value += blackrate

    # white king
    if(is_king_defended_by_pawns(match, COLORS['white'])):
        value += whiterate * 3

    if(is_rook_trapped(match, COLORS['white'])):
        value += blackrate * 3
    else:
        value += whiterate * 3

    if(is_king_centered == False):
        value += whiterate * 3

    # black king
    if(is_king_defended_by_pawns(match, COLORS['black'])):
        value += blackrate * 3

    if(is_rook_trapped(match, COLORS['black'])):
        value += whiterate * 3
    else:
        value += blackrate * 3

    if(is_king_centered == False):
        value += blackrate * 3

    return value


def score_endgame(match):
    value = 0

    whiterate = ATTACKED_SCORES[PIECES['bPw']]
    whitesteprate = whiterate / 2

    blackrate = ATTACKED_SCORES[PIECES['wPw']]
    blacksteprate = blackrate / 2

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(piece == PIECES['wPw']):
                if(pawn.is_running(match, x, y)):
                    value += whiterate
                    value += whitesteprate * y
            elif(piece == PIECES['bPw']):
                if(pawn.is_running(match, x, y)):
                    value += blackrate
                    value += blacksteprate * (7 - y)

    return value


def score_position(match, movecnt):
    status = rules.status(match)

    if(movecnt == 0 and status != STATUS['open']):
        if(status == STATUS['winner_black']):
            return ( SCORES[PIECES['wKg']] + match.count )
        elif(status == STATUS['winner_white']):
            return ( SCORES[PIECES['bKg']] - match.count )
        else: # draw
            return SCORES[PIECES['blk']]
    else:
        score = match.score
        
        color = match.next_color()

        score += score_attacks(match, color)

        score += score_supports(match, REVERSED_COLORS[color])

        score += score_controled_horizontal_files(match)
        
        score += score_controled_vertical_files(match)

        if(is_opening(match)):
            score += score_opening(match)

        if(is_endgame(match)):
            score += score_endgame(match)

        return score


def is_capture_possible(match, color):
    for y in range(8):
        for x in range(8):
            piece = match.readfield(x, y)

            if(piece == PIECES['blk']):
                continue
            elif(Match.color_of_piece(piece) != color):
                continue
            elif(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                if(pawn.is_capture_possible(match, x, y)):
                    return True
            elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                if(knight.is_capture_possible(match, x, y)):
                    return True
            elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
                if(bishop.is_capture_possible(match, x, y)):
                    return True
            elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
                if(rook.is_capture_possible(match, x, y)):
                    return True
            elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                if(bishop.is_capture_possible(match, x, y)):
                    return True
                if(rook.is_capture_possible(match, x, y)):
                    return True
            else:
                if(king.is_capture_possible(match, x, y)):
                    return True

    return False


def are_attacks_or_captures_possible(match):
    for y in range(8):
        for x in range(8):
            piece = match.readfield(x, y)

            if(piece == PIECES['blk']):
                continue
            else:
                friends, enemies = field_touches(match, Match.color_of_piece(piece), x, y)
                if(len(friends) <= len(enemies)):
                    return True
                else:
                    for enemy in enemies:
                        if(PIECES_RANK[enemy[0]] <= PIECES_RANK[piece]):
                            return True

    return False


def is_stormy(match):
    color = match.next_color()

    # is attacked
    if(are_attacks_or_captures_possible(match)):
        return True
    ###

    # is pawn on last row before promotion
    if(color == COLORS['white']):
        y = 6
        pw = PIECES['wPw']
    else:
        y = 1
        pw = PIECES['bPw']
    for x in range(8):
        piece = match.readfield(x, y)
        if(piece == pw):
            return True
    ###

    # is pinned enemy attacked
    """opp_color = REVERSED_COLORS[color]
    for y in range(8):
        for x in range(8):
            piece = match.readfield(x, y)
            if(Match.color_of_piece(piece) == color):
                direction = rules.pin_dir(match, x, y)
                if(direction != rules.DIRS['undefined']):
                    ctouch = cTouch(None, None, None, None, piece, x, y)
                    field_touches_beyond(match, color, ctouch)
                    if(len(ctouch.attacker_beyond) > 0):
                        return True"""
     ###

    return False


ANALYZE = {
        'IS_ATTACKED' : 0x10,
        'IS_PINNED' : 0x01,
        'IS_SUPPORTED' : 0x001 }

class cAnalyzer:
    def __init__(self, prio, piece, fieldx, fieldy, pin_dir):
        self.prio = prio
        self.piece = piece
        self.fieldx = fieldx
        self.fieldy = fieldy
        self.pin_dir = pin_dir
        self.attacker = []
        self.supporter = []

def analyze_position(match):
    analysis = []

    for y in range(8):
        for x in range(8):
            piece = match.readfield(x, y)

            if(piece == PIECES['blk']):
                continue
            else:
                frdlytouches, enmytouches = field_touches(match, Match.color_of_piece(piece), x, y)
                if(len(frdlytouches) > 0 or len(enmytouches) > 0):
                    pin_dir = rules.pin_dir(match, x, y)
                    analyzer = cAnalyzer(10, piece, x, y, pin_dir)
                    analyzer.attacker = enmytouches
                    analyzer.supporter = frdlytouches
                    analysis.append(analyzer)

    return analysis

