from kate.models import Match as ModelMatch, Move as ModelMove
from kate.engine import match, move


MAP_DIR = { 'model-to-engine' : 0, 'engine-to-model' : 1 }


def map_matches(nmatch, map_dir):
    if(map_dir == MAP_DIR['model-to-engine']):
        match = Match()

        for y in range(0, 8, 1):
            for x in range(0, 8, 1):
                piece = nmatch.readfield(x, y)
                match.writefield(x, y, piece)

        move = ModelMove.objects.get(match_id=nmatch.id, count=nmatch.count)
        if(move):
            match.move_list.append(move)
    else:
        match = ModelMatch()

        for y in range(0, 8, 1):
            for x in range(0, 8, 1):
                piece = nmatch.readfield(x, y)
                match.writefield(x, y, piece)

    match.status = nmatch.status
    match.count = nmatch.count
    match.score = nmatch.score
    match.white_player = nmatch.white_player
    match.white_player_human = nmatch.white_player_human
    match.elapsed_time_white = nmatch.elapsed_time_white
    match.black_player = nmatch.black_player
    match.black_player_human = nmatch.black_player_human
    match.elapsed_time_black = nmatch.elapsed_time_black
    match.level = nmatch.level
    match.fifty_moves_count = nmatch.fifty_moves_count
    match.wKg_x = nmatch.wKg_x
    match.wKg_y = nmatch.wKg_y
    match.bKg_x = nmatch.bKg_x
    match.bKg_y = nmatch.bKg_y
    match.wKg_first_movecnt = nmatch.wKg_first_movecnt
    match.bKg_first_movecnt = nmatch.bKg_first_movecnt
    match.wRk_a1_first_movecnt = nmatch.wRk_a1_first_movecnt
    match.wRk_h1_first_movecnt = nmatch.wRk_h1_first_movecnt
    match.bRk_a8_first_movecnt = nmatch.bRk_a8_first_movecnt
    match.bRk_h8_first_movecnt = nmatch.bRk_h8_first_movecnt

    return match


def map_moves(src, map_dir):
    if(map_dir == MAP_DIR['model-to-engine']):
        move = Move()
    else:
        move = ModelMove()

     move.match = src.match
     move.count = src.count
     move.move_type = src.move_type
     move.srcx = src.srcx
     move.srcy = src.srcy
     move.dstx = src.dstx.
     move.dsty = src.dsty
     move.e_p_fieldx = src.e_p_fieldx
     move.e_p_fieldy = src.e_p_fieldy
     move.captured_piece = src.captured_piece
     move.prom_piece = src.prom_piece
     move.fifty_moves_count = src.fifty_moves_count

     return move

