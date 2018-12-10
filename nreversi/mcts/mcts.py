
import numpy as np
from random import randint
import copy

from board import Board
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


  def get_action(self, board, turn):
    moves = board.get_moves(turn)
    probs = self.get_probabilities(board, turn)
    actions = moves_from_tuples(moves, self.n)
    act = sample(probs, actions)
    return act

  def get_probabilities(self, board, turn):
    for _ in range(self.runs):
      self.search(copy.deepcopy(board), turn)

    probs = np.ones((self.size))
    if self.network is not None:
      probs = self.network(prepare_board(board, turn))
      probs = probs.squeeze().cpu().detach().numpy()

    bhash = board.hash()
    qs = (self.qs[bhash] * self.ns[bhash] * turn)
    if np.min(qs) < 0:
      qs = qs - np.min(qs)
    qs = qs / np.sum(qs)
    probs = probs * qs

    return probs

  def search(self, board, turn):
    moves = board.get_moves(turn)
    bhash = board.hash()
    if bhash not in self.vs:
      self.vs[bhash] = 0
    if len(moves) < 1:
      self.vs[bhash] += board.get_winner()
    else:
      if bhash not in self.qs:
        self.qs[bhash] = np.zeros((self.size))
      if bhash not in self.ns:
        self.ns[bhash] = np.zeros((self.size))

      probs = np.ones((self.size))
      if self.network is not None:
        probs = self.network(prepare_board(board, turn))
        probs = probs.squeeze().cpu().detach().numpy()

      qs = (self.qs[bhash] * self.ns[bhash] * turn)
      if np.min(qs) < 0:
        qs = qs - np.min(qs)
      qs = qs / np.sum(qs)
      probs = probs * qs

      actions = moves_from_tuples(moves, self.n)
      act = sample(probs, actions)

      board.move(moves[act], turn)
      v = self.search(board, turn*-1)
      self.vs[bhash] += v
      self.qs[bhash][act] += v
      self.ns[bhash][act] += 1

    return self.vs[bhash]
