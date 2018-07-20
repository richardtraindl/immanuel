import re
from engine.match import *
from engine.rules import *
from engine.calc import Msgs, calc_move
from engine.debug import prnt_attributes, prnt_board
from engine.matchmove import do_move, undo_move
from engine.helper import coord_to_index


dictionary = []


class Word():
    def __init__(self, name=None, code=None, info=None):
        self.name = name
        self.code = code
        self.info = info

def new_word(name, code, info):
    for dword in dictionary:
        if(dword.name == name):
            print("naming error...")
            return False

    word = Word(name, code, info)
    dictionary.append(word)

    return True


def init_words():
    if(new_word("help", word_help, "this help") == False):
        return False
    if(new_word("?", word_help, "this help") == False):
        return False
    if(new_word("bye",    word_bye, "exit") == False):
        return False
    if(new_word("pause",  word_pause, "pauses match") == False):
        return False
    if(new_word("resume", word_resume, "resumes (paused) match") == False):
        return False
    if(new_word("show",   word_show, "prints debug info") == False):
        return False
    if(new_word("set",    word_set, "sets attributes, e.g. set level medium") == False):
        return False
    if(new_word("move", word_move, "moves piece(s), e.g. move e2-e4") == False):
        return False
    if(new_word("undo", word_undo, "undos last move") == False):
        return False
    if(new_word("list", word_list, "lists all saved matches") == False):
        return False
    if(new_word("save", word_save, "saves match") == False):
        return False
    if(new_word("load", word_load, "loads match with id, e.g. load 3") == False):
        return False
    if(new_word("delete", word_delete, "deletes match with id, e.g. delete 3") == False):
        return False
    return True


def calc_and_domove(match):
    if(status(match) == STATUS['open'] and match.is_next_color_human() == False):
        candidates = calc_move(match, Msgs())
        gmove = candidates[0]
        do_move(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
        prnt_board(match)


def new_match(lstparam):
    if(len(lstparam) != 4):
        print("")
        return None

    match = Match()

    match.white_player_name = lstparam[0]

    if(lstparam[1] == "h" or lstparam[1] == "0"):
        match.white_player_is_human = True
    else:
        match.white_player_is_human = False

    match.black_player_name = lstparam[2]

    if(lstparam[3] == "h" or lstparam[3] == "0"):
        match.black_player_is_human = True
    else:
        match.black_player_is_human = False

    return match


def word_pause(match, params):
    if(status(match) == STATUS['open']):
        match.status = STATUS['paused']

    return True


def word_resume(match, params):
    if(status(match) == STATUS['open']):
        match.status = STATUS['open']

    calc_and_domove(match)

    return True


def word_show(match, params):
    prnt_attributes(match, ", ")

    prnt_board(match)

    return True


def word_set(match, params):
    if(params == "?"):
        print("set level blitz | low | medium | high")
        print("set white-player Richard")
        print("set black-player Hermann")
        print("set white-human j | n")
        print("set black-human j | n")
        return True

    tokens = params.split(" ")

    if(len(tokens) != 2):
        print("??? params...")
        return True

    if(tokens[0] == "level"):
        try:
            match.level = LEVELS[tokens[1]]
            match.seconds_per_move = SECONDS_PER_MOVE[match.level]
        except KeyError:
            print("??? value")
    elif(tokens[0] == "white-player"):
        match.white_player_name = tokens[1]
    elif(tokens[0] == "black-player"):
        match.black_player_name = tokens[1]
    elif(tokens[0] == "white-human"):
        if(tokens[1] == "J" or tokens[1] == "j"):
            match.white_player_is_human = True
        else:
            match.white_player_is_human = False
            match.black_player_is_human = True
    elif(tokens[0] == "black-human"):
        if(tokens[1] == "J" or tokens[1] == "j"):
            match.black_player_is_human = True
        else:
            match.black_player_is_human = False
            match.white_player_is_human = True
    else:
        print("??? params...")

    return True


def word_move(match, params):
    match.status = status(match)
    if(match.status != STATUS['open']):
        print(reverse_lookup(STATUS, match.status))
        return True

    prom_piece = "blk"

    matchobj = re.search(r"^\s*(?P<src>[a-hA-H][1-8])\s*[-xX]*\s*(?P<dst>[a-hA-H][1-8])\s*$", params)
    if(matchobj):
        srcx, srcy = coord_to_index(matchobj.group("src"))
        dstx, dsty = coord_to_index(matchobj.group("dst"))
    else:
        matchobj = re.search(r"^\s*(?P<src>[a-hA-H][1-8])\s*[-xX]*\s*(?P<dst>[a-hA-H][1-8])\s*[-,;]*\s*(?P<prom>\w+)\s*$", params)
        if(matchobj):
            srcx, srcy = coord_to_index(matchobj.group("src"))
            dstx, dsty = coord_to_index(matchobj.group("dst"))
            prom_piece = matchobj.group("prom")

            valid = False
            for piece in PIECES:
                if(piece == prom_piece):
                    valid = True
                    break
            if(valid == False):
                print("invalid move!")
                return True
        else:
            matchobj = re.search(r"^\s*(?P<short>[0oO][-][0oO])\s*$", params)
            if(matchobj):
                if(match.next_color() == COLORS['white']):
                    srcx = match.wKg_x
                    srcy = match.wKg_y
                else:
                    srcx = match.bKg_x
                    srcy = match.bKg_y
                dstx = srcx + 2
                dsty = srcy
            else:
                matchobj = re.search(r"^\s*(?P<long>[0oO][-][0oO][-][0oO])\s*$", params)
                if(matchobj):
                    if(match.next_color() == COLORS['white']):
                        srcx = match.wKg_x
                        srcy = match.wKg_y
                    else:
                        srcx = match.bKg_x
                        srcy = match.bKg_y
                    dstx = srcx - 2
                    dsty = srcy
                else:
                    print("invalid move!")
                    return True

    if(is_move_valid(match, srcx, srcy, dstx, dsty, PIECES[prom_piece])[0]):
        do_move(match, srcx, srcy, dstx, dsty, PIECES[prom_piece])
        prnt_board(match)
    else:
        print("invalid move!")

    return True


def word_undo(match, params):
    undo_move(match)
    prnt_board(match)

    if(status(match) == STATUS['open']):
        match.status = STATUS['paused']

    return True


def word_list(match, params):
    print("under construction")

    return False


def word_save(match, params):
    print("under construction")

    return False


def word_load(match, params):
    print("under construction")

    return False


def word_delete(match, params):
    print("under construction")

    return False


def word_help(match, params):
    for dword in dictionary:
        if(dword.name == "?"):
            continue
        print(dword.name + " *** " + dword.info)

    return True


def word_bye(match, params):
    print("bye")

    return False

