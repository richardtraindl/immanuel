import random, threading, copy
from .. models import Match as ModelMatch, Move as ModelMove
from .. engine.match import *
from .. engine.move import *
from .. engine import matchmove, rules, calc


MAP_DIR = { 'model-to-engine' : 0, 'engine-to-model' : 1 }


def map_matches(src, dst, map_dir):
    if(map_dir == MAP_DIR['model-to-engine']):
        moves = ModelMove.objects.filter(match_id=src.id).order_by("count")
        if(len(moves) > 0):
            for move in moves:
                dst.move_list.append(move)

    dst.id = src.id
    dst.status = src.status
    dst.count = src.count
    dst.score = src.score
    dst.white_player = src.white_player
    dst.white_player_human = src.white_player_human
    dst.elapsed_time_white = src.elapsed_time_white
    dst.black_player = src.black_player
    dst.black_player_human = src.black_player_human
    dst.elapsed_time_black = src.elapsed_time_black
    dst.level = src.level
    dst.fifty_moves_count = src.fifty_moves_count
    dst.wKg_x = src.wKg_x
    dst.wKg_y = src.wKg_y
    dst.bKg_x = src.bKg_x
    dst.bKg_y = src.bKg_y
    dst.wKg_first_movecnt = src.wKg_first_movecnt
    dst.bKg_first_movecnt = src.bKg_first_movecnt
    dst.wRk_a1_first_movecnt = src.wRk_a1_first_movecnt
    dst.wRk_h1_first_movecnt = src.wRk_h1_first_movecnt
    dst.bRk_a8_first_movecnt = src.bRk_a8_first_movecnt
    dst.bRk_h8_first_movecnt = src.bRk_h8_first_movecnt

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = src.readfield(x, y)
            dst.writefield(x, y, piece)


def map_moves(src, dst, map_dir):
    if(map_dir == MAP_DIR['model-to-engine']):
        dst.id = src.id
        dst.match = src.match

    dst.count = src.count
    dst.move_type = src.move_type
    dst.srcx = src.srcx
    dst.srcy = src.srcy
    dst.dstx = src.dstx
    dst.dsty = src.dsty
    dst.e_p_fieldx = src.e_p_fieldx
    dst.e_p_fieldy = src.e_p_fieldy
    dst.captured_piece = src.captured_piece
    dst.prom_piece = src.prom_piece
    dst.fifty_moves_count = src.fifty_moves_count


def game_status(modelmatch):
    match = Match()
    map_matches(modelmatch, match, MAP_DIR['model-to-engine'])
    return rules.game_status(match)


def is_move_valid(modelmatch, srcx, srcy, dstx, dsty, prom_piece):
    match = Match()
    map_matches(modelmatch, match, MAP_DIR['model-to-engine'])
    return rules.is_move_valid(match, srcx, srcy, dstx, dsty, prom_piece)

 
def do_move(modelmatch, srcx, srcy, dstx, dsty, prom_piece):
    match = Match()
    map_matches(modelmatch, match, MAP_DIR['model-to-engine'])
    move = matchmove.do_move(match, srcx, srcy, dstx, dsty, prom_piece)
    map_matches(match, modelmatch, MAP_DIR['engine-to-model'])
    modelmatch.save()

    modelmove = ModelMove()                
    map_moves(move, modelmove, MAP_DIR['engine-to-model'])
    modelmove.match = modelmatch
    modelmove.save()


def undo_move(modelmatch):
    match = Match()
    map_matches(modelmatch, match, MAP_DIR['model-to-engine'])
    move = matchmove.undo_move(match)
    if(move):
        map_matches(match, modelmatch, MAP_DIR['engine-to-model'])
        modelmatch.save()

        modelmove = ModelMove.objects.filter(match_id=modelmatch.id, count=move.count).last()
        if(modelmove):
            modelmove.delete()


class immanuelsThread(threading.Thread):
    def __init__(self, name, match):
        threading.Thread.__init__(self)
        self.name = name
        self.running = True
        self.match = copy.deepcopy(match)

        ModelMatch.add_thread(self)


    def run(self):
        print("Thread starting " + str(self.name))
        gmove = calc.calc_move(self.match)
        if(gmove and ModelMatch.get_active_thread(self.match) and self.running):
            move = matchmove.do_move(self.match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

            modelmatch = ModelMatch()
            map_matches(self.match, modelmatch, MAP_DIR['engine-to-model'])
            modelmatch.save()

            modelmove = ModelMove()            
            map_moves(move, modelmove, MAP_DIR['engine-to-model'])
            modelmove.match = modelmatch
            modelmove.save()
            print("move saved")
        else:
            print("no move found or thread outdated!")


def thread_do_move(match):
    thread = immanuelsThread("immanuel-" + str(random.randint(0, 100000)), match)
    thread.start()


def calc_move_for_immanuel(modelmatch):
    match = Match()
    map_matches(modelmatch, match, MAP_DIR['model-to-engine'])
    if(rules.game_status(match) != STATUS['open']):
        return False, rules.game_status(match)
    elif(match.next_color_human()):
        return False, rules.RETURN_CODES['wrong-color']
    else:
        thread_do_move(match)
        return True, 0


def next_color_human(modelmatch):
    match = Match()
    map_matches(modelmatch, match, MAP_DIR['model-to-engine'])
    return match.next_color_human()

