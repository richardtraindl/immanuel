import random
from .values import *
from .match import *
from .move import *
from .openings import DEPTH, fill_openings
from .helper import coord_to_index, index_to_coord


def retrieve_move(match):
    if(match.movecnt() >= DEPTH):
        print("############ depth not supported ############")
        return None

    root = fill_openings()
    node = root
    for move in match.move_list:
        str_move = index_to_coord(move.srcx, move.srcy)
        str_move += "-"
        str_move += index_to_coord(move.dstx, move.dsty)
        ok = False
        for childnode in node.children:
            #print("childnode: " + str(childnode.str_move) + " str_move: " + str_move)
            if(childnode.str_move == str_move):
                    node = childnode
                    ok = True
                    break
        if(ok):
            continue
        else:
            node = None

    if(match.movecnt() > 0 and (node is None or node is root or len(node.children) == 0)):
        print("############ No opening move found ############")
        return None
    else:
        if(match.movecnt() == 0):
            node = root
        idx = random.randint(0, len(node.children) - 1)
        candidate = node.children[idx]
        srcx, srcy = coord_to_index(candidate.str_move[:2])
        dstx, dsty = coord_to_index(candidate.str_move[3:])
        return cGenMove(match, srcx, srcy, dstx, dsty, PIECES['blk'])

 