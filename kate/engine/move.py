from .helper import reverse_lookup, index_to_coord


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
                      reverse_lookup(self.match.PIECES, self.prom_piece)
            return fmtmove
        else:
            fmtmove = index_to_coord(self.srcx, self.srcy) + "x" + \
                      index_to_coord(self.dstx, self.dsty) + " e.p."
            return fmtmove
            
    def prnt_move(self, headmsg, tailmsg):
        print(headmsg + 
            index_to_coord(self.srcx, self.srcy) + "-" +
            index_to_coord(self.dstx, self.dsty), end="")

        if(self.prom_piece != self.match.PIECES['blk']):
            print(" " + reverse_lookup(self.match.PIECES, self.prom_piece), end="")
        print(tailmsg, end="")

# class end


class GenMove(object):
    def __init__(self, srcx=None, srcy=None, dstx=None, dsty=None, prom_piece=None):
        self.srcx = srcx
        self.srcy = srcy
        self.dstx = dstx
        self.dsty = dsty
        self.prom_piece = prom_piece

    def format_genmove(self):
        fmtmove = index_to_coord(self.srcx, self.srcy) + \
                  "-" + \
                  index_to_coord(self.dstx, self.dsty)
        return fmtmove

# class end


class PrioMove:
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
        'defend-check' : 0,
        'defend-king-attack-urgent' : 1,
        'defend-king-attack' : 2,
        'promotion' : 3,
        'tactical-draw' : 4,
        'capture-good-deal' : 5,
        'running-pawn-in-endgame' : 6, 
        'attack-king-good-deal' : 7,
        'does-unpin' : 8, 
        'attack-stormy' : 9,
        'flee-urgent' : 10,
        'support-good-deal' : 11,
        'block' : 12,
        'discl-support-good-deal' : 13,
        'defend-fork' : 14,
        'attack-good-deal' : 15,
        'discl-attack-good-deal' : 16,
        'controles-file-good-deal' : 17,
        'castling' : 18,
        'capture-bad-deal' : 19,
        'attack-king-bad-deal' : 20,
        'defend-fork-downgraded' : 21,
        'flee-downgraded' : 22,
        'support-downgraded' : 23,
        'attack-downgraded' : 24,
        'support-unattacked' : 25,
        'progress' : 26, 
        'flee' : 27,
        'attack-bad-deal' : 28,
        'support-bad-deal' : 29,
        'undefined' : 30 }

    TACTICS_TO_PRIO = {
          TACTICS['defend-check'] : PRIO['prio1'],
          TACTICS['defend-king-attack-urgent'] : PRIO['prio2'],
          TACTICS['defend-king-attack'] : PRIO['prio2'],
          TACTICS['promotion'] : PRIO['prio2'],
          TACTICS['tactical-draw'] : PRIO['prio2'],
          TACTICS['capture-good-deal'] : PRIO['prio2'],
          TACTICS['running-pawn-in-endgame'] : PRIO['prio2'], 
          TACTICS['attack-king-good-deal'] : PRIO['prio2'],
          TACTICS['does-unpin'] : PRIO['prio2'], 
          TACTICS['attack-stormy'] : PRIO['prio3'],
          TACTICS['flee-urgent'] : PRIO['prio3'], 
          TACTICS['support-good-deal'] : PRIO['prio4'], 
          TACTICS['block'] : PRIO['prio4'], 
          TACTICS['discl-support-good-deal'] : PRIO['prio4'], 
          TACTICS['defend-fork'] : PRIO['prio4'], 
          TACTICS['attack-good-deal'] : PRIO['prio4'], 
          TACTICS['discl-attack-good-deal'] : PRIO['prio4'], 
          TACTICS['controles-file-good-deal'] : PRIO['prio5'], 
          TACTICS['castling'] : PRIO['prio5'],
          TACTICS['capture-bad-deal'] : PRIO['prio6'], 
          TACTICS['attack-king-bad-deal'] : PRIO['prio6'], 
          TACTICS['defend-fork-downgraded'] : PRIO['prio7'], 
          TACTICS['flee-downgraded'] : PRIO['prio7'], 
          TACTICS['support-downgraded'] : PRIO['prio7'], 
          TACTICS['attack-downgraded'] : PRIO['prio7'],
          TACTICS['support-unattacked'] : PRIO['prio8'], 
          TACTICS['progress'] : PRIO['prio8'], 
          TACTICS['flee'] : PRIO['prio8'],
          TACTICS['attack-bad-deal'] : PRIO['prio9'], 
          TACTICS['support-bad-deal'] : PRIO['prio9'],
          TACTICS['undefined'] : PRIO['prio10'] }

    def __init__(self, gmove=None):
        self.gmove = gmove
        self.tactics = []
        self.prio = self.PRIO['prio10']
        self.prio_sec = self.PRIO['prio10']

    def downgrade(self, old_tactic, new_tactic):
        self.prio = self.TACTICS_TO_PRIO[new_tactic]
        for idx in range(len(self.tactics)):
            if(self.tactics[idx] == old_tactic):
                self.tactics[idx] = new_tactic
                return

    def fetch_tactics(self, idx):
        if(len(self.tactics) > idx):
            return self.tactics[idx]
        else:
            return self.TACTICS['undefined']
    
    def find_tactic(self, tactic):
        for tactic_item in self.tactics:
            if(tactic_item == tactic):
                return True
        return False

    def is_tactic_stormy(self):
        for tactic in self.tactics:
            if(tactic == self.TACTICS['defend-check'] or
               tactic == self.TACTICS['defend-king-attack-urgent'] or
               tactic == self.TACTICS['defend-king-attack'] or
               tactic == self.TACTICS['promotion'] or
               tactic == self.TACTICS['capture-good-deal'] or
               tactic == self.TACTICS['attack-king-good-deal'] or 
               tactic == self.TACTICS['capture-bad-deal'] or 
               tactic == self.TACTICS['attack-king-bad-deal'] or
               tactic == self.TACTICS['attack-stormy']):
                return True
        return False

    def is_tactic_urgent(self):
        for tactic in self.tactics:
            if(tactic == self.TACTICS['promotion'] or
               tactic == self.TACTICS['capture-good-deal']): # tactic == self.TACTICS['defend-check'] or or tactic == self.TACTICS['capture-bad-deal']
                return True
        return False

    def concat_tactics(self, delimiter):
        str_tactics = ""
        length = len(self.tactics)
        i = 1
        for tactic in self.tactics:
            str_tactics += reverse_lookup(self.TACTICS, tactic)

            if(i < length):
                str_tactics += delimiter
            i += 1
        return str_tactics

    def prnt_tactics(self):
        length = len(self.tactics)
        i = 1
        for tactic in self.tactics:
            if(i < length):
                print(reverse_lookup(self.TACTICS, tactic), end=" | ")
            else:
                print(reverse_lookup(self.TACTICS, tactic), end="")
            i += 1

# class end


