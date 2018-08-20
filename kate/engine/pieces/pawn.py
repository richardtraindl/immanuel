from .piece import cPiece


class cPawn(cPiece):
    DIRS = { 'north' : 1,
             'south' : 2,
             'north-east' : 5,
             'south-west' : 6,
             'north-west' : 7,
             'south-east' : 8,
             '2north' : 9,
             '2south' : 10,
             'valid' : 13,
             'undefined' : 14 }

    REVERSE_DIRS = { DIRS['north'] : DIRS['south'],
                     DIRS['south'] : DIRS['north'],
                     DIRS['north-east'] : DIRS['south-west'],
                     DIRS['south-west'] : DIRS['north-east'],
                     DIRS['north-west'] : DIRS['south-east'],
                     DIRS['south-east'] : DIRS['north-west'],
                     DIRS['2north'] : DIRS['2south'],
                     DIRS['2south'] : DIRS['2north'],
                     DIRS['valid']  : DIRS['valid'],
                     DIRS['undefined']  : DIRS['undefined'] }

    STEP_1N_X = 0
    STEP_1N_Y = 1
    STEP_2N_X = 0
    STEP_2N_Y = 2
    STEP_1N1E_X = 1
    STEP_1N1E_Y = 1
    STEP_1N1W_X = -1
    STEP_1N1W_Y = 1
    STEP_1S_X = 0
    STEP_1S_Y = -1
    STEP_2S_X = 0
    STEP_2S_Y = -2
    STEP_1S1E_X = 1
    STEP_1S1E_Y = -1
    STEP_1S1W_X = -1
    STEP_1S1W_Y = -1
    
    A2_Y = 1
    A7_Y = 6

    def __init__(self, match, xpos, ypos):
        super().__init__(match, xpos, ypos)
        if(self.color == self.match.COLORS['white']):
            self.STEPS = [ [1, 1], [-1, 1] ]
            self.BACK_STEPS = [ [1, -1], [-1, -1] ]
        else:
            self.STEPS = [ [1, -1], [-1, -1] ]
            self.BACK_STEPS = [ [1, 1], [-1, 1] ]

    @classmethod
    def dir_for_move(cls, srcx, srcy, dstx, dsty):
        step_x = dstx - srcx
        step_y = dsty - srcy
        if(step_x == cls.STEP_1N_X and step_y == cls.STEP_1N_Y):
            return cls.DIRS['north']
        elif(step_x == cls.STEP_2N_X and step_y == cls.STEP_2N_Y and srcy == cls.A2_Y):
            return cls.DIRS['2north']
        elif(step_x == cls.STEP_1N1E_X and step_y == cls.STEP_1N1E_Y):
            return cls.DIRS['north-east']
        elif(step_x == cls.STEP_1N1W_X and step_y == cls.STEP_1N1W_Y):
            return cls.DIRS['north-west']
        elif(step_x == cls.STEP_1S_X and step_y == cls.STEP_1S_Y):
            return cls.DIRS['south']
        elif(step_x == cls.STEP_2S_X and step_y == cls.STEP_2S_Y and srcy == cls.A7_Y):
            return cls.DIRS['2south']
        elif(step_x == cls.STEP_1S1E_X and step_y == cls.STEP_1S1E_Y):
            return cls.DIRS['south-east']
        elif(step_x == cls.STEP_1S1W_X and step_y == cls.STEP_1S1W_Y):
            return cls.DIRS['south-west']
        else:
            return cls.DIRS['undefined']

    #step_for_dir(direction):
        # not used for pawn

    def is_piece_trapped(self):
        return False # pawn cannot be trapped

    #is_piece_stuck_new(self):
        # works with inherited class

    #is_move_stuck(self, dstx, dsty)
        # works with inherited class

    def is_move_valid(self, dstx, dsty, prom_piece):
        direction = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        if(direction == self.DIRS['undefined']):
            return False

        pin_dir = self.match.evaluate_pin_dir(self.xpos, self.ypos) #self.color, 

        dstpiece = self.match.readfield(dstx, dsty)

        if(self.color == self.match.COLORS['white']):
            # check pins
            if(direction == self.DIRS['north'] or direction == self.DIRS['2north']):
                if(pin_dir != self.DIRS['north'] and pin_dir != self.DIRS['south'] and pin_dir != self.DIRS['undefined']):
                    return False
            elif(direction == self.DIRS['north-west']):
                if(pin_dir != self.DIRS['north-west'] and pin_dir != self.DIRS['south-east'] and pin_dir != self.DIRS['undefined']):
                    return False
            elif(direction == self.DIRS['north-east']):
                if(pin_dir != self.DIRS['north-east'] and pin_dir != self.DIRS['south-west'] and pin_dir != self.DIRS['undefined']):
                    return False

            # check fields
            if(direction == self.DIRS['north'] and dstpiece != self.match.PIECES['blk']):
                return False
            elif(direction == self.DIRS['2north']):
                midpiece = self.match.readfield(dstx, self.ypos + self.STEP_1N_Y)
                if(midpiece != self.match.PIECES['blk'] or dstpiece != self.match.PIECES['blk']):
                    return False
            elif(direction == self.DIRS['north-west'] or direction == self.DIRS['north-east']):
                if(self.match.color_of_piece(dstpiece) != self.match.COLORS['black']):
                    return self.is_white_ep_move_ok(dstx, dsty)

            # check promotion
            if(dsty == 7 and prom_piece != self.match.PIECES['wQu'] and prom_piece != self.match.PIECES['wRk'] and prom_piece != self.match.PIECES['wBp'] and prom_piece != self.match.PIECES['wKn']):
                return False
            elif(dsty < 7 and prom_piece != self.match.PIECES['blk']):
                return False
        else:
            # check pins
            if(direction == self.DIRS['south'] or direction == self.DIRS['2south']):
                if(pin_dir != self.DIRS['north'] and pin_dir != self.DIRS['south'] and pin_dir != self.DIRS['undefined']):
                    return False
            elif(direction == self.DIRS['south-east']):
                if(pin_dir != self.DIRS['north-west'] and pin_dir != self.DIRS['south-east'] and pin_dir != self.DIRS['undefined']):
                    return False
            elif(direction == self.DIRS['south-west']):
                if(pin_dir != self.DIRS['north-east'] and pin_dir != self.DIRS['south-west'] and pin_dir != self.DIRS['undefined']):
                    return False
            
            # check fields
            if(direction == self.DIRS['south'] and dstpiece != self.match.PIECES['blk']):
                return False
            elif(direction == self.DIRS['2south']):
                midpiece = self.match.readfield(dstx, self.ypos + self.STEP_1S_Y)
                if(midpiece != self.match.PIECES['blk'] or dstpiece != self.match.PIECES['blk']):
                    return False
            elif(direction == self.DIRS['south-east'] or direction == self.DIRS['south-west']):
                if(self.match.color_of_piece(dstpiece) != self.match.COLORS['white']):
                    return self.is_black_ep_move_ok(dstx, dsty)

            # check promotion
            if(dsty == 0 and prom_piece != self.match.PIECES['bQu'] and prom_piece != self.match.PIECES['bRk'] and prom_piece != self.match.PIECES['bBp'] and prom_piece != self.match.PIECES['bKn']):
                return False
            elif(dsty > 0 and prom_piece != self.match.PIECES['blk']):
                return False

        return True

    def is_white_ep_move_ok(self, dstx, dsty):
        if(len(self.match.move_list) == 0):
            return False
        else:
            move = self.match.move_list[-1]

        dstpiece = self.match.readfield(dstx, dsty)
        opp_piece = self.match.readfield(move.dstx, move.dsty)
        if(dstpiece == self.match.PIECES['blk'] and opp_piece == self.match.PIECES['bPw'] and 
           move.srcy - move.dsty == 2 and move.dsty == self.ypos and move.dstx == dstx and 
           move.dsty - dsty == -1):
            return True
        else:
            return False


    def is_black_ep_move_ok(self, dstx, dsty):
        if(len(self.match.move_list) == 0):
            return False
        else:
            move = self.match.move_list[-1]

        dstpiece = self.match.readfield(dstx, dsty)
        opp_piece = self.match.readfield(move.dstx, move.dsty)
        if(dstpiece == self.match.PIECES['blk'] and opp_piece == self.match.PIECES['wPw'] and 
           move.srcy - move.dsty == -2 and move.dsty == self.ypos and move.dstx == dstx and 
           move.dsty - dsty == 1):
            return True
        else:
            return False
        
    def find_attacks_and_supports(self, dstx, dsty, attacked, supported):
        opp_color = match.oppcolor_of_piece(self.piece)

        for step in self.STEPS:
            x1 = dstx + step[0]
            y1 = dsty + step[1]
            if(self.match.is_inbounds(x1, y1)):
                if(x1 == self.xpos and y1 == self.ypos):
                    continue

                piece = self.match.readfield(x1, y1)
            
                if(piece == self.match.PIECES['blk']):
                    continue

                cpawn = cPawn(self.match, dstx, dsty)
                if(self.is_move_stuck(x1, y1)):
                    continue

                if(self.match.color_of_piece(piece) == opp_color):
                    ctouch_beyond = cTouchBeyond(self.xpos, self.ypos, dstx, dsty, piece, x1, y1)
                    attacked.append(ctouch_beyond)
                    ###
                    self.match.writefield(self.xpos, self.ypos, self.match.PIECES['blk'])
                    field_touches_beyond(self.match, opp_color, ctouch_beyond)
                    self.match.writefield(self.xpos, self.ypos, self.piece)
                    ###
                else:
                    if(piece == self.match.PIECES['blk'] or piece == self.match.PIECES['wKg'] or piece == self.match.PIECES['bKg']):
                        continue

                    ctouch_beyond = cTouchBeyond(self.xpos, self.ypos, dstx, dsty, piece, x1, y1)
                    supported.append(ctouch_beyond)
                    ###
                    self.match.writefield(self.xpos, self.ypos, self.match.PIECES['blk'])
                    field_touches_beyond(self.match, self.color, ctouch_beyond)
                    self.match.writefield(self.xpos, self.ypos, self.piece)
                    ###

# class end

