import random, threading, copy, time
from django.conf import settings
from .. models import Match as ModelMatch, Move as ModelMove
from .. engine.values import *
from .. engine.match import *
from .. engine.move import *
from .. engine import calc


MAP_DIR = { 'model-to-engine' : 0, 'engine-to-model' : 1 }


def map_matches(src, dst, map_dir):
    if(map_dir == MAP_DIR['model-to-engine']):
        modelmoves = ModelMove.objects.filter(match_id=src.id).order_by("count")
        if(len(modelmoves) > 0):
            for modelmove in modelmoves:
                move = cMove()
                move.match = dst
                map_moves(modelmove, move, MAP_DIR['model-to-engine'])
                dst.move_list.append(move)

    dst.id = src.id
    dst.status = src.status
    dst.level = src.level
    dst.begin = src.begin
    dst.time_start = src.time_start
    if(map_dir == MAP_DIR['model-to-engine']):
        dst.white_player.name = src.white_player_name
        dst.white_player.is_human = src.white_player_is_human
        dst.white_player.elapsed_seconds = src.white_elapsed_seconds
        dst.black_player.name = src.black_player_name
        dst.black_player.is_human = src.black_player_is_human
        dst.black_player.elapsed_seconds = src.black_elapsed_seconds
    else:
        dst.white_player_name = src.white_player.name
        dst.white_player_is_human = src.white_player.is_human
        dst.white_elapsed_seconds = src.white_player.elapsed_seconds
        dst.black_player_name = src.black_player.name
        dst.black_player_is_human = src.black_player.is_human
        dst.black_elapsed_seconds = src.black_player.elapsed_seconds

    for y in range(8):
        for x in range(8):
            piece = src.readfield(x, y)
            dst.writefield(x, y, piece)

    if(map_dir == MAP_DIR['model-to-engine']):
        dst.update_attributes()


def map_moves(src, dst, map_dir):
    if(map_dir == MAP_DIR['model-to-engine']):
        dst.id = src.id
        #dst.match = src.match

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
    match = cMatch()
    map_matches(modelmatch, match, MAP_DIR['model-to-engine'])
    return match.evaluate_status()


def is_move_valid(modelmatch, srcx, srcy, dstx, dsty, prom_piece):
    match = cMatch()
    print("before mapper")
    map_matches(modelmatch, match, MAP_DIR['model-to-engine'])
    print("after before mapper")
    return match.is_move_valid(srcx, srcy, dstx, dsty, prom_piece)


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
    match = cMatch()
    map_matches(modelmatch, match, MAP_DIR['model-to-engine'])

    ### time
    if(match.time_start > 0):
        elapsed_time = time.time() - match.time_start
        if(match.next_color() == COLORS['white']):
            match.white_player.elapsed_seconds += elapsed_time
        else:
            match.black_player.elapsed_seconds += elapsed_time

    match.time_start = time.time()
    ###

    move = match.do_move(srcx, srcy, dstx, dsty, prom_piece)
    match.status = match.evaluate_status() #STATUS['open']
    map_matches(match, modelmatch, MAP_DIR['engine-to-model'])
    modelmatch.save()

    modelmove = ModelMove()                
    map_moves(move, modelmove, MAP_DIR['engine-to-model'])
    modelmove.match = modelmatch
    modelmove.save()


def undo_move(modelmatch):
    match = cMatch()
    map_matches(modelmatch, match, MAP_DIR['model-to-engine'])
    move = match.undo_move()
    if(move):
        map_matches(match, modelmatch, MAP_DIR['engine-to-model'])
        modelmatch.save()

        modelmove = ModelMove.objects.filter(match_id=modelmatch.id, count=move.count).last()
        if(modelmove):
            modelmove.delete()


class ImmanuelsThread(threading.Thread):
    def __init__(self, name, match):
        threading.Thread.__init__(self)
        self.name = name
        self.match = copy.deepcopy(match)
        self.msgs = calc.Msgs()

    def run(self):
        print("Thread starting " + str(self.name))
        candidates = calc.calc_move(self.match, self.msgs) 
        if(len(candidates) > 0):
            gmove = candidates[0]

            move = self.match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

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


def calc_move_for_immanuel(modelmatch):
    match = cMatch()
    map_matches(modelmatch, match, MAP_DIR['model-to-engine'])
    status = match.evaluate_status()
    if(status != match.STATUS['open']):
        return False, status
    elif(match.is_next_color_human()):
        return False, match.RETURN_CODES['wrong-color']
    else:
        thread = ImmanuelsThread("immanuel-" + str(random.randint(0, 100000)), match)
        thread.start()
        return True, match.RETURN_CODES['ok']

