#from .. match import *
#from .. import rules
from .. cvalues import *


def count_contacts(contacts):
    pawncnt = 0
    officercnt = 0
    queencnt = 0

    for contact in contacts:
        if(contact == PIECES['wPw'] or contact == PIECES['bPw']):
            pawncnt += 1
        elif(contact == PIECES['wQu'] or contact == PIECES['bQu']):
            queencnt += 1
        else:
            officercnt += 1
    return pawncnt, officercnt, queencnt

