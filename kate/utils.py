from kate.models import Match as ModelMatch, Move as ModelMove
from kate.engine.match import *
from kate.engine.move import *
from kate.engine import helper
from kate.modules import interface


def fill_fmtboard(modelmatch, switch):
    fmtboard = [ [ [0  for k in range(2)] for x in range(8)] for x in range(8) ]
    if(switch == 0):
        rowstart = 7
        rowend = -1
        rowstep = -1
        colstart = 0
        colend = 8
        colstep = 1
    else:
        rowstart = 0
        rowend = 8
        rowstep = 1
        colstart = 7
        colend = -1
        colstep = -1
    idx1 = 0
    for i in range(rowstart, rowend, rowstep):
        idx2 = 0
        for j in range(colstart, colend, colstep):
            fmtboard[idx1][idx2][0] = modelmatch.readfield(j, i)
            field = chr(ord('a') + j) + chr(ord('1') + i)
            fmtboard[idx1][idx2][1] = field
            idx2 += 1
        idx1 += 1

    return fmtboard
    
