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
        'prio0' : 0,
        'prio1' : 10,
        'prio2' : 20,
        'prio3' : 30,
        'prio4' : 40,
        'prio5' : 50 }

    TACTICS = {
        'defend-check' :         10,
        'capture' :              20,  # 'good-deal' | 'bad-deal'
        'attack-king' :          30,  # 'good-deal' | 'bad-deal'
        'attack' :               40,  # 'stormy' | 'good-deal' | 'bad-deal'
        'discl-attack' :         50,  # 'good-deal' | 'bad-deal' | 'downgraded'
        'support' :              60,  # 'good-deal' | 'bad-deal'
        'discl-support' :        70,  # 'good-deal' | 'bad-deal' | 'downgraded'
        'support-running-pawn' : 80,  # 'good-deal' | 'bad-deal'
        'support-unattacked' :   90,  # 'good-deal' | 'bad-deal'
        'flee' :                 100, # 'urgent' | 'downgraded'
        'defend-fork' :          110, # 'downgraded'
        'does-unpin' :           120,
        'block' :                130,
        'promotion' :            140, 
        'tactical-draw' :        150,
        'running-pawn' :         160, 
        'controle-file' :        170,
        'castling' :             180,
        'progress' :             190,
        'undefined' :            200 }

    SUB_TACTICS = {
        'stormy' : 1,
        'urgent' : 2,
        'good-deal' : 3,
        'downgraded' : 4,
        'bad-deal' : 5,
        'undefined' : 6 }

    TACTICS_TO_PRIO = {
        TACTICS['defend-check'] : PRIO['prio1'],
        TACTICS['capture'] : PRIO['prio2'],
        TACTICS['attack-king'] : PRIO['prio2'],
        TACTICS['attack'] : PRIO['prio3'],
        TACTICS['discl-attack'] : PRIO['prio3'],
        TACTICS['support'] : PRIO['prio3'],
        TACTICS['discl-support'] : PRIO['prio3'], 
        TACTICS['support-running-pawn'] : PRIO['prio3'], 
        TACTICS['support-unattacked'] : PRIO['prio4'],
        TACTICS['flee'] : PRIO['prio3'],
        TACTICS['defend-fork'] : PRIO['prio2'], 
        TACTICS['does-unpin'] : PRIO['prio2'], 
        TACTICS['block'] : PRIO['prio3'], 
        TACTICS['promotion'] : PRIO['prio2'],
        TACTICS['tactical-draw'] : PRIO['prio1'],
        TACTICS['running-pawn'] : PRIO['prio2'], 
        TACTICS['controle-file'] : PRIO['prio3'], 
        TACTICS['castling'] : PRIO['prio3'],
        TACTICS['progress'] : PRIO['prio3'], 
        TACTICS['undefined'] : PRIO['prio5'] }

    SUB_TACTICS_TO_ADJUST = {
        SUB_TACTICS['stormy'] : -10,
        SUB_TACTICS['urgent'] : -10,
        SUB_TACTICS['good-deal'] : -5,
        SUB_TACTICS['undefined'] : 0, 
        SUB_TACTICS['downgraded'] : 10,
        SUB_TACTICS['bad-deal'] : 15 }

    def __init__(self, gmove=None, prio=PRIO['prio5']):
        self.gmove = gmove
        self.tactics = []
        self.prio = prio

    def evaluate_priorities(self):
        self.prio = self.PRIO['prio5']
        if(self.tactics):
            for tactitem in self.tactics:
                prio_new = self.TACTICS_TO_PRIO[tactitem.tactic] + \
                           self.SUB_TACTICS_TO_ADJUST[tactitem.subtactic]
                self.prio = min(self.prio, prio_new)
            self.prio -= len(self.tactics)

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

    def has_subtactic(self, subtactic):
        for tactitem in self.tactics:
            if(tactitem.subtactic == subtactic):
                return True
        return False

    def is_tactic_stormy(self):
        for tactitem in self.tactics:
            if(tactitem.tactic == self.TACTICS['defend-check'] or
               tactitem.tactic == self.TACTICS['promotion'] or
               tactitem.tactic == self.TACTICS['capture'] or
               tactitem.tactic == self.TACTICS['attack-king'] or 
               (tactitem.tactic == self.TACTICS['attack'] and 
                (tactitem.subtactic == self.SUB_TACTICS['stormy'] or
                 tactitem.subtactic == self.SUB_TACTICS['urgent'] or
                 tactitem.subtactic == self.SUB_TACTICS['good-deal']))):
                return True
        return False

    def is_tactic_urgent(self):
        for tactitem in self.tactics:
            if(tactitem.tactic == self.TACTICS['promotion'] or
               tactitem.tactic == self.TACTICS['capture'] or
               (tactitem.tactic == self.TACTICS['attack'] and 
                (tactitem.subtactic == self.SUB_TACTICS['stormy'] or
                 tactitem.subtactic == self.SUB_TACTICS['urgent'] or
                 tactitem.subtactic == self.SUB_TACTICS['good-deal']))):
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
            if(tactitem.subtactic != self.SUB_TACTICS['undefined']):
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


