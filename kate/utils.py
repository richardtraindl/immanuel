

def preformat_board(board, switch):
    data = []

    if(switch == '0'):
        data.append(['letter1', ''])
        for i in range(8):
            data.append(['letter', chr(i + ord('A'))])
        data.append(['letter10', ''])

        for y in range(7, -1, -1):
            data.append(['number1', chr(y + ord('1'))])

            for x in range(8):
                offset = y * 32 + x * 4
                coord = chr(ord('a') + x) + chr(ord('1') + y)
                data.append([coord, board[offset:(offset+3)]])

            data.append(['number10', chr(y + ord('1'))])

        data.append(['letter1', ''])
        for i in range(8):
            data.append(['letter',chr(i + ord('A'))])
        data.append(['letter10', ''])
    else:
        data.append(['letter1', ''])
        for i in range(8):
            data.append(['letter', chr(ord('H') - i)])
        data.append(['letter10', ''])

        for y in range(8):
            data.append(['number1', chr(ord('1') + y)])

            for x in range(7, -1, -1):
                offset = y * 32 + x * 4
                coord = chr(ord('a') + x) + chr(ord('1') + y)
                data.append([coord, board[offset:(offset+3)]])

            data.append(['number10', chr(ord('1') + y)])

        data.append(['letter1', ''])
        for i in range(8):
            data.append(['letter', chr(ord('H') - i)])
        data.append(['letter10', ''])

    return data
