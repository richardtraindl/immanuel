import re, os, types
from engine.match import *
from engine.move import *
from engine.rules import *
from engine.calc import calc_move, Msgs
from engine.debug import prnt_match_attributes, prnt_board, list_match_attributes, list_move_attributes
from engine.matchmove import do_move, undo_move
from engine.helper import coord_to_index, reverse_lookup


dictionary = []
immanuels_dir = "/home/richard/.immanuel"


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


def calc_and_domove(session):
    if(status(session.match) == STATUS['open'] and session.match.is_next_color_human() == False):
        candidates = calc_move(session.match, session.msgs)
        gmove = candidates[0]
        do_move(session.match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
        prnt_board(session.match)


def new_match(lstparam):
    if(len(lstparam) != 4):
        print("??? params")
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


def word_pause(session, params):
    if(status(session.match) == STATUS['open']):
        session.match.status = STATUS['paused']

    return True


def word_resume(session, params):
    if(session.status(match) == STATUS['open']):
        session.match.status = STATUS['open']

    calc_and_domove(session)

    return True


def word_show(session, params):
    prnt_match_attributes(session.match, ", ")

    prnt_board(session.match)

    return True


def word_set(session, params):
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
            session.match.level = LEVELS[tokens[1]]
            session.match.seconds_per_move = SECONDS_PER_MOVE[session.match.level]
        except KeyError:
            print("??? value")
    elif(tokens[0] == "white-player"):
        session.match.white_player_name = tokens[1]
    elif(tokens[0] == "black-player"):
        session.match.black_player_name = tokens[1]
    elif(tokens[0] == "white-human"):
        if(tokens[1] == "J" or tokens[1] == "j"):
            session.match.white_player_is_human = True
        else:
            session.match.white_player_is_human = False
            session.match.black_player_is_human = True
    elif(tokens[0] == "black-human"):
        if(tokens[1] == "J" or tokens[1] == "j"):
            session.match.black_player_is_human = True
        else:
            session.match.black_player_is_human = False
            session.match.white_player_is_human = True
    else:
        print("??? params...")

    return True


def word_move(session, params):
    session.match.status = status(session.match)
    if(session.match.status != STATUS['open']):
        print(reverse_lookup(STATUS, session.match.status))
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

    if(is_move_valid(session.match, srcx, srcy, dstx, dsty, PIECES[prom_piece])[0]):
        do_move(session.match, srcx, srcy, dstx, dsty, PIECES[prom_piece])
        prnt_board(session.match)
    else:
        print("invalid move!")

    return True


def word_undo(session, params):
    undo_move(session.match)
    prnt_board(session.match)

    if(status(session.match) == STATUS['open']):
        session.match.status = STATUS['paused']

    return True


def word_list(session, params):
    filennames = os.listdir(immanuels_dir)
    print("[ ", end="")
    for filenname in filennames:
        if(filenname == "counter.txt"):
            continue
        else:
            print(filenname.replace(".txt", " "), end="")
    print("]")

    return True


def word_save(session, params):
    counter = None

    if not os.path.isdir(immanuels_dir):
        os.makedirs(immanuels_dir)

    try:
        fobject = open(immanuels_dir + "/counter.txt", "r")
        data = fobject.read()
        fobject.close()
        counter = int(data)
        counter += 1
    except FileNotFoundError:
        counter = 1
    
    fobject = open(immanuels_dir + "/counter.txt", "w")
    fobject.write(str(counter))
    fobject.close()    

    #----------------------------
    fobject = open(immanuels_dir + "/" + str(counter) + ".txt", "w")

    attributes = list_match_attributes(session.match)
    for classattr in attributes:
        fobject.write(classattr.label + ":" + str(classattr.attribute) + ";")

    strboard = "board:"
    for y in range(8):
        for x in range(8):
            strboard += reverse_lookup(PIECES, session.match.readfield(x, y))
    fobject.write(strboard + ";")

    fobject.write("movecnt:" + str(len(session.match.move_list)) + ";")
    for move in session.match.move_list:
        attributes = list_move_attributes(move)
        for classattr in attributes:
            if(classattr.label == "match"):
                fobject.write(classattr.label + ":" + "None" + ";")
            else:
                fobject.write(classattr.label + ":" + str(classattr.attribute) + ";")
    #----------------------------
    fobject.close()

    return True


def word_load(session, params):
    try:
        fobject = open(immanuels_dir + "/" + params.strip() + ".txt", "r")
    except FileNotFoundError:
        print("??? file not found: " + params.strip())
        return True

    match = Match()

    tokens = fobject.read().split(";")
    index = 0

    # -----------------------
    attributes = list_match_attributes(match)
    for i in range(len(attributes)):
        for classattr in attributes:
            label_len = len(classattr.label)
            if(classattr.label == tokens[index][:label_len]):
                if(classattr.label == "begin"):
                    match.begin = datetime.now()
                elif(classattr.label == "time_start"):
                    match.time_start = 0
                else:
                    if(type(classattr.attribute) == bool):
                        classattr.attribute = bool(tokens[index].replace(classattr.label + ":", ""))
                    elif(type(classattr.attribute) == int):
                        classattr.attribute = int(float(tokens[index].replace(classattr.label + ":", "")))
                    else:
                        classattr.attribute = tokens[index].replace(classattr.label + ":", "")
                break
        index += 1
    # -----------------------

    # -----------------------
    strboard = tokens[index].replace("board:", "")
    index += 1

    for y in range(8):
        for x in range(8):
            idx = (y * 24) + (x * 3)
            strfield = strboard[idx:idx+3]
            match.writefield(x, y, PIECES[strfield])
    # -----------------------

    # -----------------------
    strmovecnt = tokens[index].replace("movecnt:", "")
    index += 1

    movecnt = int(strmovecnt)
    
    for i in range(movecnt):
        move = Move()
        attributes = list_move_attributes(move)
        for classattr in attributes:
            label_len = len(classattr.label)
            if(classattr.label == tokens[index][:label_len]):
                if(classattr.label == "match"):
                    move.match = match
                elif(tokens[index] == "None"):
                    classattr.attribute = None
                else:
                    classattr.attribute = int(tokens[index].replace(classattr.label + ":", ""))

        match.move_list.append(move)
        index += 1
    # -----------------------

    fobject.close()

    session.match = match
    session.msgs = Msgs()
    
    prnt_match_attributes(session.match, ", ")
    prnt_board(session.match)

    return True


def word_delete(session, params):
    print("under construction")

    return True


def word_help(session, params):
    for dword in dictionary:
        if(dword.name == "?"):
            continue
        print(dword.name + " *** " + dword.info)

    return True


def word_bye(session, params):
    print("bye")

    return False

