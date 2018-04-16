

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

PRIO2 = {
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
    'controles-file-good-deal' : 13,
    'castling' : 14,
    'flee' : 15,
    'good' : 16,
    'support-unattacked' : 17,
    'attack-bad-deal' : 18,
    'support-bad-deal' : 19,
    'last' : 20 }

PRIO2_LIMES3 = PRIO2['single-silent-move'] # attack-king-bad-deal
PRIO2_LIMES2 = PRIO2['attack-stormy']
PRIO2_LIMES1 = PRIO2['castling']


MV_IS_PROMOTION                        = 0x80000000000000000
MV_IS_CAPTURE                          = 0x40000000000000000
MV_IS_ATTACK                           = 0x20000000000000000
MV_IS_DISCLOSURE                       = 0x10000000000000000
MV_IS_FORK                             = 0x08000000000000000
MV_IS_FORK_DEFENSE                     = 0x04000000000000000
MV_DEFENDS_CHECK                       = 0x02000000000000000
MV_IS_CASTLING                         = 0x01000000000000000
MV_IS_SUPPORT                          = 0x00800000000000000
MV_IS_FLEE                             = 0x00400000000000000
MV_IS_SUPPORT_UNATTACKED               = 0x00200000000000000
MV_IS_PROGRESS                         = 0x00100000000000000
MV_IS_RUNNING_PAWN                     = 0x00080000000000000
MV_CONTROLES_FILE                      = 0x00040000000000000

MV_PIECE_IS_PW                         = 0x0000800000000000
MV_PIECE_IS_KN                         = 0x0000400000000000
MV_PIECE_IS_BP                         = 0x0000200000000000
MV_PIECE_IS_RK                         = 0x0000100000000000
MV_PIECE_IS_QU                         = 0x0000080000000000
MV_PIECE_IS_KG                         = 0x0000040000000000

SRCFLD_IS_FRDL_TOU_BY_PW               = 0x0000020000000000
SRCFLD_IS_FRDL_TOU_BY_KN               = 0x0000010000000000
SRCFLD_IS_FRDL_TOU_BY_BP               = 0x0000008000000000
SRCFLD_IS_FRDL_TOU_BY_RK               = 0x0000004000000000
SRCFLD_IS_FRDL_TOU_BY_QU               = 0x0000002000000000
SRCFLD_IS_FRDL_TOU_BY_KG               = 0x0000001000000000

SRCFLD_IS_ENM_TOU_BY_PW                = 0x0000000800000000
SRCFLD_IS_ENM_TOU_BY_KN                = 0x0000000400000000
SRCFLD_IS_ENM_TOU_BY_BP                = 0x0000000200000000
SRCFLD_IS_ENM_TOU_BY_RK                = 0x0000000100000000
SRCFLD_IS_ENM_TOU_BY_QU                = 0x0000000080000000
SRCFLD_IS_ENM_TOU_BY_KG                = 0x0000000040000000

DSTFLD_IS_FRDL_TOU_BY_PW               = 0x0000000020000000
DSTFLD_IS_FRDL_TOU_BY_KN               = 0x0000000010000000
DSTFLD_IS_FRDL_TOU_BY_BP               = 0x0000000008000000
DSTFLD_IS_FRDL_TOU_BY_RK               = 0x0000000004000000
DSTFLD_IS_FRDL_TOU_BY_QU               = 0x0000000002000000
DSTFLD_IS_FRDL_TOU_BY_KG               = 0x0000000001000000

DSTFLD_IS_ENM_TOU_BY_PW                = 0x0000000000800000
DSTFLD_IS_ENM_TOU_BY_KN                = 0x0000000000400000
DSTFLD_IS_ENM_TOU_BY_BP                = 0x0000000000200000
DSTFLD_IS_ENM_TOU_BY_RK                = 0x0000000000100000
DSTFLD_IS_ENM_TOU_BY_QU                = 0x0000000000080000
DSTFLD_IS_ENM_TOU_BY_KG                = 0x0000000000040000

CAPTURED_IS_PW                         = 0x0000000000020000
CAPTURED_IS_KN                         = 0x0000000000010000
CAPTURED_IS_BP                         = 0x0000000000008000
CAPTURED_IS_RK                         = 0x0000000000004000
CAPTURED_IS_QU                         = 0x0000000000002000

ATTACKED_IS_PW                         = 0x0000000000001000
ATTACKED_IS_KN                         = 0x0000000000000800
ATTACKED_IS_BP                         = 0x0000000000000400
ATTACKED_IS_RK                         = 0x0000000000000200
ATTACKED_IS_QU                         = 0x0000000000000100
ATTACKED_IS_KG                         = 0x0000000000000080

ATTACK_IS_PIN                          = 0x0000000000000040
ATTACK_IS_SOFT_PIN                     = 0x0000000000000020

SUPPORTED_IS_PW                        = 0x0000000000000010
SUPPORTED_IS_KN                        = 0x0000000000000008
SUPPORTED_IS_BP                        = 0x0000000000000004
SUPPORTED_IS_RK                        = 0x0000000000000002
SUPPORTED_IS_QU                        = 0x0000000000000001

TOKEN_TEXT = {
    MV_IS_CASTLING : "MV_IS_CASTLING",
    MV_IS_PROMOTION : "MV_IS_PROMOTION",
    MV_IS_CAPTURE : "MV_IS_CAPTURE",
    MV_IS_ATTACK : "MV_IS_ATTACK",
    MV_IS_DISCLOSURE : "MV_IS_DISCLOSURE",
    MV_IS_FORK : "MV_IS_FORK",
    MV_IS_FORK_DEFENSE : "MV_IS_FORK_DEFENSE",
    MV_DEFENDS_CHECK : "MV_DEFENDS_CHECK",    
    MV_IS_SUPPORT : "MV_IS_SUPPORT",
    MV_IS_SUPPORT_UNATTACKED : "MV_IS_SUPPORT_UNATTACKED",
    MV_IS_FLEE : "MV_IS_FLEE",
    MV_IS_PROGRESS : "MV_IS_PROGRESS",
    MV_IS_RUNNING_PAWN : "MV_IS_RUNNING_PAWN",
    MV_CONTROLES_FILE : "MV_CONTROLES_FILE",
    MV_PIECE_IS_PW : "MV_PIECE_IS_PW",
    MV_PIECE_IS_KN : "MV_PIECE_IS_KN",
    MV_PIECE_IS_BP : "MV_PIECE_IS_BP",
    MV_PIECE_IS_RK : "MV_PIECE_IS_RK",    
    MV_PIECE_IS_QU : "MV_PIECE_IS_QU",
    MV_PIECE_IS_KG : "MV_PIECE_IS_KG",
    SRCFLD_IS_FRDL_TOU_BY_PW : "SRCFLD_IS_FRDL_TOU_BY_PW",
    SRCFLD_IS_FRDL_TOU_BY_KN : "SRCFLD_IS_FRDL_TOU_BY_KN",
    SRCFLD_IS_FRDL_TOU_BY_BP : "SRCFLD_IS_FRDL_TOU_BY_BP",
    SRCFLD_IS_FRDL_TOU_BY_RK : "SRCFLD_IS_FRDL_TOU_BY_RK",
    SRCFLD_IS_FRDL_TOU_BY_QU : "SRCFLD_IS_FRDL_TOU_BY_QU",
    SRCFLD_IS_FRDL_TOU_BY_KG : "SRCFLD_IS_FRDL_TOU_BY_KG",
    SRCFLD_IS_ENM_TOU_BY_PW : "SRCFLD_IS_ENM_TOU_BY_PW",
    SRCFLD_IS_ENM_TOU_BY_KN : "SRCFLD_IS_ENM_TOU_BY_KN",
    SRCFLD_IS_ENM_TOU_BY_BP : "SRCFLD_IS_ENM_TOU_BY_BP",
    SRCFLD_IS_ENM_TOU_BY_RK : "SRCFLD_IS_ENM_TOU_BY_RK",
    SRCFLD_IS_ENM_TOU_BY_QU : "SRCFLD_IS_ENM_TOU_BY_QU",
    SRCFLD_IS_ENM_TOU_BY_KG : "SRCFLD_IS_ENM_TOU_BY_KG",
    DSTFLD_IS_FRDL_TOU_BY_PW : "DSTFLD_IS_FRDL_TOU_BY_PW",
    DSTFLD_IS_FRDL_TOU_BY_KN : "DSTFLD_IS_FRDL_TOU_BY_KN",
    DSTFLD_IS_FRDL_TOU_BY_BP : "DSTFLD_IS_FRDL_TOU_BY_BP",
    DSTFLD_IS_FRDL_TOU_BY_RK : "DSTFLD_IS_FRDL_TOU_BY_RK",
    DSTFLD_IS_FRDL_TOU_BY_QU : "DSTFLD_IS_FRDL_TOU_BY_QU",
    DSTFLD_IS_FRDL_TOU_BY_KG : "DSTFLD_IS_FRDL_TOU_BY_KG",
    DSTFLD_IS_ENM_TOU_BY_PW : "DSTFLD_IS_ENM_TOU_BY_PW",
    DSTFLD_IS_ENM_TOU_BY_KN : "DSTFLD_IS_ENM_TOU_BY_KN",
    DSTFLD_IS_ENM_TOU_BY_BP : "DSTFLD_IS_ENM_TOU_BY_BP",
    DSTFLD_IS_ENM_TOU_BY_RK : "DSTFLD_IS_ENM_TOU_BY_RK",
    DSTFLD_IS_ENM_TOU_BY_QU : "DSTFLD_IS_ENM_TOU_BY_QU",
    DSTFLD_IS_ENM_TOU_BY_KG : "DSTFLD_IS_ENM_TOU_BY_KG",
    CAPTURED_IS_PW : "CAPTURED_IS_PW",
    CAPTURED_IS_KN : "CAPTURED_IS_KN",
    CAPTURED_IS_BP : "CAPTURED_IS_BP",
    CAPTURED_IS_RK : "CAPTURED_IS_RK",
    CAPTURED_IS_QU : "CAPTURED_IS_QU",    
    ATTACKED_IS_PW : "ATTACKED_IS_PW",
    ATTACKED_IS_KN : "ATTACKED_IS_KN",
    ATTACKED_IS_BP : "ATTACKED_IS_BP",
    ATTACKED_IS_RK : "ATTACKED_IS_RK",
    ATTACKED_IS_QU : "ATTACKED_IS_QU",
    ATTACKED_IS_KG : "ATTACKED_IS_KG",
    ATTACK_IS_PIN  : "ATTACK_IS_PIN",
    ATTACK_IS_SOFT_PIN : "ATTACK_IS_SOFT_PIN",    
    SUPPORTED_IS_PW : "SUPPORTED_IS_PW",
    SUPPORTED_IS_KN : "SUPPORTED_IS_KN",
    SUPPORTED_IS_BP : "SUPPORTED_IS_BP",
    SUPPORTED_IS_RK : "SUPPORTED_IS_RK",
    SUPPORTED_IS_QU : "SUPPORTED_IS_QU" }

