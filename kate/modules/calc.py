from kate.models import Match, Move
from kate.modules import values, rules


def calc_min(match):
  color = match.next_color()

  for j in range(8):
    for i in range(8):
      field = match.readfield(i, j)
      if(Match.color_of_piece(field) == color):
        return 0
  
  return 1
