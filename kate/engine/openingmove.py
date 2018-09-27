import random
from .values import *
from .match import *
from .move import *
from .openings import *
from .helper import coord_to_index, index_to_coord


def retrieve_move(match):
    if(match.movecnt >= DEPTH):
        print("############ depth not supported ############")
        return None
        
    lastmoves = ""
    for move in match.move_list:
        lastmoves += index_to_coord(move.srcx, move.srcy)
        lastmoves += "-"
        lastmoves += index_to_coord(move.dstx, move.dsty)
        lastmoves += ","
    
    lastmoves = lastmoves[:-1]
    print("lastmoves: " + lastmoves)

    if(match.movecnt == 0):
        omovelist = FIRST
    elif(match.movecnt == 1):
        omovelist = SECOND
    elif(match.movecnt == 2):
        omovelist = THIRD
    else:
        omovelist = FOURTH

    candidates = []
    for omove in omovelist:
        if(omove[0] == lastmoves):            
            candidates = omove[1:]
            break

    if(len(candidates) == 0):
        print("############ No opening move found ############")
        return None
    else:
        idx = random.randint(0, len(candidates) - 1)
        candidate = candidates[idx]
        srcx, srcy = coord_to_index(candidate[:2])
        dstx, dsty = coord_to_index(candidate[3:])
        return cGenMove(match, srcx, srcy, dstx, dsty, PIECES['blk'])

