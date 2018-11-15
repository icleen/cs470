from random import randint
import numpy as np
from game_utils import *

class RandomAI():

  def move(self, state, rnd, me):
    state = np.array(state)
    other = 2
    if me == 2:
      other = 1
    state[state == other] = -1
    state[state == me] = 1
    me = 1
    other = -1
    self.state = state
    validMoves = getValidMoves(state, rnd, me)
    return validMoves[randint(0, len(validMoves) - 1)][:2]
