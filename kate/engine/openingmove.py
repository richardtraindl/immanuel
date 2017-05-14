from kate.engine import match, move, openings, rules, calc
from kate.engine.match import *
from kate.engine.openings import * 
import random, copy


def retrieve_move(match):
    if(match.count >= DEPTH):
        print("############ depth not supported ############")
        return None
        
    lastmoves = ""
    for move in match.move_list:
        lastmoves += Match.index_to_koord(move.srcx, move.srcy)
        lastmoves += "-"
        lastmoves +=Match.index_to_koord(move.dstx, move.dsty)
        lastmoves += ","
    
    lastmoves = lastmoves[:-1]
    print("lastmoves: " + lastmoves)

    if(match.count == 0):
        omovelist = FIRST
    elif(match.count == 1):
        omovelist = SECOND
    else:
        omovelist = THIRD

    candidates = []
    for omove in omovelist:
        if(omove[0] == lastmoves):
            candidates.append(omove[1])

    if(len(candidates) == 0):
        print("############ No opening move found ############")
        return None
    else:
        idx = random.randint(0, len(candidates) - 1)
        candidate = candidates[idx]
        srcx, srcy = Match.koord_to_index(candidate[:2])
        dstx, dsty = Match.koord_to_index(candidate[3:])
        return calc.GenMove(srcx, srcy, dstx, dsty, PIECES['blk'])

