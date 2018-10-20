import datetime, time, re
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
from .engine.values import *
from .engine.match import *
from .engine.move import *
from .engine.validator import *
from .engine.helper import index_to_coord, coord_to_index
from .engine.debug import list_match_attributes
from .engine.pieces.king import cKing
from .engine.analyze_position import is_rook_on_baseline_trapped


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

    if(matchid is None):
        modelmatch = ModelMatch(white_player_name=None, black_player_name=None)
    else:
        modelmatch = get_object_or_404(ModelMatch, pk=matchid)
    match = cMatch()
    interface.map_matches(modelmatch, match, interface.MAP_DIR['model-to-engine'])
    match.status = match.evaluate_status()

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
            move = cMove()
            move.match = match
            interface.map_moves(qmove, move)
            moves.append(move)

    comments = ModelComment.objects.filter(match_id=modelmatch.id).order_by("created_at").reverse()[:5]

    urgent = False

    if(msgcode is None):
        msg = ""
        """if(match.status == STATUS['winner_white']):
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
            msg = "" """
    elif(msgcode == cValidator.RETURN_CODES['ok']):
        #urgent = False
        msg = match.RETURN_MSGS[msgcode]
    else:
        urgent = True
        msg = match.RETURN_MSGS[msgcode]

    if(match.status == match.STATUS['winner_white'] or 
       match.status == match.STATUS['winner_black'] or 
       match.status == match.STATUS['draw']):
        urgent = True

    domoveform = DoMoveForm()
    fmtboard = preformat_board(modelmatch.board, switch)
    return render(request, 'kate/match.html', { 'match': match, 'fmtboard': fmtboard, 'domoveform': domoveform, 'switch': switch, 'movesrc': movesrc, 'movedst': movedst, 'moves': moves, 'comments': comments, 'urgent': urgent, 'msg': msg } )


def do_move(request, matchid=None):
    context = RequestContext(request)
    switch = int(request.GET.get('switch', '0'))

    if(request.method == 'POST'):
        modelmatch = get_object_or_404(ModelMatch, pk=matchid)
        if(interface.is_next_color_human(modelmatch) == False):
            msgcode= cValidator.RETURN_CODES['wrong-color']
            return HttpResponseRedirect("%s?switch=%s" % (reverse('kate:match', args=(modelmatch.id,)), switch))

        form = DoMoveForm(request.POST)
        if(form.is_valid()):
            srcx, srcy = coord_to_index(form.move_src)
            dstx, dsty = coord_to_index(form.move_dst)
            prom_piece = PIECES[form.prom_piece]
            valid, msgcode = interface.is_move_valid(modelmatch, srcx, srcy, dstx, dsty, prom_piece)
            if(valid):
                interface.do_move(modelmatch, srcx, srcy, dstx, dsty, prom_piece)
                interface.calc_move_for_immanuel(modelmatch)
        else:
            msgcode= cValidator.RETURN_CODES['format-error']

        return HttpResponseRedirect("%s?switch=%s&msgcode=%s" % (reverse('kate:match', args=(modelmatch.id,)), switch, msgcode))
    else:
        return HttpResponseRedirect("%s?switch=%s" % (reverse('kate:match', args=(matchid,)), switch))


def undo_move(request, matchid=None):
    context = RequestContext(request)
    switch = int(request.GET.get('switch', '0'))
    modelmatch = get_object_or_404(ModelMatch, pk=matchid)
    interface.undo_move(modelmatch)
    return HttpResponseRedirect("%s?switch=%s" % (reverse('kate:match', args=(modelmatch.id,)), switch))


def pause(request, matchid=None):
    context = RequestContext(request)
    switch = int(request.GET.get('switch', '0'))

    modelmatch = get_object_or_404(ModelMatch, pk=matchid)
    if(modelmatch.status == cMatch.STATUS['open']):
        if(modelmatch.time_start > 0):
            elapsed_time = time.time() - modelmatch.time_start

            movecnt = ModelMove.objects.filter(match_id=modelmatch.id).count()
            if(movecnt % 2 == 0):
                modelmatch.white_elapsed_seconds += elapsed_time
            else:
                modelmatch.black_elapsed_seconds += elapsed_time

            modelmatch.time_start = 0

        modelmatch.status = cMatch.STATUS['paused']
        modelmatch.save()

    return HttpResponseRedirect("%s?switch=%s" % (reverse('kate:match', args=(modelmatch.id,)), switch))


def resume(request, matchid=None):
    context = RequestContext(request)
    switch = int(request.GET.get('switch', '0'))

    modelmatch = get_object_or_404(ModelMatch, pk=matchid)
    if(modelmatch.status == cMatch.STATUS['paused']):
        modelmatch.status = cMatch.STATUS['open']
        modelmatch.save()

    # TODO: check if calculation is already running
    flag, msgcode = interface.calc_move_for_immanuel(modelmatch)
    if(flag == False):
        return HttpResponseRedirect("%s?switch=%s&msgcode=%s" % (reverse('kate:match', args=(modelmatch.id,)), switch, msgcode))

    return HttpResponseRedirect("%s?switch=%s" % (reverse('kate:match', args=(modelmatch.id,)), switch))


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
    return HttpResponseRedirect('/kate/')


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
    match = cMatch()
    interface.map_matches(modelmatch, match, interface.MAP_DIR['model-to-engine'])
    if(match.time_start > 0):
        elapsed_time = time.time() - match.time_start
    else:
        elapsed_time = 0

    if(match.next_color() == COLORS['white']):
        match.white_player.elapsed_seconds += elapsed_time
    else:
        match.black_player.elapsed_seconds += elapsed_time

    lastmove = ModelMove.objects.filter(match_id=modelmatch.id).order_by("count").last()

    if(modelmatch and lastmove and lastmove.count > movecnt):
        data = "1" + "|" + fmttime(match.white_player.elapsed_seconds) + "|" + fmttime(match.black_player.elapsed_seconds)
    else:
        data = "0" + "|" + fmttime(match.white_player.elapsed_seconds) + "|" + fmttime(match.black_player.elapsed_seconds)

    return HttpResponse(data)


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


def dbginfo(request, matchid=None):
    context = RequestContext(request)
    switch = int(request.GET.get('switch', '0'))

    modelmatch = get_object_or_404(ModelMatch, pk=matchid)
    match = cMatch()
    interface.map_matches(modelmatch, match, interface.MAP_DIR['model-to-engine'])
    
    moves = "moves:"
    modelmoves = ModelMove.objects.filter(match_id=modelmatch.id).order_by("-count")
    idx = 0
    for modelmove in reversed(modelmoves):
        idx += 1
        move = cMove()
        move.match = match
        interface.map_moves(modelmove, move)
        if(idx == 1):
            moves += move.format_move()
        else:
            moves += "|" + move.format_move()

    attributes = list_match_attributes(match)
    
    str_dbgfunc = []
    king = cKing(match, match.board.wKg_x, match.board.wKg_y)
    str_dbgfunc.append("wKg - is_king_safe: " + str(king.is_king_safe()))
    king = cKing(match, match.board.bKg_x, match.board.bKg_y)
    str_dbgfunc.append("bKg - is_king_safe: " + str(king.is_king_safe()))
    str_dbgfunc.append("is_rook_on_baseline_trapped - white: " + str(is_rook_on_baseline_trapped(match, COLORS['white'])))
    str_dbgfunc.append("is_rook_on_baseline_trapped - black: " + str(is_rook_on_baseline_trapped(match, COLORS['black'])))

    return render(request, 'kate/dbginfo.html', { 'match': match, 'moves': moves, 'attributes': attributes, 'dbgfunc': str_dbgfunc, 'switch': switch } )


def import_match(request):
    context = RequestContext(request)

    if(request.method == 'POST'):
        form = ImportMatchForm(request.POST)
        if(form.is_valid()):
            modelmatch = ModelMatch()

            result = re.search(r"level:\s*(?P<level>\w+)", form.match_data)
            modelmatch.level = int(result.group("level"))

            result = re.search(r"begin:\s*(?P<begin>\w+-\w+-\w+\-\w+:\w+:\w+)", form.match_data)
            strdatetime = result.group("begin")
            modelmatch.begin = datetime.strptime(strdatetime, '%Y-%m-%d-%H:%M:%S')

            result = re.search(r"white_player_name:\s*(?P<white_player_name>\w+)", form.match_data)
            modelmatch.white_player.name = result.group("white_player_name")
            
            result = re.search(r"white_player_is_human:\s*(?P<white_player_is_human>\w+)", form.match_data)
            if(result.group("white_player_is_human") == "True"):
                modelmatch.white_player.is_human = True
            else:
                modelmatch.white_player.is_human = False

            result = re.search(r"white_elapsed_seconds:\s*(?P<white_elapsed_seconds>\w+)", form.match_data)
            modelmatch.white_player.elapsed.seconds = int(result.group("white_elapsed_seconds"))

            result = re.search(r"black_player_name:\s*(?P<black_player_name>\w+)", form.match_data)
            modelmatch.black_player.name = result.group("black_player_name")
            
            result = re.search(r"black_player_is_human:\s*(?P<black_player_is_human>\w+)", form.match_data)
            if(result.group("black_player_is_human") == "True"):
                modelmatch.black_player.is_human = True
            else:
                modelmatch.black_player.is_human = False

            result = re.search(r"black_elapsed_seconds:\s*(?P<black_elapsed_seconds>\w+)", form.match_data)
            modelmatch.black_player.elapsed_seconds = int(result.group("black_elapsed_seconds"))

            modelmatch.save()

            result = re.search(r"moves:\s*(?P<moves>[\w+\W\w+|]+)", form.match_data)
            strmoves = result.group("moves")
            print(strmoves)

            moves = strmoves.split("|")
            idx = 0
            for move in moves:
                idx += 1
                print("move: " + move)
                if(move == "0-0"):
                    if(idx % 2 == 1):
                        y = 0
                    else:
                        y = 7
                    srcx = 4
                    srcy = y
                    dstx = 6
                    dsty = y
                elif(move == "0-0-0"):
                    if(idx % 2 == 1):
                        y = 0
                    else:
                        y = 7
                    srcx = 4
                    srcy = y
                    dstx = 2
                    dsty = y
                else:
                    srcx, srcy = coord_to_index(move[0:2])
                    dstx, dsty = coord_to_index(move[3:5])

                if(len(move) == 9):
                    prom_piece = PIECES[move[6:9]]
                else:
                    prom_piece = PIECES['blk']
                interface.do_move(modelmatch, srcx, srcy, dstx, dsty, prom_piece)

            return HttpResponseRedirect(reverse('kate:match', args=(modelmatch.id,)))
    else:
        form = ImportMatchForm()
        return render(request, 'kate/import.html', { 'form': form } )

def clone(request, matchid=None):
    context = RequestContext(request)

    modelmatch = get_object_or_404(ModelMatch, pk=matchid)
    modelmatch.id = None
    modelmatch.begin = datetime.now()
    modelmatch.save()
    
    modelmoves = ModelMove.objects.filter(match_id=matchid)
    for modelmove in modelmoves:
        modelmove.match_id = modelmatch.id
        modelmove.id = None
        modelmove.save()

    return HttpResponseRedirect(reverse('kate:match', args=(modelmatch.id,)))
