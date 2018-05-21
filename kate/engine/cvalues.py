

TACTICS = {
    'defend-check' : 0,
    'defend-king-attack-urgent' : 1,
    'defend-king-attack' : 2,
    'promotion' : 3,
    'position-repeat' : 4,
    'capture-good-deal' : 5,
    'running-pawn-in-endgame' : 6, 
    'attack-king-good-deal' : 7,
    'does-unpin' : 8, 
    'attack-stormy' : 9,
    'flee-urgent' : 10,
    'support-good-deal' : 11,
    'discl-support-good-deal' : 12,
    'defend-fork' : 13,
    'attack-good-deal' : 14,
    'discl-attack-good-deal' : 15,
    'capture-bad-deal' : 16,
    'attack-king-bad-deal' : 17,
    'controles-file-good-deal' : 18,
    'castling' : 19,
    'defend-fork-downgraded' : 20,
    'flee-downgraded' : 21,
    'support-downgraded' : 22,
    'attack-downgraded' : 23,
    'support-unattacked' : 24,
    'progress' : 25, 
    'flee' : 26,
    'attack-bad-deal' : 27,
    'support-bad-deal' : 28,
    'undefined' : 29 }


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


TACTICS_TO_PRIO = {
      TACTICS['defend-check'] : PRIO['prio1'],
      TACTICS['defend-king-attack-urgent'] : PRIO['prio2'],
      TACTICS['defend-king-attack'] : PRIO['prio2'],
      TACTICS['promotion'] : PRIO['prio2'],
      TACTICS['position-repeat'] : PRIO['prio2'],
      TACTICS['capture-good-deal'] : PRIO['prio2'],
      TACTICS['running-pawn-in-endgame'] : PRIO['prio2'], 
      TACTICS['attack-king-good-deal'] : PRIO['prio2'],
      TACTICS['does-unpin'] : PRIO['prio2'], 
      TACTICS['attack-stormy'] : PRIO['prio3'],
      TACTICS['flee-urgent'] : PRIO['prio3'], 
      TACTICS['support-good-deal'] : PRIO['prio4'], 
      TACTICS['discl-support-good-deal'] : PRIO['prio4'], 
      TACTICS['defend-fork'] : PRIO['prio4'], 
      TACTICS['attack-good-deal'] : PRIO['prio4'], 
      TACTICS['discl-attack-good-deal'] : PRIO['prio4'], 
      TACTICS['capture-bad-deal'] : PRIO['prio5'], 
      TACTICS['attack-king-bad-deal'] : PRIO['prio5'], 
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

