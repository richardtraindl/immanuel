from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from kate.models import Match, Move, Comment
from kate.modules import values, rules

def index(request, matchid=None):
    context = RequestContext(request)
    if matchid == None:
        match = Match(white_player=None, black_player=None)
        match.setboardbase()
    else:
        match = Match.objects.get(id=matchid)

    chessbd = match.readboard()
    board = [ [ [0  for k in range(2)] for x in range(8)] for x in range(8) ]
    for i in range(8):
        for j in range(8):
            board[i][j][0] = chessbd[i][j]
            field = chr(ord('a') + j) + chr(ord('1') + i)
            board[i][j][1] = field

    curr_move = Move.objects.filter(match_id=matchid).order_by("count").last()
    if(curr_move == None):
        fmtmoves = []
    else:
        if(curr_move.count % 2 == 0):
            limit = 10
        else:
            limit = 11
        moves = Move.objects.filter(match_id=matchid).order_by("count")[:limit]
        fmtmoves = []
        for move in moves:
            if(move.count % 2 == 1 ):
                fmtmoves.append("<tr><td>" + str( (move.count + 1) // 2) + ".</td>")
                fmtmoves.append("<td>" + values.format_move(move) + "</td>")
            else:
                fmtmoves.append("<td>" + values.format_move(move) + "</td></tr>")
        if(len(moves) % 2 == 1):
            fmtmoves.append("<td>&nbsp;</td></tr>")

    comments = Comment.objects.filter().order_by("created_at").reverse()[:5]

    return render(request, 'kate/index.html', {'match': match, 'board': board, 'fmtmoves': fmtmoves, 'comments': comments, } )


def new(request):
    context = RequestContext(request)
    return render(request, 'kate/new.html', {} )


def create(request):
    context = RequestContext(request)
    if request.method == 'POST':
        match = Match()
        match.white_player = request.POST['white_player']
        match.black_player = request.POST['black_player']
        match.setboardbase()
        match.save()
        return HttpResponseRedirect(reverse('kate:index', args=(match.id,)))
    else:
        return HttpResponseRedirect(reverse('kate:index'))


def load(request):
    context = RequestContext(request)
    matches = Match.objects.order_by("begin").reverse()[:10]
    return render(request, 'kate/load.html', {'matches': matches} )


def move(request, matchid):
    context = RequestContext(request)
    if request.method == 'POST':
        match = get_object_or_404(Match, pk=matchid)
        movesrc = request.POST['move_src']
        movedst = request.POST['move_dst']
        prom_piece = request.POST['prom_piece']
        if(len(movesrc) > 0 and len(movedst) > 0 and len(prom_piece) > 0):
            src = values.koord_to_index(movesrc)
            dest = values.koord_to_index(movedst)
            if(rules.is_move_valid(match, src, dest, prom_piece) == True):
                match = Match.objects.get(id=matchid)
                move = match.do_move(src, dest, prom_piece)
                move.save()
                match.save()
                return HttpResponseRedirect(reverse('kate:index', args=(match.id,)))

    return HttpResponseRedirect(reverse('kate:index'))


def undo_move(request, matchid):
    context = RequestContext(request)
    match = Match.objects.get(id=matchid)
    move = match.undo_move()
    if(move != None):
        move.delete()
        match.save()
    return HttpResponseRedirect(reverse('kate:index', args=(match.id,)))


def add_comment(request):
    context = RequestContext(request)

    newcomment = request.GET['newcomment']
    print(": " + newcomment)
    if(len(newcomment) > 0):
        comment = Comment()
        comment.text = newcomment
        comment.save()

    comments = Comment.objects.filter().order_by("created_at").reverse()[:5]
    data = ""
    for comment in reversed(comments):
        data += "<p>" + comment.text + "</p>"

    return HttpResponse(data)


def retrieve_comments(request):
    context = RequestContext(request)

    comments = Comment.objects.filter().order_by("created_at").reverse()[:5]
    data = ""
    for comment in reversed(comments):
        data += "<p>" + comment.text + "</p>"

    return HttpResponse(data)


