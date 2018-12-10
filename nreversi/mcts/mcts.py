
import numpy as np
from random import randint
import copy

from game import Othello
from utils import *

class MCTS(object):
  """docstring for MCTS."""
  def __init__(self, network=None, runs=25, n=8):
    super(MCTS, self).__init__()
    self.network = network
    self.runs = runs
    self.n = n
    self.size = n*n

    self.vs = {}
    self.ns = {}
    self.qs = {}
    self.scores = {}


  def get_action(self, game):
    actions = game.get_actions()
    probs = self.get_probabilities(game)
    act = sample(probs, actions)
    return act

  def get_probabilities(self, game):
    for _ in range(self.runs):
      self.search(copy.deepcopy(game))

    probs = np.ones((self.size))
    if self.network is not None:
      probs = self.network(prepare_game(game))
      probs = probs.squeeze().cpu().detach().numpy()

    bhash = game.hash()
    qs = (self.qs[bhash] * self.ns[bhash] * game.get_turn())
    if np.min(qs) < 0:
      qs = qs - np.min(qs)
    qs = qs / np.sum(qs)
    probs = probs * qs

    return probs / np.sum(probs)

  def search(self, game):
    bhash = game.hash()
    if bhash not in self.vs:
      self.vs[bhash] = 0
    if game.game_over():
      self.vs[bhash] += game.get_winner()
    else:
      if bhash not in self.qs:
        self.qs[bhash] = np.zeros((self.size))
      if bhash not in self.ns:
        self.ns[bhash] = np.zeros((self.size))

      probs = np.ones((self.size))
      if self.network is not None:
        probs = self.network(prepare_game(game))
        probs = probs.squeeze().cpu().detach().numpy()

      qs = (self.qs[bhash] * self.ns[bhash] * game.get_turn())
      if np.min(qs) < 0:
        qs = qs - np.min(qs)
      qs = qs / np.sum(qs)
      probs = probs * qs

      actions = game.get_actions()
      act = sample(probs, actions)

      game.move(act)
      v = self.search(game)
      self.vs[bhash] += v
      self.qs[bhash][act] += v
      self.ns[bhash][act] += 1

    return self.vs[bhash]

def main():
  mcts = MCTS()
  game = Othello()

  for i in range(5):
    action = mcts.get_action(game)
    game.move(action)
    print(game.get_true_state())
    if game.game_over():
      break

  print('game over')


if __name__ == '__main__':
  main()
