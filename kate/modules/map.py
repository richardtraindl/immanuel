from kate.models import Match as ModelMatch, Move as ModelMove
from kate.engine import match, move


def database_to_engine(modelmatch):
    match = Match()
    match.status = modelmatch.status
    match.count = modelmatch.count
    match.score = modelmatch.score
    match.white_player = modelmatch.white_player
    match.white_player_human = modelmatch.white_player_human
    match.elapsed_time_white = modelmatch.elapsed_time_white
    match.black_player = modelmatch.black_player
    match.black_player_human = modelmatch.black_player_human
    match.elapsed_time_black = modelmatch.elapsed_time_black
    match.level = modelmatch.level
    match.fifty_moves_count = modelmatch.fifty_moves_count
    match.wKg_x = modelmatch.wKg_x
    match.wKg_y = modelmatch.wKg_y
    match.bKg_x = modelmatch.bKg_x
    match.bKg_y = modelmatch.bKg_y
    match.wKg_first_movecnt = modelmatch.wKg_first_movecnt
    match.bKg_first_movecnt = modelmatch.bKg_first_movecnt
    match.wRk_a1_first_movecnt = modelmatch.wRk_a1_first_movecnt
    match.wRk_h1_first_movecnt = modelmatch.wRk_h1_first_movecnt
    match.bRk_a8_first_movecnt = modelmatch.bRk_a8_first_movecnt
    match.bRk_h8_first_movecnt = modelmatch.bRk_h8_first_movecnt
        
    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = modelmatch.readfield(x, y)                
            match.writefield(x, y, PIECES[piece])       
        
    move = ModelMove.objects.get(match_id=modelmatch.id, count=modelmatch.count)        
    match.move_list.append(move)
    
    return match


