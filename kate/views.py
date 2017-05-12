from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from kate.models import Match as ModelMatch, Move as ModelMove, Comment as ModelComment
from kate.engine.match import *
from kate.engine.move import *
from kate.engine.matchmove import *
from kate.modules import interface
from kate.engine import rules
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
            map_moves(qmove, move, MAP_DIR['model-to-engine'])
            moves.append(move)

    comments = ModelComment.objects.filter(match_id=modelmatch.id).order_by("created_at").reverse()[:3]
    
    if(msg == None):
        fmtmsg = "<p class='ok'></p>"
    elif(int(msg) == 0):
        fmtmsg = "<p class='ok'>" + rules.RETURN_MSGS[int(msg)] + "</p>"
    else:
        fmtmsg = "<p class='error'>" + rules.RETURN_MSGS[int(msg)] + "</p>"

    if(int(switch) == 0):
        rangeobj = range(8)
    else:
        rangeobj = range(7, -1, -1)

    thread = Match.get_active_thread(modelmatch)
    if(thread and thread.running):
        if(thread.searchcnt and thread.search):
            cnt = thread.searchcnt
            gmove = thread.search
            search = "current search: " + str(cnt) + ". " + Match.index_to_koord(gmove.srcx, gmove.srcy) + "-" + Match.index_to_koord(gmove.dstx, gmove.dsty)
        else:
            search = "current search:"

        if(thread.candidates[0]):
            candidates = "candidates: "
            for cand in thread.candidates[:3]:
                if(cand):
                    candidates += "[" + Match.index_to_koord(cand.srcx, cand.srcy) + "-" + Match.index_to_koord(cand.dstx, cand.dsty) + "]"
        else:
            candidates = "candidates:"
            
        if(thread.debuginfo):
            debuginfo = thread.debuginfo
        else:
            debuginfo = ""
    else:
        search = "current search:"
        candidates = "candidates:"
        debuginfo = ""

    return render(request, 'kate/match.html', { 'match': modelmatch, 'board': fmtboard, 'switch': switch, 'movesrc': movesrc, 'movedst': movedst, 'moves': moves, 'comments': comments, 'msg': fmtmsg, 'range': rangeobj, 'search': search, 'candidates': candidates, 'debuginfo': debuginfo } )


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

        """match = map_matches(modelmatch, MAP_DIR['model-to-engine'])
        status = rules.game_status(match)
        if(status != STATUS['open']):
            if(status == STATUS['draw']):
                msg = rules.RETURN_CODES['draw']
            elif(status == STATUS['winner_white']):
                msg = rules.RETURN_CODES['winner_white']
            elif(status == STATUS['winner_black']):
                msg = rules.RETURN_CODES['winner_black']
            else:
                msg = rules.RETURN_CODES['match-cancelled']
            return HttpResponseRedirect(reverse('kate:match', args=(matchid, switch, msg)))

        if(match.next_color_human() == False):
            msg= rules.RETURN_CODES['wrong-color']
            return HttpResponseRedirect(reverse('kate:match', args=(matchid, switch, msg)))"""

        movesrc = request.POST['move_src']
        movedst = request.POST['move_dst']
        prompiece = request.POST['prom_piece']        
        if(len(movesrc) > 0 and len(movedst) > 0 and len(prompiece) > 0):
            srcx,srcy = Match.koord_to_index(movesrc)
            dstx,dsty = Match.koord_to_index(movedst)
            prom_piece = PIECES[prompiece]
            match = Match()
            map_matches(modelmatch, match, MAP_DIR['model-to-engine'])
            flag, msg = rules.is_move_valid(match, srcx, srcy, dstx, dsty, prom_piece)
            if(flag == True):
                interface.do_move(modelmatch, srcx, srcy, dstx, dsty, prom_piece)
                interface.calc_move_for_immanuel(modelmatch)
        else:
            msg = rules.RETURN_CODES['format-error']

        return HttpResponseRedirect(reverse('kate:match', args=(matchid, switch, msg)))
    else:
        return HttpResponseRedirect(reverse('kate:match', args=(matchid, switch)))


def force_move(request, matchid, switch=0):
    context = RequestContext(request)
    modelmatch = ModelMatch.objects.get(id=matchid)

    thread = Match.get_active_thread(modelmatch)
    if(thread and thread.running and thread.candidates[0]):
        thread.running = False
        gmove = thread.candidates[0]
        Match.remove_threads(modelmatch)
        msg = rules.RETURN_CODES['ok']
        interface.do_move(modelmatch, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
        return HttpResponseRedirect(reverse('kate:match', args=(matchid, switch, msg)))
    else:
        return HttpResponseRedirect(reverse('kate:match', args=(matchid, switch)))


def undo_move(request, matchid, switch=0):
    context = RequestContext(request)
    modelmatch = ModelMatch.objects.get(id=matchid)

    thread = Match.get_active_thread(modelmatch)
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
            ModelMatch.remove_threads(modelmatch)
            calc_move_for_immanuel(modelmatch)
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
    movecnt = request.GET['movecnt']
    switchflag = request.GET['switchflag']
    modelmatch = ModelMatch.objects.get(id=matchid)
    if(modelmatch == None):
        data = "§§§§"
    else:
        lastmove = ModelMove.objects.filter(match_id=modelmatch.id).order_by("count").last()
        if(lastmove != None):
            movesrc = Match.index_to_koord(lastmove.srcx, lastmove.srcy)
            movedst = Match.index_to_koord(lastmove.dstx, lastmove.dsty)

        if(int(movecnt) == modelmatch.count):
            data = "§§"
        else:
            data = html_board(modelmatch, int(switchflag), movesrc, movedst)
            data += "§" + html_moves(modelmatch)
            data += "§<p>Score: &nbsp;" + str(modelmatch.score) + "</p>"

        thread = Match.get_active_thread(modelmatch)
        if(thread and thread.running):
            if(thread.searchcnt and thread.search):
                cnt = thread.searchcnt
                gmove = thread.search
                data += "§<p>current search: " + str(cnt) + ". "
                data += Match.index_to_koord(gmove.srcx, gmove.srcy) + "-" + Match.index_to_koord(gmove.dstx, gmove.dsty)
                data += "</p>"
            else:
                data += "§"

            if(thread.candidates[0]):
                data += "§<p>candidates: "
                for cand in thread.candidates[:3]:
                    if(cand):
                        data += "[" + Match.index_to_koord(cand.srcx, cand.srcy) + "-" + Match.index_to_koord(cand.dstx, cand.dsty) + "]"
                data += "</p>"
            else:
                data += "§"
        else:
            data += "§§"

    return HttpResponse(data)

