
    
    def is_move_ok(match, src, dest, prom_piece):
      piece = match.readfield(src)
      if(piece == 'wPw' and (dest // 8) == 7 and not (prom_piece == 'wQu' or prom_piece == 'wRk' or prom_piece == 'wBp' or prom_piece == 'wKn')):
        return False
      elif(piece == 'bPw' and dest // 8 == 0 and not (prom_piece == 'bQu' or prom_piece == 'bRk' or prom_piece == 'bBp' or prom_piece == 'bKn')):
        return False

      return True
