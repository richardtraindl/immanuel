from kate.models import Match as ModelMatch, Move as ModelMove
from kate.engine.match import *
from kate.engine.move import *
from kate.engine import kate, helper
from kate.engine.calc import calc_move
from kate.modules.interface import *
import random, threading, copy


def fill_fmtboard(modelmatch, switch):
    fmtboard = [ [ [0  for k in range(2)] for x in range(8)] for x in range(8) ]
    if(switch == 0):
        rowstart = 7
        rowend = -1
        rowstep = -1
        colstart = 0
        colend = 8
        colstep = 1
    else:
        rowstart = 0
        rowend = 8
        rowstep = 1
        colstart = 7
        colend = -1
        colstep = -1
    idx1 = 0
    for i in range(rowstart, rowend, rowstep):
        idx2 = 0
        for j in range(colstart, colend, colstep):
            fmtboard[idx1][idx2][0] = modelmatch.readfield(j, i)
            field = chr(ord('a') + j) + chr(ord('1') + i)
            fmtboard[idx1][idx2][1] = field
            idx2 += 1
        idx1 += 1

    return fmtboard
    

def html_board(match, switch, movesrc, movedst):
    fmtboard = fill_fmtboard(match, switch)
    htmldata = "<table id=\"board\" matchid=\"" + str(match.id) + "\" movecnt=\"" + str(match.count) + "\">"
    htmldata += "<tr id=\"board-letters1\"><td>&nbsp;</td>"
    if(switch == 0):
        for i in range(8):
            htmldata += "<td>" + chr(i + ord('A')) + "</td>"
    else:
        for i in range(8):
            htmldata += "<td>" + chr(ord('H') - i) + "</td>"
    htmldata += "<td>&nbsp;</td></tr>"
    for row in fmtboard:
        htmldata += "<tr><td class=\"board-label\">" + str(row[0][1])[1] + "</td>"
        for col in row:
            if(col[1] == movesrc or col[1] == movedst):
                htmldata += "<td id=\"" + str(col[1]) + "\" class=\"hint droppable\"  value=\"" + str(col[0]) + "\">"
            else:
                htmldata += "<td id=\"" + str(col[1]) + "\" class=\"droppable\" value=\"" + str(col[0]) + "\">"

            if(col[0] == 0):
                htmldata += "&nbsp;"
            else:
                piece = helper.reverse_lookup(PIECES, col[0])
                htmldata += "<img class=\"draggable\" " + " src=\"/static/img/" + piece + ".png\">"
            htmldata += "</td>"
        htmldata += "<td class=\"board-label\">" + str(row[0][1])[1] + "</td></tr>"
    htmldata += "<tr id=\"board-letters2\"><td>&nbsp;</td>"
    if(switch == 0):
        for i in range(8):
            htmldata += "<td>" + chr(i + ord('A')) + "</td>"
    else:
        for i in range(8):
            htmldata += "<td>" + chr(ord('H') - i) + "</td>"
    htmldata += "<td>&nbsp;</td></tr></table>"
    return htmldata


def html_moves(modelmatch):
    htmlmoves = "<table>"
    htmlmoves += "<tr><td>&nbsp;</td>"
    if(modelmatch.white_player_human == False):
        htmlmoves += "<td><span class=\"fbold\">" + modelmatch.white_player + "</span></td>"
    else:
        htmlmoves += "<td>" + modelmatch.white_player + "</td>"
    if(modelmatch.black_player_human == False):
        htmlmoves += "<td><span class=\"fbold\">" + modelmatch.black_player + "</span></td>"
    else:
        htmlmoves += "<td>" + modelmatch.black_player + "</td>"
    htmlmoves += "</tr>"

    currmove = ModelMove.objects.filter(match_id=modelmatch.id).order_by("count").last()
    if(currmove != None):
        if(currmove.count % 2 == 0):
            limit = 22
        else:
            limit = 21
        moves = ModelMove.objects.filter(match_id=modelmatch.id).order_by("-count")[:limit]
        for move in reversed(moves):
            emove = Move()
            map_moves(move, emove, MAP_DIR['model-to-engine'])
            if(emove.count % 2 == 1 ):
                htmlmoves += "<tr><td>" + str( (emove.count + 1) // 2) + ".</td>"
                htmlmoves += "<td>" + emove.format_move() + "</td>"
            else:
                htmlmoves += "<td>" + emove.format_move() + "</td></tr>"
        if(len(moves) % 2 == 1):
            htmlmoves += "<td>&nbsp;</td></tr>"
    htmlmoves += "</table>"
    return htmlmoves


class immanuelsThread(threading.Thread):
    def __init__(self, name, match):
        threading.Thread.__init__(self)
        self.name = name
        self.running = True
        self.match = copy.deepcopy(match)
        self.searchcnt = None
        self.search = None
        self.candidates = [None] * 10
        self.debuginfo = None

        Match.remove_threads(match)
        Match.add_thread(self)
        print("match.id: " + str(match.id))


    def run(self):
        print("Starting " + str(self.name))
        # move = Move.objects.filter(match_id=self.match.id).order_by("count").last()
        # if(move != None):
        #     self.match.move_list.append(move)

        gmove = calc_move(self.match)
        if(gmove and Match.does_thread_exist(self) and self.running):
            move = kate.do_move(self.match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

            modelmatch = ModelMatch()
            map_matches(self.match, modelmatch, MAP_DIR['engine-to-model'])
            modelmatch.save()

            modelmove = ModelMove()
            modelmove.match = modelmatch
            map_moves(move, modelmove, MAP_DIR['engine-to-model'])                
            modelmove.save()
            print("move saved")
        else:
            print("thread outdated - move dropped")

        return gmove


    def populate_candiates(self, candiates):
        if(candiates[0]):
            idx = 0
            for cand in candiates:
                if(cand):
                    self.candidates[idx] = cand
                    idx += 1
                else:
                    break


    def populate_search(self, gmove, cnt):
        if(gmove and cnt):
            self.searchcnt = cnt
            self.search = gmove


    def populate_debuginfo(self, debuginfo):
        if(debuginfo):
            self.debuginfo = debuginfo


def thread_do_move(match):
    thread = immanuelsThread("immanuel-" + str(random.randint(0, 100000)), match)
    thread.start()