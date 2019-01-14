from .. values import *
from .. move import *


class cPiece:
    DIRS = { 'valid' : 13, 'undefined' : 14 }
    DIRS_ARY = [DIRS['valid'], DIRS['undefined']]
    REVERSE_DIRS = { DIRS['valid'] : DIRS['valid'], DIRS['undefined'] : DIRS['undefined'] }
    STEPS = []
    UNDEF_X = 8
    UNDEF_Y = 8

    GEN_STEPS = None

    def __init__(self, match, xpos, ypos):
        self.match = match
        self.xpos = xpos
        self.ypos = ypos
        self.piece = match.readfield(xpos, ypos)
        self.color = match.color_of_piece(self.piece)

    @classmethod
    def dir_for_move(cls, srcx, srcy, dstx, dsty):
        return cls.DIRS['undefined']

    @classmethod
    def step_for_dir(cls, direction):
        return cls.UNDEF_X, cls.UNDEF_Y

    def is_trapped(self):
        from .. analyze_helper import list_all_field_touches
        
        if(self.match.is_field_touched(REVERSED_COLORS[self.color], self.xpos, self.ypos, self.match.EVAL_MODES['only-pins-to-king']) == False):
            return False

        for step in self.STEPS:
            x1 = self.xpos + step[0]
            y1 = self.ypos + step[1]
            if(self.match.is_inbounds(x1, y1)):
                dstpiece = self.match.readfield(x1, y1)
                if(self.match.color_of_piece(dstpiece) == self.color):
                    continue
                else:
                    if(dstpiece != PIECES['blk'] and PIECES_RANK[self.piece] <= PIECES_RANK[dstpiece]):
                        return False
                    frdlytouches, enmytouches = list_all_field_touches(self.match, self.color, x1, y1)
                    enmy_is_lower = False
                    for enmy in enmytouches:
                        if(PIECES_RANK[enmy.piece] < PIECES_RANK[self.piece]):
                            enmy_is_lower = True
                            break
                    if(len(frdlytouches) >= len(enmytouches) and enmy_is_lower == False):
                        return False
        return True

    def is_piece_stuck(self):
        pin_dir = self.match.eval_pin_dir(self.xpos, self.ypos)
        if(pin_dir == self.DIRS['undefined']):
            return False
        for piecedir in self.DIRS_ARY:
            if(pin_dir == piecedir):
                return False
        return True

    def is_move_stuck(self, dstx, dsty):
        mv_dir = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        pin_dir = self.match.eval_pin_dir(self.xpos, self.ypos)
        if(pin_dir == self.DIRS['undefined'] or mv_dir == pin_dir or self.REVERSE_DIRS[mv_dir] == pin_dir):
            return False
        else:
            return True

    # version for queen, rook and bishop - other pieces override function
    def is_move_valid(self, dstx, dsty, prom_piece=PIECES['blk']):
        direction = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        if(direction == self.DIRS['undefined']):
            return False

        stepx, stepy = self.step_for_dir(direction)
        pin_dir = self.match.eval_pin_dir(self.xpos, self.ypos)
        for piecedir in self.DIRS_ARY:
            if(direction == piecedir):
                if(pin_dir != piecedir and pin_dir != self.REVERSE_DIRS[piecedir] and pin_dir != self.DIRS['undefined']):
                    return False

        x = self.xpos + stepx
        y = self.ypos + stepy
        while(x >= 0 and x <= 7 and y >= 0 and y <= 7):
            field = self.match.readfield(x, y)
            if(x == dstx and y == dsty):
                if(self.match.color_of_piece(field) == self.color):
                    return False
                else:
                    return True
            elif(field != PIECES['blk']):
                return False

            x += stepx
            y += stepy

        return False

    def do_move(self, dstx, dsty, prom_piece):
        move = cMove(self.match, 
                    self.match.movecnt() + 1, 
                    cMove.TYPES['standard'],
                    self.xpos, 
                    self.ypos, 
                    dstx, 
                    dsty, 
                    None,
                    None,
                    PIECES['blk'], 
                    prom_piece, 
                    self.match.board.fifty_moves_count)

        dstpiece = self.match.readfield(move.dstx, move.dsty)

        move.captured_piece = dstpiece

        self.match.writefield(move.srcx, move.srcy, PIECES['blk'])
        self.match.writefield(move.dstx, move.dsty, self.piece)

        if(self.match.color_of_piece(self.piece) == COLORS['white']):
            self.match.board.domove_white_movecnt_short_castling_lost(move.srcx, move.srcy, move.count)
            self.match.board.domove_white_movecnt_long_castling_lost(move.srcx, move.srcy, move.count)
        else:
            self.match.board.domove_black_movecnt_short_castling_lost(move.srcx, move.srcy, move.count)
            self.match.board.domove_black_movecnt_long_castling_lost(move.srcx, move.srcy, move.count)

        self.match.board.domove_counter(dstpiece)
        self.match.board.domove_fifty_moves_count(self.piece, dstpiece)

        self.match.score += SCORES[dstpiece]
        self.match.move_list.append(move)
        return move

    def undo_move(self, move):
        self.match.writefield(move.srcx, move.srcy, self.piece)
        self.match.writefield(move.dstx, move.dsty, move.captured_piece)
        self.match.score -= SCORES[move.captured_piece]

        if(self.match.color_of_piece(self.piece) == COLORS['white']):
            self.match.board.undomove_white_movecnt_short_castling_lost(move)
            self.match.board.undomove_white_movecnt_long_castling_lost(move)
        else:
            self.match.board.undomove_black_movecnt_short_castling_lost(move)
            self.match.board.undomove_black_movecnt_long_castling_lost(move)

        self.match.board.undomove_counter(move)
        self.match.board.undomove_fifty_moves_count(move)
        return move


    # version for queen, rook and bishop - other pieces override function
    def find_attacks_and_supports(self, dstx, dsty, attacked, supported):
        from .. analyze_helper import list_field_touches_beyond
        if(self.piece == PIECES['wPw'] or self.piece == PIECES['bPw'] or 
           self.piece == PIECES['wKn'] or self.piece == PIECES['bKn'] or
           self.piece == PIECES['wKg'] or self.piece == PIECES['bKg']):
            outer_maxcnt = 1
            inner_maxcnt = 0
        else:
            outer_maxcnt = 7
            inner_maxcnt = 7
        opp_color = self.match.oppcolor_of_piece(self.color)
        for step in self.STEPS:
            stepx = step[0]
            stepy = step[1]
            x1, y1 = self.match.search(dstx, dsty, stepx , stepy, outer_maxcnt)
            if(x1):
                if(x1 == self.xpos and y1 == self.ypos):
                    x1, y1 = self.match.search(x1, y1, stepx, stepy, inner_maxcnt)
                    if(x1 is None):
                        continue
                cpiece = cPiece(self.match, dstx, dsty)
                if(cpiece.is_move_stuck(x1, y1)):
                    continue
                piece = self.match.readfield(x1, y1)
                if(self.match.color_of_piece(piece) == opp_color):
                    ctouch_beyond = cTouchBeyond(self.xpos, self.ypos, dstx, dsty, piece, x1, y1)
                    attacked.append(ctouch_beyond)
                    ###
                    self.match.writefield(self.xpos, self.ypos, PIECES['blk'])
                    list_field_touches_beyond(self.match, opp_color, ctouch_beyond)
                    self.match.writefield(self.xpos, self.ypos, self.piece)
                    ###
                elif(self.match.color_of_piece(piece) == self.color):
                    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
                        continue
                    ctouch_beyond = cTouchBeyond(self.xpos, self.ypos, dstx, dsty, piece, x1, y1)
                    supported.append(ctouch_beyond)
                    ###
                    self.match.writefield(self.xpos, self.ypos, PIECES['blk'])
                    list_field_touches_beyond(self.match, self.color, ctouch_beyond)
                    self.match.writefield(self.xpos, self.ypos, self.piece)
                    ###

    def forks(self):
        from .. analyze_helper import list_all_field_touches
        count = 0
        for step in self.STEPS:
            x1, y1 = self.match.search(self.xpos, self.ypos, step[0], step[1])
            if(x1):
                if(self.is_move_stuck(x1, y1)):
                    continue
                dstpiece = self.match.readfield(x1, y1)
                if(self.match.color_of_piece(dstpiece) == REVERSED_COLORS[self.color]):
                    friends, enemies = list_all_field_touches(self.match, self.match.color_of_piece(dstpiece), x1, y1)
                    if(len(friends) == 0 or
                       len(friends) < len(enemies) or 
                       PIECES_RANK[dstpiece] >= PIECES_RANK[self.piece]):
                        count += 1
        if(count >= 2):
            return True
        else:
            return False

    def move_defends_fork(self, dstx, dsty):
        from .. analyze_helper import list_all_field_touches, is_fork_field
        if(self.is_move_stuck(dstx, dsty)):
            return False
        for step in self.STEPS:
            x1, y1 = self.match.search(dstx, dsty, step[0], step[1])
            if(x1):
                if(x1 == dstx and y1 == dsty):
                    continue
                piece = self.match.readfield(x1, y1)
                if(piece == PIECES['blk'] or 
                   self.match.color_of_piece(piece) == self.color):
                    frdlytouches, enmytouches = list_all_field_touches(self.match, self.color, x1, y1)
                    if(len(frdlytouches) < len(enmytouches)):
                        if(is_fork_field(self.match, x1, y1, REVERSED_COLORS[self.color])):
                            return True
        return False

    def move_controles_file(self, dstx, dsty):
        cnt = 0
        move_dir = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        move_opp_dir = self.match.REVERSE_DIRS[move_dir]
    
        for step in self.STEPS:
            stepx = step[0]
            stepy = step[1]
            direction = self.dir_for_move(dstx, dsty, dstx + stepx, dsty + stepy)
            if(direction == move_dir or direction == move_opp_dir):
                continue
            x1 = dstx + stepx
            y1 = dsty + stepy
            while(self.match.is_inbounds(x1, y1)):
                piece = self.match.readfield(x1, y1)
                if(self.match.color_of_piece(piece) == self.color):
                    break
                else:
                    cnt += 1
                    x1 += stepx
                    y1 += stepy

        if(cnt >= 5):
            return True
        else:
            return False

    def score_for_score_touches(self, touched, x1, y1):
        from .. analyze_helper import list_all_field_touches
        score = 0
        frdlytouches, enmytouches = list_all_field_touches(self.match, self.color, x1, y1)
        if(self.match.color_of_piece(touched) == self.color):
            if(len(enmytouches) > 0):
                addjust = 1
            else:
                addjust = 4
            score += SUPPORTED_SCORES[touched] // addjust
            # extra score if supported is pinned
            if(self.match.is_soft_pin(x1, y1)[0]):
                score += SUPPORTED_SCORES[touched] // addjust
        else:
            if(len(frdlytouches) >= len(enmytouches) or
               PIECES_RANK[touched] >= PIECES_RANK[self.piece]):
                addjust = 1
            else:
                addjust = 4
            score += ATTACKED_SCORES[touched] // addjust
            # extra score if attacked is pinned
            if(self.match.is_soft_pin(x1, y1)[0]):
                score += ATTACKED_SCORES[touched] // addjust
        return score

    def score_touches_ori(self):
        from .. analyze_helper import list_all_field_touches
        score = 0

        """frdlytouches, enmytouches = list_all_field_touches(self.match, self.color, self.xpos, self.ypos)
        if(len(frdlytouches) < len(enmytouches)):
            return score"""

        for step in self.STEPS:
            stepx = step[0]
            stepy = step[1]
            x1, y1 = self.match.search(self.xpos, self.ypos, stepx, stepy)
            if(x1 is None):
                continue
            else:
                if(self.is_move_stuck(x1, y1)):
                    """if(self.color == COLORS['white']):
                        score += ATTACKED_SCORES[PIECES['wPw']]
                    else:
                        score += ATTACKED_SCORES[PIECES['bPw']]"""
                    continue

                touched = self.match.readfield(x1, y1)
                score += self.score_for_score_touches(touched, x1, y1)
        return score

    def score_touches(self):
        from .. analyze_helper import list_all_field_touches
        support_score = 0
        attack_score = 0

        frdlytouches, enmytouches = list_all_field_touches(self.match, self.color, self.xpos, self.ypos)
        if(len(frdlytouches) > 0):
            if(len(enmytouches) == 0):
                support_score += SUPPORTED_SCORES[self.piece] // 2
            else:
                support_score += SUPPORTED_SCORES[self.piece]

        if(len(enmytouches) > 0):
            attack_score += ATTACKED_SCORES[self.piece]

        if(self.match.is_soft_pin(self.xpos, self.ypos)[0]):
            rank = PIECES_RANK[PIECES['wKg']]
            for enmy in enmytouches:
                if(PIECES_RANK[enmy.piece] < rank):
                    rank = PIECES_RANK[enmy.piece]
            attack_score += attack_score // max(1, (rank - PIECES_RANK[PIECES['bPw']]))

        return support_score + attack_score

    def list_moves(self):
        movelist = []
        for step in self.STEPS:
            x1 = self.xpos + step[0]
            y1 = self.ypos + step[1]
            if(self.match.is_inbounds(x1, y1)):
                piece = self.match.readfield(x1, y1)
                if(self.match.color_of_piece(piece) != self.color):
                    movelist.append([x1, y1])
        return movelist

    def generate_moves(self):
        moves = []
        for direction in self.GEN_STEPS:
            for step in direction:
                dstx = self.xpos + step[0]
                dsty = self.ypos + step[1]
                flag, errcode = self.match.is_move_valid(self.xpos, self.ypos, dstx, dsty, step[2])
                if(flag):
                    moves.append(cGenMove(self.match, self.xpos, self.ypos, dstx, dsty, step[2]))
                elif(errcode == 31): #RETURN_CODES['out-of-bounds']
                    break
        return moves

    def generate_priomoves(self):
        moves = []
        for direction in self.GEN_STEPS:
            for step in direction:
                dstx = self.xpos + step[0]
                dsty = self.ypos + step[1]
                flag, errcode = self.match.is_move_valid(self.xpos, self.ypos, dstx, dsty, step[2])
                if(flag):
                    gmove = cGenMove(self.match, self.xpos, self.ypos, dstx, dsty, step[2])
                    moves.append(cPrioMove(gmove))
                elif(errcode == 31): #RETURN_CODES['out-of-bounds']
                    break
        return moves

# class end


class cTouch:
    def __init__(self, piece, fieldx, fieldy):
        self.piece = piece
        self.fieldx = fieldx
        self.fieldy = fieldy


class cTouchBeyond:
    def __init__(self, srcx, srcy, dstx, dsty, piece, fieldx, fieldy):
        self.agent_srcx = srcx
        self.agent_srcy = srcy
        self.agent_dstx = dstx
        self.agent_dsty = dsty        
        self.piece = piece
        self.fieldx = fieldx
        self.fieldy = fieldy
        self.attacker_beyond = []
        self.supporter_beyond = []


class cFork:
    def __init__(self, srcx, srcy, dstx, dsty, forkx, forky):
        self.agent_srcx = srcx
        self.agent_srcy = srcy
        self.agent_dstx = dstx
        self.agent_dsty = dsty        
        self.forkx = forkx
        self.forky = forky

