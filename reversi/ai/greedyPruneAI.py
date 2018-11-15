from random import randint
import numpy as np
from game_utils import *

class GreedyPruneAI():

    def __init__(self, maxDepth=6):
        self.maxDepth = maxDepth

    def move(self, state, rnd, me):
        state = np.array(state)
        other = 2
        if me == 2:
            other = 1
        state[state == other] = -1
        state[state == me] = 1
        me = 1
        other = -1
        self.rnd = rnd

        # print(state)
        # print(self.value(state))

        # for the first four moves, just do random
        if (rnd < 4):
            validMoves = getValidMoves(state, rnd, me)
            return validMoves[randint(0, len(validMoves) - 1)][:2]

        validMoves = getValidMoves(state, rnd, me=me)
        bestvm = 0
        bestval = float('-inf')
        depth = 0
        # print(updateBoard(state.copy(), validMoves[0][0], validMoves[0][1], me))
        # print(self.value(updateBoard(state.copy(), validMoves[0][0], validMoves[0][1], me)))
        # print('depth: {}, topval: {}, branches: {}'.format(depth, bestval, len(validMoves)))
        bestval = self.minSearch(updateBoard(state.copy(),
                                 validMoves[0][0], validMoves[0][1], me),
                                 bestval, depth+1, me*-1)
        # print('depth: {}, topval: {}, branches: {}'.format(depth, bestval, len(validMoves)))
        for i, vm in enumerate(validMoves[1:]):
            val = self.minSearch(updateBoard(state.copy(),
                                 validMoves[0][0], validMoves[0][1], me),
                                 bestval, depth+1, me*-1)
            if val > bestval:
                bestvm = i
                bestval = val
        # input('bestval so far: {}'.format(bestval))
        return validMoves[bestvm][:2]

    # look at your branches and select the highest valued branch
    # if necessary, look recursively at branches by looking at the minSearch values
    def maxSearch(self, state, topval, depth, me):
        validMoves = getValidMoves(state, self.rnd, me=me)
        # print('max - depth: {}, topval: {}, branches: {}'.format(depth, topval, len(validMoves)))
        if len(validMoves) < 1:
            return 0
        if depth == self.maxDepth:
            bestval = self.value(updateBoard(state.copy(), validMoves[0][0], validMoves[0][1], me))
            # print('depth: {}, bestval: {}'.format(depth, bestval))
            if bestval >= topval:
                return bestval
            for i, vm in enumerate(validMoves[1:]):
                val = self.value(updateBoard(state.copy(), vm[0], vm[1], me))
                # print('depth: {}, val: {}'.format(depth, val))
                if bestval < val:
                    bestval = val
                    # print('depth: {}, bestval: {}'.format(depth, bestval))
                    if bestval >= topval:
                        return bestval
        else:
            bestval = self.minSearch(updateBoard(state.copy(),
                                     validMoves[0][0], validMoves[0][1], me*-1),
                                     float('-inf'), depth+1, me*-1)
            # print('depth: {}, bestval: {}'.format(depth, bestval))
            if bestval >= topval:
                return bestval
            for i, vm in enumerate(validMoves[1:]):
                val = self.minSearch(updateBoard(state.copy(), vm[0], vm[1], me*-1),
                                         bestval, depth+1, me*-1)
                # print('depth: {}, val: {}'.format(depth, val))
                if bestval < val:
                    bestval = val
                    # print('depth: {}, bestval: {}'.format(depth, bestval))
                    if bestval >= topval:
                        return bestval
        return bestval

    # look at your branches and select the lowest value branch
    # if necessary, look recursively at branches by looking at the maxSearch values
    def minSearch(self, state, topval, depth, me):
        validMoves = getValidMoves(state, self.rnd, me=me)
        # print('min - depth: {}, topval: {}, branches: {}'.format(depth, topval, len(validMoves)))
        if len(validMoves) < 1:
            return 0
        if depth == self.maxDepth:
            bestval = self.value(updateBoard(state.copy(), validMoves[0][0], validMoves[0][1], me))
            # print('depth: {}, bestval: {}'.format(depth, bestval))
            if bestval <= topval:
                return bestval
            for i, vm in enumerate(validMoves[1:]):
                val = self.value(updateBoard(state.copy(), vm[0], vm[1], me))
                # print('depth: {}, val: {}'.format(depth, val))
                if bestval > val:
                    bestval = val
                    # print('depth: {}, bestval: {}'.format(depth, bestval))
                    if bestval <= topval:
                        return bestval
        else:
            bestval = self.maxSearch(updateBoard(state.copy(),
                                     validMoves[0][0], validMoves[0][1], me*-1),
                                     float('inf'), depth+1, me*-1)
            # print('depth: {}, bestval: {}'.format(depth, bestval))
            if bestval <= topval:
                return bestval
            for i, vm in enumerate(validMoves[1:]):
                val = self.maxSearch(updateBoard(state.copy(), vm[0], vm[1], me*-1),
                                         bestval, depth+1, me*-1)
                # print('depth: {}, val: {}'.format(depth, val))
                if bestval > val:
                    bestval = val
                    # print('depth: {}, bestval: {}'.format(depth, bestval))
                    if bestval <= topval:
                        return bestval

        return bestval

    # a generalized version of the above methods where the values are just
    # switched every time you go down a layer
    def genericSearch(self, state, topval, depth):
        validMoves = getValidMoves(state)
        if depth == self.maxDepth:
            bestval = self.value(updateBoard(state.copy(), validMoves[0][0], validMoves[0][1])),
            if bestval >= topval:
                return bestval
            for i, vm in enumerate(validMoves[1:]):
                val = self.value(updateBoard(state.copy(), vm[0], vm[1]))
                if bestval < val:
                    bestval = val
                    if bestval >= topval:
                        return bestval
        else:
            bestval = self.genericSearch(updateBoard(state.copy(),
                                     validMoves[0][0], validMoves[0][1])*-1,
                                     float('inf'), depth+1)*-1
            for i, vm in enumerate(validMoves[1:]):
                val = self.genericSearch(updateBoard(state.copy(), vm[0], vm[1])*-1,
                                         topval*-1, depth+1, me*-1)*-1
                if bestval < val:
                    bestval = val
        return bestval

    def value(self, state):
        # add up the positions player has on the top and bottom rows
        val = np.sum(state[0]) + np.sum(state[-1])
        # add the positions player has on the right and left cols
        val += np.sum(state[:, 0]) + np.sum(state[:, -1])
        # add the corner positions
        val += state[0,0] + state[-1,0] + state[0,-1] + state[-1,-1]
        # return the value with edge pieces getting higher value
        return np.sum(state) + val
