from .values import *
from .match import *
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
    attributes.append(ClassAttr(match.white_player.name, "white_player_name"))
    attributes.append(ClassAttr(match.white_player.is_human, "white_player_is_human"))
    attributes.append(ClassAttr(match.white_player.elapsed_seconds, "white_elapsed_seconds"))
    attributes.append(ClassAttr(match.black_player.name, "black_player_name"))
    attributes.append(ClassAttr(match.black_player.is_human, "black_player_is_human"))
    attributes.append(ClassAttr(match.black_player.elapsed_seconds, "black_elapsed_seconds"))
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


    
BLANK  = [ u"\u0020\u0020\u0020\u0020\u0020\u0020\u0020" ] * 4

KING   = [ u"\u0020\u0020\u0020\u254B\u0020\u0020\u0020", # 253C 2542
           u"\u0020\u0020\u2599\u2584\u259F\u0020\u0020", 
           u"\u0020\u0020\u2587\u2587\u2587\u0020\u0020",
           u"\u0020\u0020\u2580\u2580\u2580\u0020\u0020" ]

QUEEN   = [ u"\u0020\u0020\u0020\u25D3\u0020\u0020\u0020", 
            u"\u0020\u0020\u2599\u2584\u259F\u0020\u0020", 
            u"\u0020\u0020\u2590\u2588\u258D\u0020\u0020",
            u"\u0020\u0020\u259D\u2580\u2598\u0020\u0020" ]

ROOK   = [ u"\u0020\u0020\u0020\u0020\u0020\u0020\u0020", 
           u"\u0020\u0020\u2596\u2584\u2597\u0020\u0020",
           u"\u0020\u0020\u2590\u2588\u258D\u0020\u0020",
           u"\u0020\u0020\u2580\u2580\u2580\u0020\u0020" ] 

BISHOP   = [ u"\u0020\u0020\u0020\u0020\u0020\u0020\u0020", 
             u"\u0020\u0020\u0020\u2584\u0020\u0020\u0020",
             u"\u0020\u0020\u2590\u2588\u258D\u0020\u0020",
             u"\u0020\u0020\u2580\u2580\u2580\u0020\u0020" ]

KNIGHT   = [ u"\u0020\u0020\u0020\u0020\u0020\u0020\u0020", 
             u"\u0020\u0020\u0020\u2584\u2584\u0020\u0020",
             u"\u0020\u2584\u2580\u259C\u2588\u2599\u0020", 
             u"\u0020\u0020\u0020\u2580\u2580\u2580\u2580" ]

PAWN     = [ u"\u0020\u0020\u0020\u0020\u0020\u0020\u0020",
             u"\u0020\u0020\u2597\u2584\u2596\u0020\u0020", 
             u"\u0020\u0020\u2588\u2588\u2588\u0020\u0020",
             u"\u0020\u0020\u0020\u0020\u0020\u0020\u0020" ]

WHITE_TEXT = "\033[37m"
BLACK_TEXT = "\033[30m"
WHITE_BACK = "\033[47m"
BLUE_BACK  = "\033[44m"
BOLD_ON    = "\033[1m"
RESET_ALL  = "\033[0m"

def prnt_row(match, pieces):
    for i in range(4):
        for k in range(8):
            piece = pieces[k][0]
            backcolor = pieces[k][1]

            if(match.color_of_piece(piece) == COLORS['white']):
                forecolor = "white"
            else:
                forecolor = "black"

            if(piece == PIECES['blk']):
                piecemap = BLANK
            elif(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                piecemap = PAWN
            elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                piecemap = KNIGHT
            elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
                piecemap = BISHOP
            elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
                piecemap = ROOK
            elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                piecemap = QUEEN
            else:
                piecemap = KING

            if(k == 7):
                endstr = "\n"
            else:
                endstr = ""

            offset = i * 9


            if(forecolor == "white"):
                if(backcolor == "white"):
                    print(WHITE_BACK + WHITE_TEXT + BOLD_ON + piecemap[i] + RESET_ALL, end=endstr)
                else:
                    print(BLUE_BACK + WHITE_TEXT + BOLD_ON + piecemap[i] + RESET_ALL, end=endstr)
            else:
                if(backcolor == "white"):
                    print(WHITE_BACK + BLACK_TEXT + piecemap[i] + RESET_ALL, end=endstr)
                else:
                    print(BLUE_BACK + BLACK_TEXT + piecemap[i] + RESET_ALL, end=endstr)


def prnt_board(match):
    pieces = []
    for y in range(7, -1, -1):
        for x in range(8):
            if((y % 2 + x) % 2 == 1):
                backcolor = "white"
            else:
                backcolor = "black"
            pieces.append([match.readfield(x, y), backcolor])
        prnt_row(match, pieces)
        pieces.clear()


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


