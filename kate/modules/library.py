from kate.models import OpeningMove
from kate.fixtures import seed_e2e4_e7e5

def populate_openings(move_list)
        prevmove = None
        for move in move_list:
            if(omove.movecnt == 1):
                prevmove = None
            else:
                while(previous.movecnt != omove.movecnt - 1):
                    prevmove = prevmove.previous

            openingmove = OpeningMove(prevmove, move[0], move[1], move[2])
            try:
                openingmove.save()
            except:
                print("populate_openings error")
                break


populate_openings(seed_e2e4_e7e5.M1)