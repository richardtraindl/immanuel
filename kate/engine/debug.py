from .match import *
from .cvalues import *
from .move import *
from .helper import *


def prnt_minutes(match):
    count = 1
    print("------------------------------------------------------")
    for move in match.move_list[1:]:
        print(str(count) + ":" + 
              index_to_coord(move.srcx, move.srcy) + " " +
              index_to_coord(move.dstx, move.dsty) + " " +
              reverse_lookup(PIECES, move.prom_piece))
        count += 1
    print("------------------------------------------------------")


class ClassAttr:
    def __init__(self, attribute=None, label=None):
        self.attribute = attribute
        self.label = label

def list_match_attributes(match):
    attributes = []

    attributes.append(ClassAttr(match.status, "status"))
    attributes.append(ClassAttr(match.movecnt, "movecnt"))
    attributes.append(ClassAttr(match.score, "score"))
    attributes.append(ClassAttr(match.level, "level"))
    attributes.append(ClassAttr(match.seconds_per_move, "seconds_per_move"))
    attributes.append(ClassAttr(match.begin, "begin"))
    attributes.append(ClassAttr(match.time_start, "time_start"))
    attributes.append(ClassAttr(match.white_player_name, "white_player_name"))
    attributes.append(ClassAttr(match.white_player_is_human, "white_player_is_human"))
    attributes.append(ClassAttr(match.white_elapsed_seconds, "white_elapsed_seconds"))
    attributes.append(ClassAttr(match.black_player_name, "black_player_name"))
    attributes.append(ClassAttr(match.black_player_is_human, "black_player_is_human"))
    attributes.append(ClassAttr(match.black_elapsed_seconds, "black_elapsed_seconds"))
    attributes.append(ClassAttr(match.fifty_moves_count, "fifty_moves_count"))
    attributes.append(ClassAttr(match.white_movecnt_short_castling_lost, "white_movecnt_short_castling_lost"))
    attributes.append(ClassAttr(match.white_movecnt_long_castling_lost, "white_movecnt_long_castling_lost"))
    attributes.append(ClassAttr(match.black_movecnt_short_castling_lost, "black_movecnt_short_castling_lost"))
    attributes.append(ClassAttr(match.black_movecnt_long_castling_lost, "black_movecnt_long_castling_lost"))
    attributes.append(ClassAttr(match.wKg_x, "wKg_x"))
    attributes.append(ClassAttr(match.wKg_y, "wKg_y"))
    attributes.append(ClassAttr(match.bKg_x, "bKg_x"))
    attributes.append(ClassAttr(match.bKg_y, "bKg_y"))
    attributes.append(ClassAttr(match.wQu_cnt, "wQu_cnt"))
    attributes.append(ClassAttr(match.bQu_cnt, "bQu_cnt"))
    attributes.append(ClassAttr(match.wOfficer_cnt, "wOfficer_cnt"))
    attributes.append(ClassAttr(match.bOfficer_cnt, "bOfficer_cnt"))

    return attributes


def prnt_match_attributes(match, delimiter):
    classattrs = list_match_attributes(match)

    print("------------------------------------------------------")

    for classattr in classattrs:
        print(classattr.label + ":" + str(classattr.attribute) + delimiter, end="\n")

    print("------------------------------------------------------")


    
BLANK  = "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
KING   = "000000+0000000000+++++0000000000+0000000++000+000++0++++00+00++++0+++++++++++00+++0+++0+++0"
QUEEN  = "000000000000000+000+000+000+++0+++0+++0+++++++++++++++0+++0+++0++0+++++++++++00+++0+++0+++0"
ROOK   = "00000000000000++00+++00++00++00+++00++00+++++++++++000++0+++0++0000+++++++++000+++0+++0+++0"
BISHOP = "000000+00000000000+++000000000++0++0000000++000++00000++++0++++000+++++++++++000+++++++++00"
KNIGHT = "000000++0000000000++++0000000+++++++00000+++000+++000++00000++++000000+++++000000++++++++00"
PAWN   = "0000000000000000000000000000000+++000000000+++++000000+++++++++00000+++++++0000+++++++++++0"

def prnt_line(pieces):
    for i in range(7):
        for k in range(8):
            if(Match.color_of_piece(pieces[i]) == COLORS['white']):
                forecolor = 0
            else:
                forecolor = 1

            """if((y % 2 + x) % 2 == 1):
                backcolor = 0
            else:
                backcolor = 1"""

        if(forecolor == 0):
            invert = False
        else:
            invert = True

        if(pieces[k] == PIECES['blk']):
            map = BLANK
            invert = False
        elif(pieces[k] == PIECES['wPw'] or pieces[k] == PIECES['bPw']):
            map = PAWN
        elif(pieces[k] == PIECES['wKn'] or pieces[k] == PIECES['bKn']):
            map = KNIGHT
        elif(pieces[k] == PIECES['wBp'] or pieces[k] == PIECES['bBp']):
            map = BISHOP
        elif(pieces[k] == PIECES['wRk'] or pieces[k] == PIECES['bRk']):
            map = ROOK
        elif(pieces[k] == PIECES['wQu'] or pieces[k] == PIECES['bQu']):
            map = QUEEN
        else:
            map = KING

        for j in range(13):
            character = map[(i * 13) + j]
            if((character == "0" and invert == False) or (character == "+" and invert)):
                print(" ", end="")
            else:
                print("*", end="")
    print("")

def prnt_board(match):
    pieces = [8]
    for y in range(7, -1, -1):
        for x in range(8):
            pieces[x] = match.readfield(x, y)
        prnt_line(pieces)


def list_move_attributes(move):
    attributes = []

    attributes.append(ClassAttr(move.match, "match"))
    attributes.append(ClassAttr(move.count, "count"))
    attributes.append(ClassAttr(move.move_type, "move_type"))
    attributes.append(ClassAttr(move.srcx, "srcx"))
    attributes.append(ClassAttr(move.srcy, "srcy"))
    attributes.append(ClassAttr(move.dstx, "dstx"))
    attributes.append(ClassAttr(move.dsty, "dsty"))
    attributes.append(ClassAttr(move.e_p_fieldx, "e_p_fieldx"))
    attributes.append(ClassAttr(move.e_p_fieldy, "e_p_fieldy"))
    attributes.append(ClassAttr(move.captured_piece, "captured_piece"))
    attributes.append(ClassAttr(move.prom_piece, "prom_piece"))
    attributes.append(ClassAttr(move.fifty_moves_count, "fifty_moves_count"))

    return attributes

