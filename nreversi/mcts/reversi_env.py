
import numpy as np
from random import randint

from game import Othello
from utils import *

class ReversiEnv(object):
  """docstring for ReversiEnv."""
  def __init__(self):
    super(ReversiEnv, self).__init__()
    self.n = 8

  def length(self):
    return self.n*self.n

  def reset(self):
    self.game = Othello()
    return self.game.get_state(), self.game.get_turn()

  def action_space(self):
    return self.game.get_actions()

  def step(self, action):
    self.game.move(action)
    reward = self.game.get_winner()
    return self.game.get_state(), self.game.get_turn(), reward


def main():
  env = ReversiEnv()
  state, turn = env.reset()
  print(state)
  actions = env.action_space()
  print(actions)
  done = False

  for i in range(64):
    if len(actions) < 1:
      print(state)
    probs = np.ones(actions.shape[0])
    action = sample(probs, actions)
    # print(action)
    state, turn, reward = env.step(action)
    actions = env.action_space()
    if reward != 0:
      done = True
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
