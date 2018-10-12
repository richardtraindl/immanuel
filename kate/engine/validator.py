from .values import *
from .pieces.pawn import cPawn
from .pieces.knight import cKnight
from .pieces.bishop import cBishop
from .pieces.rook import cRook
from .pieces.king import cKing
from .pieces.queen import cQueen
from .pieces.pawnfield import cPawnField
from .pieces.knightfield import cKnightField
from .pieces.rookfield import cRookField
from .pieces.bishopfield import cBishopField
from .pieces.kingfield import cKingField


class cValidator:
    RETURN_CODES = {
        'ok' : 10,
        'draw' : 11,
        'winner_white' : 12,
        'winner_black' : 13,
        'match-cancelled' : 14,
        'wrong-color' : 15,
        'pawn-error' : 20,
        'rook-error' : 21,
        'knight-error' : 22,
        'bishop-error' : 23,
        'queen-error' : 24,
        'king-error' : 25,
        'format-error' : 30,
        'out-of-bounds' : 31,
        'general-error' : 40,
    }

    RETURN_MSGS = {
        RETURN_CODES['ok'] : "move okay",
        RETURN_CODES['draw'] : "draw",
        RETURN_CODES['winner_white'] : "winner white",
        RETURN_CODES['winner_black'] : "winner black",
        RETURN_CODES['match-cancelled'] : " match is cancelled",
        RETURN_CODES['wrong-color'] : "wrong color",
        RETURN_CODES['pawn-error'] : "pawn error",
        RETURN_CODES['rook-error'] : "rook error",
        RETURN_CODES['knight-error'] : "knight error",
        RETURN_CODES['bishop-error'] : "bishop error",
        RETURN_CODES['queen-error'] : "queen error",
        RETURN_CODES['king-error'] : "king error",
        RETURN_CODES['format-error'] : "format wrror",
        RETURN_CODES['out-of-bounds'] : "wrong square",
        RETURN_CODES['general-error'] : "general error",
    }

    @classmethod
    def is_move_valid(cls, match, srcx, srcy, dstx, dsty, prom_piece):
        if(not match.is_move_inbounds(srcx, srcy, dstx, dsty)):
            return False, cls.RETURN_CODES['out-of-bounds']

        piece = match.readfield(srcx, srcy)

        if(match.next_color() != match.color_of_piece(piece)):
            return False, cls.RETURN_CODES['wrong-color']

        if(piece != match.PIECES['wKg'] and piece != match.PIECES['bKg']):
            if(cls.is_king_after_move_attacked(match, srcx, srcy, dstx, dsty)):
                return False, cls.RETURN_CODES['king-error']

        if(piece == match.PIECES['wPw'] or piece == match.PIECES['bPw']):
            cpawn = cPawn(match, srcx, srcy)
            if(cpawn.is_move_valid(dstx, dsty, prom_piece)):
                return True, cls.RETURN_CODES['ok']
            else:
                return False, cls.RETURN_CODES['pawn-error']
        elif(piece == match.PIECES['wRk'] or piece == match.PIECES['bRk']):
            crook = cRook(match, srcx, srcy)
            if(crook.is_move_valid(dstx, dsty)):
                return True, cls.RETURN_CODES['ok']
            else:
                return False, cls.RETURN_CODES['rook-error']
        elif(piece == match.PIECES['wKn'] or piece == match.PIECES['bKn']):
            cknight = cKnight(match, srcx, srcy)
            if(cknight.is_move_valid(dstx, dsty)):
                return True, cls.RETURN_CODES['ok']
            else:
                return False, cls.RETURN_CODES['knight-error']
        elif(piece == match.PIECES['wBp'] or piece == match.PIECES['bBp']):
            cbishop = cBishop(match, srcx, srcy)
            if(cbishop.is_move_valid(dstx, dsty)):
                return True, cls.RETURN_CODES['ok']
            else:
                return False, cls.RETURN_CODES['bishop-error']
        elif(piece == match.PIECES['wQu'] or piece == match.PIECES['bQu']):
            cqueen = cQueen(match, srcx, srcy)
            if(cqueen.is_move_valid(dstx, dsty)):
                return True, cls.RETURN_CODES['ok']
            else:
                return False, cls.RETURN_CODES['queen-error']
        elif(piece == match.PIECES['wKg'] or piece == match.PIECES['bKg']):
            cking = cKing(match, srcx, srcy)
            if(cking.is_move_valid(dstx, dsty)):
                return True, cls.RETURN_CODES['ok']
            else:
                return False, cls.RETURN_CODES['king-error']
        else:
            return False, cls.RETURN_CODES['general-error']    

    @classmethod
    def is_king_after_move_attacked(cls, match, srcx, srcy, dstx, dsty):
        piece = match.readfield(srcx, srcy)
        pawnenmy = None
        if(piece == match.PIECES['wPw']):
            cpawn = cPawn(match, srcx, srcy)
            if(cpawn.is_white_ep_move_ok(dstx, dsty)):
                pawnenmy = match.readfield(dstx, srcy)
                match.writefield(dstx, srcy, match.PIECES['blk'])
        elif(piece == match.PIECES['bPw']):
            cpawn = cPawn(match, srcx, srcy)
            if(cpawn.is_black_ep_move_ok(dstx, dsty)):
                pawnenmy = match.readfield(dstx, srcy)
                match.writefield(dstx, srcy, match.PIECES['blk'])

        match.writefield(srcx, srcy, match.PIECES['blk'])
        dstpiece = match.readfield(dstx, dsty)
        match.writefield(dstx, dsty, piece)

        if(match.color_of_piece(piece) == match.COLORS['white']):
            flag = cls.is_field_touched(match, match.COLORS['black'], match.board.wKg_x, match.board.wKg_y, 0)
        else:
            flag = cls.is_field_touched(match, match.COLORS['white'], match.board.bKg_x, match.board.bKg_y, 0)

        match.writefield(dstx, dsty, dstpiece)
        match.writefield(srcx, srcy, piece)
        if(pawnenmy):
            match.writefield(dstx, srcy, pawnenmy)

        return flag

    @classmethod
    def is_field_touched(cls, match, color, srcx, srcy, mode):
        crookfield = cRookField(match, srcx, srcy)
        if(crookfield.is_field_touched(color, mode)):
            return True
        cbishopfield = cBishopField(match, srcx, srcy)
        if(cbishopfield.is_field_touched(color, mode)):
            return True
        cknightfield = cKnightField(match, srcx, srcy)
        if(cknightfield.is_field_touched(color, mode)):
            return True
        ckingfield = cKingField(match, srcx, srcy)
        if(ckingfield.is_field_touched(color)):
            return True
        cpawnfield = cPawnField(match, srcx, srcy)
        if(cpawnfield.is_field_touched(color, mode)):
            return True
        return False

    @classmethod
    def is_move_available(cls, match):
        color = match.next_color()
        for y1 in range(8):
            for x1 in range(8):
                piece = match.readfield(x1, y1)
                if(color == match.color_of_piece(piece)):
                    if(piece == match.PIECES['wPw'] and y1 == match.board.COORD['7']):
                        prom_piece = match.PIECES['wQu']
                    elif(piece == match.PIECES['bPw'] and y1 == match.board.COORD['2']):
                        prom_piece = match.PIECES['bQu']
                    else:
                        prom_piece = match.PIECES['blk']
                    for y2 in range(8):
                        for x2 in range(8):
                            flag = cls.is_move_valid(match, x1, y1, x2, y2, prom_piece)[0]
                            if(flag):
                                return True
        return False

    @classmethod
    def evaluate_pin_dir(cls, match, srcx, srcy):
        cpieces = [cRook, cBishop]
        white_faces = [match.PIECES['wRk'], match.PIECES['wBp']]
        black_faces = [match.PIECES['bRk'], match.PIECES['bBp']]

        for idx in range(2):
            piece = match.readfield(srcx, srcy)
            color = match.color_of_piece(piece)
            if(color == match.COLORS['white']):
                kgx = match.board.wKg_x
                kgy = match.board.wKg_y
            else:
                kgx = match.board.bKg_x
                kgy = match.board.bKg_y
            direction = cpieces[idx].dir_for_move(srcx, srcy, kgx, kgy)
            if(direction != match.DIRS['undefined']):
                stepx, stepy = cpieces[idx].step_for_dir(direction)
                dstx, dsty = match.search(srcx, srcy, stepx, stepy)
                if(dstx is not None):
                    piece = match.readfield(dstx, dsty)
                    if( (color == match.COLORS['white'] and piece == match.PIECES['wKg']) or
                        (color == match.COLORS['black'] and piece == match.PIECES['bKg']) ):
                        reverse_dir = match.REVERSE_DIRS[direction]
                        stepx, stepy = cpieces[idx].step_for_dir(reverse_dir)
                        dstx, dsty = match.search(srcx, srcy, stepx, stepy)
                        if(dstx is not None):
                            piece = match.readfield(dstx, dsty)
                            if(color == match.COLORS['white']):
                                if(piece == match.PIECES['bQu'] or piece == black_faces[idx]):
                                    return direction
                                else:
                                    return match.DIRS['undefined']
                            else:
                                if(piece == match.PIECES['wQu'] or piece == white_faces[idx]):
                                    return direction
                                else:
                                    return match.DIRS['undefined']
        return match.DIRS['undefined']

    @classmethod
    def is_pinned(cls, match, x, y):
        piece = match.readfield(x, y)
        direction = cls.evaluate_pin_dir(x, y)
        return direction != match.DIRS['undefined']

    @classmethod
    def is_soft_pin(cls, match, srcx, srcy):
        piece = match.readfield(srcx, srcy)
        color = match.color_of_piece(piece)
        opp_color = match.oppcolor_of_piece(piece)
        crookfield = cRookField(match, srcx, srcy)
        enemies = crookfield.list_field_touches(opp_color)        
        for enemy in enemies:
            enemy_dir = cRook.dir_for_move(srcx, srcy, enemy.fieldx, enemy.fieldy)
            stepx, stepy = cRook.step_for_dir(match.REVERSE_DIRS[enemy_dir])
            x1, y1 = match.search(srcx, srcy, stepx, stepy)
            if(x1 is not None):
                friend = match.readfield(x1, y1)
                if(match.color_of_piece(friend) == color and 
                   match.PIECES_RANK[friend] > match.PIECES_RANK[piece] and 
                   match.PIECES_RANK[friend] > match.PIECES_RANK[enemy.piece]):
                    return True

        enemies.clear()
        cbishopfield = cBishopField(match, srcx, srcy)
        enemies = cbishopfield.list_field_touches(opp_color) 
        for enemy in enemies:
            enemy_dir = cBishop.dir_for_move(srcx, srcy, enemy.fieldx, enemy.fieldy)
            stepx, stepy = cBishop.step_for_dir(match.REVERSE_DIRS[enemy_dir])
            x1, y1 = match.search(srcx, srcy, stepx, stepy)
            if(x1 is not None):
                friend = match.readfield(x1, y1)
                if(match.color_of_piece(friend) == color and 
                   match.PIECES_RANK[friend] > match.PIECES_RANK[piece] and 
                   match.PIECES_RANK[friend] > match.PIECES_RANK[enemy.piece]):
                    return True
        return False

    @classmethod
    def dir_for_move(cls, match, srcx, srcy, dstx, dsty):
        piece = match.readfield(srcx, srcy)

        if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
            return cPawn.dir_for_move(srcx, srcy, dstx, dsty)
        elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
            return cRook.dir_for_move(srcx, srcy, dstx, dsty)
        elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
            return cKnight.dir_for_move(srcx, srcy, dstx, dsty)
        elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
            return cBishop.dir_for_move(srcx, srcy, dstx, dsty)
        elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
            return cQueen.dir_for_move(srcx, srcy, dstx, dsty)
        elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
            return cKing.dir_for_move(srcx, srcy, dstx, dsty)
        else:
            return cPiece.DIRS['undefined']

# class end
