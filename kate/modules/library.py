from kate.models import Match
from kate.modules import values, rules

FIRST = { (e2, e4, blk), (d2, d4, blk), (c2, c4, blk), (g2, g3, blk), (g1, f3, blk), 
          (e2, e3, blk), (d2, d3, blk) }

SECOND_1 = { (e7, e5, blk), (c7, c5, blk), (g8, f6, blk), (g7, g6, blk), (d7, d5, blk) }
SECOND_2 = { (d7, d5, blk), (g8, f6, blk), (g7, g6, blk), (e7, e6, blk) }
SECOND_3 = { (e7, e5, blk), (c7, c5, blk), (g8, f6, blk), (g7, g6, blk), (d7, d5, blk), (e7, e6, blk) }


SECOND_3 = { (e2, e4, blk), (d2, d4, blk), (c2, c4, blk), (g2, g3, blk), (g1, f3, blk), 
          (e2, e3, blk), (d2, d3, blk) }
SECOND_4 = { (e2, e4, blk), (d2, d4, blk), (c2, c4, blk), (g2, g3, blk), (g1, f3, blk), 
          (e2, e3, blk), (d2, d3, blk) }
SECOND_5 = { (e2, e4, blk), (d2, d4, blk), (c2, c4, blk), (g2, g3, blk), (g1, f3, blk), 
          (e2, e3, blk), (d2, d3, blk) }
SECOND_6 = { (e2, e4, blk), (d2, d4, blk), (c2, c4, blk), (g2, g3, blk), (g1, f3, blk), 
          (e2, e3, blk), (d2, d3, blk) }
SECOND_7 = { (e2, e4, blk), (d2, d4, blk), (c2, c4, blk), (g2, g3, blk), (g1, f3, blk), 
          (e2, e3, blk), (d2, d3, blk) }


def calc_first(match):
  if(match.count == 0):
    
    
