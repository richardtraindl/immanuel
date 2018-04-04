import random, threading, copy
from django.conf import settings
from .. models import Match as ModelMatch, Move as ModelMove
from .. engine.match import *
from .. engine.move import *
from .. engine import matchmove, rules, calc
from .. engine.analyze_position import score_position


MAP_DIR = { 'model-to-engine' : 0, 'engine-to-model' : 1 }


def map_matches(src, dst, map_dir):
    if(map_dir == MAP_DIR['model-to-engine']):
        moves = ModelMove.objects.filter(match_id=src.id).order_by("count")
        if(len(moves) > 0):
            for move in moves:
                dst.move_list.append(move)

    dst.id = src.id
    dst.status = src.status
    dst.level = src.level
    dst.begin = src.begin
    dst.white_player_name = src.white_player_name
    dst.white_player_is_human = src.white_player_is_human
    dst.elapsed_time_white = src.elapsed_time_white
    dst.black_player_name = src.black_player_name
    dst.black_player_is_human = src.black_player_is_human
    dst.elapsed_time_black = src.elapsed_time_black

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = src.readfield(x, y)
            dst.writefield(x, y, piece)

    if(map_dir == MAP_DIR['model-to-engine']):
        dst.update_attributes()


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


def status(modelmatch):
    match = Match()
    map_matches(modelmatch, match, MAP_DIR['model-to-engine'])
    return rules.status(match)


def is_move_valid(modelmatch, srcx, srcy, dstx, dsty, prom_piece):
    match = Match()
    map_matches(modelmatch, match, MAP_DIR['model-to-engine'])
    return rules.is_move_valid(match, srcx, srcy, dstx, dsty, prom_piece)


def movecnt(modelmatch):
    moves = ModelMove.objects.filter(match_id=modelmatch.id)
    return len(moves)


def is_next_color_human(modelmatch):
    moves = ModelMove.objects.filter(match_id=modelmatch.id)
    if(len(moves) % 2 == 0):
        return modelmatch.white_player_is_human
    else:
        return modelmatch.black_player_is_human


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
        candidates = calc.calc_move(self.match) 
        if(len(candidates) > 0 and ModelMatch.get_active_thread(self.match)): #  and self.running
            gmove = candidates[0]

            move = matchmove.do_move(self.match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

            modelmatch = ModelMatch()
            map_matches(self.match, modelmatch, MAP_DIR['engine-to-model'])
            modelmatch.save()

            modelmove = ModelMove()            
            map_moves(move, modelmove, MAP_DIR['engine-to-model'])
            modelmove.match = modelmatch
            modelmove.save()
            self.running = False
            print("move saved")
        else:
            print("no move found or thread outdated!")


def calc_move_for_immanuel(modelmatch):
    match = Match()
    map_matches(modelmatch, match, MAP_DIR['model-to-engine'])
    if(rules.status(match) != STATUS['open']):
        return False, rules.status(match)
    elif(match.is_next_color_human()):
        return False, rules.RETURN_CODES['wrong-color']
    else:
        thread = immanuelsThread("immanuel-" + str(random.randint(0, 100000)), match)
        thread.start()
        return True, 0


def read_searchmoves(): 
    return debug.read_searchmoves(settings.BASE_DIR + "/kate/engine")


def debug_score_position(modelmatch):
    match = Match()
    map_matches(modelmatch, match, MAP_DIR['model-to-engine'])
    score = score_position(match, movecnt)
    print("from function score_position")
    print("match.score: " + str(match.score) + " score: " + str(score))

