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


def contacts_to_token(token, frdlycontacts, enmycontacts):
    pawncnt, officercnt, queencnt = count_contacts(frdlycontacts)
    if(pawncnt > 0):
        token = token | MV_DSTFIELD_IS_FRDLYTOUCHED_BY_PAWN
    if(officercnt > 0):
        token = token | MV_DSTFIELD_IS_FRDLYTOUCHED_BY_OFFICER
    if(queencnt > 0):
        token = token | MV_DSTFIELD_IS_FRDLYTOUCHED_BY_QUEEN

    pawncnt, officercnt, queencnt = count_contacts(enmycontacts)
    if(pawncnt > 0):
        token = token | MV_DSTFIELD_IS_ENMYTOUCHED_BY_PAWN
    if(officercnt > 0):
        token = token | MV_DSTFIELD_IS_ENMYTOUCHED_BY_OFFICER
    if(queencnt > 0):
        token = token | MV_DSTFIELD_IS_ENMYTOUCHED_BY_QUEEN

    return token

