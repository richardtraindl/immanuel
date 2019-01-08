

PIECES = {
    'blk' : 0,
    'wKg' : 1,
    'wPw' : 2,
    'wRk' : 3,
    'wKn' : 4,
    'wBp' : 5,
    'wQu' : 6,
    'bKg' : 9,
    'bPw' : 10,
    'bRk' : 11,
    'bKn' : 12,
    'bBp' : 13,
    'bQu' : 14 
}


COLORS = {
    'undefined' : 0,
    'white' : 1,
    'black' : 9 
}


REVERSED_COLORS = { 
    COLORS['undefined'] : COLORS['undefined'],
    COLORS['white'] : COLORS['black'],
    COLORS['black'] : COLORS['white'] 
}


PIECES_COLOR = {
    PIECES['blk'] : COLORS['undefined'],
    PIECES['wKg'] : COLORS['white'],
    PIECES['wPw'] : COLORS['white'],
    PIECES['wRk'] : COLORS['white'],
    PIECES['wKn'] : COLORS['white'],
    PIECES['wBp'] : COLORS['white'],
    PIECES['wQu'] : COLORS['white'],
    PIECES['bKg'] : COLORS['black'],
    PIECES['bPw'] : COLORS['black'],
    PIECES['bRk'] : COLORS['black'],
    PIECES['bKn'] : COLORS['black'],
    PIECES['bBp'] : COLORS['black'],
    PIECES['bQu'] : COLORS['black'] 
}


PIECES_RANK = {
    PIECES['blk'] : 0,
    PIECES['wPw'] : 2,
    PIECES['bPw'] : 2,
    PIECES['wKn'] : 4,
    PIECES['bKn'] : 4,
    PIECES['wBp'] : 4,
    PIECES['bBp'] : 4,
    PIECES['wRk'] : 5,
    PIECES['bRk'] : 5,
    PIECES['wQu'] : 7,
    PIECES['bQu'] : 7,
    PIECES['wKg'] : 9,
    PIECES['bKg'] : 9 
}


SCORES = { 
    PIECES['blk'] : 0,
    PIECES['wKg'] : -20000,
    PIECES['wPw'] : -100,
    PIECES['wRk'] : -450,
    PIECES['wKn'] : -340,
    PIECES['wBp'] : -340,
    PIECES['wQu'] : -900,
    PIECES['bKg'] : 20000,
    PIECES['bPw'] : 100,
    PIECES['bRk'] : 450,
    PIECES['bKn'] : 340,
    PIECES['bBp'] : 340,
    PIECES['bQu'] : 900 
}


SUPPORTED_SCORES = {
    PIECES['blk'] : 0,
    PIECES['wKg'] : 0,
    PIECES['wPw'] : 6,
    PIECES['wRk'] : 24,
    PIECES['wKn'] : 18,
    PIECES['wBp'] : 18,
    PIECES['wQu'] : 30,
    PIECES['bKg'] : 0,
    PIECES['bPw'] : -6,
    PIECES['bRk'] : -24,
    PIECES['bKn'] : -18,
    PIECES['bBp'] : -18,
    PIECES['bQu'] : -30 
}


ATTACKED_SCORES = {
    PIECES['blk'] : 0,
    PIECES['wKg'] : 0,
    PIECES['wPw'] : -6,
    PIECES['wRk'] : -24,
    PIECES['wKn'] : -18,
    PIECES['wBp'] : -18,
    PIECES['wQu'] : -30,
    PIECES['bKg'] : 0,
    PIECES['bPw'] : 6,
    PIECES['bRk'] : 24,
    PIECES['bKn'] : 18,
    PIECES['bBp'] : 18,
    PIECES['bQu'] : 30
}

OPERATORS = {
        'less'        : 0,
        'equal'       : 1,
        'fairy-equal' : 2,
        'greater'     : 3 }

