#from .. match import *
#from .. import rules
from .. cvalues import *


def count_contacts(contacts):
    pawncnt = 0
    officercnt = 0
    queencnt = 0
    kingcnt = 0

    for contact in contacts:
        if(contact == PIECES['wPw'] or contact == PIECES['bPw']):
            pawncnt += 1
        elif(contact == PIECES['wQu'] or contact == PIECES['bQu']):
            queencnt += 1
        elif(contact == PIECES['wKg'] or contact == PIECES['bKg']):
            kingcnt += 1
        else:
            officercnt += 1
    return pawncnt, officercnt, queencnt, kingcnt


def contacts_to_token(frdlycontacts, enmycontacts, mode):
    token = 0x0

    frdlypawncnt, frdlyofficercnt, frdlyqueencnt, frdlykingcnt = count_contacts(frdlycontacts)
    enmypawncnt, enmyofficercnt, enmyqueencnt, enmykingcnt = count_contacts(enmycontacts)

    if(mode == "SRCFIELDTOUCHES"):
        if(frdlypawncnt > 0):
            token = token | SRCFIELD_IS_FRDLYTOUCHED_BY_PAWN
        if(frdlyofficercnt > 0):
            token = token | SRCFIELD_IS_FRDLYTOUCHED_BY_OFFICER
        if(frdlyqueencnt > 0):
            token = token | SRCFIELD_IS_FRDLYTOUCHED_BY_QUEEN
        if(frdlykingcnt > 0):
            token = token | SRCFIELD_IS_FRDLYTOUCHED_BY_KING
        
        if(enmypawncnt > 0):
            token = token | SRCFIELD_IS_ENMYTOUCHED_BY_PAWN
        if(enmyofficercnt > 0):
            token = token | SRCFIELD_IS_ENMYTOUCHED_BY_OFFICER
        if(enmyqueencnt > 0):
            token = token | SRCFIELD_IS_ENMYTOUCHED_BY_QUEEN
        if(enmykingcnt > 0):
            token = token | SRCFIELD_IS_ENMYTOUCHED_BY_KING
    elif(mode == "DSTFIELDTOUCHES"):
        if(frdlypawncnt > 0):
            token = token | DSTFIELD_IS_FRDLYTOUCHED_BY_PAWN
        if(frdlyofficercnt > 0):
            token = token | DSTFIELD_IS_FRDLYTOUCHED_BY_OFFICER
        if(frdlyqueencnt > 0):
            token = token | DSTFIELD_IS_FRDLYTOUCHED_BY_QUEEN
        if(frdlykingcnt > 0):
            token = token | DSTFIELD_IS_FRDLYTOUCHED_BY_KING

        if(enmypawncnt > 0):
            token = token | DSTFIELD_IS_ENMYTOUCHED_BY_PAWN
        if(enmyofficercnt > 0):
            token = token | DSTFIELD_IS_ENMYTOUCHED_BY_OFFICER
        if(enmyqueencnt > 0):
            token = token | DSTFIELD_IS_ENMYTOUCHED_BY_QUEEN
        if(enmykingcnt > 0):
            token = token | DSTFIELD_IS_ENMYTOUCHED_BY_KING
    elif(mode == "ATTACKTOUCHES"):
        if(frdlypawncnt > 0):
            token = token | ATTACKED_IS_ADD_ATT_FROM_PAWN
        if(frdlyofficercnt + frdlyqueencnt + frdlykingcnt > 0):
            token = token | ATTACKED_IS_ADD_ATT_FROM_OFFICER

        if(enmypawncnt > 0):
            token = token | ATTACKED_IS_SUPP_BY_PAWN
        if(enmyofficercnt > 0 or enmyqueencnt > 0 or enmykingcnt > 0):
            token = token | ATTACKED_IS_SUPP_BY_OFFICER
    elif(mode == "SUPPORTTOUCHES"):
        if(frdlypawncnt > 0):
            token = token | SUPPORTED_IS_ADD_SUPP_BY_PAWN
        if(frdlyofficercnt + frdlyqueencnt + frdlykingcnt > 0):
            token = token | SUPPORTED_IS_ADD_SUPP_BY_OFFICER

        if(enmypawncnt > 0):
            token = token | SUPPORTED_IS_ATT_FROM_PAWN
        if(enmyofficercnt > 0 or enmyqueencnt > 0 or enmykingcnt > 0):
            token = token | SUPPORTED_IS_ATT_FROM_OFFICER

    return token

