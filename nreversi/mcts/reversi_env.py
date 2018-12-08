
import numpy as np
from random import randint

from board import Board
from utils import *

class ReversiEnv(object):
  """docstring for ReversiEnv."""
  def __init__(self):
    super(ReversiEnv, self).__init__()
    self.turn = 1
    self.moves = 0
    self.n = 8

  def length(self):
    return self.n*self.n

  def reset(self):
    self.board = Board()
    return self.board.get_state(), 1

  def action_space(self):
    moves = self.board.get_moves(self.turn)
    actions = np.zeros(self.n*self.n)
    if len(moves) <= 0:
      return 0
    for mov in moves:
      actions[mov[0]*self.n+mov[1]] = 1
    return actions

  def step(self, action):
    # print(((action//self.n), (action%self.n)))
    over = self.board.move(((action//self.n), (action%self.n)), self.turn)
    self.moves += 1
    self.turn *= -1
    reward = 0
    if over:
      if self.board.sum() < 0:
        reward = -1
      elif self.board.sum() > 0:
        reward = 1
    return self.board.get_state(), self.turn, reward, over


def main():
  env = ReversiEnv()
  state = env.reset()
  print(state)
  actions = env.action_space()
  print(actions)

  for i in range(64):
    if len(actions) <= 0:
      print(state)
    probs = np.ones(actions.shape[0])
    action = sample(probs, actions)
    # print(action)
    state, turn, reward, done = env.step(action)
    actions = env.action_space()
    # print('end p1')
    if done:
      break
    # print(state)
    # input('round: {}'.format(i))

  print(state)
  print(reward)
  print(done)

if __name__ == '__main__':
  main()
