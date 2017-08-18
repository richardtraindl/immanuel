import os
from .match import *
from .move import *
from .helper import *
from .cvalues import *


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


def write_searchmoves(match, debug_candidates, path):
    os.makedirs(path + "/data", exist_ok=True)
    try:
        fobject = open(path + "/data/searchmoves.dat","w")
    except FileNotFoundError:
        return

    fobject.write(str(match.id) + "\n")
    fobject.write(str(match.status) + "\n")
    fobject.write(str(match.count) + "\n")
    fobject.write(str(match.score) + "\n")
    fobject.write(str(match.white_player) + "\n")
    fobject.write(str(match.white_player_human) + "\n")
    fobject.write(str(match.elapsed_time_white) + "\n")
    fobject.write(str(match.black_player) + "\n")
    fobject.write(str(match.black_player_human) + "\n")
    fobject.write(str(match.elapsed_time_black) + "\n")
    
    for y in range(8):
        for x in range(8):
            if(x < 7):
                delimeter = ";"
            else:
                delimeter = "\n"
            fobject.write( str(match.readfield(x, y)) + delimeter )

    fobject.write(str(match.fifty_moves_count) + "\n")
    fobject.write(str(match.wKg_x) + "\n")
    fobject.write(str(match.wKg_y) + "\n")
    fobject.write(str(match.bKg_x) + "\n")
    fobject.write(str(match.bKg_y) + "\n")
    fobject.write(str(match.wKg_first_movecnt) + "\n")
    fobject.write(str(match.bKg_first_movecnt) + "\n")
    fobject.write(str(match.wRk_a1_first_movecnt) + "\n")
    fobject.write(str(match.wRk_h1_first_movecnt) + "\n")
    fobject.write(str(match.bRk_a8_first_movecnt) + "\n")
    fobject.write(str(match.bRk_h8_first_movecnt) + "\n")

    if(len(match.move_list) == 0):
        fobject.write("\n")
    else:
        move = match.move_list[-1]
        fobject.write(str(move.match.id) + ";")
        fobject.write(str(move.count) + ";")
        fobject.write(str(move.move_type) + ";")
        fobject.write(str(move.srcx) + ";")
        fobject.write(str(move.srcy) + ";")
        fobject.write(str(move.dstx) + ";")
        fobject.write(str(move.dsty) + ";")
        fobject.write(str(move.e_p_fieldx) + ";")
        fobject.write(str(move.e_p_fieldy) + ";")
        fobject.write(str(move.captured_piece) + ";")
        fobject.write(str(move.prom_piece) + ";")
        fobject.write(str(move.fifty_moves_count) + ";\n")

    for threadmoves in debug_candidates:
        for gmove in threadmoves:
            if(gmove):
                src = str(gmove.srcx) + ";" + str(gmove.srcy) + ";" 
                fobject.write(src)
                dst = str(gmove.dstx) + ";" + str(gmove.dsty) + ";"
                fobject.write(dst)
                prom = str(gmove.prom_piece) + "]"
                fobject.write(prom)
            else:
                break

        fobject.write("\n")

    fobject.close()


def read_searchmoves(path):
    try:
        fobject = open(path + "/data/searchmoves.dat","r")
    except FileNotFoundError:
        return

    lines = fobject.read().splitlines() 
    match = Match()    
    match.id = lines[0].rstrip('\n')
    match.status = int(lines[1].rstrip('\n'))
    match.count = int(lines[2].rstrip('\n'))
    match.score = int(lines[3].rstrip('\n'))
    match.white_player = lines[4].rstrip('\n')
    match.white_player_human = bool(lines[5].rstrip('\n'))
    match.elapsed_time_white = int(lines[6].rstrip('\n'))
    match.black_player = lines[7].rstrip('\n')
    match.black_player_human = bool(lines[8].rstrip('\n'))
    match.elapsed_time_black = int(lines[9].rstrip('\n'))

    y = 0
    for line in lines[10:18]:
        line = line.rstrip('\n')
        fields = line.split(";")
        x = 0
        for field in fields:
            match.writefield(x, y, int(field))
            x += 1
        y += 1

    match.fifty_moves_count = int(lines[18].rstrip('\n'))
    match.wKg_x = int(lines[19].rstrip('\n'))
    match.wKg_y = int(lines[20].rstrip('\n'))
    match.bKg_x = int(lines[21].rstrip('\n'))
    match.bKg_y = int(lines[22].rstrip('\n'))
    match.wKg_first_movecnt = int(lines[23].rstrip('\n'))
    match.bKg_first_movecnt = int(lines[24].rstrip('\n'))
    match.wRk_a1_first_movecnt = int(lines[25].rstrip('\n'))
    match.wRk_h1_first_movecnt = int(lines[26].rstrip('\n'))
    match.bRk_a8_first_movecnt = int(lines[27].rstrip('\n'))
    match.bRk_h8_first_movecnt = int(lines[28].rstrip('\n'))

    line = lines[29].rstrip('\n')
    if(len(line) > 0):
        moveattr = line.split(";")
        if(len(moveattr) == 12):
            move = Move()
            move.match.id = moveattr[0]
            move.count = int(moveattr[1])
            move.move_type = int(moveattr[2])
            move.srcx = int(moveattr[3])
            move.srcy = int(moveattr[4])
            move.dstx = int(moveattr[5])
            move.dsty = int(moveattr[6])
            move.e_p_fieldx = int(moveattr[7])
            move.e_p_fieldy = int(moveattr[8])
            move.captured_piece = int(moveattr[9])
            move.prom_piece = int(moveattr[10])
            move.fifty_moves_count = int(moveattr[11])

            match.move_list.append(move)

    debug_candidates = []
    for line in lines[30:51]:
        line = line.rstrip('\n')
        searchmoves = line.split("]")
        if(len(searchmoves) > 0):
            threadmoves = []
            for searchmove in searchmoves:
                gmoveattr = searchmove.split(";")
                if(len(gmoveattr) == 5):
                    gmove = GenMove()
                    gmove.srcx = int(gmoveattr[0])
                    gmove.srcy = int(gmoveattr[1])
                    gmove.dstx = int(gmoveattr[2])
                    gmove.dsty = int(gmoveattr[3])
                    gmove.prom_piece = int(gmoveattr[4])
                    threadmoves.append(gmove)
                else:
                    break

            debug_candidates.append(threadmoves)

    fobject.close()

    return match, debug_candidates


def token_to_text(token):
    tokentext = ""
    for key in TOKEN_TEXT:
        if(token & key > 0):
            tokentext += "\n" + TOKEN_TEXT[key]

    return tokentext


