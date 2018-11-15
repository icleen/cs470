from random import randint
import numpy as np
import sys

maxDepth = 2

valcnt = -1
thevals = [8, 2, 0, 1, 9, 2, 10, 3, 4,
           2, 0, 9, 5, 5, 10, 3, 7, 2]

def value():
    global valcnt
    valcnt += 1
    return thevals[valcnt]

def getBranches():
    return range(3)

def maxSearch(state, topval, depth, me):
    validMoves = getBranches()
    print('max - depth: {}, topval: {}, branches: {}'.format(depth, topval, len(validMoves)))
    if len(validMoves) < 1:
        return 0
    if depth == maxDepth:
        bestval = value()
        print('depth: {}, bestval: {}'.format(depth, bestval))
        if bestval >= topval:
            return bestval
        for i, vm in enumerate(validMoves[1:]):
            val = value()
            print('depth: {}, val: {}'.format(depth, val))
            if bestval < val:
                bestval = val
                print('depth: {}, bestval: {}'.format(depth, bestval))
                if bestval >= topval:
                    return bestval
    else:
        bestval = minSearch(state, float('-inf'), depth+1, me*-1)
        print('depth: {}, bestval: {}'.format(depth, bestval))
        if bestval >= topval:
            return bestval
        for i, vm in enumerate(validMoves[1:]):
            val = minSearch(state, bestval, depth+1, me*-1)
            print('depth: {}, val: {}'.format(depth, val))
            if bestval < val:
                bestval = val
                print('depth: {}, bestval: {}'.format(depth, bestval))
                if bestval >= topval:
                    return bestval
    return bestval

def minSearch(state, topval, depth, me):
    validMoves = getBranches()
    print('min - depth: {}, topval: {}, branches: {}'.format(depth, topval, len(validMoves)))
    if len(validMoves) < 1:
        return 0
    if depth == maxDepth:
        bestval = value()
        print('depth: {}, bestval: {}'.format(depth, bestval))
        if bestval <= topval:
            return bestval
        for i, vm in enumerate(validMoves[1:]):
            val = value()
            print('depth: {}, val: {}'.format(depth, val))
            if bestval > val:
                bestval = val
                print('depth: {}, bestval: {}'.format(depth, bestval))
                if bestval <= topval:
                    return bestval
    else:
        bestval = maxSearch(state, float('inf'), depth+1, me*-1)
        print('depth: {}, bestval: {}'.format(depth, bestval))
        if bestval <= topval:
            return bestval
        for i, vm in enumerate(validMoves[1:]):
            val = maxSearch(state, bestval, depth+1, me*-1)
            print('depth: {}, val: {}'.format(depth, val))
            if bestval > val:
                bestval = val
                print('depth: {}, bestval: {}'.format(depth, bestval))
                if bestval <= topval:
                    return bestval

    return bestval

if __name__ == "__main__":
    me = 1
    bestvm = 0
    bestval = float('-inf')
    depth = 0
    validMoves = getBranches()
    bestval = minSearch(None, bestval, depth+1, me*-1)
    print('depth: {}, topval: {}, branches: {}'.format(depth, bestval, len(validMoves)))
    for i, vm in enumerate(validMoves[1:]):
        val = minSearch(None, bestval, depth+1, me*-1)
        print('depth: {}, val: {}, branches: {}'.format(depth, bestval, len(validMoves)))
        if val > bestval:
            bestvm = i
            bestval = val

    print('bestval so far: {}'.format(bestval))
