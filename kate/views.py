from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from .forms import DoMoveForm
from .models import Match as ModelMatch, Move as ModelMove, Comment as ModelComment
from .modules import interface
from .utils import *
from .engine.match import *
from .engine.move import *
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
    if(thread):
        running = "calculation is running..."
    else:
        running = ""

    form = DoMoveForm()
    form.switch = switch

    return render(request, 'kate/match.html', { 'match': modelmatch, 'board': fmtboard, 'form': form, 'switch': switch, 'movesrc': movesrc, 'movedst': movedst, 'moves': moves, 'comments': comments, 'msg': fmtmsg, 'range': rangeobj, 'running': running } )


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


def do_move(request, matchid, switch=0):
    context = RequestContext(request)
    if(request.method == 'POST'):
        modelmatch = get_object_or_404(ModelMatch, pk=matchid)
        if(not interface.next_color_human(modelmatch)):
            msg = RETURN_CODES['wrong-color']
        elif(interface.game_status(modelmatch) != STATUS['open']):
            status = interface.game_status(modelmatch)            
            if(status == STATUS['winner_white']):
                msg = RETURN_CODES['winner_white']    
            elif(status == STATUS['winner_black']):
                msg = RETURN_CODES['winner_black']
            else:
                msg = RETURN_CODES['draw']
        else:
            form = DoMoveForm(request.POST)
            if(form.is_valid()):
                srcx,srcy = Match.koord_to_index(form.cleaned_data['move_src'])
                dstx,dsty = Match.koord_to_index(form.cleaned_data['move_dst'])
                prom_piece = PIECES[form.cleaned_data['prom_piece']]
                valid, msg = interface.is_move_valid(modelmatch, srcx, srcy, dstx, dsty, prom_piece)
                if(valid):
                    interface.do_move(modelmatch, srcx, srcy, dstx, dsty, prom_piece)
                    interface.calc_move_for_immanuel(modelmatch)
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
            interface.calc_move_for_immanuel(modelmatch)
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

