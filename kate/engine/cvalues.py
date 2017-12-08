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
        PIECES['wKg'] : -10,
        PIECES['wPw'] : -1,
        PIECES['wRk'] : -5,
        PIECES['wKn'] : -4,
        PIECES['wBp'] : -4,
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
    'unrated' : 6,
    'last' : 7 }

PRIO_INDICES = {
    PRIO['prio1'] : 0,
    PRIO['prio2' ] : 1,
    PRIO['prio3'] : 2,
    PRIO['prio4'] : 3,
    PRIO['prio5'] : 4,
    PRIO['unrated'] : 5,
    PRIO['last'] : 6 }


MV_IS_CASTLING                         = 0x800000000000
MV_IS_PROMOTION                        = 0x400000000000
MV_IS_CAPTURE                          = 0x200000000000
MV_IS_ATTACK                           = 0x100000000000
MV_IS_FORK_DEFENSE                     = 0x080000000000
# MV_IS_FORK                             = 0x080000000000
MV_IS_SUPPORT                          = 0x040000000000
MV_IS_FLEE                             = 0x020000000000
MV_IS_PROGRESS                         = 0x010000000000

PIECE_IS_PAWN                          = 0x008000000000
PIECE_IS_OFFICER                       = 0x004000000000
PIECE_IS_QUEEN                         = 0x002000000000
PIECE_IS_KING                          = 0x001000000000

SRCFIELD_IS_FRDLYTOUCHED_BY_PAWN       = 0x000800000000
SRCFIELD_IS_FRDLYTOUCHED_BY_OFFICER    = 0x000400000000
SRCFIELD_IS_FRDLYTOUCHED_BY_QUEEN      = 0x000200000000
SRCFIELD_IS_FRDLYTOUCHED_BY_KING       = 0x000100000000

SRCFIELD_IS_ENMYTOUCHED_BY_PAWN        = 0x000080000000
SRCFIELD_IS_ENMYTOUCHED_BY_OFFICER     = 0x000040000000
SRCFIELD_IS_ENMYTOUCHED_BY_QUEEN       = 0x000020000000
SRCFIELD_IS_ENMYTOUCHED_BY_KING        = 0x000010000000

DSTFIELD_IS_FRDLYTOUCHED_BY_PAWN       = 0x000008000000
DSTFIELD_IS_FRDLYTOUCHED_BY_OFFICER    = 0x000004000000
DSTFIELD_IS_FRDLYTOUCHED_BY_QUEEN      = 0x000002000000
DSTFIELD_IS_FRDLYTOUCHED_BY_KING       = 0x000001000000

DSTFIELD_IS_ENMYTOUCHED_BY_PAWN        = 0x000000800000
DSTFIELD_IS_ENMYTOUCHED_BY_OFFICER     = 0x000000400000
DSTFIELD_IS_ENMYTOUCHED_BY_QUEEN       = 0x000000200000
DSTFIELD_IS_ENMYTOUCHED_BY_KING        = 0x000000100000

CAPTURED_IS_PAWN                       = 0x000000080000
CAPTURED_IS_OFFICER                    = 0x000000040000
CAPTURED_IS_QUEEN                      = 0x000000020000

ATTACKED_IS_PAWN                       = 0x000000008000
ATTACKED_IS_OFFICER                    = 0x000000004000
ATTACKED_IS_QUEEN                      = 0x000000002000
ATTACKED_IS_KING                       = 0x000000001000
ATTACKED_IS_ADD_ATT_FROM_PAWN          = 0x000000000800
ATTACKED_IS_ADD_ATT_FROM_OFFICER       = 0x000000000400
ATTACKED_IS_SUPP_BY_PAWN               = 0x000000000200
ATTACKED_IS_SUPP_BY_OFFICER            = 0x000000000100

SUPPORTED_IS_PAWN                      = 0x000000000080
SUPPORTED_IS_OFFICER                   = 0x000000000040
SUPPORTED_IS_QUEEN                     = 0x000000000020
SUPPORTED_IS_ATT_FROM_PAWN             = 0x000000000008
SUPPORTED_IS_ATT_FROM_OFFICER          = 0x000000000004
SUPPORTED_IS_ADD_SUPP_BY_PAWN          = 0x000000000002
SUPPORTED_IS_ADD_SUPP_BY_OFFICER       = 0x000000000001

TOKEN_TEXT = {
    MV_IS_CASTLING : "MV_IS_CAST",
    MV_IS_PROMOTION : "MV_IS_PROM",
    MV_IS_CAPTURE : "MV_IS_CAPT",
    MV_IS_ATTACK : "MV_IS_ATT",
    MV_IS_FORK_DEFENSE : "MV_IS_FORK_DEFENSE",
    #MV_IS_FORK : "MV_IS_FORK",
    MV_IS_SUPPORT : "MV_IS_SUPP",
    MV_IS_FLEE : "MV_IS_FLEE",
    MV_IS_PROGRESS : "MV_IS_PROGR",
    PIECE_IS_PAWN : "MV_PIECE_IS_PW",
    PIECE_IS_OFFICER : "MV_PIECE_IS_OFF",
    PIECE_IS_QUEEN : "MV_PIECE_IS_QU",
    PIECE_IS_KING : "MV_PIECE_IS_KG",
    SRCFIELD_IS_FRDLYTOUCHED_BY_PAWN : "SRCFLD_IS_FRDLYTOUCH_BY_PW",
    SRCFIELD_IS_FRDLYTOUCHED_BY_OFFICER : "SRCFLD_IS_FRDLYTOUCH_BY_OFF",
    SRCFIELD_IS_FRDLYTOUCHED_BY_QUEEN : "SRCFLD_IS_FRDLYTOUCH_BY_QU",
    SRCFIELD_IS_ENMYTOUCHED_BY_PAWN : "SRCFLD_IS_ENMYTOUCH_BY_PW",
    SRCFIELD_IS_ENMYTOUCHED_BY_OFFICER : "SRCFLD_IS_ENMYTOUCH_BY_OFF",
    SRCFIELD_IS_ENMYTOUCHED_BY_QUEEN : "SRCFLD_IS_ENMYTOUCH_BY_QU",
    DSTFIELD_IS_FRDLYTOUCHED_BY_PAWN : "DSTFLD_IS_FRDLYTOUCH_BY_PW",
    DSTFIELD_IS_FRDLYTOUCHED_BY_OFFICER : "DSTFLD_IS_FRDLYTOUCH_BY_OFF",
    DSTFIELD_IS_FRDLYTOUCHED_BY_QUEEN : "DSTFLD_IS_FRDLYTOUCH_BY_QU",
    DSTFIELD_IS_ENMYTOUCHED_BY_PAWN : "DSTFLD_IS_ENMYTOUCH_BY_PW",
    DSTFIELD_IS_ENMYTOUCHED_BY_OFFICER : "DSTFLD_IS_ENMYTOUCH_BY_OFF",
    DSTFIELD_IS_ENMYTOUCHED_BY_QUEEN : "DSTFLD_IS_ENMYTOUCH_BY_QU",
    CAPTURED_IS_PAWN : "CAPT_IS_PW",
    CAPTURED_IS_OFFICER : "CAPT_IS_OFF",
    CAPTURED_IS_QUEEN : "CAPT_IS_QU",
    ATTACKED_IS_PAWN : "ATT_IS_PW",
    ATTACKED_IS_OFFICER : "ATT_IS_OFF",
    ATTACKED_IS_QUEEN : "ATT_IS_QU",
    ATTACKED_IS_KING : "ATT_IS_KG",
    ATTACKED_IS_ADD_ATT_FROM_PAWN : "ATT_IS_ADD_ATT_FROM_PW",
    ATTACKED_IS_ADD_ATT_FROM_OFFICER : "ATT_IS_ADD_ATT_FROM_OFF",
    ATTACKED_IS_SUPP_BY_PAWN : "ATT_IS_SUPP_BY_PW",
    ATTACKED_IS_SUPP_BY_OFFICER : "ATT_IS_SUPP_BY_OFF",
    SUPPORTED_IS_PAWN : "SUPP_IS_PW",
    SUPPORTED_IS_OFFICER : "SUPP_IS_OFF",
    SUPPORTED_IS_QUEEN : "SUPP_IS_QU",
    SUPPORTED_IS_ATT_FROM_PAWN : "SUPP_IS_ATT_FROM_PW",
    SUPPORTED_IS_ATT_FROM_OFFICER : "SUPP_IS_ATT_FROM_OFF",
    SUPPORTED_IS_ADD_SUPP_BY_PAWN : "SUPP_IS_ADD_SUPP_BY_PW",
    SUPPORTED_IS_ADD_SUPP_BY_OFFICER : "SUPP_IS_ADD_SUPP_BY_OFF" }

