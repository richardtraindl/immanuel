from .match import PIECES


PIECES_RANK = {
        PIECES['blk'] : 0,
        PIECES['wPw'] : 1,
        PIECES['bPw'] : 1,
        PIECES['wKn'] : 2,
        PIECES['bKn'] : 2,
        PIECES['wBp'] : 2,
        PIECES['bBp'] : 2,
        PIECES['wRk'] : 4,
        PIECES['bRk'] : 4,
        PIECES['wQu'] : 5,
        PIECES['bQu'] : 5,
        PIECES['wKg'] : 6,
        PIECES['bKg'] : 6 }


SCORES = { 
        PIECES['blk'] : 0,
        PIECES['wKg'] : -20000,
        PIECES['wPw'] : -100,
        PIECES['wRk'] : -500,
        PIECES['wKn'] : -336,
        PIECES['wBp'] : -340,
        PIECES['wQu'] : -950,
        PIECES['bKg'] : 20000,
        PIECES['bPw'] : 100,
        PIECES['bRk'] : 500,
        PIECES['bKn'] : 336,
        PIECES['bBp'] : 340,
        PIECES['bQu'] : 950 }


ATTACKED_SCORES = {
        PIECES['blk'] : 0,
        PIECES['wKg'] : 0,
        PIECES['wPw'] : -2,
        PIECES['wRk'] : -5,
        PIECES['wKn'] : -4,
        PIECES['wBp'] : -4,
        PIECES['wQu'] : -9,
        PIECES['bKg'] : 0,
        PIECES['bPw'] : 2,
        PIECES['bRk'] : 5,
        PIECES['bKn'] : 4,
        PIECES['bBp'] : 4,
        PIECES['bQu'] : 9 }


SUPPORTED_SCORES = {
        PIECES['blk'] : 0,
        PIECES['wKg'] : 0,
        PIECES['wPw'] : 2,
        PIECES['wRk'] : 5,
        PIECES['wKn'] : 4,
        PIECES['wBp'] : 4,
        PIECES['wQu'] : 9,
        PIECES['bKg'] : 0,
        PIECES['bPw'] : -2,
        PIECES['bRk'] : -5,
        PIECES['bKn'] : -4,
        PIECES['bBp'] : -4,
        PIECES['bQu'] : -9 }


PRIO = {
    'defend-check' : 0,
    'promotion' : 1,
    'capture-good-deal' : 2,
    'capture-bad-deal' : 3,
    'single-silent-move' : 4,
    'flee-urgent' : 5,
    'support-good-deal' : 6,
    'attack-king-good-deal' : 7,
    'attack-king-bad-deal' : 8,    
    'defend-fork' : 9,
    'attack-good-deal' : 10,
    'disclosed-attack' : 11,
    'castling' : 12,
    'flee' : 13,
    'good' : 14,
    'good-postponed' : 15,
    'support-unattacked' : 16,
    'attack-bad-deal' : 17,
    'support-bad-deal' : 18,
    'bad' : 19,
    'last' : 20 }

PRIO_URGENT_LIMES = PRIO['single-silent-move']
PRIO1_LIMES = PRIO['castling']


MV_IS_CASTLING                         = 0x8000000000000000
MV_IS_PROMOTION                        = 0x4000000000000000
MV_IS_CAPTURE                          = 0x2000000000000000
MV_IS_ATTACK                           = 0x1000000000000000
MV_IS_DISCLOSURE                       = 0x0800000000000000
MV_IS_FORK                             = 0x0400000000000000
MV_IS_FORK_DEFENSE                     = 0x0200000000000000
MV_DEFENDS_CHECK                       = 0x0100000000000000
MV_IS_SUPPORT                          = 0x0080000000000000
MV_IS_FLEE                             = 0x0040000000000000
MV_IS_PROGRESS                         = 0x0020000000000000
MV_CONTROLES_FILE                      = 0x0010000000000000

MV_PIECE_IS_PW                         = 0x0008000000000000
MV_PIECE_IS_KN                         = 0x0004000000000000
MV_PIECE_IS_BP                         = 0x0002000000000000
MV_PIECE_IS_RK                         = 0x0001000000000000
MV_PIECE_IS_QU                         = 0x0000800000000000
MV_PIECE_IS_KG                         = 0x0000400000000000

SRCFLD_IS_FRDL_TOU_BY_PW               = 0x0000080000000000
SRCFLD_IS_FRDL_TOU_BY_KN               = 0x0000040000000000
SRCFLD_IS_FRDL_TOU_BY_BP               = 0x0000020000000000
SRCFLD_IS_FRDL_TOU_BY_RK               = 0x0000010000000000
SRCFLD_IS_FRDL_TOU_BY_QU               = 0x0000008000000000
SRCFLD_IS_FRDL_TOU_BY_KG               = 0x0000004000000000

SRCFLD_IS_ENM_TOU_BY_PW                = 0x0000002000000000
SRCFLD_IS_ENM_TOU_BY_KN                = 0x0000001000000000
SRCFLD_IS_ENM_TOU_BY_BP                = 0x0000000800000000
SRCFLD_IS_ENM_TOU_BY_RK                = 0x0000000400000000
SRCFLD_IS_ENM_TOU_BY_QU                = 0x0000000200000000
SRCFLD_IS_ENM_TOU_BY_KG                = 0x0000000100000000

DSTFLD_IS_FRDL_TOU_BY_PW               = 0x0000000080000000
DSTFLD_IS_FRDL_TOU_BY_KN               = 0x0000000040000000
DSTFLD_IS_FRDL_TOU_BY_BP               = 0x0000000020000000
DSTFLD_IS_FRDL_TOU_BY_RK               = 0x0000000010000000
DSTFLD_IS_FRDL_TOU_BY_QU               = 0x0000000008000000
DSTFLD_IS_FRDL_TOU_BY_KG               = 0x0000000004000000

DSTFLD_IS_ENM_TOU_BY_PW                = 0x0000000002000000
DSTFLD_IS_ENM_TOU_BY_KN                = 0x0000000001000000
DSTFLD_IS_ENM_TOU_BY_BP                = 0x0000000000800000
DSTFLD_IS_ENM_TOU_BY_RK                = 0x0000000000400000
DSTFLD_IS_ENM_TOU_BY_QU                = 0x0000000000200000
DSTFLD_IS_ENM_TOU_BY_KG                = 0x0000000000100000

CAPTURED_IS_PW                         = 0x0000000000080000
CAPTURED_IS_KN                         = 0x0000000000040000
CAPTURED_IS_BP                         = 0x0000000000020000
CAPTURED_IS_RK                         = 0x0000000000010000
CAPTURED_IS_QU                         = 0x0000000000008000

ATTACKED_IS_PW                         = 0x0000000000004000
ATTACKED_IS_KN                         = 0x0000000000002000
ATTACKED_IS_BP                         = 0x0000000000001000
ATTACKED_IS_RK                         = 0x0000000000000800
ATTACKED_IS_QU                         = 0x0000000000000400
ATTACKED_IS_KG                         = 0x0000000000000200

SUPPORTED_IS_PW                        = 0x0000000000000100
SUPPORTED_IS_KN                        = 0x0000000000000080
SUPPORTED_IS_BP                        = 0x0000000000000040
SUPPORTED_IS_RK                        = 0x0000000000000020
SUPPORTED_IS_QU                        = 0x0000000000000010

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
    MV_IS_FLEE : "MV_IS_FLEE",
    MV_IS_PROGRESS : "MV_IS_PROGRESS",
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
    SUPPORTED_IS_PW : "SUPPORTED_IS_PW",
    SUPPORTED_IS_KN : "SUPPORTED_IS_KN",
    SUPPORTED_IS_BP : "SUPPORTED_IS_BP",
    SUPPORTED_IS_RK : "SUPPORTED_IS_RK",
    SUPPORTED_IS_QU : "SUPPORTED_IS_QU" }

