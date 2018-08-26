import re, os, threading, copy
from engine.match import *
from engine.move import *
from engine.calc import calc_move, Msgs
from engine.debug import prnt_match_attributes, prnt_board, list_match_attributes, list_move_attributes
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
    if(new_word("terminate", word_terminate, "terminates match") == False):
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


class CalcThread(threading.Thread):
    def __init__(self, session):
        threading.Thread.__init__(self)
        self.session = session
        self.calc_match = copy.deepcopy(session.match)

    def run(self):
        self.session.thread_is_busy = True
        print("Thread starting...")
        candidates = calc_move(self.calc_match, self.session.msgs)
        if(len(candidates) > 0):
            gmove = candidates[0]
            self.session.match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
            prnt_board(self.session.match)
        else:
            print("no move found!")

        self.session.thread_is_busy = False


def calc_and_domove(session):
    match = session.match
    if(session.thread_is_busy == False and match.evaluate_status() == match.STATUS['open'] and match.is_next_color_human() == False):
        session.thread = CalcThread(session)
        session.thread.start()


def new_match(lstparam):
    if(len(lstparam) != 4):
        print("??? params")
        return None

    match = cMatch()

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
    m = session.match
    if(m.evaluate_status() == m.STATUS['open']):
        m.status = m.STATUS['paused']
    return True


def word_resume(session, params):
    match = session.match
    if(match.evaluate_status() == match.STATUS['open']):
        match.status = match.STATUS['open']
    calc_and_domove(session)
    return True


def word_terminate(session, params):
    if(session.thread_is_busy):
        session.msgs.terminate = True
        print("try to terminante calculation...")
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
    match = session.match
    match.status = match.evaluate_status()
    if(match.status != match.STATUS['open']):
        print("??? " + reverse_lookup(match.STATUS, match.status))
        return True
    elif(match.is_next_color_human() == False):
        print("??? wrong color")
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
            for piece in match.PIECES:
                if(piece == prom_piece):
                    valid = True
                    break
            if(valid == False):
                return True
        else:
            matchobj = re.search(r"^\s*(?P<short>[0oO][-][0oO])\s*$", params)
            if(matchobj):
                if(match.next_color() == match.COLORS['white']):
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
                    if(match.next_color() == match.COLORS['white']):
                        srcx = match.wKg_x
                        srcy = match.wKg_y
                    else:
                        srcx = match.bKg_x
                        srcy = match.bKg_y
                    dstx = srcx - 2
                    dsty = srcy
                else:
                    return True

    if(match.is_move_valid(srcx, srcy, dstx, dsty, match.PIECES[prom_piece])[0]):
        match.do_move(srcx, srcy, dstx, dsty, match.PIECES[prom_piece])
        prnt_board(match)
    else:
        print("invalid move!")

    return True


def word_undo(session, params):
    match = session.match
    
    match.undo_move()
    prnt_board(match)

    if(match.evaluate_status() == match.STATUS['open']):
        match.status = match.STATUS['paused']
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
    match = session.match

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
            strboard += reverse_lookup(match.PIECES, match.readfield(x, y))
    fobject.write(strboard + ";")

    fobject.write("movelistcnt:" + str(len(match.move_list)) + ";")
    for move in match.move_list:
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
                    value = datetime.now()
                elif(classattr.label == "time_start"):
                    value = 0
                else:
                    strvalue= tokens[index].replace(classattr.label + ":", "")
                    if(strvalue == "None"):
                        value = None
                    elif(strvalue == "True"):
                        value = True
                    elif(strvalue == "False"):
                        value = False
                    else:
                        try: 
                            value = int(strvalue)
                        except ValueError:
                            value = strvalue

                setattr(match, classattr.label, value)
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
            match.writefield(x, y, match.PIECES[strfield])
    # -----------------------

    # -----------------------
    movecnt = int(tokens[index].replace("movelistcnt:", ""))
    index += 1
    
    for i in range(movecnt):
        move = Move()
        attributes = list_move_attributes(move)
        for classattr in attributes:
            label_len = len(classattr.label)
            if(classattr.label == tokens[index][:label_len]):
                if(classattr.label == "match"):
                    value = match
                else:
                    strvalue= tokens[index].replace(classattr.label + ":", "")
                    if(strvalue == "None"):
                        value = None
                    elif(strvalue == "True"):
                        value = True
                    elif(strvalue == "False"):
                        value = False
                    else:
                        try: 
                            value = int(strvalue)
                        except ValueError:
                            value = strvalue

                setattr(move, classattr.label, value)
                index += 1

        match.move_list.append(move)
        index += 1
    # -----------------------

    fobject.close()

    match.update_attributes()
    session.match = match
    session.msgs = Msgs()
    
    prnt_match_attributes(session.match, ", ")
    prnt_board(session.match)

    return True


def word_delete(session, params):
    delfile = immanuels_dir + "/" + params.strip() + ".txt"

    if os.path.isfile(delfile):
        os.remove(delfile)
    else:
        print("Error: %s file not found" % delfile)

    return True


def word_help(session, params):
    for dword in dictionary:
        if(dword.name == "?"):
            continue
        print(dword.name + " *** " + dword.info)

    return True


def word_bye(session, params):
    if(session.thread and session.thread_is_busy):
        print("terminate calculation. please wait...")
        session.terminate = True
        session.thread.join()
        session.thread = None
        session.terminate = False
    print("bye")

    return False

