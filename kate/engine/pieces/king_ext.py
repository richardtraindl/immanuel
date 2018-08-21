from .king import cKing
from .piece import cTouchBeyond
from .. import analyze_helper


STEPS = [ [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1] ]

def score_attacks(match, srcx, srcy):
    score = 0

    king = match.readfield(srcx, srcy)

    color = match.color_of_piece(king)
    opp_color = match.oppcolor_of_piece(king)

    for i in range(8):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(match.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(match.color_of_piece(piece) == opp_color):
                score += match.ATTACKED_SCORES[piece]

                # extra score if attacked is pinned
                enmy_pin = match.evaluate_pin_dir(x1, y1) #opp_color, 
                if(enmy_pin != match.DIRS['undefined']):
                    score += match.ATTACKED_SCORES[piece]

                if(analyze_helper.is_soft_pin(match, x1, y1)):
                    score += match.ATTACKED_SCORES[piece]

    return score


def score_supports(match, srcx, srcy):
    score = 0

    king = match.readfield(srcx, srcy)

    color = match.color_of_piece(king)
    opp_color = match.oppcolor_of_piece(king)

    for i in range(8):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(match.is_inbounds(x1, y1)):
            if(x1 == srcx and y1 == srcy):
                continue

            frdlytouches, enmytouches = analyze_helper.field_touches(match, color, x1, y1)
            if(len(frdlytouches) < len(enmytouches)):
                continue

            piece = match.readfield(x1, y1)

            if(match.color_of_piece(piece) == color):
                if(len(enmytouches) == 0):
                    score += match.ATTACKED_SCORES[piece]

                # extra score if attacked is pinned
                enmy_pin = match.evaluate_pin_dir(x1, y1) # opp_color, 
                if(enmy_pin != match.DIRS['undefined']):
                    score += match.ATTACKED_SCORES[piece]

                if(analyze_helper.is_soft_pin(match, x1, y1)):
                    score += match.ATTACKED_SCORES[piece]

    return score 


def is_king_safe(match, color):
    if(color == match.COLORS['white']):
        Kg_x = match.wKg_x
        Kg_y = match.wKg_y
    else:
        Kg_x = match.bKg_x
        Kg_y = match.bKg_y

    for i in range(8):
        x1 = Kg_x + STEPS[i][0]
        y1 = Kg_y + STEPS[i][1]
        if(match.is_inbounds(x1, y1)):
            friends, enemies = field_touches(match, color, x1, y1)
            if(len(friends) < len(enemies)):
                return False

    friends.clear()
    enemies.clear()
    friends, enemies = field_touches(match, color, Kg_x, Kg_y)
    if(len(enemies) >= 2):
        return False

    for enemy in enemies:
        friends_beyond, enemies_beyond = field_touches(match, color, enemy[1], enemy[2])
        if(len(friends_beyond) >= len(enemies_beyond)):
            continue

        direction = rook.rk_dir(Kg_x, Kg_y, enemy[1], enemy[2])
        if(direction != match.DIRS['undefined']):
            direction, step_x, step_y = rook.rk_step(direction, None, None, None, None)
        else:
            direction = bishop.bp_dir(Kg_x, Kg_y, enemy[1], enemy[2])
            if(direction != match.DIRS['undefined']):
                direction, step_x, step_y = bishop.bp_step(direction, None, None, None, None)
            else:
                return False

        x1 = Kg_x + step_x
        y1 = Kg_y + step_y
        while(match.is_inbounds(x1, y1)):
            blocking_friends, blocking_enemies = field_touches(match, color, x1, y1)
            if(len(blocking_friends) > 0):
                break

    return True

