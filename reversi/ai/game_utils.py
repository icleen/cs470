import sys
import socket
import time
from random import randint


def checkDirection(state, row, col, incx, incy, me):
    count = 0
    other = -1*me

    for i in range(1, 8):
        r = row + incy * i
        c = col + incx * i

        if ((r < 0) or (r > 7) or (c < 0) or (c > 7)):
            break

        if (state[r][c] == other):
            count += 1
        else:
            if ((state[r][c] == me) and (count > 0)):
                return True
            break
    return False

def checkLoc(state, row, col, me):
    for incx in range(-1, 2):
        for incy in range(-1, 2):
            # don't check the 0,0 direction
            if ((incx == 0) and (incy == 0)):
                continue

            # check sides and diagnols
            if(checkDirection(state, row, col, incx, incy, me)):
                return True

    return False

# generates the set of valid moves for the player; returns a list of valid moves (validMoves)
def getValidMoves(state, round, me):
    validMoves = []
    # print("Round: " + str(round))

    # for i in range(8):
    #     print(state[i])

    if (round < 4):
        if (state[3][3] == 0):
            validMoves.append([3, 3])
        if (state[3][4] == 0):
            validMoves.append([3, 4])
        if (state[4][3] == 0):
            validMoves.append([4, 3])
        if (state[4][4] == 0):
            validMoves.append([4, 4])
    else:
        for i in range(8):
            for j in range(8):
                if (state[i][j] == 0):
                    if(checkLoc(state, i, j, me)):
                        validMoves.append([i, j])

    return validMoves


def updateDirection(state, row, col, incx, incy, me):
    count = 0
    other = -1*me
    isDirection = False
    for i in range(1, 8):
        r = row + incy * i
        c = col + incx * i

        if ((r < 0) or (r > 7) or (c < 0) or (c > 7)):
            break

        if (state[r][c] == other):
            count += 1
        else:
            if ((state[r][c] == me) and (count > 0)):
                isDirection = True
            break

    if isDirection:
        for i in range(1, count+1):
            r = row + incy * i
            c = col + incx * i
            state[r,c] = me

    return state

def updateBoard(state, row, col, me):
    newstate = state.copy()
    for incx in range(-1, 2):
        for incy in range(-1, 2):
            # don't check the 0,0 direction
            if ((incx == 0) and (incy == 0)):
                continue

            # check sides and diagnols
            newstate = updateDirection(newstate, row, col, incx, incy, me)

    newstate[row, col] = me
    return newstate
