from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from .forms import *
from .models import Match as ModelMatch, Move as ModelMove, Comment as ModelComment
from .modules import interface
from .engine.match import *
from .engine.move import *
from .engine.helper import index_to_coord, coord_to_index
from .engine.rules import RETURN_CODES, RETURN_MSGS, STATUS



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
        if(modelmatch is None):
            return HttpResponseRedirect(reverse('kate:index'))

    lastmove = ModelMove.objects.filter(match_id=modelmatch.id).order_by("count").last()
    if(lastmove):
        movesrc = index_to_coord(lastmove.srcx, lastmove.srcy)
        movedst = index_to_coord(lastmove.dstx, lastmove.dsty)
    else:
        movesrc = ''
        movedst = ''

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
        status = interface.game_status(modelmatch)
        if(status != STATUS['open']):
            if(status == STATUS['winner_white']):
                msg = RETURN_CODES['winner_white']
            elif(status == STATUS['winner_black']):
                msg = RETURN_CODES['winner_black']
            else:
                msg = RETURN_CODES['draw']

            fmtmsg = "<p class='error'>" + RETURN_MSGS[msg] + "</p>"
        else:
            fmtmsg = "<p class='ok'></p>"
    elif(int(msg) == RETURN_CODES['ok']):
        fmtmsg = "<p class='ok'>" + RETURN_MSGS[int(msg)] + "</p>"
    else:
        fmtmsg = "<p class='error'>" + RETURN_MSGS[int(msg)] + "</p>"

    thread = ModelMatch.get_active_thread(modelmatch)
    if(thread):
        running = "calculation is running..."
    else:
        running = ""

    form = DoMoveForm()

    return render(request, 'kate/match.html', { 'match': modelmatch, 'form': form, 'switch': switch, 'movesrc': movesrc, 'movedst': movedst, 'moves': moves, 'comments': comments, 'msg': fmtmsg, 'running': running } )


def settings(request, matchid=None, switch=0):
    context = RequestContext(request)

    if(matchid == None):
        modelmatch = ModelMatch()
    else:
        modelmatch = get_object_or_404(ModelMatch, pk=matchid)

    if(request.method == 'POST' and modelmatch):
        form = MatchForm(request.POST)
        if(form.is_valid()):
            modelmatch.white_player = form.white_player
            modelmatch.white_player_human = form.white_player_human
            modelmatch.black_player = form.black_player
            modelmatch.black_player_human = form.black_player_human
            modelmatch.level = form.level
            modelmatch.save()
            
            thread = ModelMatch.get_active_thread(modelmatch)
            if(thread is None):
                interface.calc_move_for_immanuel(modelmatch)

            return HttpResponseRedirect(reverse('kate:match', args=(modelmatch.id, switch)))
        else:
            return render(request, 'kate/settings.html', { 'form': form, 'matchid': matchid, 'switch': switch } )
    else:
        if(matchid == None):
            form = MatchForm()
            return render(request, 'kate/settings.html', { 'form': form } )
        else:
            form = MatchForm(initial={
                'white_player': modelmatch.white_player, 
                'white_player_human': modelmatch.white_player_human, 
                'black_player': modelmatch.black_player, 
                'black_player_human': modelmatch.black_player_human, 
                'level': modelmatch.level })
            return render(request, 'kate/settings.html', { 'form': form, 'matchid': matchid, 'switch': switch } )


def delete(request, matchid):
    ModelMatch.objects.filter(id=matchid).delete()
    return index(request)


def do_move(request, matchid, switch=0):
    context = RequestContext(request)
    if(request.method == 'POST'):
        modelmatch = get_object_or_404(ModelMatch, pk=matchid)
        if(not modelmatch):
            return HttpResponseRedirect(reverse('kate:index', args=(switch)))
        form = DoMoveForm(request.POST)
        if(form.is_valid()):
            srcx,srcy = coord_to_index(form.move_src)
            dstx,dsty = coord_to_index(form.move_dst)
            prom_piece = PIECES[form.prom_piece]
            valid, msg = interface.is_move_valid(modelmatch, srcx, srcy, dstx, dsty, prom_piece)
            if(valid):
                interface.do_move(modelmatch, srcx, srcy, dstx, dsty, prom_piece)
                interface.calc_move_for_immanuel(modelmatch)
                status = interface.game_status(modelmatch)
                if(status != STATUS['open']):
                    if(status == STATUS['winner_white']):
                        msg = RETURN_CODES['winner_white']    
                    elif(status == STATUS['winner_black']):
                        msg = RETURN_CODES['winner_black']
                    else:
                        msg = RETURN_CODES['draw']
        else:
            msg= RETURN_CODES['format-error']

        return HttpResponseRedirect(reverse('kate:match', args=(matchid, switch, msg)))
    else:
        return HttpResponseRedirect(reverse('kate:match', args=(matchid, switch)))


def undo_move(request, matchid, switch=0):
    context = RequestContext(request)
    modelmatch = ModelMatch.objects.get(id=matchid)
    if(modelmatch):
        thread = ModelMatch.get_active_thread(modelmatch)
        if(thread):
            ModelMatch.deactivate_threads(modelmatch)
            ModelMatch.remove_outdated_threads()
        interface.undo_move(modelmatch)
        return HttpResponseRedirect(reverse('kate:match', args=(modelmatch.id, switch)))


def resume(request, matchid, switch=0):
    context = RequestContext(request)
    modelmatch = ModelMatch.objects.get(id=matchid)
    if(modelmatch):
        thread = ModelMatch.get_active_thread(modelmatch)
        if(thread is None):
            flag, msg = interface.calc_move_for_immanuel(modelmatch)
            print(str(msg))
            if(flag == False):
                return HttpResponseRedirect(reverse('kate:match', args=(modelmatch.id, switch, msg)))

        return HttpResponseRedirect(reverse('kate:match', args=(modelmatch.id, switch)))


def add_comment(request, matchid):
    context = RequestContext(request)
    modelmatch = get_object_or_404(ModelMatch, pk=matchid)
    if(request.method == 'POST' and modelmatch):
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
    if(request.method == 'GET'):
        matchid = request.GET['matchid']
        comments = ModelComment.objects.filter(match_id=matchid).order_by("created_at").reverse()[:3]
        data = ""
        for comment in reversed(comments):
            data += "<p>" + comment.text + "</p>"
        return HttpResponse(data)


def fetch_match(request):
    context = RequestContext(request)
    matchid = request.GET['matchid']
    movecnt = request.GET['movecnt']

    modelmatch = ModelMatch.objects.get(id=matchid)
    if(modelmatch):
        if(modelmatch.count != int(movecnt)):
            data = "1"
        else:
            data = ""
        return HttpResponse(data)

