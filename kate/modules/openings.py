from kate.models import Match, Move
from kate.modules import values, calc, rules
import random


WHITEMOVES = [ ("e2", "e4"), ("d2", "d4"), ("c2", "c4"), ("g1", "f3"), ("g1", "e2"), 
           ("b1", "c3"), ("b1", "d2"), ("g2", "g3"), ("e2", "e3"), ("d2", "d3"), 
           ("c2", "c3") ]

BLACKMOVES = [ ("e7", "e5"), ("d7", "d5"), ("c7", "c5"), ("g8", "f6"), ("g8", "e7"), 
           ("b8", "c6"), ("b8", "d7"), ("g7", "g6"), ("e7", "e6"), ("d7", "d6"), 
           ("c7", "c6") ]

CNT = 11


def generate_move(match, cnt):
    if(cnt >= CNT):
        return -1, None
    if(match.next_color() == Match.COLORS['white']):
        print("w")
        move_list = WHITEMOVES
    else:
        print("b")
        move_list = BLACKMOVES

    for i in range(cnt, CNT):
        print("openings")
        x1, y1 = values.koord_to_index(move_list[i][0])
        x2, y2 = values.koord_to_index(move_list[i][1])
        if(rules.is_move_valid(match, x1, y1, x2, y2, Match.PIECES['blk'])[0]):
            print("openings found")
            gmove = calc.GenMove(x1, y1, x2, y2, Match.PIECES['blk'])  
            return i, gmove

    return -1, None

