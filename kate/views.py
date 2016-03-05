from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from kate.models import Match, Move, Comment
from kate.modules import values, rules


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


def index(request):
    context = RequestContext(request)
    matches = Match.objects.order_by("begin").reverse()[:10]
    return render(request, 'kate/index.html', {'matches': matches} )


def match(request, match_id=None, switch=0, newmove=0):
    context = RequestContext(request)
    if match_id == None:
        match = Match(white_player=None, black_player=None)
        match.setboardbase()
    else:
        match = Match.objects.get(id=match_id)

    movesrc = ''
    movedst = ''
    if(int(newmove) == 1):
        lastmove = Move.objects.filter(match_id=match.id).order_by("count").last()
        if(lastmove != None):
            movesrc = values.index_to_koord(lastmove.srcx, lastmove.srcy)
            movedst = values.index_to_koord(lastmove.dstx, lastmove.dsty)

    fmtboard = fill_fmtboard(match, int(switch))
    fmtmoves = fill_fmtmoves(match)
    comments = Comment.objects.filter(match_id=match_id).order_by("created_at").reverse()[:5]
    msg = "<p class='ok'></p>"
    return render(request, 'kate/match.html', {'match': match, 'board': fmtboard, 'switch': switch, 'movesrc': movesrc, 'movedst': movedst, 'fmtmoves': fmtmoves, 'comments': comments, 'msg': msg } )


def new(request):
    context = RequestContext(request)
    return render(request, 'kate/new.html', {'white_player': "", 'black_player': "" } )


def create(request):
    context = RequestContext(request)
    if request.method == 'POST':
        match = Match()
        match.white_player = request.POST['white_player']
        match.black_player = request.POST['black_player']
        if(len(match.white_player) > 0 and len(match.black_player)):
            match.setboardbase()
            match.save()
            return HttpResponseRedirect(reverse('kate:match', args=(match.id,)))
    return render(request, 'kate/new.html', {'white_player': match.white_player, 'black_player': match.black_player } )


def do_move(request, match_id):
    context = RequestContext(request)
    if request.method == 'POST':
        match = get_object_or_404(Match, pk=match_id)
        movesrc = request.POST['move_src']
        movedst = request.POST['move_dst']
        prompiece = request.POST['prom_piece']
        switch = request.POST['switch']
        if(len(movesrc) > 0 and len(movedst) > 0 and len(prompiece) > 0):
            srcx,srcy = values.koord_to_index(movesrc)
            dstx,dsty = values.koord_to_index(movedst)
            prom_piece = match.PIECES[prompiece]
            if(rules.is_move_valid(match, srcx, srcy, dstx, dsty, prom_piece) == True):
                match = Match.objects.get(id=match_id)
                move = match.do_move(srcx, srcy, dstx, dsty, prom_piece)
                move.save()
                match.save()
                msg = "<p class='ok'>Zug ist OK.</p>"
            else:
                msg = "<p class='error'>Zug ist ungültig.</p>"
        else:
            msg = "<p class='error'>Zug-Format ist ungültig.</p>"
        fmtboard = fill_fmtboard(match, int(switch))
        fmtmoves = fill_fmtmoves(match)
        comments = Comment.objects.filter(match_id=match_id).order_by("created_at").reverse()[:5]
        return render(request, 'kate/match.html', {'match': match, 'board': fmtboard, 'switch': switch, 'movesrc': movesrc, 'movedst': movedst, 'fmtmoves': fmtmoves, 'comments': comments, 'msg': msg } )
    else:
        return HttpResponseRedirect(reverse('kate:match', args=(match_id, switch)))


def undo_move(request, match_id, switch=None):
    context = RequestContext(request)
    match = Match.objects.get(id=match_id)
    move = match.undo_move()
    if(move != None):
        move.delete()
        match.save()
    return HttpResponseRedirect(reverse('kate:match', args=(match.id, switch)))


def add_comment(request, match_id):
    context = RequestContext(request)
    match = get_object_or_404(Match, pk=match_id)
    if request.method == 'POST':
        newcomment = request.POST['newcomment']
        if(len(newcomment) > 0):
            comment = Comment()
            comment.match_id = match.id
            comment.text = newcomment
            comment.save()
    return HttpResponseRedirect(reverse('kate:match', args=(match.id, 0)))


def fetch_comments(request):
    context = RequestContext(request)
    if request.method == 'GET':
        match_id = request.GET['matchid']
        comments = Comment.objects.filter(match_id=match_id).order_by("created_at").reverse()[:5]
        data = ""
        for comment in reversed(comments):
            data += "<p>" + comment.text + "</p>"
        return HttpResponse(data)


def fetch_board(request):
    context = RequestContext(request)
    matchid = request.GET['matchid']
    movecnt = request.GET['movecnt']
    match = Match.objects.get(id=matchid)
    print(" " + str(movecnt) + " " + str(match.count))
    if(int(movecnt) == match.count):
        data = 0
    else:
        data = 1
    return HttpResponse(data)
    
