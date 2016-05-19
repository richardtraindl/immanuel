from kate.models import OpeningMove


def populate_openings(move_list)
       previous = None
       for move in move_list:
              omove = OpeningMove(previous, move[0], move[1], move[2])
              try:
                  omove.save()
              except:
                  omove = OpeningMove.objects.get(movecnt=move[0], src=move[1], dst=move[2])
              if(omove == None):
                  break
              else:
                  previous = omove

