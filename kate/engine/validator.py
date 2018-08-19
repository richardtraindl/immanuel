

class cValidator:
    def __init__(self, match, xpos, ypos):
        self.match = match

    RETURN_CODES = {
        'ok' : 10,
        'draw' : 11,
        'winner_white' : 12,
        'winner_black' : 13,
        'match-cancelled' : 14,
        'wrong-color' : 15,
        'pawn-error' : 20,
        'rook-error' : 21,
        'knight-error' : 22,
        'bishop-error' : 23,
        'queen-error' : 24,
        'king-error' : 25,
        'format-error' : 30,
        'out-of-bounds' : 31,
        'general-error' : 40,
    }

    RETURN_MSGS = {
        RETURN_CODES['ok'] : "move okay",
        RETURN_CODES['draw'] : "draw",
        RETURN_CODES['winner_white'] : "winner white",
        RETURN_CODES['winner_black'] : "winner black",
        RETURN_CODES['match-cancelled'] : " match is cancelled",
        RETURN_CODES['wrong-color'] : "wrong color",
        RETURN_CODES['pawn-error'] : "pawn error",
        RETURN_CODES['rook-error'] : "rook error",
        RETURN_CODES['knight-error'] : "knight error",
        RETURN_CODES['bishop-error'] : "bishop error",
        RETURN_CODES['queen-error'] : "queen error",
        RETURN_CODES['king-error'] : "king error",
        RETURN_CODES['format-error'] : "format wrror",
        RETURN_CODES['out-of-bounds'] : "wrong square",
        RETURN_CODES['general-error'] : "general error",
    }

# class end
