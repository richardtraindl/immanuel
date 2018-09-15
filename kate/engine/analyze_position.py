from .match import *
from .pieces.pawn import cPawn
from .pieces.knight import cKnight
from .pieces.bishop import cBishop
from .pieces.rook import cRook
from .pieces.king import cKing
from .pieces.queen import cQueen
from .analyze_helper import list_all_field_touches, is_piece_stuck_new


def score_supports(match, color):
    score = 0

    for y in range(8):
        for x in range(8):
            piece = match.readfield(x, y)

            if(piece == match.PIECES['blk']):
                continue
            elif(match.color_of_piece(piece) != color):
                continue
            elif(piece == match.PIECES['wPw'] or piece == match.PIECES['bPw']):
                cpawn= cPawn(match, x, y)
                score += cpawn.score_supports()
            elif(piece == match.PIECES['wKn'] or piece == match.PIECES['bKn']):
                cknight= cKnight(match, x, y)
                score += cknight.score_supports()
            elif(piece == match.PIECES['wBp'] or piece == match.PIECES['bBp']):
                cbishop= cBishop(match, x, y)
                score += cbishop.score_supports()
            elif(piece == match.PIECES['wRk'] or piece == match.PIECES['bRk']):
                crook= cRook(match, x, y)
                score += crook.score_supports()
            elif(piece == match.PIECES['wQu'] or piece == match.PIECES['bQu']):
                cqueen= cQueen(match, x, y)
                score += cqueen.score_supports()
            else:
                cking= cKing(match, x, y)
                score += cking.score_supports()

    return score


def score_attacks(match, color):
    score = 0

    for y in range(8):
        for x in range(8):
            piece = match.readfield(x, y)

            if(piece == match.PIECES['blk']):
                continue
            #elif(Match.color_of_piece(piece) != color):
                #continue
            elif(piece == match.PIECES['wPw'] or piece == match.PIECES['bPw']):
                cpawn= cPawn(match, x, y)
                score += cpawn.score_attacks()
            elif(piece == match.PIECES['wKn'] or piece == match.PIECES['bKn']):
                cknight= cKnight(match, x, y)
                score += cknight.score_attacks()
            elif(piece == match.PIECES['wBp'] or piece == match.PIECES['bBp']):
                cbishop= cBishop(match, x, y)
                score += cbishop.score_attacks()
            elif(piece == match.PIECES['wRk'] or piece == match.PIECES['bRk']):
                crook= cRook(match, x, y)
                score += crook.score_attacks()    
            elif(piece == match.PIECES['wQu'] or piece == match.PIECES['bQu']):
                cqueen= cQueen(match, x, y)
                score += cqueen.score_attacks()
            else:
                cking= cKing(match, x, y)
                score += cking.score_attacks()

    return score


def score_controled_horizontal_files(match):
    score = 0

    whiterate = match.ATTACKED_SCORES[match.PIECES['bKn']]
    
    blackrate = match.ATTACKED_SCORES[match.PIECES['wKn']]

    for y in range(0, 2, 1):
        wcnt = 0
        bcnt = 0
        for x in range(8):
            piece = match.readfield(x, y)
            if(piece == match.PIECES['wRk'] or piece == match.PIECES['wQu']):
                wcnt += 1
            elif(piece == match.PIECES['bRk'] or piece == match.PIECES['bQu']):
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
            if(piece == match.PIECES['bRk'] or piece == match.PIECES['bQu']):
                bcnt += 1
            elif(piece == match.PIECES['wRk'] or piece == match.PIECES['wQu']):
                wcnt += 1
            else:
                continue

        if(wcnt > bcnt):
            score += whiterate

    return score


def score_controled_vertical_files(match):
    score = 0

    whiterate = match.ATTACKED_SCORES[match.PIECES['bKn']]
    
    blackrate = match.ATTACKED_SCORES[match.PIECES['wKn']]

    for x in range(8):
        wcnt = 0
        bcnt = 0
        wpwcnt = 0
        bpwcnt = 0
        for y in range(8):
            piece = match.readfield(x, y)
            if(piece == match.PIECES['blk']):
                continue
            elif(piece == match.PIECES['wPw']):
                wpwcnt += 1
                continue
            elif(piece == match.PIECES['bPw']):
                bpwcnt += 1
                continue
            elif(piece == match.PIECES['wRk'] or piece == match.PIECES['wQu']):
                wcnt += 1
                continue
            elif(piece == match.PIECES['bRk'] or piece == match.PIECES['bQu']):
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


def is_king_guarded(match, color):
    if(color == match.COLORS['white']):
        Kg_x = match.wKg_x
        Kg_y = match.wKg_y
        pawn = match.PIECES['wPw']

        if(match.is_endgame() == False and Kg_y > 0):
            return False
    else:
        Kg_x = match.bKg_x
        Kg_y = match.bKg_y
        pawn = match.PIECES['bPw']

        if(match.is_endgame() == False and Kg_y < 7):
            return False

    count = 0

    for i in range(8):
        x1 = Kg_x + cKing.STEPS[i][0]
        y1 = Kg_y + cKing.STEPS[i][1]
        if(match.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(piece == pawn):
                count += 2
            elif(match.color_of_piece(piece) == color):
                count += 1

    if(count >= 3):
        return True
    else:
        return False


def is_king_centered(match, color):
    if(color == match.COLORS['white']):
        x = match.wKg_x
        y = match.wKg_y
    else:
        x = match.bKg_x
        y = match.bKg_y

    if(x >= 2 and x <= 5 and y >= 2 and y <= 5):
        return True
    else:
        return False


def is_king_exposed(match, color):
    if(color == match.COLORS['white']):
        x = match.wKg_x
    else:
        x = match.bKg_x

    if(x == 3 or x == 4):
        return True
    else:
        return False


def is_rook_locked(match, color):
    if(color == match.COLORS['white']):
        y = 0
        rook = match.PIECES['wRk']
        king = match.PIECES['wKg']
    else:
        y = 7
        rook = match.PIECES['bRk']
        king = match.PIECES['bKg']

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

            if(piece == match.PIECES['blk']):
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


"""def score_baseline_cMatch.PIECES(match):
    score = 0

    cnt = 0
    y = 0
    for x in range(8):
        piece = match.readfield(x, y)
        if(piece == match.PIECES['wKn'] or piece == match.PIECES['wBp']):
            cnt += 1

    score += (cnt * match.ATTACKED_SCORES[match.PIECES['wKn']])

    cnt = 0
    y = 7
    for x in range(8):
        piece = match.readfield(x, y)
        if(piece == match.PIECES['bKn'] or piece == match.PIECES['bBp']):
            cnt += 1

    score += (cnt * match.ATTACKED_SCORES[match.PIECES['bKn']])

    return score"""


def score_opening(match):
    value = 0

    whiterate = match.ATTACKED_SCORES[match.PIECES['bKn']]

    blackrate = match.ATTACKED_SCORES[match.PIECES['wKn']]
    
    # white position
    y = 0
    cnt = 0
    for x in range(8):
        piece = match.readfield(x, y)
        if(piece == match.PIECES['wKn'] or piece == match.PIECES['wBp']):
            cnt += 1
    if(cnt > 1):
        value += cnt * blackrate
    ###

    # white king
    if(is_king_guarded(match, match.COLORS['white'])):
        value += whiterate

    if(match.white_movecnt_short_castling_lost > 0 and 
       match.white_movecnt_long_castling_lost > 0 and 
       is_king_exposed(match, match.COLORS['white'])):
        value += blackrate
    ###

    # white rook
    if(is_rook_locked(match, match.COLORS['white'])):
        value += blackrate
    ###

    # black position
    y = 7
    cnt = 0
    for x in range(8):
        piece = match.readfield(x, y)
        if(piece == match.PIECES['bKn'] or piece == match.PIECES['bBp']):
            cnt += 1
    if(cnt > 1):
        value += cnt * whiterate
    ###

    # black king
    if(is_king_guarded(match, match.COLORS['black'])):
        value += blackrate

    if(match.black_movecnt_short_castling_lost > 0 and
       match.black_movecnt_long_castling_lost > 0 and 
       is_king_exposed(match, match.COLORS['black'])):
        value += whiterate
    ###

    # black rook
    if(is_rook_locked(match, match.COLORS['black'])):
        value += whiterate
    ###

    return value


def score_game(match):
    value = 0

    whiterate = match.ATTACKED_SCORES[match.PIECES['bKn']]

    blackrate = match.ATTACKED_SCORES[match.PIECES['wKn']]

    # white
    if(is_king_guarded(match, match.COLORS['white'])):
        value += whiterate

    if(is_king_exposed(match, match.COLORS['white'])):
        value += blackrate

    if(is_rook_locked(match, match.COLORS['white'])):
        value += blackrate

    # black
    if(is_king_guarded(match, match.COLORS['black'])):
        value += blackrate

    if(is_king_exposed(match, match.COLORS['black'])):
        value += whiterate

    if(is_rook_locked(match, match.COLORS['black'])):
        value += whiterate

    return value


def score_endgame(match):
    value = 0

    whiterate = match.ATTACKED_SCORES[match.PIECES['bPw']]
    white_step_rates = [ 0, 0, 0, 2, 3, 5, 8, 12]
    blackrate = match.ATTACKED_SCORES[match.PIECES['wPw']]
    black_step_rates = [12, 8, 5, 3, 2, 0, 0, 0 ]

    for y in range(8):
        for x in range(8):
            piece = match.readfield(x, y)
            if(piece == match.PIECES['wPw']):
                cpawn = cPawn(match, x, y)
                if(cpawn.is_running()):
                    value += whiterate
                    value += whiterate * white_step_rates[y]
            elif(piece == match.PIECES['bPw']):
                cpawn = cPawn(match, x, y)
                if(cpawn.is_running()):
                    value += blackrate
                    value += blackrate * black_step_rates[y]

    """if(is_king_centered(match, match.COLORS['white'])):
        value += whiterate

    if(is_king_centered(match, match.COLORS['black'])):
          value += blackrate"""

    return value


def score_stucks(match):
    whiterate = match.ATTACKED_SCORES[match.PIECES['bPw']]
    blackrate = match.ATTACKED_SCORES[match.PIECES['wPw']]
    score = 0

    for y in range(8):
        for x in range(8):
            piece = match.readfield(x, y)
            if(piece == match.PIECES['blk']):
                continue

            if(is_piece_stuck_new(match, x, y)):
                if(match.color_of_piece(piece) == match.COLORS['white']):
                    score += blackrate
                else:
                    score += whiterate

    return score


def score_position(match, movecnt):
    status = match.evaluate_status()

    if(movecnt == 0 and status != match.STATUS['open']):
        if(status == match.STATUS['winner_black']):
            return ( match.SCORES[match.PIECES['wKg']] + match.movecnt )
        elif(status == match.STATUS['winner_white']):
            return ( match.SCORES[match.PIECES['bKg']] - match.movecnt )
        else: # draw
            return match.SCORES[match.PIECES['blk']]
    else:
        score = match.score

        color = match.next_color()

        #score += score_stucks(match)

        #----------------------------------------
        #score += score_attacks(match, color)

        #score += score_supports(match, match.REVERSED_COLORS[color])

        #score += score_controled_horizontal_files(match)

        #score += score_controled_vertical_files(match)
        #----------------------------------------

        if(match.is_opening()):
            score += score_opening(match)
        elif(match.is_endgame()):
            score += score_endgame(match)
        else:
            score += score_game(match)

        return score


"""def is_capture_possible(match, color):
    for y in range(8):
        for x in range(8):
            piece = match.readfield(x, y)

            if(piece == match.PIECES['blk']):
                continue
            elif(Match.color_of_piece(piece) != color):
                continue
            elif(piece == match.PIECES['wPw'] or piece == match.PIECES['bPw']):
                if(pawn.is_capture_possible(match, x, y)):
                    return True
            elif(piece == match.PIECES['wKn'] or piece == match.PIECES['bKn']):
                if(knight.is_capture_possible(match, x, y)):
                    return True
            elif(piece == match.PIECES['wBp'] or piece == match.PIECES['bBp']):
                if(bishop.is_capture_possible(match, x, y)):
                    return True
            elif(piece == match.PIECES['wRk'] or piece == match.PIECES['bRk']):
                if(rook.is_capture_possible(match, x, y)):
                    return True
            elif(piece == match.PIECES['wQu'] or piece == match.PIECES['bQu']):
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

            if(piece == match.PIECES['blk']):
                continue
            else:
                friends, enemies = list_all_field_touches(match, Match.color_of_piece(piece), x, y)
                if(len(friends) < len(enemies)):
                    return True
                else:
                    for enemy in enemies:
                        if(match.PIECES_RANK[enemy.piece] <= match.PIECES_RANK[piece]):
                            return True

    return False


def is_stormy(match):
    color = match.next_color()

    ### is pawn on last row before promotion
    if(color == match.COLORS['white']):
        y = 6
        pw = match.PIECES['wPw']
    else:
        y = 1
        pw = match.PIECES['bPw']
    for x in range(8):
        piece = match.readfield(x, y)
        if(piece == pw):
            return True
    ###

    ### attacks
    for y in range(8):
        for x in range(8):
            piece = match.readfield(x, y)
            if(piece == match.PIECES['blk']):
                continue

            piece_color = match.color_of_piece(piece)

            frdlytouches, enmytouches = list_all_field_touches(match, piece_color, x, y)

            if(piece == match.PIECES['wKg'] or piece == match.PIECES['bKg']):
                if(len(enmytouches) > 0):
                    return True
                else:
                    continue

            #if(len(enmytouches) > len(frdlytouches)):
                #return True

            if(match.is_pinned(x, y) or match.is_soft_pin(x, y)):
                return True

            for enmy in enmytouches:
                if(match.PIECES_RANK[enmy.piece] < match.PIECES_RANK[piece]):
                    return True

                """enmyfriends, enmyenemies = list_all_field_touches(match, Match.color_of_piece(enmy.piece), enmy.fieldx, enmy.fieldy)
                if(len(enmyenemies) == 0):
                    print("is_stormy: enmyenemies == 0")
                    return True"""
    ###

    return False


