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


REVERSED_SCORES = {
        PIECES['blk'] : PIECES['blk'],
        PIECES['wKg'] : PIECES['bKg'],
        PIECES['wPw'] : PIECES['bPw'],
        PIECES['wRk'] : PIECES['bRk'] ,
        PIECES['wKn'] : PIECES['bKn'],
        PIECES['wBp'] : PIECES['bBp'],
        PIECES['wQu'] : PIECES['bQu'],
        PIECES['bKg'] : PIECES['wKg'],
        PIECES['bPw'] : PIECES['wPw'],
        PIECES['bRk'] : PIECES['wRk'],
        PIECES['bKn'] : PIECES['wKn'],
        PIECES['bBp'] : PIECES['wBp'],
        PIECES['bQu'] : PIECES['wQu'] }


ATTACKED_SCORES = {
        PIECES['blk'] : 0,
        PIECES['wKg'] : -10,
        PIECES['wPw'] : -1,
        PIECES['wRk'] : -5,
        PIECES['wKn'] : -4,
        PIECES['wBp'] : 
-4,
        PIECES['wQu'] : -7,
        PIECES['bKg'] : 10,
        PIECES['bPw'] : 1,
        PIECES['bRk'] : 5,
        PIECES['bKn'] : 4,
        PIECES['bBp'] : 4,
        PIECES['bQu'] : 7 }


SUPPORTED_SCORES = {
        PIECES['blk'] : 0,
        PIECES['wKg'] : 10,
        PIECES['wPw'] : 1,
        PIECES['wRk'] : 5,
        PIECES['wKn'] : 4,
        PIECES['wBp'] : 4,
        PIECES['wQu'] : 7,
        PIECES['bKg'] : -10,
        PIECES['bPw'] : -1,
        PIECES['bRk'] : -5,
        PIECES['bKn'] : -4,
        PIECES['bBp'] : -4,
        PIECES['bQu'] : -7 }


PRIO = {
    'prio1' : 1,
    'prio2' : 2,
    'prio3' : 3,
    'prio4' : 4,
    'prio5' : 5,
    'prio6' : 6,
    'priolast' : 7,
    'undefined' : 10 }


MV_IS_CASTLING                     = 0x80000000

MV_IS_PROMOTION                    = 0x40000000

MV_IS_FLEE                         = 0x20000000
FIELD_IS_ATT_FROM_PAWN             = 0x00000008
FIELD_IS_ATT_FROM_OFFICER          = 0x00000004
FIELD_IS_SUPP_BY_PAWN              = 0x00000002
FIELD_IS_SUPP_BY_OFFICER           = 0x00000001

MV_IS_PROGRESS                     = 0x10000000

MV_IS_CAPTURE                      = 0x08000000
CAPTURED_IS_PAWN                   = 0x04000000
CAPTURED_IS_OFFICER                = 0x02000000
CAPTURED_IS_ADD_ATT_FROM_PAWN      = 0x00800000
CAPTURED_IS_ADD_ATT_FROM_OFFICER   = 0x00400000
CAPTURED_IS_SUPP_BY_PAWN           = 0x00200000
CAPTURED_IS_SUPP_BY_OFFICER        = 0x00100000

MV_IS_ATTACK                       = 0x00080000
ATTACKED_IS_PAWN                   = 0x00040000
ATTACKED_IS_OFFICER                = 0x00020000
ATTACKED_IS_KING                   = 0x00010000
ATT_IS_ADD_ATT_FROM_PAWN           = 0x00008000
ATT_IS_ADD_ATT_FROM_OFFICER        = 0x00004000
ATT_IS_SUPP_BY_PAWN                = 0x00002000
ATT_IS_SUPP_BY_OFFICER             = 0x00001000

MV_IS_SUPPORT                      = 0x00000800
SUPPORTED_IS_PAWN                  = 0x00000400
SUPPORTED_IS_OFFICER               = 0x00000200
SUPPORTED_IS_ATT_FROM_PAWN         = 0x00000080
SUPPORTED_IS_ATT_FROM_OFFICER      = 0x00000040
SUPPORTED_IS_ADD_SUPP_BY_PAWN      = 0x00000020
SUPPORTED_IS_ADD_SUPP_BY_OFFICER   = 0x00000010
