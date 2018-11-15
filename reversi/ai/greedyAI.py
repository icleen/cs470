from random import randint
import numpy as np
from game_utils import *

class GreedyAI():

    def __init__(self):
        self.state = None

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

        # choose random start move
        if (rnd < 4):
            validMoves = getValidMoves(state, rnd, me)
            return validMoves[randint(0, len(validMoves) - 1)][:2]

        validMoves = getValidMoves(state, rnd, me)
        bestvm = 0
        bestval = validMoves[0][-1]
        for i, vm in enumerate(validMoves[1:]):
            if bestval < vm[-1]:
                bestvm = i
                bestval = vm[-1]
        return validMoves[bestvm][:2]

    def value(self, moov, me):
        lookstate = updateBoard(self.state.copy(), moov[0], moov[0], me)
        return np.sum(lookstate[lookstate==me]) - np.sum(lookstate[lookstate==other])
