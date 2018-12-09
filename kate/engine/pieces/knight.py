from .. values import *
from . piece import *


class cKnight(cPiece):
    STEPS = [ [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2] ]

    STEP_2N1E_X = 1
    STEP_2N1E_Y = 2
    STEP_1N2E_X = 2
    STEP_1N2E_Y = 1
    STEP_1S2E_X = 2
    STEP_1S2E_Y = -1
    STEP_2S1E_X = 1
    STEP_2S1E_Y = -2
    STEP_2S1W_X = -1
    STEP_2S1W_Y = -2
    STEP_1S2W_X = -2
    STEP_1S2W_Y = -1
    STEP_1N2W_X = -2
    STEP_1N2W_Y = 1
    STEP_2N1W_X = -1
    STEP_2N1W_Y = 2

    GEN_STEPS = [ [[1, 2, PIECES['blk']]],
                  [[2, 1, PIECES['blk']]],
                  [[2, -1, PIECES['blk']]], 
                  [[1, -2, PIECES['blk']]],
                  [[-1, -2, PIECES['blk']]],
                  [[-2, -1, PIECES['blk']]],
                  [[-2, 1, PIECES['blk']]],
                  [[-1, 2, PIECES['blk']]] ]

    def __init__(self, match, xpos, ypos):
        super().__init__(match, xpos, ypos)

    @classmethod
    def dir_for_move(cls, srcx, srcy, dstx, dsty):
        step_x = dstx - srcx
        step_y = dsty - srcy
        if(step_x == cls.STEP_2N1E_X and step_y == cls.STEP_2N1E_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_1N2E_X and step_y == cls.STEP_1N2E_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_1S2E_X and step_y == cls.STEP_1S2E_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_2S1E_X and step_y == cls.STEP_2S1E_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_2S1W_X and step_y == cls.STEP_2S1W_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_1S2W_X and step_y == cls.STEP_1S2W_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_1N2W_X and step_y == cls.STEP_1N2W_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_2N1W_X and step_y == cls.STEP_2N1W_Y):
            return cls.DIRS['valid']
        else:
            return cls.DIRS['undefined']

    #step_for_dir(direction):
        # not used for knight

    def is_piece_trapped(self):
        return False # knight cannot be trapped

    #is_piece_stuck(self):
        # works with inherited class

    def is_move_stuck(self, dstx, dsty):
        return False # not used for knight

    def is_move_valid(self, dstx, dsty):
        direction = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        if(direction == self.match.DIRS['undefined']):
            return False

        pin_dir = self.match.evaluate_pin_dir(self.xpos, self.ypos) #self.color, 
        if(pin_dir != self.match.DIRS['undefined']):
            return False

        dstpiece = self.match.readfield(dstx, dsty)
        if(self.match.color_of_piece(dstpiece) == self.color):
            return False

        return True

    #do_move(self, dstx, dsty, prom_piece)
        # works with inherited class

    #undo_move(self, move)
        # works with inherited class

    def find_attacks_and_supports(self, dstx, dsty, attacked, supported):
        from .. analyze_helper import list_field_touches_beyond

        cknight = cKnight(self.match, dstx, dsty)
        if(cknight.is_piece_stuck()):
            return

        opp_color =  self.match.oppcolor_of_piece(self.piece)
        for step in self.STEPS:
            x1 = dstx + step[0]
            y1 = dsty + step[1]
            if(self.match.is_inbounds(x1, y1)):
                if(x1 == self.xpos and y1 == self.ypos):
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
                else:
                    if(piece == PIECES['blk'] or piece == PIECES['wKg'] or piece == PIECES['bKg']):
                        continue
                    ctouch_beyond = cTouchBeyond(self.xpos, self.ypos, dstx, dsty, piece, x1, y1)
                    supported.append(ctouch_beyond)
                    ###
                    self.match.writefield(self.xpos, self.ypos, PIECES['blk'])
                    list_field_touches_beyond(self.match, self.color, ctouch_beyond)
                    self.match.writefield(self.xpos, self.ypos, self.piece)
                    ###

    def move_defends_forked_field(self, dstx, dsty):
        from .. analyze_helper import list_all_field_touches, is_fork_field

        if(self.is_move_stuck(dstx, dsty)):
            return False

        for step in self.STEPS:
            x1 = dstx + step[0]
            y1 = dsty + step[1]

            if(x1 == self.xpos and y1 == self.ypos):
                continue

            if(self.match.is_inbounds(x1, y1)):
                piece = self.match.readfield(x1, y1)

                if(piece == PIECES['blk'] or 
                   self.match.color_of_piece(piece) == self.color):
                    frdlytouches, enmytouches = list_all_field_touches(self.match, self.color, x1, y1)
                    if(len(frdlytouches) < len(enmytouches)):
                        excludes = []
                        excludes.append([self.xpos, self.ypos])
                        if(is_fork_field(self.match, self.color, x1, y1, excludes)):
                            return True

        return False

    def move_controles_file(self, dstx, dsty):
        return False

    def score_attacks(self):
        from .. analyze_helper import list_all_field_touches

        score = 0

        if(self.is_piece_stuck()):
            return score

        opp_color = self.match.oppcolor_of_piece(self.piece)

        frdlytouches, enmytouches = list_all_field_touches(self.match, self.color, self.xpos, self.ypos)
        if(len(frdlytouches) < len(enmytouches)):
            return score

        for step in self.STEPS:
            x1 = self.xpos + step[0]
            y1 = self.ypos + step[1]
            if(self.match.is_inbounds(x1, y1)):
                frdlytouches, enmytouches = list_all_field_touches(self.match, self.color, x1, y1)
                #if(len(frdlytouches) < len(enmytouches)):
                    #continue

                attacked = self.match.readfield(x1, y1)

                if(self.match.color_of_piece(attacked) == opp_color):
                    if(len(enmytouches) == 0 or 
                       PIECES_RANK[attacked] > PIECES_RANK[self.piece]):
                        score += ATTACKED_SCORES[attacked]

                    # extra score if attacked is pinned
                    enmy_pin = self.match.evaluate_pin_dir(x1, y1) #opp_color, 
                    if(enmy_pin != self.DIRS['undefined']):
                        score += ATTACKED_SCORES[attacked]

                    if(self.match.is_soft_pin(x1, y1)):
                        score += ATTACKED_SCORES[attacked]
        return score

    def score_supports(self):
        score = 0

        if(self.is_piece_stuck()):
            return score

        opp_color = self.match.oppcolor_of_piece(self.piece)

        for step in self.STEPS:
            stepx = step[0]
            stepy = step[1]
            x1, y1 = self.match.search(self.xpos, self.ypos, stepx , stepy)
            if(x1 is not None):
                if(x1 == self.xpos and y1 == self.ypos):
                    continue

                supported = self.match.readfield(x1, y1)

                if(supported == PIECES['blk']):
                    continue

                if(self.match.color_of_piece(supported) == self.color):
                    if(self.match.is_field_touched(opp_color, x1, y1, 1)):
                        score += SUPPORTED_SCORES[supported]
        return score 

    # list_moves(self):
       # works with inherited class

    # generate_moves(self):
       # works with inherited class

    # generate_priomoves(self):
       # works with inherited class

# class end

