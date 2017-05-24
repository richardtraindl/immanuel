

def reverse_lookup(dic, value):
    for key in dic:
        if dic[key] == value:
            return key

def coord_to_index(coord):
    x = ord(coord[0]) - ord('a')
    y = ord(coord[1]) - ord('1')
    return x,y


def index_to_coord(x, y):
    col = chr(x + ord('a'))
    row = chr(y + ord('1'))
    coord = str(col + row)
    return coord

