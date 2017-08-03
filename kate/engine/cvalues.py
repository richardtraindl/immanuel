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
    'unrated' : 5,
    'progress' : 6 }


MV_IS_CASTLING                     = 0x8000000000
MV_IS_PROMOTION                    = 0x4000000000
MV_IS_CAPTURE                      = 0x2000000000
MV_IS_ATTACK                       = 0x1000000000
MV_IS_SUPPORT                      = 0x0800000000
MV_IS_FLEE                         = 0x0400000000
MV_IS_PROGRESS                     = 0x0200000000
# MV_IS_SILENT                       = 0x0100000000

MV_PIECE_IS_PAWN                   = 0x0080000000
MV_PIECE_IS_OFFICER                = 0x0040000000
MV_PIECE_IS_KING                   = 0x0020000000

CAPTURED_IS_PAWN                   = 0x0008000000
CAPTURED_IS_OFFICER                = 0x0004000000
CAPTURED_IS_ADD_ATT_FROM_PAWN      = 0x0002000000
CAPTURED_IS_ADD_ATT_FROM_OFFICER   = 0x0001000000
CAPTURED_IS_SUPP_BY_PAWN           = 0x0000800000
CAPTURED_IS_SUPP_BY_OFFICER        = 0x0000400000

ATTACKED_IS_PAWN                   = 0x0000080000
ATTACKED_IS_OFFICER                = 0x0000040000
ATTACKED_IS_KING                   = 0x0000020000
ATT_IS_ADD_ATT_FROM_PAWN           = 0x0000010000
ATT_IS_ADD_ATT_FROM_OFFICER        = 0x0000008000
ATT_IS_SUPP_BY_PAWN                = 0x0000004000
ATT_IS_SUPP_BY_OFFICER             = 0x0000002000

SUPPORTED_IS_PAWN                  = 0x0000000800
SUPPORTED_IS_OFFICER               = 0x0000000400
SUPPORTED_IS_ATT_FROM_PAWN         = 0x0000000200
SUPPORTED_IS_ATT_FROM_OFFICER      = 0x0000000100
SUPPORTED_IS_ADD_SUPP_BY_PAWN      = 0x0000000080
SUPPORTED_IS_ADD_SUPP_BY_OFFICER   = 0x0000000040

FIELD_IS_ATT_FROM_PAWN             = 0x0000000008
FIELD_IS_ATT_FROM_OFFICER          = 0x0000000004
FIELD_IS_SUPP_BY_PAWN              = 0x0000000002
FIELD_IS_SUPP_BY_OFFICER           = 0x0000000001

