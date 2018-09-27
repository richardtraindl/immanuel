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

    def is_piece_trapped(self):
        for step in self.STEPS:
            x1 = self.xpos + step[0]
            y1 = self.ypos + step[1]
            if(self.match.is_inbounds(x1, y1)):
                dstpiece = self.match.readfield(x1, y1)
                if(dstpiece == PIECES['blk']):
                    return False
                elif(self.match.color_of_piece(dstpiece) == self.color):
                    continue
                else:
                    if(self.match.is_field_touched(self.match.oppcolor_of_piece(self.piece), x1, y1, 0)):
                        if(PIECES_RANK[self.piece] <= PIECES_RANK[dstpiece]):
                            return False
                    else:
                        return False
        return True

    def is_piece_stuck_new(self):
        pin_dir = self.match.evaluate_pin_dir(self.xpos, self.ypos)
        for piecedir in self.DIRS_ARY:
            if(pin_dir == piecedir):
                return False
        return True

    def is_move_stuck(self, dstx, dsty):
        mv_dir = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        pin_dir = self.match.evaluate_pin_dir(self.xpos, self.ypos)
        if(pin_dir == self.DIRS['undefined'] or mv_dir == pin_dir or self.REVERSE_DIRS[mv_dir] == pin_dir):
            return False
        else:
            return True

    # version for queen, rook and bishop - other pieces override function
    def is_move_valid(self, dstx, dsty):
        direction = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        if(direction == self.DIRS['undefined']):
            return False

        stepx, stepy = self.step_for_dir(direction)
        pin_dir = self.match.evaluate_pin_dir(self.xpos, self.ypos) # self.color, 
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
                    self.match.movecnt + 1, 
                    cMove.TYPES['standard'],
                    self.xpos, 
                    self.ypos, 
                    dstx, 
                    dsty, 
                    None,
                    None,
                    PIECES['blk'], 
                    prom_piece, 
                    self.match.fifty_moves_count)

        srcpiece = self.match.readfield(move.srcx, move.srcy)
        dstpiece = self.match.readfield(move.dstx, move.dsty)

        if(dstpiece == PIECES['wQu']):
            self.match.wQu_cnt -= 1
        elif(dstpiece == PIECES['bQu']):
            self.match.bQu_cnt -= 1
        elif(dstpiece == PIECES['wKn'] or dstpiece == PIECES['wBp'] or dstpiece == PIECES['wRk']):
            self.match.wOfficer_cnt -= 1
        elif(dstpiece == PIECES['bKn'] or dstpiece == PIECES['bBp'] or dstpiece == PIECES['bRk']):
            self.match.bOfficer_cnt -= 1

        move.captured_piece = dstpiece

        self.match.movecnt += 1
        self.match.writefield(move.srcx, move.srcy, PIECES['blk'])
        self.match.writefield(move.dstx, move.dsty, srcpiece)
        if(dstpiece != PIECES['blk']):
            self.match.fifty_moves_count = 0
            move.fifty_moves_count = self.match.fifty_moves_count
        else:
            self.match.fifty_moves_count += 1
            move.fifty_moves_count = self.match.fifty_moves_count

        if(srcpiece == PIECES['wRk']):
            if(move.srcx == 0 and move.srcy == 0 and self.match.white_movecnt_long_castling_lost == 0):
                self.match.white_movecnt_long_castling_lost = self.match.movecnt
            elif(move.srcx == 7 and move.srcy == 0 and self.match.white_movecnt_short_castling_lost == 0):
                self.match.white_movecnt_short_castling_lost = self.match.movecnt
        elif(srcpiece == PIECES['bRk']):
            if(move.srcx == 0 and move.srcy == 7 and self.match.black_movecnt_long_castling_lost == 0):
                self.match.black_movecnt_long_castling_lost == self.match.movecnt
            elif(move.srcx == 7 and move.srcy == 7 and self.match.black_movecnt_short_castling_lost == 0):
                self.match.black_movecnt_short_castling_lost == self.match.movecnt

        self.match.score += SCORES[dstpiece]

        self.match.move_list.append(move)

        return move

    def undo_move(self, move):
        if(move.captured_piece == PIECES['wQu']):
            self.match.wQu_cnt += 1
        elif(move.captured_piece == PIECES['bQu']):
            self.match.bQu_cnt += 1
        elif(move.captured_piece == PIECES['wKn'] or move.captured_piece == PIECES['wBp'] or move.captured_piece == PIECES['wRk']):
            self.match.wOfficer_cnt += 1
        elif(move.captured_piece == PIECES['bKn'] or move.captured_piece == PIECES['bBp'] or move.captured_piece == PIECES['bRk']):
            self.match.bOfficer_cnt += 1

        self.match.movecnt -= 1
        self.match.fifty_moves_count = move.fifty_moves_count

        piece = self.match.readfield(move.dstx, move.dsty)
        self.match.writefield(move.srcx, move.srcy, piece)
        self.match.writefield(move.dstx, move.dsty, move.captured_piece)

        self.match.score -= SCORES[move.captured_piece]

        if(piece == PIECES['wRk']):
            if(self.match.white_movecnt_short_castling_lost == self.match.movecnt + 1):
                self.match.white_movecnt_short_castling_lost = 0
            if(self.match.white_movecnt_long_castling_lost == self.match.movecnt + 1):
                self.match.white_movecnt_long_castling_lost = 0
        elif(piece == PIECES['bRk']):
            if(self.match.black_movecnt_short_castling_lost == self.match.movecnt + 1):
                self.match.black_movecnt_short_castling_lost = 0
            if(self.match.black_movecnt_long_castling_lost == self.match.movecnt + 1):
                self.match.black_movecnt_long_castling_lost = 0

        return move


    # version for queen, rook and bishop - other pieces override function
    def find_attacks_and_supports(self, dstx, dsty, attacked, supported):
        from .. analyze_helper import field_touches_beyond

        opp_color = self.match.oppcolor_of_piece(self.color)
        for step in self.STEPS:
            stepx = step[0]
            stepy = step[1]
            x1, y1 = self.match.search(dstx, dsty, stepx , stepy)
            if(x1 is not None):
                if(x1 == self.xpos and y1 == self.ypos):
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
                    field_touches_beyond(self.match, opp_color, ctouch_beyond)
                    self.match.writefield(self.xpos, self.ypos, self.piece)
                    ###
                else:
                    if(piece == PIECES['blk'] or piece == PIECES['wKg'] or piece == PIECES['bKg']):
                        continue
                    ctouch_beyond = cTouchBeyond(self.xpos, self.ypos, dstx, dsty, piece, x1, y1)
                    supported.append(ctouch_beyond)
                    ###
                    self.match.writefield(self.xpos, self.ypos, PIECES['blk'])
                    field_touches_beyond(self.match, self.color, ctouch_beyond)
                    self.match.writefield(self.xpos, self.ypos, self.piece)
                    ###

    def move_defends_forked_field(self, dstx, dsty):
        from .. analyze_helper import is_fork_field

        if(self.is_move_stuck(dstx, dsty)):
            return False

        opp_color = self.match.oppcolor_of_piece(self.piece)

        direction = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        if(direction == self.DIRS_ARY[0] or direction == self.DIRS_ARY[1]):
            STEPS = [self.STEPS[0], self.STEPS[1]]
        else:
            STEPS = [self.STEPS[2], self.STEPS[3]]

        for step in STEPS:
            stepx = step[0]
            stepy = step[1]

            x1 = dstx + stepx
            y1 = dsty + stepy
            while(self.match.is_inbounds(x1, y1)):
                piece = self.match.readfield(x1, y1)
                if(piece == PIECES['blk'] or self.match.color_of_piece(piece) == self.color):
                    if(is_fork_field(self.match, self.color, x1, y1)):
                        #cfork = cFork(srcx, srcy, dstx, dsty, x1, y1)
                        #analyses.lst_fork_defended.append(cfork)
                        return True
                x1 += stepx
                y1 += stepy

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

    def score_attacks(self):
        from .. analyze_helper import list_all_field_touches

        score = 0

        opp_color = self.match.oppcolor_of_piece(self.piece)

        frdlytouches, enmytouches = list_all_field_touches(self.match, self.color, self.xpos, self.ypos)
        if(len(frdlytouches) < len(enmytouches)):
            return score

        for step in self.STEPS:
            stepx = step[0]
            stepy = step[1]
            x1, y1 = self.match.search(self.xpos, self.ypos, stepx, stepy)
            if(x1 is not None):
                if(self.is_move_stuck(x1, y1)):
                    continue

                frdlytouches, enmytouches = list_all_field_touches(self.match, self.color, x1, y1)
                #if(len(frdlytouches) < len(enmytouches)):
                    #continue
                    
                attacked = self.match.readfield(x1, y1)

                if(self.match.color_of_piece(attacked) == opp_color):
                    if(len(enmytouches) == 0 or 
                       PIECES_RANK[self.piece] <= PIECES_RANK[attacked]):
                        score += ATTACKED_SCORES[attacked]

                    # extra score if attacked is pinned
                    direction = self.dir_for_move(self.xpos, self.ypos, x1, y1)
                    enmy_pin = self.match.evaluate_pin_dir(x1, y1) #opp_color, 
                    if(enmy_pin != self.match.DIRS['undefined']):
                        if(enmy_pin != direction and 
                           enmy_pin != self.match.REVERSE_DIRS[direction]):
                            score += ATTACKED_SCORES[attacked]
                        else:
                            if(PIECES_RANK[attacked] != PIECES_RANK[self.piece] and
                               attacked != PIECES['wPw'] and attacked != PIECES['bPw']):
                                score += ATTACKED_SCORES[attacked]

                    if(self.match.is_soft_pin(x1, y1)):
                        score += ATTACKED_SCORES[attacked]
        return score


    def score_supports(self):
        score = 0

        opp_color = self.match.oppcolor_of_piece(self.piece)

        for step in self.STEPS:
            stepx = step[0]
            stepy = step[1]
            x1, y1 = self.match.search(self.xpos, self.ypos, stepx , stepy)
            if(x1 is not None):
                if(x1 == self.xpos and y1 == self.ypos):
                    continue

                if(self.is_move_stuck(x1, y1)):
                    continue

                supported = self.match.readfield(x1, y1)

                if(self.match.color_of_piece(supported) == self.color):
                    if(self.match.is_field_touched(opp_color, x1, y1, 1)):
                        score += SUPPORTED_SCORES[supported]
        return score


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


    def generate_moves(self, mode):
        genmoves = []
        for direction in self.GEN_STEPS:
            for step in direction:
                dstx = self.xpos + step[0]
                dsty = self.ypos + step[1]
                flag, errcode = self.match.is_move_valid(self.xpos, self.ypos, dstx, dsty, step[2])
                if(flag):
                    if(mode == 0):
                        genmoves.append(GenMove(self.match, self.xpos, self.ypos, dstx, dsty, step[2]))
                    else:
                        gmove = cGenMove(self.match, self.xpos, self.ypos, dstx, dsty, step[2])
                        genmoves.append(cPrioMove(gmove))
                elif(errcode == 31): #cValidator.RETURN_CODES['out-of-bounds']
                    break
        return genmoves
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

