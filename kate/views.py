from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from kate.models import Match, Move, Comment
from kate.modules import helper, rules, calc, kate


def calc_move_for_immanuel(match):
    if(rules.game_status(match) == Match.STATUS['open'] and match.next_color_human() == False):
        calc.thread_do_move(match)


def fill_fmtboard(match, switch):
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
            fmtboard[idx1][idx2][0] = match.board[i][j]
            field = chr(ord('a') + j) + chr(ord('1') + i)
            fmtboard[idx1][idx2][1] = field
            idx2 += 1
        idx1 += 1

    return fmtboard


def index(request):
    context = RequestContext(request)
    matches = Match.objects.order_by("begin").reverse()[:10]
    return render(request, 'kate/index.html', { 'matches': matches } )


def match(request, matchid=None, switch=0, msg=None):
    context = RequestContext(request)
    if(matchid == None):
        match = Match(white_player=None, black_player=None)
        match.setboardbase()
    else:
        match = Match.objects.get(id=matchid)

    lastmove = Move.objects.filter(match_id=match.id).order_by("count").last()
    if(lastmove):
        movesrc = Match.index_to_koord(lastmove.srcx, lastmove.srcy)
        movedst = Match.index_to_koord(lastmove.dstx, lastmove.dsty)
    else:
        movesrc = ''
        movedst = ''

    fmtboard = fill_fmtboard(match, int(switch))

    moves = []
    currmove = Move.objects.filter(match_id=match.id).order_by("count").last()
    if(currmove != None):
        if(currmove.count % 2 == 0):
            limit = 22
        else:
            limit = 21
        qmoves = Move.objects.filter(match_id=match.id).order_by("-count")[:limit]
        for qmove in reversed(qmoves):
            moves.append(qmove)

    comments = Comment.objects.filter(match_id=match.id).order_by("created_at").reverse()[:3]
    
    if(msg == None):
        fmtmsg = "<p class='ok'></p>"
    elif(int(msg) == 0):
        fmtmsg = "<p class='ok'>" + rules.RETURN_MSGS[int(msg)] + "</p>"
    else:
        fmtmsg = "<p class='error'>" + rules.RETURN_MSGS[int(msg)] + "</p>"

    if(int(switch) == 0):
        rangeobj = range(8)
    else:
        rangeobj = range(7, -1, -1)

    thread = Match.get_active_thread(match)
    if(thread and thread.running):
        if(thread.search):
            gmove = thread.search
            search = "current search: " + Match.index_to_koord(gmove.srcx, gmove.srcy) + "-" + Match.index_to_koord(gmove.dstx, gmove.dsty)
        else:
            search = "current search: ---"

        if(thread.candidates[0]):
            candidates = "candidates: "
            for cand in thread.candidates[:3]:
                if(cand):
                    candidates += "[" + Match.index_to_koord(cand.srcx, cand.srcy) + "-" + Match.index_to_koord(cand.dstx, cand.dsty) + "]"
        else:
            candidates = "candidates: ---"
    else:
        search = "current search: ---"
        candidates = "candidates: ---"

    return render(request, 'kate/match.html', { 'match': match, 'board': fmtboard, 'switch': switch, 'movesrc': movesrc, 'movedst': movedst, 'moves': moves, 'comments': comments, 'msg': fmtmsg, 'range': rangeobj, 'search': search, 'candidates': candidates } )


def new(request):
    context = RequestContext(request)
    return render(request, 'kate/new.html', { 'white_player': "", 'white_player_human': True, 'black_player': "", 'black_player_human': True } )


def create(request):
    context = RequestContext(request)
    if(request.method == 'POST'):
        match = Match()

        match.white_player = request.POST['white_player']
        if(request.POST.get('white_player_human')):
            match.white_player_human = True
        else:
            match.white_player_human = False

        match.black_player = request.POST['black_player']
        if(request.POST.get('black_player_human')):
            match.black_player_human = True
        else:
            match.black_player_human = False

        levellist = request.POST.getlist('level')
        match.level = Match.LEVELS[levellist[0]]

        if(len(match.white_player) > 0 and len(match.black_player) > 0):
            match.setboardbase()
            match.save()
            calc_move_for_immanuel(match)
            return HttpResponseRedirect(reverse('kate:match', args=(match.id,)))

    return render(request, 'kate/new.html', { 'white_player': match.white_player, 'white_player_human': match.white_player_human, 'black_player': match.black_player, 'black_player_human': match.black_player_human } )


def edit(request, matchid, switch=0):
    context = RequestContext(request)
    match = get_object_or_404(Match, pk=matchid)
    return render(request, 'kate/edit.html', { 'match': match, 'switch': switch } )


def update(request, matchid, switch=0):
    context = RequestContext(request)
    match = get_object_or_404(Match, pk=matchid)
    if(request.method == 'POST'):
        match.white_player = request.POST['white_player']
        if(request.POST.get('white_player_human')):
            match.white_player_human = True
        else:
            match.white_player_human = False

        match.black_player = request.POST['black_player']
        if(request.POST.get('black_player_human')):
            match.black_player_human = True
        else:
            match.black_player_human = False

        levellist = request.POST.getlist('level')
        match.level = Match.LEVELS[levellist[0]]

        if(len(match.white_player) > 0 and len(match.black_player) > 0):
            match.save()
            calc_move_for_immanuel(match)
            return HttpResponseRedirect(reverse('kate:match', args=(match.id, switch,)))

    return render(request, 'kate/edit.html', { 'match': match, 'switch': switch } )


def delete(request, matchid):
    Match.objects.filter(id=matchid).delete()
    return index(request)


def do_move(request, matchid):
    context = RequestContext(request)
    if request.method == 'POST':
        match = get_object_or_404(Match, pk=matchid)
        switch = request.POST['switch']        
        status = rules.game_status(match)
        if(status != Match.STATUS['open']):
            if(status == Match.STATUS['draw']):
                msg = rules.RETURN_CODES['draw']
            elif(status == Match.STATUS['winner_white']):
                msg = rules.RETURN_CODES['winner_white']
            elif(status == Match.STATUS['winner_black']):
                msg = rules.RETURN_CODES['winner_black']
            else:
                msg = rules.RETURN_CODES['match-cancelled']
            return HttpResponseRedirect(reverse('kate:match', args=(matchid, switch, msg)))
        if(match.next_color_human() == False):
            msg= rules.RETURN_CODES['wrong-color']
            return HttpResponseRedirect(reverse('kate:match', args=(matchid, switch, msg)))

        movesrc = request.POST['move_src']
        movedst = request.POST['move_dst']
        prompiece = request.POST['prom_piece']        
        if(len(movesrc) > 0 and len(movedst) > 0 and len(prompiece) > 0):
            srcx,srcy = Match.koord_to_index(movesrc)
            dstx,dsty = Match.koord_to_index(movedst)
            prom_piece = match.PIECES[prompiece]
            flag, msg = rules.is_move_valid(match, srcx, srcy, dstx, dsty, prom_piece)
            if(flag == True):
                move = kate.do_move(match, srcx, srcy, dstx, dsty, prom_piece)
                move.save()
                match.save()
                calc_move_for_immanuel(match)
        else:
            msg = rules.RETURN_CODES['format-error']

        return HttpResponseRedirect(reverse('kate:match', args=(matchid, switch, msg)))
    else:
        return HttpResponseRedirect(reverse('kate:match', args=(matchid, switch)))


def force_move(request, matchid, switch=0):
    context = RequestContext(request)
    match = Match.objects.get(id=matchid)

    thread = Match.get_active_thread(match)
    if(thread and thread.running and thread.candidates[0]):
        thread.running = False
        gmove = thread.candidates[0]
        msg = rules.RETURN_CODES['ok']
        move = kate.do_move(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
        move.save()
        match.save()
        return HttpResponseRedirect(reverse('kate:match', args=(matchid, switch, msg)))
    else:
        return HttpResponseRedirect(reverse('kate:match', args=(matchid, switch)))


def undo_move(request, matchid, switch=0):
    context = RequestContext(request)
    match = Match.objects.get(id=matchid)

    thread = Match.get_active_thread(match)
    if(thread):
        thread.running = False
    move = kate.undo_move(match, False)

    if(move != None):
        move.delete()
        match.save()

    return HttpResponseRedirect(reverse('kate:match', args=(match.id, switch)))


def resume(request, matchid, switch=0):
    context = RequestContext(request)
    match = Match.objects.get(id=matchid)
    calc_move_for_immanuel(match)
    return HttpResponseRedirect(reverse('kate:match', args=(match.id, switch)))


def add_comment(request, matchid):
    context = RequestContext(request)
    match = get_object_or_404(Match, pk=matchid)
    if request.method == 'POST':
        newcomment = request.POST['newcomment']
        switchflag = request.POST['switchflag']        
        if(len(newcomment) > 0):
            comment = Comment()
            comment.match_id = match.id
            comment.text = newcomment
            comment.save()
    return HttpResponseRedirect(reverse('kate:match', args=(match.id, switchflag)))


def fetch_comments(request):
    context = RequestContext(request)
    if request.method == 'GET':
        matchid = request.GET['matchid']
        comments = Comment.objects.filter(match_id=matchid).order_by("created_at").reverse()[:3]
        data = ""
        for comment in reversed(comments):
            data += "<p>" + comment.text + "</p>"
        return HttpResponse(data)


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
                piece = helper.reverse_lookup(Match.PIECES, col[0])
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


def html_moves(match):
    htmlmoves = "<table>"
    htmlmoves += "<tr><td>&nbsp;</td>"
    if(match.white_player_human == False):
        htmlmoves += "<td><span class=\"fbold\">" + match.white_player + "</span></td>"
    else:
        htmlmoves += "<td>" + match.white_player + "</td>"
    if(match.black_player_human == False):
        htmlmoves += "<td><span class=\"fbold\">" + match.black_player + "</span></td>"
    else:
        htmlmoves += "<td>" + match.black_player + "</td>"
    htmlmoves += "</tr>"

    currmove = Move.objects.filter(match_id=match.id).order_by("count").last()
    if(currmove != None):
        if(currmove.count % 2 == 0):
            limit = 22
        else:
            limit = 21
        moves = Move.objects.filter(match_id=match.id).order_by("-count")[:limit]
        for move in reversed(moves):
            if(move.count % 2 == 1 ):
                htmlmoves += "<tr><td>" + str( (move.count + 1) // 2) + ".</td>"
                htmlmoves += "<td>" + move.format_move() + "</td>"
            else:
                htmlmoves += "<td>" + move.format_move() + "</td></tr>"
        if(len(moves) % 2 == 1):
            htmlmoves += "<td>&nbsp;</td></tr>"
    htmlmoves += "</table>"
    return htmlmoves


def fetch_match(request):
    context = RequestContext(request)
    matchid = request.GET['matchid']
    movecnt = request.GET['movecnt']
    switchflag = request.GET['switchflag']
    match = Match.objects.get(id=matchid)
    if(match == None):
        data = "§§§§"
    else:
        lastmove = Move.objects.filter(match_id=match.id).order_by("count").last()
        if(lastmove != None):
            movesrc = Match.index_to_koord(lastmove.srcx, lastmove.srcy)
            movedst = Match.index_to_koord(lastmove.dstx, lastmove.dsty)
        if(int(movecnt) == match.count):
            data = "§§"
        else:
            data = html_board(match, int(switchflag), movesrc, movedst)
            data += "§" + html_moves(match)
            data += "§<p>Score: &nbsp;" + str(match.score) + "</p>"

        thread = Match.get_active_thread(match)
        if(thread and thread.search and thread.candidates[0]):
            gmove = thread.search
            data += "§<p>current search: " 
            data += Match.index_to_koord(gmove.srcx, gmove.srcy) + "-" + Match.index_to_koord(gmove.dstx, gmove.dsty)
            data += "</p>"

            data += "§<br>candidates: <br>"
            for cand in thread.candidates[:3]:
                if(cand):
                    data += "[" + Match.index_to_koord(cand.srcx, cand.srcy) + "-" + Match.index_to_koord(cand.dstx, cand.dsty) + "]"
            data += "</p>"
        else:
            data += "§§"

    return HttpResponse(data)

