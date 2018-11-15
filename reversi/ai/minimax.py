from random import randint
import numpy as np
from game_utils import *

class MinimaxAI():

    def __init__(self, maxDepth=6):
        self.maxDepth = maxDepth
        self.rnd = 0

        self.cornerWeight = 5
        self.edgeWeight = 3

    def move(self, state, rnd, me):
        self.rnd = rnd

        validMoves = getValidMoves(state, rnd, me=me)

        # for the first four moves, just do random
        # if (rnd < 4):
        #     return validMoves[randint(0, len(validMoves) - 1)][:2]

        print(state)

        depth = 0
        topval = float('-inf')
        botval = float('inf')
        bestval = float('-inf')
        val = 0
        bestvm = 0
        for i, vm in enumerate(validMoves):
            newstate = updateBoard(state, vm[0], vm[1], me)
            print(newstate)
            val = self.minSearch(newstate, topval, botval, depth+1)
            if val > bestval:
                bestval = val
                bestvm = i
                topval = max(topval, val)

        return validMoves[bestvm]

    # look at your branches and select the highest valued branch
    # if necessary, look recursively at branches by looking at the minSearch values
    def maxSearch(self, state, topval, botval, depth):
        # print('max - depth: {}, topval: {}, branches: {}'.format(depth, topval, len(validMoves)))
        if depth == self.maxDepth:
            return self.value(state)
        else:
            me = 1
            validMoves = getValidMoves(state, self.rnd+depth, me)
            if len(validMoves) < 1:
                return self.value(state)

            val = float('-inf')
            for i, vm in enumerate(validMoves):
                val = max(val,
                    self.minSearch(
                    updateBoard(state, vm[0], vm[1], me),
                    topval, botval, depth+1)
                    )
                if val >= botval:
                    return val
                topval = max(topval, val)
            return val

    # look at your branches and select the lowest value branch
    # if necessary, look recursively at branches by looking at the maxSearch values
    def minSearch(self, state, topval, botval, depth):
        if depth == self.maxDepth:
            return self.value(state)
        else:
            me = -1
            validMoves = getValidMoves(state, self.rnd+depth, me)
            if len(validMoves) < 1:
                return self.value(state)
            val = float('inf')
            for i, vm in enumerate(validMoves):
                val = max(val,
                    self.maxSearch(
                    updateBoard(state, vm[0], vm[1], me),
                    topval, botval, depth+1)
                    )
                if val <= topval:
                    return val
                botval = min(botval, val)
            return val

    def value(self, state):
        # add up the pieces player has minus pieces opponent has
        val = np.sum(state)
        # add up the positions player has on the top and bottom rows
        val += np.sum(state[0]) + np.sum(state[-1]) * self.edgeWeight
        # add the positions player has on the right and left cols
        val += np.sum(state[:, 0]) + np.sum(state[:, -1]) * self.edgeWeight
        # add the corner positions
        val += (state[0,0] + state[-1,0] + state[0,-1] + state[-1,-1]) * self.cornerWeight
        # add the number of valid moves in the state
        val += len(getValidMoves(state, self.rnd, 1))
        return np.sum(state) + val
