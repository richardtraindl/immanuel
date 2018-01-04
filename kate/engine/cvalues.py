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
        PIECES['wKg'] : -20,
        PIECES['wPw'] : -2,
        PIECES['wRk'] : -8,
        PIECES['wKn'] : -6,
        PIECES['wBp'] : -6,
        PIECES['wQu'] : -14,
        PIECES['bKg'] : 20,
        PIECES['bPw'] : 2,
        PIECES['bRk'] : 8,
        PIECES['bKn'] : 6,
        PIECES['bBp'] : 6,
        PIECES['bQu'] : 14 }


SUPPORTED_SCORES = {
        PIECES['blk'] : 0,
        PIECES['wKg'] : 20,
        PIECES['wPw'] : 2,
        PIECES['wRk'] : 8,
        PIECES['wKn'] : 6,
        PIECES['wBp'] : 6,
        PIECES['wQu'] : 14,
        PIECES['bKg'] : -20,
        PIECES['bPw'] : -2,
        PIECES['bRk'] : -8,
        PIECES['bKn'] : -6,
        PIECES['bBp'] : -6,
        PIECES['bQu'] : -14 }

PRIO_STEP = 4
PRIO_HALF_STEP = 2

PRIO = {
    'prio1a' : 1,
    'prio1b' : 2,
    'prio1c' : 3,
    'prio1d' : 4,
    'prio2a' : 5,
    'prio2b' : 6,
    'prio2c' : 7,
    'prio2d' : 8,
    'prio3a' : 9,
    'prio3b' : 10,
    'prio3c' : 11,
    'prio3d' : 12,
    'prio4a' : 13,
    'prio4b' : 14,
    'prio4c' : 15,
    'prio4d' : 16,
    'last' : 17 }

PRIO_INDICES = {
    PRIO['prio1a'] : 0,
    PRIO['prio1b'] : 1,
    PRIO['prio1c'] : 2,
    PRIO['prio1d'] : 3,
    PRIO['prio2a' ] : 4,
    PRIO['prio2b' ] : 5,
    PRIO['prio2c' ] : 6,
    PRIO['prio2d' ] : 7,
    PRIO['prio3a'] : 8,
    PRIO['prio3b'] : 9,
    PRIO['prio3c'] : 10,
    PRIO['prio3d'] : 11,
    PRIO['prio4a'] : 12,
    PRIO['prio4b'] : 13,
    PRIO['prio4c'] : 14,
    PRIO['prio4d'] : 15,
    PRIO['last'] : 16 }


MV_IS_CASTLING                         = 0x8000000000000000
MV_IS_PROMOTION                        = 0x4000000000000000
MV_IS_CAPTURE                          = 0x2000000000000000
MV_IS_ATTACK                           = 0x1000000000000000
MV_IS_FORK                             = 0x0800000000000000
MV_IS_FORK_DEFENSE                     = 0x0400000000000000
MV_IS_DISCLOSURE                       = 0x0200000000000000
MV_IS_SUPPORT                          = 0x0100000000000000
MV_IS_FLEE                             = 0x0080000000000000
MV_IS_PROGRESS                         = 0x0040000000000000

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
    MV_IS_FORK : "MV_IS_FORK",
    MV_IS_FORK_DEFENSE : "MV_IS_FORK_DEFENSE",
    MV_IS_DISCLOSURE : "MV_IS_DISCLOSURE",
    MV_IS_SUPPORT : "MV_IS_SUPPORT",
    MV_IS_FLEE : "MV_IS_FLEE",
    MV_IS_PROGRESS : "MV_IS_PROGRESS",
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

