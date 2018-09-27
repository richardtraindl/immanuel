

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
    PIECES['wRk'] : -500,
    PIECES['wKn'] : -336,
    PIECES['wBp'] : -340,
    PIECES['wQu'] : -950,
    PIECES['bKg'] : 20000,
    PIECES['bPw'] : 100,
    PIECES['bRk'] : 500,
    PIECES['bKn'] : 336,
    PIECES['bBp'] : 340,
    PIECES['bQu'] : 950 
}


SUPPORTED_SCORES = {
    PIECES['blk'] : 0,
    PIECES['wKg'] : 0,
    PIECES['wPw'] : 4,
    PIECES['wRk'] : 10,
    PIECES['wKn'] : 8,
    PIECES['wBp'] : 8,
    PIECES['wQu'] : 16,
    PIECES['bKg'] : 0,
    PIECES['bPw'] : -4,
    PIECES['bRk'] : -10,
    PIECES['bKn'] : -8,
    PIECES['bBp'] : -8,
    PIECES['bQu'] : -16 
}


ATTACKED_SCORES = {
    PIECES['blk'] : 0,
    PIECES['wKg'] : 0,
    PIECES['wPw'] : -4,
    PIECES['wRk'] : -10,
    PIECES['wKn'] : -8,
    PIECES['wBp'] : -8,
    PIECES['wQu'] : -16,
    PIECES['bKg'] : 0,
    PIECES['bPw'] : 4,
    PIECES['bRk'] : 10,
    PIECES['bKn'] : 8,
    PIECES['bBp'] : 8,
    PIECES['bQu'] : 16 
}


