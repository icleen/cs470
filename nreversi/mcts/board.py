import numpy as np
from random import randint

class Board(object):
  """docstring for Board."""
  def __init__(self):
    super(Board, self).__init__()

    self.board = np.zeros((8, 8), dtype=np.int)
    self.movenum = 0
    self.maxturns = 8 * 8

  def get_moves(self, player):
    moves = []
    if (self.movenum < 4):
      if (self.board[3,3] == 0):
        moves.append((3, 3))
      if (self.board[3,4] == 0):
        moves.append((3, 4))
      if (self.board[4,3] == 0):
        moves.append((4, 3))
      if (self.board[4,4] == 0):
        moves.append((4, 4))
    else:
      for row in range(8):
        for col in range(8):
          if (self.board[row][col] == 0):
            if (self.check_valid(row, col, player)):
              moves.append((row, col))
    return moves

  def check_valid(self, row, col, player):
    for incr in range(-1, 2):
      for incc in range(-1, 2):
        if ((incr != 0) or (incc != 0)):
          if (self.ch_direction(row, col, incr, incc, player)):
            return True
    return False

  def ch_direction(self, row, col, incr, incc, player, turn=False):
    count = 0
    isDirection = False
    for i in range(1, 8):
      r = row + incr * i
      c = col + incc * i
      if ((r < 0) or (r > 7) or (c < 0) or (c > 7)):
        break

      if self.board[r,c] == -1*player:
        count += 1
      else:
        if self.board[r,c] == player and count > 0:
          isDirection = True
        break

    if not turn:
      return isDirection

    if isDirection:
      for i in range(1,count+1):
        r = row + incr*i
        c = col + incc*i
        self.board[r,c] = player


  def move(self, location, player):
    for incx in range(-1, 2):
      for incy in range(-1, 2):
        if ((incx != 0) or (incy != 0)):
          self.ch_direction(
            location[0], location[1], incx, incy, player, True)
    self.board[location] = player
    self.movenum += 1
    moves = self.get_moves(player*-1)
    if len(moves) <= 0 or self.movenum >= self.maxturns:
      return True
    else:
      return False

  def get_state(self):
    return self.board

  def update_state(self, state):
    self.board = np.array(state)

  def sum(self):
    return np.sum(self.board)


def main():
  board = Board()

  for i in range(30):
    moves = board.get_moves(1)
    # print(moves)
    if len(moves) <= 0:
      return
    loc = randint(0, len(moves) - 1)
    board.move(moves[loc], 1)
    # print('end p1')

    moves = board.get_moves(-1)
    # print(moves)
    loc = randint(0, len(moves) - 1)
    board.move(moves[loc], -1)
    # print('end p2')


if __name__ == '__main__':
  main()
