from kate.models import Match
from kate.modules import values, rules, calc


WHITEMOVES = [ ("c4", "b5"), ("c4", "d5"), ("d4", "c5"), ("d4", "e5"), 
               ("e4", "d5"), ("e4", "f5"), ("c5", "b6"), ("c5", "d6"), 
               ("d5", "c6"), ("d5", "e6"), ("e5", "d6"), ("e5", "f6"), 
               ("f5", "e6"), ("f5", "g6"), ("e2", "e4"), ("d2", "d4"), 
               ("c2", "c4"), ("g1", "f3"), ("g1", "e2"), ("b1", "c3"), 
               ("b1", "d2"), ("g2", "g3"), ("e2", "e3"), ("d2", "d3"), 
               ("c2", "c3") ]

BLACKMOVES = [ ("c5", "b4"), ("c5", "d4"), ("d5", "c4"), ("d5", "e4"),
               ("e5", "d4"), ("e5", "f4"), ("c4", "b3"), ("c4", "d3"), 
               ("d4", "c3"), ("d4", "e3"), ("e4", "d3"), ("e4", "f3"), 
               ("f4", "e3"), ("f4", "g3"), ("e7", "e5"), ("d7", "d5"), 
               ("c7", "c5"), ("g8", "f6"), ("g8", "e7"), ("b8", "c6"), 
               ("b8", "d7"), ("g7", "g6"), ("e7", "e6"), ("d7", "d6"), 
               ("c7", "c6") ]
CNT = 25


def generate_move(match, cnt):
    if(match.next_color() == Match.COLORS['white']):
        move_list = WHITEMOVES
    else:
        move_list = BLACKMOVES

    if(cnt >= CNT):
        return CNT + 1, None

    for i in range(cnt, CNT):
        x1, y1 = values.koord_to_index(move_list[i][0])
        x2, y2 = values.koord_to_index(move_list[i][1])
        if(rules.is_move_valid(match, x1, y1, x2, y2, Match.PIECES['blk'])[0]):
            gmove = calc.GenMove(x1, y1, x2, y2, Match.PIECES['blk'])
            return i, gmove

    return CNT + 1, None

