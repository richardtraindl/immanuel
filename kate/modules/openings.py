from kate.models import Match, Move
from kate.modules import values, calc
import random



def calc_opening(match):
    score = 0
    print(str(match.count))
    if(match.count == 0):
        MOVES1 = [ ("e2", "e4"), ("d2", "d4"), ("c2", "c4"), ("g1", "f3"), 
                  ("g2", "g3"), ("e2", "e3"), ("d2", "d3") ]
        idx = random.randint(0, 6)
        x1, y1 = values.koord_to_index(MOVES1[idx][0])
        x2, y2 = values.koord_to_index(MOVES1[idx][1])
        gmove = calc.GenMove(x1, y1, x2, y2, Match.PIECES['blk'])
    elif(match.count == 1):
        MOVES2 = [ ("d7", "d5"), ("c7", "c5"), ("e7", "e5"), ("g8", "f6"), 
                  ("g7", "g6"), ("e7", "e6"), ("d7", "d6") ]
        idx = random.randint(0, 6)
        x1, y1 = values.koord_to_index(MOVES2[idx][0])
        x2, y2 = values.koord_to_index(MOVES2[idx][1])
        gmove = calc.GenMove(x1, y1, x2, y2, Match.PIECES['blk'])
    elif(match.count == 2):
        gmove = None
    elif(match.count == 3):
        gmove = None
    elif(match.count == 4):
        gmove = None
    else:
        gmove = None
    return score, gmove