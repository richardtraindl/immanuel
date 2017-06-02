from .match import *
from .move import *
from .helper import *


def prnt_moves(match):
    count = 1
    print("------------------------------------------------------")
    for move in match.move_list[1:]:
        print(str(count) + ": " + 
              index_to_coord(move.srcx, move.srcy) + " " +
              index_to_coord(move.dstx, move.dsty) + " " +
              reverse_lookup(PIECES, move.prom_piece))
        count += 1
    print("------------------------------------------------------")



def prnt_attributes(match):
    print("------------------------------------------------------")
    print("status: " + str(match.status))
    print("count: " + str(match.count))
    print("score: " + str(match.score)) 
    print("white_player: " + str(match.white_player))
    print("white_player_human: " + str(match.white_player_human))
    print("black_player: " + str(match.black_player))
    print("black_player_human: " + str(match.black_player_human))
    print("fifty_moves_count: " + str(match.fifty_moves_count))
    print("wKg_x: " + str(match.wKg_x))
    print("wKg_y: " + str(match.wKg_y))
    print("bKg_x: " + str(match.bKg_x))
    print("bKg_y: " + str(match.bKg_y))
    print("wKg_first_movecnt: " + str(match.wKg_first_movecnt))
    print("bKg_first_movecnt: " + str(match.bKg_first_movecnt))
    print("wRk_a1_first_movecnt: " + str(match.wRk_a1_first_movecnt))
    print("wRk_h1_first_movecnt: " + str(match.wRk_h1_first_movecnt)) 
    print("bRk_a8_first_movecnt: " + str(match.bRk_a8_first_movecnt)) 
    print("bRk_h8_first_movecnt: " + str(match.bRk_h8_first_movecnt))
    print("level: " + str(match.level))    
    print("------------------------------------------------------")


def prnt_board(match):
    print("------------------------------------------------------")
    for i in range(7, -1, -1):
        for j in range(8):
            piece = match.readfield(j, i)
            print(reverse_lookup(PIECES, piece) + " ", end="")
        print("")
    print("------------------------------------------------------")


def prnt_generator(generator):
    print("------------------------------------------------------")
    print("steps: " + str(generator.steps))
    print("board_x: " + str(generator.board_x))
    print("board_y: " + str(generator.board_y))
    print("dir_idx: " + str(generator.dir_idx))
    print("max_dir: " + str(generator.max_dir))
    print("step_idx: " + str(generator.step_idx))
    print("max_step: " + str(generator.max_step))
    print("------------------------------------------------------")


def write_searchmoves(debug_candidates, path):
    fobject = open(path + "/data/searchmoves.py","w")

    for i in range(20):
        """if(debug_candidates[i][0]):"""
        for cand in debug_candidates[i]:
            if(cand):
                str_move = index_to_coord(cand.srcx, cand.srcy) + "-"
                str_move += index_to_coord(cand.dstx, cand.dsty) + "-"
                str_move += reverse_lookup(PIECES, cand.prom_piece) + ";"
                fobject.write(str_move)
            else:
                fobject.write("\n")
                break
        """else:
               break"""

    fobject.close()


def read_searchmoves(path):
    fobject = open(path + "/data/searchmoves.py","r")
    
    data = ""

    for line in fobject:
        data += "[" + line + "]"

    fobject.close()

    return data



