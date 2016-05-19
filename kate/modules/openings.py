from kate.models import OpeningMove


def populate_openings(move_list)
       previous = None
       for move in move_list:
              omove = OpeningMove(previous, move[0], move[1], move[2])
              omove.save()
              previous = omove

WHITEMOVES1 = [ ("e2", "e4"), ("d2", "d4"), ("c2", "c4"), ("g1", "f3"), ("g1", "e2"), 
           ("b1", "c3"), ("b1", "d2"), ("g2", "g3"), ("e2", "e3"), ("d2", "d3"), 
           ("c2", "c3") ]

BLACKMOVES1 = [ ("e7", "e5"), ("d7", "d5"), ("c7", "c5"), ("g8", "f6"), ("g8", "e7"), 
           ("b8", "c6"), ("b8", "d7"), ("g7", "g6"), ("e7", "e6"), ("d7", "d6"), 
           ("c7", "c6") ]
CNT1 = 11

WHITEMOVES2 = [ ("e2", "e4"), ("d2", "d4"), ("c2", "c4"), ("g1", "f3"), ("g1", "e2"), 
           ("b1", "c3"), ("b1", "d2"), ("g2", "g3"), ("e2", "e3"), ("d2", "d3"), 
           ("c2", "c3"), ("e4", "d5"), ("e4", "f5"), ("d4", "c5"), ("d4", "e5"), 
           ("c4", "b5"), ("c4", "d5") ]

BLACKMOVES2 = [ ("e7", "e5"), ("d7", "d5"), ("c7", "c5"), ("g8", "f6"), ("g8", "e7"), 
           ("b8", "c6"), ("b8", "d7"), ("g7", "g6"), ("e7", "e6"), ("d7", "d6"), 
           ("c7", "c6"), ("e5", "d4"), ("e5", "f4"), ("d5", "c4"), ("d5", "e4"),
           ("c5", "b4"), ("c5", "d4") ]
CNT2 = 17


WHITEMOVES3 = [ ("e2", "e4"), ("d2", "d4"), ("c2", "c4"), ("g1", "f3"), ("g1", "e2"), 
           ("b1", "c3"), ("b1", "d2"), ("g2", "g3"), ("e2", "e3"), ("d2", "d3"), 
           ("c2", "c3"), ("e4", "d5"), ("e4", "f5"), ("d4", "c5"), ("d4", "e5"), 
           ("c4", "b5"), ("c4", "d5") ]

BLACKMOVES3 = [ ("e7", "e5"), ("d7", "d5"), ("c7", "c5"), ("g8", "f6"), ("g8", "e7"), 
           ("b8", "c6"), ("b8", "d7"), ("g7", "g6"), ("e7", "e6"), ("d7", "d6"), 
           ("c7", "c6"), ("e5", "d4"), ("e5", "f4"), ("d5", "c4"), ("d5", "e4"),
           ("c5", "b4"), ("c5", "d4") ]
CNT3 = 17



def generate_move(match, cnt):
    if(match.next_color() == Match.COLORS['white']):
        if(match.count == 0):
            print("w1")
            move_list = WHITEMOVES1
            count = CNT1
        elif(match.count == 2):
            print("w2")
            move_list = WHITEMOVES2
            count = CNT2
        else:
            print("w3+")
            move_list = WHITEMOVES3
            count = CNT3
    else:
        if(match.count == 1):
            print("b1")
            move_list = BLACKMOVES1
            count = CNT1
        elif(match.count == 3):
            print("b2")
            move_list = BLACKMOVES2
            count = CNT2
        else:
            print("b3+")
            move_list = BLACKMOVES3
            count = CNT3

    if(cnt >= count):
        return count + 1, None

    for i in range(cnt, count):
        x1, y1 = values.koord_to_index(move_list[i][0])
        x2, y2 = values.koord_to_index(move_list[i][1])
        if(rules.is_move_valid(match, x1, y1, x2, y2, Match.PIECES['blk'])[0]):
            gmove = calc.GenMove(x1, y1, x2, y2, Match.PIECES['blk'])
            return i, gmove

    return count + 1, None

