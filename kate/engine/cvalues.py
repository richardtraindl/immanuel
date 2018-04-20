

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

PRIO_LIMES3 = PRIO['prio2']
PRIO_LIMES2 = PRIO['prio3']
PRIO_LIMES1 = PRIO['prio5']


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


ANALYSES = {
    'MV_PIECE_IS_PW' : 0,
    'MV_PIECE_IS_KN' : 1,
    'MV_PIECE_IS_BP' : 2,
    'MV_PIECE_IS_RK' : 3,
    'MV_PIECE_IS_QU' : 4,
    'MV_PIECE_IS_KG' : 5,

    'SRCFLD_IS_FRDL_TOU_BY_PW' : 10,
    'SRCFLD_IS_FRDL_TOU_BY_KN' : 11,
    'SRCFLD_IS_FRDL_TOU_BY_BP' : 12,
    'SRCFLD_IS_FRDL_TOU_BY_RK' : 13,
    'SRCFLD_IS_FRDL_TOU_BY_QU' : 14,
    'SRCFLD_IS_FRDL_TOU_BY_KG' : 15,

    'SRCFLD_IS_ENM_TOU_BY_PW' : 20,
    'SRCFLD_IS_ENM_TOU_BY_KN' : 21,
    'SRCFLD_IS_ENM_TOU_BY_BP' : 22,
    'SRCFLD_IS_ENM_TOU_BY_RK' : 23,
    'SRCFLD_IS_ENM_TOU_BY_QU' : 24,
    'SRCFLD_IS_ENM_TOU_BY_KG' : 25,

    'DSTFLD_IS_FRDL_TOU_BY_PW' : 30,
    'DSTFLD_IS_FRDL_TOU_BY_KN' : 31,
    'DSTFLD_IS_FRDL_TOU_BY_BP' : 32,
    'DSTFLD_IS_FRDL_TOU_BY_RK' : 33,
    'DSTFLD_IS_FRDL_TOU_BY_QU' : 34,
    'DSTFLD_IS_FRDL_TOU_BY_KG' : 35,

    'DSTFLD_IS_ENM_TOU_BY_PW' : 40,
    'DSTFLD_IS_ENM_TOU_BY_KN' : 41,
    'DSTFLD_IS_ENM_TOU_BY_BP' : 42,
    'DSTFLD_IS_ENM_TOU_BY_RK' : 43,
    'DSTFLD_IS_ENM_TOU_BY_QU' : 44,
    'DSTFLD_IS_ENM_TOU_BY_KG' : 45,

    'CAPTURED_IS_PW' : 50,
    'CAPTURED_IS_KN' : 51,
    'CAPTURED_IS_BP' : 52,
    'CAPTURED_IS_RK' : 53,
    'CAPTURED_IS_QU' : 54,

    'ATTACKED_IS_PW' : 60,
    'ATTACKED_IS_KN' : 61,
    'ATTACKED_IS_BP' : 62,
    'ATTACKED_IS_RK' : 63,
    'ATTACKED_IS_QU' : 64,
    'ATTACKED_IS_KG' : 65,

    'ATTACK_IS_PIN'      : 70,
    'ATTACK_IS_SOFT_PIN' : 71,

    'SUPPORTED_IS_PW' : 80,
    'SUPPORTED_IS_KN' : 81,
    'SUPPORTED_IS_BP' : 82,
    'SUPPORTED_IS_RK' : 83,
    'SUPPORTED_IS_QU' : 84, 

    'MV_IS_CASTLING'           : 90,
    'MV_IS_PROMOTION'          : 91,
    'MV_IS_CAPTURE'            : 92,    
    'MV_IS_ATTACK'             : 93,
    'MV_IS_DISCLOSURE'         : 94,
    'MV_IS_FORK'               : 95,
    'MV_IS_FORK_DEFENSE'       : 96,
    'MV_DEFENDS_CHECK'         : 97,
    'MV_IS_SUPPORT'            : 98,
    'MV_IS_SUPPORT_UNATTACKED' : 99,
    'MV_IS_FLEE'               : 100,
    'MV_IS_PROGRESS'           : 101,
    'MV_IS_RUNNING_PAWN'       : 102,
    'MV_CONTROLES_FILE'        : 103 }

