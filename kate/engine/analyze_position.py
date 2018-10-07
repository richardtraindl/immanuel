from .values import *
from .match import *
from .pieces.pawn import cPawn
from .pieces.knight import cKnight
from .pieces.bishop import cBishop
from .pieces.rook import cRook
from .pieces.king import cKing
from .pieces.queen import cQueen
from .analyze_helper import list_all_field_touches, is_piece_stuck_new


def score_stucks(match):
    whiterate = ATTACKED_SCORES[PIECES['bPw']]
    blackrate = ATTACKED_SCORES[PIECES['wPw']]
    score = 0

    for y in range(8):
        for x in range(8):
            piece = match.readfield(x, y)
            if(piece == PIECES['blk']):
                continue

            if(is_piece_stuck_new(match, x, y)):
                if(match.color_of_piece(piece) == COLORS['white']):
                    score += blackrate
                else:
                    score += whiterate

    return score


def score_attacks(match, color):
    score = 0

    for y in range(8):
        for x in range(8):
            piece = match.readfield(x, y)

            if(piece == PIECES['blk']):
                continue
            #elif(Match.color_of_piece(piece) != color):
                #continue
            elif(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                cpawn= cPawn(match, x, y)
                score += cpawn.score_attacks()
            elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                cknight= cKnight(match, x, y)
                score += cknight.score_attacks()
            elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
                cbishop= cBishop(match, x, y)
                score += cbishop.score_attacks()
            elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
                crook= cRook(match, x, y)
                score += crook.score_attacks()    
            elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                cqueen= cQueen(match, x, y)
                score += cqueen.score_attacks()
            else:
                cking= cKing(match, x, y)
                score += cking.score_attacks()

    return score


def score_supports(match, color):
    score = 0

    for y in range(8):
        for x in range(8):
            piece = match.readfield(x, y)

            if(piece == PIECES['blk']):
                continue
            elif(match.color_of_piece(piece) != color):
                continue
            elif(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                cpawn= cPawn(match, x, y)
                score += cpawn.score_supports()
            elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                cknight= cKnight(match, x, y)
                score += cknight.score_supports()
            elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
                cbishop= cBishop(match, x, y)
                score += cbishop.score_supports()
            elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
                crook= cRook(match, x, y)
                score += crook.score_supports()
            elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                cqueen= cQueen(match, x, y)
                score += cqueen.score_supports()
            else:
                cking= cKing(match, x, y)
                score += cking.score_supports()

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


def is_rook_on_baseline_trapped(match, color):
    if(color == COLORS['white']):
        y = match.board.COORD['1']
        rookpiece = PIECES['wRk']
    else:
        y = match.board.COORD['8']
        rookpiece = PIECES['bRk']

    for x in range(8):
        piece = match.readfield(x, y)
        if(piece == rookpiece):
            rook = cRook(match, x, y)
            if(rook.is_rook_trapped()):
                return True
    return False

def score_trapped_rooks(match):
    value = 0
    whiterate = ATTACKED_SCORES[PIECES['bKn']]
    blackrate = ATTACKED_SCORES[PIECES['wKn']]
    if(is_rook_on_baseline_trapped(match, COLORS['white'])):
        value += blackrate
    if(is_rook_on_baseline_trapped(match, COLORS['black'])):
        value += whiterate
    return value

def score_kings_safety(match):
    value = 0
    whiterate = ATTACKED_SCORES[PIECES['bKn']]
    blackrate = ATTACKED_SCORES[PIECES['wKn']]
    king = cKing(match, match.board.wKg_x, match.board.wKg_y)
    if(king.is_king_safe()):
        value += whiterate
    king = cKing(match, match.board.bKg_x, match.board.bKg_y)
    if(king.is_king_safe()):
        value += blackrate
    return value

def score_stuck_pieces_on_baseline(match):
    value = 0
    whiterate = ATTACKED_SCORES[PIECES['bKn']]
    blackrate = ATTACKED_SCORES[PIECES['wKn']]
    for i in range(2):
        if(i == 0):
            y = match.board.COORD['1']
            knight = PIECES['wKn']
            bishop = PIECES['wBp']
            rate = blackrate
        else:
            y = match.board.COORD['8']
            knight = PIECES['bKn']
            bishop = PIECES['bBp']
            rate = whiterate
        for x in range(8):
            piece = match.readfield(x, y)
            if(piece == knight or piece == bishop):
                value += rate
    return value


def score_opening(match):
    value = 0
    value += score_stuck_pieces_on_baseline(match)
    value += score_kings_safety(match)
    value += score_trapped_rooks(match)
    return value


def score_middlegame(match):
    value = 0
    value += score_stuck_pieces_on_baseline(match)
    value += score_kings_safety(match)
    value += score_trapped_rooks(match)
    return value

def score_endgame(match):
    value = 0

    whiterate = ATTACKED_SCORES[PIECES['bPw']]
    white_step_rates = [ 0, 0, 0, 2, 3, 5, 8, 12]
    blackrate = ATTACKED_SCORES[PIECES['wPw']]
    black_step_rates = [12, 8, 5, 3, 2, 0, 0, 0 ]
    for y in range(8):
        for x in range(8):
            piece = match.readfield(x, y)
            if(piece == PIECES['wPw']):
                cpawn = cPawn(match, x, y)
                if(cpawn.is_running()):
                    value += whiterate
                    value += whiterate * white_step_rates[y]
            elif(piece == PIECES['bPw']):
                cpawn = cPawn(match, x, y)
                if(cpawn.is_running()):
                    value += blackrate
                    value += blackrate * black_step_rates[y]

    value += score_stuck_pieces_on_baseline(match)
    value += score_trapped_rooks(match)
    return value


def score_position(match, movecnt):
    status = match.evaluate_status()

    if(movecnt == 0 and status != match.STATUS['open']):
        if(status == match.STATUS['winner_black']):
            return ( SCORES[PIECES['wKg']] + match.movecnt() )
        elif(status == match.STATUS['winner_white']):
            return ( SCORES[PIECES['bKg']] - match.movecnt() )
        else: # draw
            return SCORES[PIECES['blk']]
    else:
        score = match.score

        color = match.next_color()

        #score += score_stucks(match)

        #score += score_attacks(match, color)

        #score += score_supports(match, REVERSED_COLORS[color])

        #score += score_controled_horizontal_files(match)

        #score += score_controled_vertical_files(match)

        if(match.is_opening()):
            score += score_opening(match)
        elif(match.is_endgame()):
            score += score_endgame(match)
        else:
            score += score_middlegame(match)

        return score


def is_stormy(match):
    color = match.next_color()

    ### is pawn on last row before promotion
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

    ### attacks
    for y in range(8):
        for x in range(8):
            piece = match.readfield(x, y)
            if(piece == PIECES['blk']):
                continue

            piece_color = match.color_of_piece(piece)

            frdlytouches, enmytouches = list_all_field_touches(match, piece_color, x, y)

            if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
                if(len(enmytouches) > 0):
                    return True
                else:
                    continue

            #if(len(enmytouches) > len(frdlytouches)):
                #return True

            if(match.is_pinned(x, y) or match.is_soft_pin(x, y)):
                return True

            for enmy in enmytouches:
                if(PIECES_RANK[enmy.piece] < PIECES_RANK[piece]):
                    return True

                """enmyfriends, enmyenemies = list_all_field_touches(match, Match.color_of_piece(enmy.piece), enmy.fieldx, enmy.fieldy)
                if(len(enmyenemies) == 0):
                    print("is_stormy: enmyenemies == 0")
                    return True"""
    ###

    return False


