

def reverse_lookup(dic, value):
    for key in dic:
        if dic[key] == value:
            return key
    raiseValueError


def koord_to_index(koord):
    x = ord(koord[0]) - ord('a')
    y = ord(koord[1]) - ord('1')
    return x,y


def index_to_koord(x, y):
    col = chr(x + ord('a'))
    row = chr(y + ord('1'))
    koord = str(col + row)
    return koord
