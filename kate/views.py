import time
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.utils import timezone
from .utils import *
from .forms import *
from .models import Match as ModelMatch, Move as ModelMove, Comment as ModelComment
from .modules import interface
from .engine.match import *
from .engine.move import *
from .engine.calc import SearchMsgs
from .engine.helper import index_to_coord, coord_to_index
from .engine.rules import RETURN_CODES, RETURN_MSGS, STATUS
from .engine.analyze_position import score_position, is_stormy


def index(request):
    context = RequestContext(request)
    modelmatches = ModelMatch.objects.order_by("begin").reverse()[:10]

    return render(request, 'kate/index.html', { 'matches': modelmatches } )


def match(request, matchid=None):
    context = RequestContext(request)

    switch = int(request.GET.get('switch', '0'))

    msgcode = request.GET.get('msgcode', None)
    if(msgcode):
        msgcode = int(msgcode)

    currentsearch = ""

    if(matchid is None):
        modelmatch = ModelMatch(white_player_name=None, black_player_name=None)
    else:
        try:
            modelmatch = ModelMatch.objects.get(id=matchid)
        except ObjectDoesNotExist: #ModelMatch.DoesNotExist:
            return HttpResponseRedirect('/kate/')

        job = get_active_job(modelmatch.id)
        if(job):
            if(job.meta['terminate'] == False):
                currsearch = job.meta['currentsearch']
                if(currsearch):
                    for gmove in currsearch:
                        currentsearch += fmtmove(gmove)

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

    if(msgcode is None):
        if(match.status == STATUS['winner_white']):
            urgent = True
            msg = RETURN_MSGS[RETURN_CODES['winner_white']]
        elif(match.status == STATUS['winner_black']):
            urgent = True
            msg = RETURN_MSGS[RETURN_CODES['winner_black']]
        elif(match.status == STATUS['draw']):
            urgent = True
            msg = RETURN_MSGS[RETURN_CODES['draw']]
        else:
            urgent = False
            msg = ""
    elif(msgcode == RETURN_CODES['ok']):
        urgent = False
        msg = RETURN_MSGS[msgcode]
    else:
        urgent = True
        msg = RETURN_MSGS[msgcode]

    #job = get_active_job(modelmatch.id)
    #if(job):
    #    msg += " calculation is running..."

    form = DoMoveForm()

    fmtboard = preformat_board(modelmatch.board, switch)

    return render(request, 'kate/match.html', { 'match': match, 'fmtboard': fmtboard, 'form': form, 'switch': switch, 'movesrc': movesrc, 'movedst': movedst, 'moves': moves, 'comments': comments, 'urgent': urgent, 'msg': msg, "currentsearch": currentsearch } )


def settings(request, matchid=None):
    context = RequestContext(request)

    switch = int(request.GET.get('switch', '0'))

    if(matchid is None):
        modelmatch = ModelMatch()
        create = True
    else:
        modelmatch = get_object_or_404(ModelMatch, pk=matchid)
        create = False

    if(request.method == 'POST'):
        form = MatchForm(request.POST)
        if(form.is_valid()):
            modelmatch.white_player_name = form.white_player_name
            modelmatch.white_player_is_human = form.white_player_is_human
            modelmatch.black_player_name = form.black_player_name
            modelmatch.black_player_is_human = form.black_player_is_human
            modelmatch.level = form.level
            modelmatch.save()
            
            if(create):
                interface.calc_move_for_immanuel(modelmatch)

            return HttpResponseRedirect("%s?switch=%s" % (reverse('kate:match', args=(modelmatch.id,)), switch))
        else:
            return render(request, 'kate/settings.html', { 'form': form, 'matchid': modelmatch.id, 'switch': switch } )
    else:
        if(matchid is None):
            form = MatchForm()
            return render(request, 'kate/settings.html', { 'form': form } )
        else:
            form = MatchForm(initial={
                'level': modelmatch.level,
                'white_player_name': modelmatch.white_player_name, 
                'white_player_is_human': modelmatch.white_player_is_human, 
                'black_player_name': modelmatch.black_player_name, 
                'black_player_is_human': modelmatch.black_player_is_human })

            return render(request, 'kate/settings.html', { 'form': form, 'matchid': modelmatch.id, 'switch': switch } )


def delete(request, matchid=None):
    modelmatch = get_object_or_404(ModelMatch, pk=matchid)

    ModelMatch.objects.filter(id=modelmatch.id).delete()

    return HttpResponseRedirect('/kate')


def do_move(request, matchid=None):
    context = RequestContext(request)

    switch = int(request.GET.get('switch', '0'))

    if(request.method == 'POST'):
        modelmatch = get_object_or_404(ModelMatch, pk=matchid)
        if(interface.is_next_color_human(modelmatch) == False):
            msgcode = RETURN_CODES['wrong-color']
        else:
            form = DoMoveForm(request.POST)
            if(form.is_valid()):
                srcx,srcy = coord_to_index(form.move_src)
                dstx,dsty = coord_to_index(form.move_dst)
                prom_piece = PIECES[form.prom_piece]
                valid, msgcode = interface.is_move_valid(modelmatch, srcx, srcy, dstx, dsty, prom_piece)
                if(valid):
                    interface.do_move(modelmatch, srcx, srcy, dstx, dsty, prom_piece)

                    interface.calc_move_for_immanuel(modelmatch)
            else:
                msgcode= RETURN_CODES['format-error']

        return HttpResponseRedirect("%s?switch=%s&msgcode=%s" % (reverse('kate:match', args=(modelmatch.id,)), switch, msgcode))
    else:
        return HttpResponseRedirect("%s?switch=%s" % (reverse('kate:match', args=(matchid,)), switch))


def undo_move(request, matchid=None):
    context = RequestContext(request)

    switch = int(request.GET.get('switch', '0'))

    modelmatch = get_object_or_404(ModelMatch, pk=matchid)

    job = get_active_job(modelmatch.id)
    if(job):
        job.meta['isalive'] = False
        job.save_meta()

    interface.undo_move(modelmatch)

    return HttpResponseRedirect("%s?switch=%s" % (reverse('kate:match', args=(modelmatch.id,)), switch))


def force_move(request, matchid=None):
    context = RequestContext(request)

    switch = int(request.GET.get('switch', '0'))

    modelmatch = get_object_or_404(ModelMatch, pk=matchid)

    job = get_active_job(modelmatch.id)
    if(job):
        job.meta['terminate'] = True
        job.save_meta()

    return HttpResponseRedirect("%s?switch=%s" % (reverse('kate:match', args=(modelmatch.id,)), switch))


def pause(request, matchid=None):
    context = RequestContext(request)

    switch = int(request.GET.get('switch', '0'))

    modelmatch = get_object_or_404(ModelMatch, pk=matchid)

    if(modelmatch.status == STATUS['open']):
        if(modelmatch.time_start > 0):
            elapsed_time = time.time() - modelmatch.time_start

            movecnt = ModelMove.objects.filter(match_id=modelmatch.id).count()
            if(movecnt % 2 == 0):
                modelmatch.white_elapsed_seconds += elapsed_time
            else:
                modelmatch.black_elapsed_seconds += elapsed_time

            modelmatch.time_start = 0

        modelmatch.status = STATUS['paused']
        modelmatch.save()

    return HttpResponseRedirect("%s?switch=%s" % (reverse('kate:match', args=(modelmatch.id,)), switch))


def resume(request, matchid=None):
    context = RequestContext(request)

    switch = int(request.GET.get('switch', '0'))

    modelmatch = get_object_or_404(ModelMatch, pk=matchid)
    if(modelmatch.status == STATUS['paused']):
        modelmatch.status = STATUS['open']
        modelmatch.save()

    job = get_active_job(modelmatch.id)
    if(job is None):
        flag, msgcode = interface.calc_move_for_immanuel(modelmatch)
        if(flag == False):
            return HttpResponseRedirect("%s?switch=%s&msgcode=%s" % (reverse('kate:match', args=(modelmatch.id,)), switch, msgcode))

    return HttpResponseRedirect("%s?switch=%s" % (reverse('kate:match', args=(modelmatch.id,)), switch))


def add_comment(request, matchid):
    context = RequestContext(request)

    switch = int(request.GET.get('switch', '0'))

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
        matchid = request.GET.get('matchid', None)
        if(matchid):
            matchid = int(matchid)
            comments = ModelComment.objects.filter(match_id=matchid).order_by("created_at").reverse()[:3]
            data = ""
            for comment in reversed(comments):
                data += "<p>" + comment.text + "</p>"

            return HttpResponse(data)


def fetch_match(request):
    context = RequestContext(request)

    matchid = request.GET.get('matchid', None)
    if(matchid):
        matchid = int(matchid)
    else:
        return

    movecnt = request.GET.get('movecnt', None)
    if(movecnt):
        movecnt = int(movecnt)
    else:
        return

    modelmatch = ModelMatch.objects.get(id=matchid)
    match = Match()
    interface.map_matches(modelmatch, match, interface.MAP_DIR['model-to-engine'])
    if(match.time_start > 0):
        elapsed_time = time.time() - match.time_start
    else:
        elapsed_time = 0

    if(match.next_color() == COLORS['white']):
        match.white_elapsed_seconds += elapsed_time
    else:
        match.black_elapsed_seconds += elapsed_time

    currentsearch = ""

    job = get_active_job(modelmatch.id)
    if(job):
        if(job.meta['terminate'] == False):
            currsearch = job.meta['currentsearch']
            if(currsearch):
                for gmove in currsearch:
                    currentsearch += fmtmove(gmove)

    lastmove = ModelMove.objects.filter(match_id=modelmatch.id).order_by("count").last()

    if(modelmatch and lastmove and lastmove.count > movecnt):
        data = "1" + "|" + fmttime(match.white_elapsed_seconds) + "|" + fmttime(match.black_elapsed_seconds) + "|" + currentsearch
    else:
        data = "0" + "|" + fmttime(match.white_elapsed_seconds) + "|" + fmttime(match.black_elapsed_seconds) + "|" + currentsearch

    return HttpResponse(data)

