from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from kate.models import Match, Move, Comment
from kate.modules import helper, rules, calc


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


def html_board(match, switch, movesrc, movedst):
    fmtboard = fill_fmtboard(match, switch)
    htmldata = "<table id='board' matchid='" + str(match.id) + "' movecnt='" + str(match.count) + "'>"
    htmldata += "<tr id='board-letters1'><td>&nbsp;</td>"
    if(switch == 0):
        for i in range(8):
            htmldata += "<td>" + chr(i + ord('A')) + "</td>"
    else:
        for i in range(8):
            htmldata += "<td>" + chr(ord('H') - i) + "</td>"
    htmldata += "<td>&nbsp;</td></tr>"
    for row in fmtboard:
        htmldata += "<tr><td class='board-label'>" + str(row[0][1])[1] + "</td>"
        for col in row:
            if(col[1] == movesrc or col[1] == movedst):
                htmldata += "<td id='" + str(col[1]) + "' class='hint' value='" + str(col[0]) + "'>"
            else:
                htmldata += "<td id='" + str(col[1]) + "' value='" + str(col[0]) + "'>"

            if(col[0] == 0):
                htmldata += "&nbsp;"
            else:
                piece = helper.reverse_lookup(Match.PIECES, col[0])
                htmldata += "<img src='" + "/static/img/" + piece + ".png'>"
            htmldata += "</td>"
        htmldata += "<td class='board-label'>" + str(row[0][1])[1] + "</td></tr>"
    htmldata += "<tr id='board-letters2'><td>&nbsp;</td>"
    if(switch == 0):
        for i in range(8):
            htmldata += "<td>" + chr(i + ord('A')) + "</td>"
    else:
        for i in range(8):
            htmldata += "<td>" + chr(ord('H') - i) + "</td>"
    htmldata += "<td>&nbsp;</td></tr></table>"
    return htmldata


def fill_fmtmoves(match):
    fmtmoves = []
    currmove = Move.objects.filter(match_id=match.id).order_by("count").last()
    if(currmove == None):
        return fmtmoves
    else:
        if(currmove.count % 2 == 0):
            limit = 42
        else:
            limit = 41
        moves = Move.objects.filter(match_id=match.id).order_by("count").reverse()[:limit]
        for move in reversed(moves):
            if(move.count % 2 == 1 ):
                fmtmoves.append("<tr><td>" + str( (move.count + 1) // 2) + ".</td>")
                fmtmoves.append("<td>" + move.format_move() + "&nbsp;</td>")
            else:
                fmtmoves.append("<td>" + move.format_move() + "</td></tr>")
        if(len(moves) % 2 == 1):
            fmtmoves.append("<td>&nbsp;</td></tr>")
        return fmtmoves


def html_moves(match):
    fmtmoves = []
    fmtmoves = fill_fmtmoves(match)
    htmldata = ""
    for col in fmtmoves:
        htmldata += col
    return htmldata


def index(request):
    context = RequestContext(request)
    matches = Match.objects.order_by("begin").reverse()[:10]
    return render(request, 'kate/index.html', { 'matches': matches } )


def match(request, matchid=None, switch=0, markmove=0):
    context = RequestContext(request)
    if matchid == None:
        match = Match(white_player=None, black_player=None)
        match.setboardbase()
    else:
        match = Match.objects.get(id=matchid)
    movesrc = ''
    movedst = ''
    if(int(markmove) == 1):
        lastmove = Move.objects.filter(match_id=match.id).order_by("count").last()
        if(lastmove != None):
            movesrc = Match.index_to_koord(lastmove.srcx, lastmove.srcy)
            movedst = Match.index_to_koord(lastmove.dstx, lastmove.dsty)
    fmtboard = fill_fmtboard(match, int(switch))
    fmtmoves = fill_fmtmoves(match)
    comments = Comment.objects.filter(match_id=match.id).order_by("created_at").reverse()[:5]
    fmtmsg = "<p class='ok'></p>"
    if(int(switch) == 0):
        rangeobj = range(8)
    else:
        rangeobj = range(7, -1, -1)

    return render(request, 'kate/match.html', { 'match': match, 'board': fmtboard, 'switch': switch, 'movesrc': movesrc, 'movedst': movedst, 'fmtmoves': fmtmoves, 'comments': comments, 'msg': fmtmsg, 'range': rangeobj } )


def new(request):
    context = RequestContext(request)
    return render(request, 'kate/new.html', { 'white_player': "", 'white_player_human': True, 'black_player': "", 'black_player_human': True } )


def create(request):
    context = RequestContext(request)
    if request.method == 'POST':
        match = Match()
        match.white_player = request.POST['white_player']
        human = request.POST.getlist('white_player_human')
        if(len(human) == 1):
            match.white_player_human = True
        else:
            match.white_player_human = False
        match.black_player = request.POST['black_player']
        human = request.POST.getlist('black_player_human')
        if(len(human) == 1):
            match.black_player_human = True
        else:
            match.black_player_human = False
        levellist = request.POST.getlist('level')
        match.level = Match.LEVEL[levellist[0]]
        if(len(match.white_player) > 0 and len(match.black_player) > 0):
            match.setboardbase()
            match.immanuels_thread_id = None
            match.save()
            calc_move_for_immanuel(match)
            return HttpResponseRedirect(reverse('kate:match', args=(match.id,)))
    return render(request, 'kate/new.html', { 'white_player': match.white_player, 'white_player_human': match.white_player_human, 'black_player': match.black_player, 'black_player_human': match.black_player_human } )


def edit(request, matchid):
    context = RequestContext(request)
    match = get_object_or_404(Match, pk=matchid)
    return render(request, 'kate/edit.html', { 'match': match } )


def update(request, matchid):
    context = RequestContext(request)
    match = get_object_or_404(Match, pk=matchid)
    if request.method == 'POST':        
        match.white_player = request.POST['white_player']
        human = request.POST.getlist('white_player_human')
        if(len(human) == 1):
            match.white_player_human = True
        else:
            match.white_player_human = False
        match.black_player = request.POST['black_player']
        human = request.POST.getlist('black_player_human')
        if(len(human) == 1):
            match.black_player_human = True
        else:
            match.black_player_human = False
        levellist = request.POST.getlist('level')
        match.level = Match.LEVEL[levellist[0]]
        if(len(match.white_player) > 0 and len(match.black_player) > 0):
            match.save()
            calc_move_for_immanuel(match)
            return HttpResponseRedirect(reverse('kate:match', args=(match.id,)))
    return render(request, 'kate/edit.html', { 'match': match } )


def delete(request, matchid):
    Match.objects.filter(id=matchid).delete()
    return index(request)


def do_move(request, matchid):
    context = RequestContext(request)
    if request.method == 'POST':
        match = get_object_or_404(Match, pk=matchid)
        movesrc = request.POST['move_src']
        movedst = request.POST['move_dst']
        prompiece = request.POST['prom_piece']
        switch = request.POST['switch']
        if(match.next_color_human()):
            if(len(movesrc) > 0 and len(movedst) > 0 and len(prompiece) > 0):
                srcx,srcy = Match.koord_to_index(movesrc)
                dstx,dsty = Match.koord_to_index(movedst)
                prom_piece = match.PIECES[prompiece]
                flag, msg = rules.is_move_valid(match, srcx, srcy, dstx, dsty, prom_piece)
                status = rules.game_status(match)
                if(flag == True and status == Match.STATUS['open']):
                    move = match.do_move(srcx, srcy, dstx, dsty, prom_piece)
                    move.save()
                    match.save()
                    calc_move_for_immanuel(match)
                    fmtmsg = "<p class='ok'>" + rules.ERROR_MSGS[msg] + "</p>"
                else:
                    fmtmsg = "<p class='error'>" + rules.ERROR_MSGS[msg] + "</p>"
            else:
                fmtmsg = "<p class='error'>Zug-Format ist ungültig.</p>"
        else:
            fmtmsg = "<p class='error'>Mensch ist nicht am Zug.</p>"

        fmtboard = fill_fmtboard(match, int(switch))
        fmtmoves = fill_fmtmoves(match)
        comments = Comment.objects.filter(match_id=match.id).order_by("created_at").reverse()[:5]

        status = rules.game_status(match)
        if(status != Match.STATUS['open']):
            fmtmsg = "<p class='error'>" + helper.reverse_lookup(Match.STATUS, status) + "</p>"

        if(int(switch) == 0):
            rangeobj = range(8)
        else:
            rangeobj = range(7, -1, -1)

        return render(request, 'kate/match.html', { 'match': match, 'board': fmtboard, 'switch': switch, 'movesrc': movesrc, 'movedst': movedst, 'fmtmoves': fmtmoves, 'comments': comments, 'msg': fmtmsg, 'range': rangeobj } )
    else:
        return HttpResponseRedirect(reverse('kate:match', args=(matchid, switch)))


def undo_move(request, matchid, switch=None):
    context = RequestContext(request)
    match = Match.objects.get(id=matchid)
    move = match.undo_move(False)
    if(move != None):
        move.delete()
        match.save()
        calc_move_for_immanuel(match)
    return HttpResponseRedirect(reverse('kate:match', args=(match.id, switch, 1)))


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
        comments = Comment.objects.filter(match_id=matchid).order_by("created_at").reverse()[:5]
        data = ""
        for comment in reversed(comments):
            data += "<p>" + comment.text + "</p>"
        return HttpResponse(data)


def fetch_board(request):
    context = RequestContext(request)
    matchid = request.GET['matchid']
    movecnt = request.GET['movecnt']
    switchflag = request.GET['switchflag']
    match = Match.objects.get(id=matchid)
    if(match == None):
        data = ""
    else:
        lastmove = Move.objects.filter(match_id=match.id).order_by("count").last()
        if(lastmove != None):
            movesrc = Match.index_to_koord(lastmove.srcx, lastmove.srcy)
            movedst = Match.index_to_koord(lastmove.dstx, lastmove.dsty)
        if(int(movecnt) == match.count):
            data = ""
        else:
            html_player = "<tr><td>&nbsp;</td><td>"
            if(match.white_player_human == False):
                html_player += "<span class='fbold'>" + match.white_player + "</span>"
            else:
                html_player += match.white_player

            html_player += "</td><td>"
            if(match.black_player_human == False):
                html_player += "<span class='fbold'>" + match.black_player + "</span>"
            else:
                html_player += match.black_player

            html_player += "</td></tr>"

            data = html_board(match, int(switchflag), movesrc, movedst) + ":" + html_player + html_moves(match)
    return HttpResponse(data)

