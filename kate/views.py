from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from kate.models import Match as ModelMatch, Move as ModelMove, Comment as ModelComment
from kate.engine.match import *
from kate.engine.move import *
from kate.modules import interface
from kate.engine.rules import RETURN_CODES, RETURN_MSGS
from kate.utils import *


def index(request):
    context = RequestContext(request)
    modelmatches = ModelMatch.objects.order_by("begin").reverse()[:10]
    return render(request, 'kate/index.html', { 'matches': modelmatches } )


def match(request, matchid=None, switch=0, msg=None):
    context = RequestContext(request)
    if(matchid == None):
        modelmatch = ModelMatch(white_player=None, black_player=None)
    else:
        modelmatch = ModelMatch.objects.get(id=matchid)

    lastmove = ModelMove.objects.filter(match_id=modelmatch.id).order_by("count").last()
    if(lastmove):
        movesrc = Match.index_to_koord(lastmove.srcx, lastmove.srcy)
        movedst = Match.index_to_koord(lastmove.dstx, lastmove.dsty)
    else:
        movesrc = ''
        movedst = ''

    fmtboard = fill_fmtboard(modelmatch, int(switch))

    moves = []
    currmove = ModelMove.objects.filter(match_id=modelmatch.id).order_by("count").last()
    if(currmove != None):
        if(currmove.count % 2 == 0):
            limit = 22
        else:
            limit = 21
        qmoves = ModelMove.objects.filter(match_id=modelmatch.id).order_by("-count")[:limit]
        for qmove in reversed(qmoves):
            move = Move()
            interface.map_moves(qmove, move, interface.MAP_DIR['model-to-engine'])
            moves.append(move)

    comments = ModelComment.objects.filter(match_id=modelmatch.id).order_by("created_at").reverse()[:3]
    
    if(msg == None):
        fmtmsg = "<p class='ok'></p>"
    elif(int(msg) == 0):
        fmtmsg = "<p class='ok'>" + RETURN_MSGS[int(msg)] + "</p>"
    else:
        fmtmsg = "<p class='error'>" + RETURN_MSGS[int(msg)] + "</p>"

    if(int(switch) == 0):
        rangeobj = range(8)
    else:
        rangeobj = range(7, -1, -1)

    thread = ModelMatch.get_active_thread(modelmatch)
    if(thread and thread.running):
        running = "calculation is running..."
    else:
        running = ""
    return render(request, 'kate/match.html', { 'match': modelmatch, 'board': fmtboard, 'switch': switch, 'movesrc': movesrc, 'movedst': movedst, 'moves': moves, 'comments': comments, 'msg': fmtmsg, 'range': rangeobj, 'running': running } )


def new(request):
    context = RequestContext(request)
    return render(request, 'kate/new.html', { 'white_player': "", 'white_player_human': True, 'black_player': "", 'black_player_human': True } )


def create(request):
    context = RequestContext(request)
    if(request.method == 'POST'):
        modelmatch = ModelMatch()

        modelmatch.white_player = request.POST['white_player']
        if(request.POST.get('white_player_human')):
            modelmatch.white_player_human = True
        else:
            modelmatch.white_player_human = False

        modelmatch.black_player = request.POST['black_player']
        if(request.POST.get('black_player_human')):
            modelmatch.black_player_human = True
        else:
            modelmatch.black_player_human = False

        levellist = request.POST.getlist('level')
        modelmatch.level = LEVELS[levellist[0]]

        if(len(modelmatch.white_player) > 0 and len(modelmatch.black_player) > 0):
            modelmatch.save()
            interface.calc_move_for_immanuel(modelmatch)
            return HttpResponseRedirect(reverse('kate:match', args=(modelmatch.id,)))

    return render(request, 'kate/new.html', { 'white_player': modelmatch.white_player, 'white_player_human': modelmatch.white_player_human, 'black_player': modelmatch.black_player, 'black_player_human': modelmatch.black_player_human } )


def edit(request, matchid, switch=0):
    context = RequestContext(request)
    modelmatch = get_object_or_404(ModelMatch, pk=matchid)
    return render(request, 'kate/edit.html', { 'match': modelmatch, 'switch': switch } )


def update(request, matchid, switch=0):
    context = RequestContext(request)
    modelmatch = get_object_or_404(ModelMatch, pk=matchid)
    if(request.method == 'POST'):
        modelmatch.white_player = request.POST['white_player']
        if(request.POST.get('white_player_human')):
            modelmatch.white_player_human = True
        else:
            modelmatch.white_player_human = False

        modelmatch.black_player = request.POST['black_player']
        if(request.POST.get('black_player_human')):
            modelmatch.black_player_human = True
        else:
            modelmatch.black_player_human = False

        levellist = request.POST.getlist('level')
        modelmatch.level = LEVELS[levellist[0]]

        if(len(modelmatch.white_player) > 0 and len(modelmatch.black_player) > 0):
            modelmatch.save()
            interface.calc_move_for_immanuel(modelmatch)
            return HttpResponseRedirect(reverse('kate:match', args=(modelmatch.id, switch,)))

    return render(request, 'kate/edit.html', { 'match': modelmatch, 'switch': switch } )


def delete(request, matchid):
    ModelMatch.objects.filter(id=matchid).delete()
    return index(request)


def do_move(request, matchid):
    context = RequestContext(request)
    if request.method == 'POST':
        modelmatch = get_object_or_404(ModelMatch, pk=matchid)
        switch = request.POST['switch']
        movesrc = request.POST['move_src']
        movedst = request.POST['move_dst']
        prompiece = request.POST['prom_piece']        
        if(len(movesrc) > 0 and len(movedst) > 0 and len(prompiece) > 0):
            srcx,srcy = Match.koord_to_index(movesrc)
            dstx,dsty = Match.koord_to_index(movedst)
            prom_piece = PIECES[prompiece]
            valid, msg = interface.is_move_valid(modelmatch, srcx, srcy, dstx, dsty, prom_piece)
            if(valid):
                interface.do_move(modelmatch, srcx, srcy, dstx, dsty, prom_piece)
                interface.calc_move_for_immanuel(modelmatch)
        else:
            msg = RETURN_CODES['format-error']

        return HttpResponseRedirect(reverse('kate:match', args=(matchid, switch, msg)))
    else:
        return HttpResponseRedirect(reverse('kate:match', args=(matchid, switch)))


def undo_move(request, matchid, switch=0):
    context = RequestContext(request)
    modelmatch = ModelMatch.objects.get(id=matchid)

    thread = ModelMatch.get_active_thread(modelmatch)
    if(thread):
        if(thread.running):
            thread.running = False
        ModelMatch.remove_threads(modelmatch)

    interface.undo_move(modelmatch)

    return HttpResponseRedirect(reverse('kate:match', args=(modelmatch.id, switch)))


def resume(request, matchid, switch=0):
    context = RequestContext(request)
    modelmatch = ModelMatch.objects.get(id=matchid)

    thread = ModelMatch.get_active_thread(modelmatch)
    if(thread):
        if(thread.running == False):
            thread.running = True  
    else:
        interface.calc_move_for_immanuel(modelmatch)

    return HttpResponseRedirect(reverse('kate:match', args=(modelmatch.id, switch)))


def add_comment(request, matchid):
    context = RequestContext(request)
    modelmatch = get_object_or_404(ModelMatch, pk=matchid)
    if request.method == 'POST':
        newcomment = request.POST['newcomment']
        switchflag = request.POST['switchflag']        
        if(len(newcomment) > 0):
            comment = ModelComment()
            comment.match_id = modelmatch.id
            comment.text = newcomment
            comment.save()
    return HttpResponseRedirect(reverse('kate:match', args=(modelmatch.id, switchflag)))


def fetch_comments(request):
    context = RequestContext(request)
    if request.method == 'GET':
        matchid = request.GET['matchid']
        comments = ModelComment.objects.filter(match_id=matchid).order_by("created_at").reverse()[:3]
        data = ""
        for comment in reversed(comments):
            data += "<p>" + comment.text + "</p>"
        return HttpResponse(data)


def fetch_match(request):
    context = RequestContext(request)
    matchid = request.GET['matchid']
    switchflag = request.GET['switchflag']

    data = ""

    modelmatch = ModelMatch.objects.get(id=matchid)
    if(modelmatch):
        lastmove = ModelMove.objects.filter(match_id=modelmatch.id).order_by("count").last()
        if(lastmove != None):
            movesrc = Match.index_to_koord(lastmove.srcx, lastmove.srcy)
            movedst = Match.index_to_koord(lastmove.dstx, lastmove.dsty)
            data += html_board(modelmatch, int(switchflag), movesrc, movedst)

            data += "§" + html_moves(modelmatch)

            data += "§<p>Score: &nbsp; " + str(modelmatch.score) + "</p>"

        thread = ModelMatch.get_active_thread(modelmatch)
        if(thread and thread.running):
            if(len(data) > 0):
                data += "§"
            data += "<p> &nbsp; calculation is running...</p>"

    return HttpResponse(data)

