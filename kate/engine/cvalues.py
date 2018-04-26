

TACTICS = {
    'defend-check' : 0,
    'promotion' : 1,
    'capture-good-deal' : 2,
    'running-pawn-in-endgame' : 3, 
    'attack-king-good-deal' : 4,
    'single-silent-move' : 5,
    'capture-bad-deal' : 6,
    'attack-king-bad-deal' : 7,
    'attack-stormy' : 8,
    'defend-fork' : 9,
    'flee-urgent' : 10,
    'support-good-deal' : 11,
    'attack-good-deal' : 12,
    'disclosed-attack-good-deal' : 13,
    'controles-file-good-deal' : 14,
    'castling' : 15,
    'defend-fork-downgraded' : 16,
    'flee-downgraded' : 17,
    'support-downgraded' : 18,
    'attack-downgraded' : 19,
    'support-unattacked' : 20,
    'progress' : 21, 
    'flee' : 22,
    'attack-bad-deal' : 23,
    'support-bad-deal' : 24,
    'undefined' : 25 }


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


PRIO_MIN = PRIO['prio2']
PRIO_MID = PRIO['prio3']
PRIO_MAX = PRIO['prio5']


TACTICS_TO_PRIO = {
      TACTICS['defend-check'] : PRIO['prio1'],
      TACTICS['promotion'] : PRIO['prio2'],
      TACTICS['capture-good-deal'] : PRIO['prio2'],
      TACTICS['running-pawn-in-endgame'] : PRIO['prio2'], 
      TACTICS['attack-king-good-deal'] : PRIO['prio2'],
      TACTICS['single-silent-move'] : PRIO['prio2'],      
      TACTICS['capture-bad-deal'] : PRIO['prio3'], 
      TACTICS['attack-king-bad-deal'] : PRIO['prio3'], 
      TACTICS['attack-stormy'] : PRIO['prio3'],
      TACTICS['defend-fork'] : PRIO['prio4'], 
      TACTICS['flee-urgent'] : PRIO['prio4'], 
      TACTICS['support-good-deal'] : PRIO['prio5'], 
      TACTICS['attack-good-deal'] : PRIO['prio5'], 
      TACTICS['disclosed-attack-good-deal'] : PRIO['prio5'], 
      TACTICS['controles-file-good-deal'] : PRIO['prio5'], 
      TACTICS['castling'] : PRIO['prio5'],
      TACTICS['defend-fork-downgraded'] : PRIO['prio6'], 
      TACTICS['flee-downgraded'] : PRIO['prio6'], 
      TACTICS['support-downgraded'] : PRIO['prio6'], 
      TACTICS['attack-downgraded'] : PRIO['prio6'],
      TACTICS['support-unattacked'] : PRIO['prio7'], 
      TACTICS['progress'] : PRIO['prio7'], 
      TACTICS['flee'] : PRIO['prio7'],
      TACTICS['attack-bad-deal'] : PRIO['prio8'], 
      TACTICS['support-bad-deal'] : PRIO['prio8'],
      TACTICS['undefined'] : PRIO['prio10'] }

