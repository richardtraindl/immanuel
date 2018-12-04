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
        'defends-check' :         10,
        'captures' :              20,
        'attacks-king' :          30,
        'attacks' :               40,
        'supports' :              50,
        'supports-running-pawn' : 60,
        'supports-unattacked' :   70,
        'flees' :                 80,
        'forks' :                 90,
        'defends-fork' :          100,
        'pins' :                  110,
        'unpins' :                120,
        'blocks' :                130,
        'promotes' :              140, 
        'is-tactical-draw' :      150,
        'is-running-pawn' :       160, 
        'controles-file' :        170,
        'castles' :               180,
        'is-progress' :           190,
        'is-undefined' :          200 }

    SUB_TACTICS = {
        'stormy' : 1,
        'urgent' : 2,
        'good-deal' : 3,
        'downgraded' : 4,
        'upgraded' : 5,
        'bad-deal' : 6,
        'neutral' : 7 }

    TACTICS_TO_PRIO = {
        TACTICS['promotes'] :               13,
        TACTICS['captures'] :               14,
        TACTICS['is-running-pawn'] :        14, 
        TACTICS['is-tactical-draw'] :       15,
        TACTICS['castles'] :                20,
        TACTICS['attacks-king'] :           20,
        TACTICS['forks'] :                  23, 
        TACTICS['defends-fork'] :           23, 
        TACTICS['pins'] :                   23, 
        TACTICS['unpins'] :                 23, 
        TACTICS['supports-running-pawn'] :  24, 
        TACTICS['supports'] :               24,
        TACTICS['flees'] :                  24, 
        TACTICS['blocks'] :                 24,
        TACTICS['attacks'] :                25,
        TACTICS['controles-file'] :         33, 
        TACTICS['is-progress'] :            33,
        TACTICS['supports-unattacked'] :    33,
        TACTICS['defends-check']  :         50, 
        TACTICS['is-undefined'] :           50 }

    SUB_TACTICS_TO_ADJUST = {
        SUB_TACTICS['stormy'] : -7,
        SUB_TACTICS['urgent'] : -7,
        SUB_TACTICS['good-deal'] : 0,
        SUB_TACTICS['neutral'] : 0,
        SUB_TACTICS['downgraded'] : 4,
        SUB_TACTICS['upgraded'] : 0,
        SUB_TACTICS['bad-deal'] : 13 }

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

    def downgrade(self, domain_tactic):
        for tactic in self.tactics:
            if(tactic.tactic == domain_tactic):
                if(tactic.subtactic == self.SUB_TACTICS['stormy'] or
                   tactic.subtactic == self.SUB_TACTICS['urgent'] or 
                   tactic.subtactic == self.SUB_TACTICS['good-deal']):
                    tactic.subtactic = self.SUB_TACTICS['downgraded']
                return

    def upgrade(self, domain_tactic):
        for tactic in self.tactics:
            if(tactic.tactic == domain_tactic):
                if(tactic.subtactic != self.SUB_TACTICS['stormy'] and 
                   tactic.subtactic != self.SUB_TACTICS['urgent'] and 
                   tactic.subtactic != self.SUB_TACTICS['good-deal']):
                    tactic.subtactic = self.SUB_TACTICS['upgraded']
                    return

    def fetch_tactics(self, idx):
        if(len(self.tactics) > idx):
            return self.tactics[idx].tactic
        else:
            return self.TACTICS['is-undefined']

    def has_tactic(self, tactic):
        for tactitem in self.tactics:
            if(tactitem.tactic == tactic.tactic and
               tactitem.subtactic == tactic.subtactic):
                return True
        return False
    
    def has_domain_tactic(self, domain_tactic):
        for tactitem in self.tactics:
            if(tactitem.tactic == domain_tactic):
                return True
        return False

    def has_subtactic(self, subtactic):
        for tactitem in self.tactics:
            if(tactitem.subtactic == subtactic):
                return True
        return False

    def has_tactic_ext(self, tactic):
        for tactitem in self.tactics:
            if(tactitem.tactic == tactic.tactic and tactitem.subtactic == tactic.subtactic):
                return True
        return False

    def is_tactic_stormy(self, with_check):
        for tactitem in self.tactics:
            if((tactitem.tactic == self.TACTICS['promotes'] or
                tactitem.tactic == self.TACTICS['captures']) and 
                tactitem.subtactic <= self.SUB_TACTICS['good-deal']):
                return True
            if(with_check):
                # tactitem.tactic == self.TACTICS['defends-check'])
                if(tactitem.tactic == self.TACTICS['attacks-king'] and 
                   tactitem.subtactic <= self.SUB_TACTICS['good-deal']):
                    return True
        return False

    def concat_tactics(self, delimiter):
        str_tactics = ""
        length = len(self.tactics)
        i = 1
        for tactitem in self.tactics:
            str_tactics += reverse_lookup(self.TACTICS, tactitem.tactic)
            if(tactitem.subtactic != self.SUB_TACTICS['neutral']):
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
            if(tactitem.subtactic != self.SUB_TACTICS['neutral']):
                subtactic_str = " * " + reverse_lookup(self.SUB_TACTICS, tactitem.subtactic)
            else:
                subtactic_str = ""
            print(reverse_lookup(self.TACTICS, tactitem.tactic) + subtactic_str, end=str_end)
            i += 1

# class end


