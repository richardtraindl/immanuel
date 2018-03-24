from .match import *
from .cvalues import *
from . import rules
from .pieces import pawn, knight, bishop, rook, king 
from .pieces.generic_piece import cTouch
from .analyze_helper import field_touches_beyond, field_touches, is_soft_pin



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


def is_opening(match):
    return match.movecnt <= 30


def is_endgame(match):
    white_cnt = match.wQu_cnt + match.wOfficer_cnt
    black_cnt = match.bQu_cnt + match.bOfficer_cnt
    return (white_cnt <= 3 and black_cnt <= 3)


def is_king_guarded(match, color):
    if(color == COLORS['white']):
        Kg_x = match.wKg_x
        Kg_y = match.wKg_y
        pawn = PIECES['wPw']
    else:
        Kg_x = match.bKg_x
        Kg_y = match.bKg_y
        pawn = PIECES['bPw']
    
    count = 0
    
    for i in range(8):
        x1 = Kg_x + king.STEPS[i][0]
        y1 = Kg_y + king.STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(piece == pawn):
                count += 2
            elif(Match.color_of_piece(piece) == color):
                count += 1

    if(count >= 3):
        return True
    else:
        return False


def is_king_centered(match, color):
    if(color == COLORS['white']):
        x = match.wKg_x
    else:
        x = match.bKg_x

    if(x == 3 or x == 4):
        return True
    else:
        return False


def is_rook_locked(match, color):
    if(color == COLORS['white']):
        y = 0
        rook = PIECES['wRk']
        king = PIECES['wKg']
    else:
        y = 7
        rook = PIECES['bRk']
        king = PIECES['bKg']

    for i in range(2):
        if(i == 0):
            start = 0
            end = 3
            step = 1
        else:
            start = 7
            end = 4
            step = -1

        first = None
        second = None
        for x in range(start, end, step):
            piece = match.readfield(x, y)

            if(piece == PIECES['blk']):
                continue
            elif(piece == rook):
                if(first is None):
                    first = rook
                elif(second is None):
                    second = rook
            elif(piece == king):
                if(first is None):
                    first = king
                elif(second is None):
                    second = king
                else:
                    return True

        if(first == rook and second == king):
            return True

    return False


"""def score_baseline_pieces(match):
    score = 0

    cnt = 0
    y = 0
    for x in range(8):
        piece = match.readfield(x, y)
        if(piece == PIECES['wKn'] or piece == PIECES['wBp']):
            cnt += 1

    score += (cnt * ATTACKED_SCORES[PIECES['wKn']])

    cnt = 0
    y = 7
    for x in range(8):
        piece = match.readfield(x, y)
        if(piece == PIECES['bKn'] or piece == PIECES['bBp']):
            cnt += 1

    score += (cnt * ATTACKED_SCORES[PIECES['bKn']])

    return score"""


def score_opening(match):
    value = 0

    whiterate = ATTACKED_SCORES[PIECES['bKn']]

    blackrate = ATTACKED_SCORES[PIECES['wKn']]

    # white position
    y = 0
    cnt = 0
    for x in range(8):
        piece = match.readfield(x, y)
        if(piece == PIECES['wKn'] or piece == PIECES['wBp']):
            cnt += 1
    if(cnt > 1):
        value += cnt * blackrate

    # black position
    y = 7
    cnt = 0
    for x in range(8):
        piece = match.readfield(x, y)
        if(piece == PIECES['bKn'] or piece == PIECES['bBp']):
            cnt += 1
    if(cnt > 1):
        value += cnt * whiterate

    # white king
    if(is_king_guarded(match, COLORS['white'])):
        value += whiterate

    if(match.white_movecnt_short_castling_lost > -1 and 
       match.white_movecnt_long_castling_lost > -1 and 
       is_king_centered(match, COLORS['white'])):
        value += blackrate

    if(is_rook_locked(match, COLORS['white'])):
        value += blackrate

    # black king
    if(is_king_guarded(match, COLORS['black'])):
        value += blackrate

    if(match.black_movecnt_short_castling_lost > -1 and
       match.black_movecnt_long_castling_lost > -1 and 
       is_king_centered(match, COLORS['black'])):
        value += whiterate

    if(is_rook_locked(match, COLORS['black'])):
        value += whiterate

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


def score_game(match):
    value = 0

    whiterate = ATTACKED_SCORES[PIECES['bKn']]

    blackrate = ATTACKED_SCORES[PIECES['wKn']]

    # white
    if(is_king_guarded(match, COLORS['white'])):
        value += whiterate

    if(is_king_centered(match, COLORS['white'])):
        value += blackrate

    if(is_rook_locked(match, COLORS['white'])):
        value += blackrate

    # black
    if(is_king_guarded(match, COLORS['black'])):
        value += blackrate

    if(is_king_centered(match, COLORS['black'])):
        value += whiterate

    if(is_rook_locked(match, COLORS['black'])):
        value += whiterate

    return value


def score_position(match, movecnt):
    status = rules.status(match)

    if(movecnt == 0 and status != STATUS['open']):
        if(status == STATUS['winner_black']):
            return ( SCORES[PIECES['wKg']] + match.movecnt )
        elif(status == STATUS['winner_white']):
            return ( SCORES[PIECES['bKg']] - match.movecnt )
        else: # draw
            return SCORES[PIECES['blk']]
    else:
        score = match.score
        
        color = match.next_color()

        score += score_attacks(match, color)

        #score += score_supports(match, REVERSED_COLORS[color])

        #score += score_controled_horizontal_files(match)

        #score += score_controled_vertical_files(match)

        if(is_opening(match)):
            score += score_opening(match)
        elif(is_endgame(match)):
            score += score_endgame(match)
        else:
            score += score_game(match)

        return score


"""def is_capture_possible(match, color):
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

    return False"""


def are_attacks_or_captures_possible(match):
    for y in range(8):
        for x in range(8):
            piece = match.readfield(x, y)

            if(piece == PIECES['blk']):
                continue
            else:
                friends, enemies = field_touches(match, Match.color_of_piece(piece), x, y)
                if(len(friends) < len(enemies)):
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
    """for y in range(8):
        for x in range(8):
            piece = match.readfield(x, y)
            if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
                continue

            if(is_soft_pin(match, x, y)):
                return True"""

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
                    pin_dir = rules.pin_dir(match, None, x, y)
                    analyzer = cAnalyzer(10, piece, x, y, pin_dir)
                    analyzer.attacker = enmytouches
                    analyzer.supporter = frdlytouches
                    analysis.append(analyzer)

    return analysis

