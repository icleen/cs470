
from board import Board
from utils import *

class Othello(object):
  """docstring for Othello."""
  def __init__(self):
    super(Othello, self).__init__()
    self.board = Board()
    self.turn = 1
    self.n = 8
    self.movenum = 0
    self.maxturns = self.n * self.n

  def move(self, action):
    vmoves = moves_from_tuples(self.board.get_moves(self.turn, self.movenum), self.n)
    # print(vmoves)
    # print(action)
    # input('waiting')
    if vmoves[action] == 1:
      self.board.move( ((action//self.n), (action%self.n)), self.turn )
      self.movenum += 1
      self.turn *= -1
      return True
    else:
      print('invalid move!')
      return False

  def game_over(self):
    moves = self.board.get_moves(self.turn, self.movenum)
    if len(moves) < 1 or self.movenum >= self.maxturns:
      return True
    else:
      return False

  def get_turn(self):
    return self.turn

  def get_actions(self):
    return moves_from_tuples(self.board.get_moves(self.turn, self.movenum), self.n)

  def get_state(self):
    return self.board.get_state() * self.turn

  def get_true_state(self):
    return self.board.get_state()

  def update_state(self, state):
    self.board.update_state(state)

  def get_score(self):
    return self.board.sum()

  def get_winner(self):
    if self.game_over():
      sm = self.board.sum()
      if sm > 0:
        return 1
      elif sm < 0:
        return -1
      else:
        return 0
    return 0

  def hash(self):
    return self.board.hash()

def main():
  game = Othello()

  for i in range(11):
    actions = game.get_actions()
    if np.sum(actions) < 1:
      print('no moves')
      return
    probs = np.ones(actions.shape[0])
    action = sample(probs, actions)
    game.move(action)
    print(game.get_true_state())
    if game.game_over():
      break

  print(game.get_state())
  print('game over')

if __name__ == '__main__':
  main()
