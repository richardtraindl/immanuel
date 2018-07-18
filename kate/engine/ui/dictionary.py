from .. match import *
from .. rules import *
from .. calc import Msgs, calc_move
from .. debug import prnt_attributes, prnt_board
from .. matchmove import do_move
from .. helper import coord_to_index
import re


dictionary = []


class Word():
    def __init__(self, name=None, code=None):
        self.name = name
        self.code = code

def new_word(name, code):
    for dword in dictionary:
        if(dword.name == name):
            print("naming error...")
            return False

    word = Word(name, code)
    dictionary.append(word)
    return True


def init_words():
    if(new_word("pause",  word_pause) == False):
        return False
    if(new_word("resume", word_resume) == False):
        return False
    if(new_word("show",   word_show) == False):
        return False
    if(new_word("set",    word_set) == False):
        return False
    if(new_word("domove", word_domove) == False):
        return False
    if(new_word("bye",    word_bye) == False):
        return False

    return True


def calc_and_domove(match):
    if(match.status == STATUS['open'] and match.is_next_color_human() == False):
        candidates = calc_move(match, Msgs())
        gmove = candidates[0]
        do_move(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
        prnt_board(match)


def new_match(lstparam):
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
    match.status = STATUS['paused']
    return True


def word_resume(match, params):
    match.status = rules.status(match)
    calc_and_domove(match)
    return True


def word_show(match, params):
    prnt_attributes(match, ", ")
    prnt_board(match)
    return True


def word_set(match, params):
    print("under construction...")
    return True


def word_domove(match, params):
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


def word_bye(match, params):
    print("bye")
    return False

