from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from kate.models import Match, Move, Comment
from kate.modules import values, rules, calc


def calc_move_for_immanuel(match):
    if(rules.game_status(match) == Match.STATUS['open'] and match.next_color_human() == False):
        calc.thread_do_move(match)


def index(request):
    context = RequestContext(request)
    matches = Match.objects.order_by("begin").reverse()[:10]
    return render(request, 'kate/index.html', { 'matches': matches } )


def match(request, matchid=None, switch=0, markmove=0):
    context = RequestContext(request)
    if matchid == None:
        match = Match(white_player=None, black_player=None)
        match.setboardbase()
    else:
        match = Match.objects.get(id=matchid)
    movesrc = ''
    movedst = ''
    if(int(markmove) == 1):
        lastmove = Move.objects.filter(match_id=match.id).order_by("count").last()
        if(lastmove != None):
            movesrc = values.index_to_koord(lastmove.srcx, lastmove.srcy)
            movedst = values.index_to_koord(lastmove.dstx, lastmove.dsty)
    fmtboard = match.fill_fmtboard(int(switch))
    fmtmoves = Move.fill_fmtmoves(match)
    comments = Comment.objects.filter(match_id=match.id).order_by("created_at").reverse()[:5]
    fmtmsg = "<p class='ok'></p>"
    if(int(switch) == 0):
        rangeobj = range(8)
    else:
        rangeobj = range(7, -1, -1)
        
    calc_move_for_immanuel(match)

    return render(request, 'kate/match.html', { 'match': match, 'board': fmtboard, 'switch': switch, 'movesrc': movesrc, 'movedst': movedst, 'fmtmoves': fmtmoves, 'comments': comments, 'msg': fmtmsg, 'range': rangeobj } )


def new(request):
    context = RequestContext(request)
    return render(request, 'kate/new.html', { 'white_player': "", 'white_player_human': True, 'black_player': "", 'black_player_human': True } )


def create(request):
    context = RequestContext(request)
    if request.method == 'POST':
        match = Match()
        match.white_player = request.POST['white_player']
        human = request.POST.getlist('white_player_human')
        if(len(human) == 1):
            match.white_player_human = True
        else:
            match.white_player_human = False
        match.black_player = request.POST['black_player']
        human = request.POST.getlist('black_player_human')
        if(len(human) == 1):
            match.black_player_human = True
        else:
            match.black_player_human = False
        levellist = request.POST.getlist('level')
        match.level = Match.LEVEL[levellist[0]]
        if(len(match.white_player) > 0 and len(match.black_player) > 0):
            match.setboardbase()
            match.immanuels_thread_id = None
            match.save()
            return HttpResponseRedirect(reverse('kate:match', args=(match.id,)))
    return render(request, 'kate/new.html', { 'white_player': match.white_player, 'white_player_human': match.white_player_human, 'black_player': match.black_player, 'black_player_human': match.black_player_human } )


def edit(request, matchid):
    context = RequestContext(request)
    match = get_object_or_404(Match, pk=matchid)
    return render(request, 'kate/edit.html', { 'match': match } )


def update(request, matchid):
    context = RequestContext(request)
    match = get_object_or_404(Match, pk=matchid)
    if request.method == 'POST':        
        match.white_player = request.POST['white_player']
        human = request.POST.getlist('white_player_human')
        if(len(human) == 1):
            match.white_player_human = True
        else:
            match.white_player_human = False
        match.black_player = request.POST['black_player']
        human = request.POST.getlist('black_player_human')
        if(len(human) == 1):
            match.black_player_human = True
        else:
            match.black_player_human = False
        levellist = request.POST.getlist('level')
        match.level = Match.LEVEL[levellist[0]]
        if(len(match.white_player) > 0 and len(match.black_player) > 0):
            match.save()
            return HttpResponseRedirect(reverse('kate:match', args=(match.id,)))
    return render(request, 'kate/edit.html', { 'match': match } )


def delete(request, matchid):
    Match.objects.filter(id=matchid).delete()
    return index(request)


def do_move(request, matchid):
    context = RequestContext(request)
    if request.method == 'POST':
        match = get_object_or_404(Match, pk=matchid)
        movesrc = request.POST['move_src']
        movedst = request.POST['move_dst']
        prompiece = request.POST['prom_piece']
        switch = request.POST['switch']
        if(match.next_color_human()):
            if(len(movesrc) > 0 and len(movedst) > 0 and len(prompiece) > 0):
                srcx,srcy = values.koord_to_index(movesrc)
                dstx,dsty = values.koord_to_index(movedst)
                prom_piece = match.PIECES[prompiece]
                flag, msg = rules.is_move_valid(match, srcx, srcy, dstx, dsty, prom_piece)
                if(flag == True):
                    move = match.do_move(srcx, srcy, dstx, dsty, prom_piece)
                    move.save()
                    match.save()
                    status = rules.game_status(match)
                    if(status == Match.STATUS['open']):                        
                        fmtmsg = "<p class='ok'>" + rules.ERROR_MSGS[msg] + "</p>"
                        if(match.next_color_human() == False):
                            calc.thread_do_move(match)
                else:
                    fmtmsg = "<p class='error'>" + rules.ERROR_MSGS[msg] + "</p>"
            else:
                fmtmsg = "<p class='error'>Zug-Format ist ungültig.</p>"
        else:
            fmtmsg = "<p class='error'>Mensch ist nicht am Zug.</p>"
        fmtboard = match.fill_fmtboard(int(switch))
        fmtmoves = Move.fill_fmtmoves(match)
        comments = Comment.objects.filter(match_id=match.id).order_by("created_at").reverse()[:5]
        status = rules.game_status(match)
        if(status != Match.STATUS['open']):
            fmtmsg = "<p class='error'>" + values.reverse_lookup(Match.STATUS, status) + "</p>"
        if(int(switch) == 0):
            rangeobj = range(8)
        else:
            rangeobj = range(7, -1, -1)
        return render(request, 'kate/match.html', { 'match': match, 'board': fmtboard, 'switch': switch, 'movesrc': movesrc, 'movedst': movedst, 'fmtmoves': fmtmoves, 'comments': comments, 'msg': fmtmsg, 'range': rangeobj } )
    else:
        return HttpResponseRedirect(reverse('kate:match', args=(matchid, switch)))


def undo_move(request, matchid, switch=None):
    context = RequestContext(request)
    match = Match.objects.get(id=matchid)
    move = match.undo_move(False)
    if(move != None):
        move.delete()
        match.save()
    return HttpResponseRedirect(reverse('kate:match', args=(match.id, switch, 1)))


def add_comment(request, matchid):
    context = RequestContext(request)
    match = get_object_or_404(Match, pk=matchid)
    if request.method == 'POST':
        newcomment = request.POST['newcomment']
        switchflag = request.POST['switchflag']        
        if(len(newcomment) > 0):
            comment = Comment()
            comment.match_id = match.id
            comment.text = newcomment
            comment.save()
    return HttpResponseRedirect(reverse('kate:match', args=(match.id, switchflag)))


def fetch_comments(request):
    context = RequestContext(request)
    if request.method == 'GET':
        matchid = request.GET['matchid']
        comments = Comment.objects.filter(match_id=matchid).order_by("created_at").reverse()[:5]
        data = ""
        for comment in reversed(comments):
            data += "<p>" + comment.text + "</p>"
        return HttpResponse(data)


def fetch_board(request):
    context = RequestContext(request)
    matchid = request.GET['matchid']
    movecnt = request.GET['movecnt']
    switchflag = request.GET['switchflag']
    match = Match.objects.get(id=matchid)
    if(match == None):
        data = ""
    else:
        lastmove = Move.objects.filter(match_id=match.id).order_by("count").last()
        if(lastmove != None):
            movesrc = values.index_to_koord(lastmove.srcx, lastmove.srcy)
            movedst = values.index_to_koord(lastmove.dstx, lastmove.dsty)
        if(int(movecnt) == match.count):
            data = ""
        else:
            html_player = "<tr><td>&nbsp;</td><td>"
            if(match.white_player_human == False):
                html_player += "<span class='fbold'>" + match.white_player + "</span>"
            else:
                html_player += match.white_player

            html_player += "</td><td>"
            if(match.black_player_human == False):
                html_player += "<span class='fbold'>" + match.black_player + "</span>"
            else:
                html_player += match.black_player

            html_player += "</td></tr>"

            data = match.html_board(int(switchflag), movesrc, movedst) + ":" + html_player + Move.html_moves(match)
    return HttpResponse(data)

