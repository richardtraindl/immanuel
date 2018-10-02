from .helper import reverse_lookup, index_to_coord
from .values import *


class cMove:
    TYPES = { 'standard' : 1, 
          'short_castling' : 2,
          'long_castling' : 3,
          'promotion' : 4,
          'en_passant' : 5 }

    def __init__(self, match=None, 
                       count=None, 
                       move_type=None, 
                       srcx=None, 
                       srcy=None, 
                       dstx=None, 
                       dsty=None, 
                       e_p_fieldx=None, 
                       e_p_fieldy=None, 
                       captured_piece=None, 
                       prom_piece=None, 
                       fifty_moves_count=None):
        self.match = match
        self.count = count
        self.move_type = move_type
        self.srcx = srcx
        self.srcy = srcy
        self.dstx = dstx
        self.dsty = dsty
        self.e_p_fieldx = e_p_fieldx
        self.e_p_fieldy = e_p_fieldy
        self.captured_piece = captured_piece
        self.prom_piece = prom_piece
        self.fifty_moves_count = fifty_moves_count


    def format_move(self):
        if(self.move_type == self.TYPES['standard']):
            if(self.captured_piece == 0):
                hyphen = "-"
            else:
                hyphen = "x"
            fmtmove = index_to_coord(self.srcx, self.srcy) + hyphen + \
                      index_to_coord(self.dstx, self.dsty)
            return fmtmove
        elif(self.move_type == self.TYPES['short_castling']):
            return "0-0"
        elif(self.move_type == self.TYPES['long_castling']):
            return "0-0-0"
        elif(self.move_type == self.TYPES['promotion']):
            if(self.captured_piece == 0):
                hyphen = "-"
            else:
                hyphen = "x"
            fmtmove = index_to_coord(self.srcx, self.srcy) + hyphen + \
                      index_to_coord(self.dstx, self.dsty) + " " + \
                      reverse_lookup(PIECES, self.prom_piece)
            return fmtmove
        else:
            fmtmove = index_to_coord(self.srcx, self.srcy) + "x" + \
                      index_to_coord(self.dstx, self.dsty) + " e.p."
            return fmtmove
            
    def prnt_move(self, headmsg, tailmsg):
        print(headmsg + 
            index_to_coord(self.srcx, self.srcy) + "-" +
            index_to_coord(self.dstx, self.dsty), end="")

        if(self.prom_piece != PIECES['blk']):
            print(" " + reverse_lookup(PIECES, self.prom_piece), end="")
        print(tailmsg, end="")

# class end


class cGenMove(object):
    def __init__(self, match=None, srcx=None, srcy=None, dstx=None, dsty=None, prom_piece=None):
        self.match = match
        self.srcx = srcx
        self.srcy = srcy
        self.dstx = dstx
        self.dsty = dsty
        self.prom_piece = prom_piece

    def format_genmove(self):
        piece = self.match.readfield(self.srcx, self.srcy)
        dstpiece = self.match.readfield(self.dstx, self.dsty)

        if(dstpiece != PIECES['blk']):
            hyphen = "x"
        elif( (piece == PIECES['wPw'] or piece == PIECES['bPw']) and 
               self.srcx != self.dstx ):
            hyphen = "x"
        else:
            hyphen = "-"

        if(self.prom_piece and self.prom_piece != PIECES['blk']):
            trailing = ", " + reverse_lookup(PIECES, self.prom_piece)
        else:
            trailing = ""

        fmtmove = index_to_coord(self.srcx, self.srcy) + \
                  hyphen + \
                  index_to_coord(self.dstx, self.dsty) + \
                  trailing
        return fmtmove

# class end


class cTactic:
    def __init__(self, tactic=None, subtactic=None):
        self.tactic = tactic
        self.subtactic = subtactic
# class end

class cPrioMove:
    PRIO = {
        'prio1' : 0,
        'prio2' : 1,
        'prio3' : 2,
        'prio4' : 3,
        'prio5' : 4,
        'prio6' : 5,
        'prio7' : 6,
        'prio8' : 7,
        'prio9' : 8,
        'prio10' : 9 }

    TACTICS = {
        'defend-check' :        10,
        'capture' :             20,  # 'good-deal' | 'bad-deal'
        'attack-king' :         30,  # 'good-deal' | 'bad-deal'
        'attack' :              40,  # 'stormy' | 'good-deal' | 'bad-deal'
        'discl-attack' :        50,  # 'good-deal' | 'bad-deal' | 'downgraded'
        'support' :             60,  # 'good-deal' | 'bad-deal'
        'discl-support' :       70,  # 'good-deal' | 'bad-deal' | 'downgraded'
        'support-unattacked' :  80,  # 'good-deal' | 'bad-deal'
        'flee' :                90,  # 'urgent' | 'downgraded'
        'defend-fork' :         100, # 'downgraded'
        'does-unpin' :          110,
        'block' :               120,
        'promotion' :           130, 
        'tactical-draw' :       140,
        'running-pawn' :        150, 
        'controle-file' :       160,
        'castling' :            170,
        'progress' :            180,
        'undefined' :           200 }

    SUB_TACTICS = {
        'stormy' : 1,
        'urgent' : 2,
        'good-deal' : 3,
        'downgraded' : 4,
        'bad-deal' : 5,
        'undefined' : 6 }

    TACTICS_TO_PRIO = {
        TACTICS['defend-check'] : PRIO['prio2'],
        TACTICS['capture'] : PRIO['prio4'],
        TACTICS['attack-king'] : PRIO['prio4'],
        TACTICS['attack'] : PRIO['prio5'],
        TACTICS['discl-attack'] : PRIO['prio5'],
        TACTICS['support'] : PRIO['prio5'],
        TACTICS['discl-support'] : PRIO['prio5'], 
        TACTICS['support-unattacked'] : PRIO['prio7'],
        TACTICS['flee'] : PRIO['prio5'],
        TACTICS['defend-fork'] : PRIO['prio4'], 
        TACTICS['does-unpin'] : PRIO['prio4'], 
        TACTICS['block'] : PRIO['prio5'], 
        TACTICS['promotion'] : PRIO['prio4'],
        TACTICS['tactical-draw'] : PRIO['prio4'],
        TACTICS['running-pawn'] : PRIO['prio4'], 
        TACTICS['controle-file'] : PRIO['prio6'], 
        TACTICS['castling'] : PRIO['prio5'],
        TACTICS['progress'] : PRIO['prio7'], 
        TACTICS['undefined'] : PRIO['prio10'] }

    SUB_TACTICS_TO_ADJUST = {
        SUB_TACTICS['stormy'] : -2,
        SUB_TACTICS['urgent'] : -2,
        SUB_TACTICS['good-deal'] : -1,
        SUB_TACTICS['downgraded'] : 0,
        SUB_TACTICS['bad-deal'] : 1,
        SUB_TACTICS['undefined'] : 2 }

    def __init__(self, gmove=None):
        self.gmove = gmove
        self.tactics = []
        self.prio = self.PRIO['prio10']
        self.prio_sec = self.PRIO['prio10']

    def evaluate_prio(self):
        prio = self.PRIO['prio10']
        for tactitem in self.tactics:
            prio_new = max(self.PRIO['prio1'], 
                              self.TACTICS_TO_PRIO[tactitem.tactic] + \
                              self.SUB_TACTICS_TO_ADJUST[tactitem.subtactic])
            prio = min(prio, prio_new)
        return prio

    def downgrade(self, tactic):
        for tactitem in self.tactics:
            if(tactitem.tactic == tactic.tactic):
                tactitem.subtactic = self.SUB_TACTICS['downgraded']
                return

    def fetch_tactics(self, idx):
        if(len(self.tactics) > idx):
            return self.tactics[idx].tactic
        else:
            return self.TACTICS['undefined']
    
    def has_tactic(self, tactic):
        for tactitem in self.tactics:
            if(tactitem.tactic == tactic.tactic):
                return True
        return False

    def has_tactic_ext(self, tactic):
        for tactitem in self.tactics:
            if(tactitem.tactic == tactic.tactic and tactitem.subtactic == tactic.subtactic):
                return True
        return False

    def is_tactic_stormy(self):
        for tactitem in self.tactics:
            if(tactitem.tactic == self.TACTICS['defend-check'] or
               tactitem.tactic == self.TACTICS['promotion'] or
               tactitem.tactic == self.TACTICS['capture'] or
               tactitem.tactic == self.TACTICS['attack-king'] or 
               (tactitem.tactic == self.TACTICS['attack'] and 
                tactitem.subtactic == self.SUB_TACTICS['good-deal'])):
                return True
        return False

    def is_tactic_urgent(self):
        for tactitem in self.tactics:
            if(tactitem.tactic == self.TACTICS['promotion'] or
               tactitem.tactic == self.TACTICS['capture']):
                return True
        return False

    def is_tactic_silent(self):
        for tactitem in self.tactics:
            if((tactitem.tactic == self.TACTICS['capture'] and
                tactitem.subtactic == self.SUB_TACTICS['bad-deal']) or
               (tactitem.tactic == self.TACTICS['attack-king'] and
                tactitem.subtactic == self.SUB_TACTICS['bad-deal']) or               
               (tactitem.tactic == self.TACTICS['attack'] and
                tactitem.subtactic == self.SUB_TACTICS['bad-deal']) or
               (tactitem.tactic == self.TACTICS[ 'support'] and 
                tactitem.subtactic == self.SUB_TACTICS[ 'bad-deal'])):
                return False
        return True

    def concat_tactics(self, delimiter):
        str_tactics = ""
        length = len(self.tactics)
        i = 1
        for tactitem in self.tactics:
            str_tactics += reverse_lookup(self.TACTICS, tactitem.tactic)
            if((tactitem.subtactic and tactitem.subtactic != self.SUB_TACTICS['undefined']):
                str_tactics += " * " + reverse_lookup(self.SUB_TACTICS, tactitem.subtactic)
            if(i < length):
                str_tactics += delimiter
            i += 1
        return str_tactics

    def prnt_tactics(self):
        length = len(self.tactics)
        i = 1
        for tactitem in self.tactics:
            if(i < length):
                str_end = " | "
            else:
                str_end = ""
            if(tactitem.subtactic != self.SUB_TACTICS['undefined']):
                subtactic_str = " * " + reverse_lookup(self.SUB_TACTICS, tactitem.subtactic)
            else:
                subtactic_str = ""
            print(reverse_lookup(self.TACTICS, tactitem.tactic) + subtactic_str, end=str_end)
            i += 1

# class end


