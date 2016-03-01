from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from kate.models import Match, Move, Comment
from kate.modules import values, rules


def fill_fmtboard(match):
    fmtboard = [ [ [0  for k in range(2)] for x in range(8)] for x in range(8) ]

    for i in range(8):
        for j in range(8):
            fmtboard[i][j][0] = match.board[i][j]
            field = chr(ord('a') + j) + chr(ord('1') + i)
            fmtboard[i][j][1] = field
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


def match(request, match_id=None):
    context = RequestContext(request)
    if match_id == None:
        match = Match(white_player=None, black_player=None)
        match.setboardbase()
    else:
        match = Match.objects.get(id=match_id)

    fmtboard = fill_fmtboard(match)
    fmtmoves = fill_fmtmoves(match)
    comments = Comment.objects.filter(match_id=match_id).order_by("created_at").reverse()[:5]
    msg = "<p class='ok'></p>"
    return render(request, 'kate/match.html', {'match': match, 'board': fmtboard, 'fmtmoves': fmtmoves, 'comments': comments, 'msg': msg } )


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
        fmtboard = fill_fmtboard(match)
        fmtmoves = fill_fmtmoves(match)
        comments = Comment.objects.filter(match_id=match_id).order_by("created_at").reverse()[:5]
        return render(request, 'kate/match.html', {'match': match, 'board': fmtboard, 'fmtmoves': fmtmoves, 'comments': comments, 'msg': msg } )
    else:
        return HttpResponseRedirect(reverse('kate:match', args=(match_id,)))


def undo_move(request, match_id):
    context = RequestContext(request)
    match = Match.objects.get(id=match_id)
    move = match.undo_move()
    if(move != None):
        move.delete()
        match.save()
    return HttpResponseRedirect(reverse('kate:match', args=(match.id,)))


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
    return HttpResponseRedirect(reverse('kate:match', args=(match.id,)))


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


def fetch_board2(request):
    context = RequestContext(request)
    match_id = request.GET['match_id']

    match = Match.objects.get(id=match_id)
    chessbd = fill_fmtboard(match)
    # chessbd = match.readboard()
    # board = [ [ [0  for k in range(2)] for x in range(8)] for x in range(8) ]
    # for i in range(8):
    #     for j in range(8):
    #         board[i][j][0] = chessbd[i][j]
    #         field = chr(ord('a') + j) + chr(ord('1') + i)
    #         board[i][j][1] = field

    data = []
    data += "<tr id='board-letters'><td>&nbsp;</td><td>A</td><td>B</td><td>C</td><td>D</td><td>E</td><td>F</td><td>G</td><td>H</td><td>&nbsp;</td></tr>"
    for row in reversed(chessbd):
        data += "<tr><td class='board-label'>" + str((row[0][1])[1]) + "</td>"
        for col in row:
            if col[0] == 0:
                data += "<td id='" + str(col[1]) + "' value='" + str(col[0]) + "'>&nbsp;</td>"
            else:
                data += "<td id='" + str(col[1]) + "' value='" + str(col[0]) + "'><img src='/static/img/" + str(values.reverse_lookup(match.PIECES, col[0])) + ".png'></td>"
        data += "<td class='board-label'>" + str((row[0][1])[1]) + "</td></tr>"
    data += "<tr id='board-letters'><td>&nbsp;</td><td>A</td><td>B</td><td>C</td><td>D</td><td>E</td><td>F</td><td>G</td><td>H</td><td>&nbsp;</td></tr>"

    data += "|||"
    lstmoves = fill_fmtmoves(match)
    for col in lstmoves:
        data += col
    return HttpResponse(data)
    
