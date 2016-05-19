from kate.models import OpeningMove

M1 = { (1, "e2", "e4"), (2, "e7", "e5"), (3, "g1", "f3"), (4, "b8", "c6"), (5, "d2", "d4"), (6, "e5", "d4") }


def populate_openings(move_list)
       previous = None
       for move in move_list:
              omove = OpeningMove(previous, move[0], move[1], move[2])
              omove.save()
              previous = omove

M1 = { , (2, "e7", "e5", "blk"), (3, "b1", "c3", "blk"), (4, "g1", "f3", "blk"), 
       (5, "g1", "f3", "blk"), (6, "d7", "d6", "blk") }

# answer to c2-c4
M23 = { (2, "c7", "c5", "blk"), (2, "d7", "d5", "blk"), (2, "e7", "e5", "blk"), (2, "g8", "f6", "blk"), 
        (2, "g7", "g6", "blk"), (2, "e7", "e6", "blk"), (2, "d7", "d6", "blk") }

# answer to d2-d4
M22 = { (2, "d7", "d5", "blk"), (2, "e7", "e6", "blk"), (2, "g8", "f6", "blk"), (2, "g7", "g6", "blk") }

# answer to e2-e4
M21 = { (2, "c7", "c5", "blk"), (2, "d7", "d5", "blk"), (2, "e7", "e5", "blk"), (2, "g8", "f6", "blk"), 
        (2, "g7", "g6", "blk"), (2, "d7", "d6", "blk"), (2, "e7", "e6", "blk") }

# answer to g1-f3
M24 = { (2, "c7", "c5", "blk"), (2, "d7", "d5", "blk"), (2, "e7", "e5", "blk"), (2, "g8", "f6", "blk"), 
        (2, "g7", "g6", "blk"), (2, "e7", "e6", "blk"), (2, "d7", "d6", "blk") }



.....
# answer to g2-g3
M24 = { (2, "c7", "c5", "blk"), (2, "d7", "d5", "blk"), (2, "e7", "e5", "blk"), (2, "g8", "f6", "blk"), 
        (2, "g7", "g6", "blk"), (2, "e7", "e6", "blk"), (2, "d7", "d6", "blk") }
