import re
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.utils import timezone
from .forms import *
from .models import Match as ModelMatch, Move as ModelMove, Comment as ModelComment
from .modules import interface
from .engine.match import *
from .engine.move import *
from .engine import matchmove
from .engine.helper import index_to_coord, coord_to_index
from .engine.debug import str_attributes
from .engine.rules import RETURN_CODES, RETURN_MSGS, STATUS
from .modules.interface import read_searchmoves


def index(request):
    context = RequestContext(request)
    modelmatches = ModelMatch.objects.order_by("begin").reverse()[:10]

    return render(request, 'kate/index.html', { 'matches': modelmatches } )


def match(request, matchid=None):
    context = RequestContext(request)
    switch = request.GET.get('switch', '0')
    msg = request.GET.get('msg', None)
    debug = request.GET.get('debug', "false")

    if(matchid == None):
        modelmatch = ModelMatch(white_player_name=None, black_player_name=None)
    else:
        try:
            modelmatch = ModelMatch.objects.get(id=matchid)
        except ObjectDoesNotExist: #ModelMatch.DoesNotExist:
            return HttpResponseRedirect('/kate')

    match = Match()
    interface.map_matches(modelmatch, match, interface.MAP_DIR['model-to-engine'])

    lastmove = ModelMove.objects.filter(match_id=modelmatch.id).order_by("count").last()
    if(lastmove):
        movesrc = index_to_coord(lastmove.srcx, lastmove.srcy)
        movedst = index_to_coord(lastmove.dstx, lastmove.dsty)
    else:
        movesrc = ''
        movedst = ''

    moves = []
    currmove = ModelMove.objects.filter(match_id=modelmatch.id).order_by("count").last()
    if(currmove):
        if(currmove.count % 2 == 0):
            limit = 22
        else:
            limit = 21
        qmoves = ModelMove.objects.filter(match_id=modelmatch.id).order_by("-count")[:limit]
        for qmove in reversed(qmoves):
            move = Move()
            interface.map_moves(qmove, move, interface.MAP_DIR['model-to-engine'])
            moves.append(move)

    comments = ModelComment.objects.filter(match_id=modelmatch.id).order_by("created_at").reverse()[:5]
    
    if(msg == None):
        #status = interface.status(modelmatch)
        if(match.status != STATUS['open']):
            if(match.status == STATUS['winner_white']):
                msg = RETURN_CODES['winner_white']
            elif(match.status == STATUS['winner_black']):
                msg = RETURN_CODES['winner_black']
            else:
                msg = RETURN_CODES['draw']

            fmtmsg = "<span class='error'>" + RETURN_MSGS[msg] + "</span>"
        else:
            fmtmsg = "<span class='ok'>&nbsp;</span>"
    elif(int(msg) == RETURN_CODES['ok']):
        fmtmsg = "<span class='ok'>" + RETURN_MSGS[int(msg)] + "</span>"
    else:
        fmtmsg = "<span class='error'>" + RETURN_MSGS[int(msg)] + "</span>"

    thread = ModelMatch.get_active_thread(modelmatch)
    if(thread):
        running = "calculation is running..."
    else:
        running = ""

    form = DoMoveForm()

    if(debug == "true"):
        importform = ImportMatchForm()
        debug_data = str_attributes(match, "<br>")
    else:
        debug_data = ""

    return render(request, 'kate/match.html', { 'match': match, 'board': modelmatch.board, 'form': form, 'switch': switch, 'movesrc': movesrc, 'movedst': movedst, 'moves': moves, 'comments': comments, 'msg': fmtmsg, 'running': running, 'debug': debug, 'debug_data': debug_data } )


def settings(request, matchid=None):
    context = RequestContext(request)
    switch = request.GET.get('switch', '0')
    debug = request.GET.get('debug', "false")

    if(matchid == None):
        modelmatch = ModelMatch()
        create = True
    else:
        modelmatch = get_object_or_404(ModelMatch, pk=matchid)
        create = False

    if(request.method == 'POST'):
        form = MatchForm(request.POST)
        if(form.is_valid()):
            modelmatch.white_player_name = form.white_player_name
            modelmatch.is_white_player_human = form.is_white_player_human
            modelmatch.black_player_name = form.black_player_name
            modelmatch.is_black_player_human = form.is_black_player_human
            modelmatch.level = form.level
            modelmatch.save()
            
            if(create):
                interface.calc_move_for_immanuel(modelmatch)

            return HttpResponseRedirect("%s?switch=%s" % (reverse('kate:match', args=(modelmatch.id,)), switch))
        else:
            return render(request, 'kate/settings.html', { 'form': form, 'matchid': matchid, 'switch': switch } )
    else:
        if(matchid == None):
            form = MatchForm()
            return render(request, 'kate/settings.html', { 'form': form } )
        else:
            form = MatchForm(initial={
                'level': modelmatch.level,
                'white_player_name': modelmatch.white_player_name, 
                'is_white_player_human': modelmatch.is_white_player_human, 
                'black_player_name': modelmatch.black_player_name, 
                'is_black_player_human': modelmatch.is_black_player_human })

            return render(request, 'kate/settings.html', { 'form': form, 'matchid': matchid, 'switch': switch } )


def delete(request, matchid=None):
    modelmatch = get_object_or_404(ModelMatch, pk=matchid)
    ModelMatch.objects.filter(id=modelmatch.id).delete()

    return HttpResponseRedirect('/kate')


def do_move(request, matchid=None):
    context = RequestContext(request)
    switch = request.GET.get('switch', '0')

    if(request.method == 'POST'):
        modelmatch = get_object_or_404(ModelMatch, pk=matchid)
        if(interface.is_next_color_human(modelmatch) == False):
            msg = RETURN_CODES['wrong-color']
        else:
            form = DoMoveForm(request.POST)
            if(form.is_valid()):
                srcx,srcy = coord_to_index(form.move_src)
                dstx,dsty = coord_to_index(form.move_dst)
                prom_piece = PIECES[form.prom_piece]
                valid, msg = interface.is_move_valid(modelmatch, srcx, srcy, dstx, dsty, prom_piece)
                if(valid):
                    interface.do_move(modelmatch, srcx, srcy, dstx, dsty, prom_piece)
                    interface.calc_move_for_immanuel(modelmatch)
                    status = interface.status(modelmatch)
                    if(status != STATUS['open']):
                        if(status == STATUS['winner_white']):
                            msg = RETURN_CODES['winner_white']    
                        elif(status == STATUS['winner_black']):
                            msg = RETURN_CODES['winner_black']
                        else:
                            msg = RETURN_CODES['draw']
            else:
                msg= RETURN_CODES['format-error']

        return HttpResponseRedirect("%s?switch=%s&msg=%s" % (reverse('kate:match', args=(matchid,)), switch, msg))
    else:
        return HttpResponseRedirect("%s?switch=%s" % (reverse('kate:match', args=(matchid,)), switch))


def undo_move(request, matchid=None):
    context = RequestContext(request)
    switch = request.GET.get('switch', '0')

    modelmatch = get_object_or_404(ModelMatch, pk=matchid)
    thread = ModelMatch.get_active_thread(modelmatch)
    if(thread):
        ModelMatch.deactivate_threads(modelmatch)
        ModelMatch.remove_outdated_threads()

    interface.undo_move(modelmatch)
    return HttpResponseRedirect("%s?switch=%s" % (reverse('kate:match', args=(modelmatch.id,)), switch))


def resume(request, matchid=None):
    context = RequestContext(request)
    switch = request.GET.get('switch', '0')

    modelmatch = get_object_or_404(ModelMatch, pk=matchid)
    thread = ModelMatch.get_active_thread(modelmatch)
    if(thread is None):
        flag, msg = interface.calc_move_for_immanuel(modelmatch)
        if(flag == False):
            return HttpResponseRedirect("%s?switch=%s&msg=%s" % (reverse('kate:match', args=(modelmatch.id,)), switch, msg))

    return HttpResponseRedirect("%s?switch=%s" % (reverse('kate:match', args=(modelmatch.id,)), switch))


def add_comment(request, matchid):
    context = RequestContext(request)
    switch = request.GET.get('switch', '0')

    modelmatch = get_object_or_404(ModelMatch, pk=matchid)
    if(request.method == 'POST'):
        newcomment = request.POST['newcomment']
        if(len(newcomment) > 0):
            comment = ModelComment()
            comment.match_id = modelmatch.id
            comment.text = newcomment
            comment.save()

        return HttpResponseRedirect("%s?switch=%s" % (reverse('kate:match', args=(modelmatch.id,)), switch))


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
    lastmove = ModelMove.objects.filter(match_id=modelmatch.id).order_by("count").last()
    if(modelmatch and lastmove and lastmove.count > int(movecnt)):
        data = "1"
    else:
        data = ""

    return HttpResponse(data)

