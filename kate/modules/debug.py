from kate.models import Match, Move
from kate.modules import values


def prnt_moves(match):
    count = 1
    print("------------------------------------------------------")
    for move in match.move_list[1:]:
        print(str(count) + ": " + 
              values.index_to_koord(move.srcx, move.srcy) + " " +
              values.index_to_koord(move.dstx, move.dsty) + " " +
              values.reverse_lookup(Match.PIECES, move.prom_piece))
        count += 1
    print("------------------------------------------------------")



def prnt_attributes(match):
    print("------------------------------------------------------")
    print("status" + str(match.status))
    print("count" + str(match.count))
    print("score" + str(match.score)) 
    print("begin" + str(match.begin)) 
    print("white_player" + str(match.white_player))
    print("white_player_human" + str(match.white_player_human))
    print("black_player" + str(match.black_player))
    print("black_player_human" + str(match.black_player_human))
    print("fifty_moves_count" + str(match.fifty_moves_count))
    print("wKg_x" + str(match.wKg_x))
    print("wKg_y" + str(match.wKg_y))
    print("bKg_x" + str(match.bKg_x))
    print("bKg_y" + str(match.bKg_y))
    print("wKg_first_movecnt" + str(match.wKg_first_movecnt))
    print("bKg_first_movecnt" + str(match.bKg_first_movecnt))
    print("wRk_a1_first_movecnt" + str(match.wRk_a1_first_movecnt))
    print("wRk_h1_first_movecnt" + str(match.wRk_h1_first_movecnt)) 
    print("bRk_a8_first_movecnt" + str(match.bRk_a8_first_movecnt)) 
    print("bRk_h8_first_movecnt" + str(match.bRk_h8_first_movecnt))
    print("------------------------------------------------------")


def prnt_board(match):
    print("------------------------------------------------------")
    for i in range(7, -1, -1):
        for j in range(8):
            piece = match.readfield(j, i)
            print(values.reverse_lookup(Match.PIECES, piece) + " ", end="")
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


def prnt_status(match, generator):
    prnt_moves(match)
    prnt_board(match)
    prnt_attributes(match)
    prnt_generator(generator)


