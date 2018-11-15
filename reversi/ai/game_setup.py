import sys
import socket
import time
import numpy as np
from random import randint

from randomAI import RandomAI
from greedyAI import GreedyAI
from greedyPruneAI import GreedyPruneAI
from minimax import MinimaxAI

t1 = 0.0  # the amount of time remaining to player 1
t2 = 0.0  # the amount of time remaining to player 2

state = np.array([[0 for x in range(8)] for y in range(8)])  # state[0][0] is the bottom left corner of the board (on the GUI)


# You should modify this function
# validMoves is a list of valid locations that you could place your "stone" on this turn
# Note that "state" is a global variable 2D list that shows the state of the game
def move(validMoves):
    # just return a random move
    myMove = randint(0, len(validMoves) - 1)

    return myMove


# establishes a connection with the server
def initClient(me, thehost):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (thehost, 3333 + me)
    print('starting up on %s port %s' % server_address, file=sys.stderr)
    sock.connect(server_address)

    info = sock.recv(1024)

    print(info)

    return sock


# reads messages from the server
def readMessage(sock):
    message = sock.recv(1024).decode("utf-8").split("\n")
    # print(message)

    turn = int(message[0])
    # print("Turn: " + str(turn))

    if (turn == -999):
        time.sleep(1)
        sys.exit()

    round = int(message[1])
    print("Round: " + str(round))
    # t1 = float(message[2])  # update of the amount of time available to player 1
    # print t1
    # t2 = float(message[3])  # update of the amount of time available to player 2
    # print t2

    count = 4
    for i in range(8):
        for j in range(8):
            state[i][j] = int(message[count])
            count = count + 1
        # print(state[i])

    return turn, round


def checkDirection(row, col, incx, incy, me):
    sequence = []
    for i in range(1, 8):
        r = row + incy * i
        c = col + incx * i

        if ((r < 0) or (r > 7) or (c < 0) or (c > 7)):
            break

        sequence.append(state[r][c])

    count = 0
    for i in range(len(sequence)):
        if (me == 1):
            if (sequence[i] == 2):
                count = count + 1
            else:
                if ((sequence[i] == 1) and (count > 0)):
                    return True
                break
        else:
            if (sequence[i] == 1):
                count = count + 1
            else:
                if ((sequence[i] == 2) and (count > 0)):
                    return True
                break

    return False


def couldBe(row, col, me):
    for incx in range(-1, 2):
        for incy in range(-1, 2):
            if ((incx == 0) and (incy == 0)):
                continue

            if (checkDirection(row, col, incx, incy, me)):
                return True

    return False


# generates the set of valid moves for the player; returns a list of valid moves (validMoves)
def getValidMoves(round, me):
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
                    if (couldBe(i, j, me)):
                        validMoves.append([i, j])

    return validMoves


# main function that (1) establishes a connection with the server,
# and (2) then plays whenever it is this player's turn
# noinspection PyTypeChecker
def playGame(me, thehost, ai):
    # create a random number generator

    sock = initClient(me, thehost)

    while (True):
        # print("Read")
        status = readMessage(sock)

        if (status[0] == me):
            print("Move")

            other = 2 if me == 1 else 1
            state[state == other] = -1
            state[state == me] = 1
            myMove = ai.move(state, status[1], 1)

            sel = str(myMove[0]) + "\n" + str(myMove[1]) + "\n"
            # print("<" + sel + ">")
            sock.send(sel.encode("utf-8"))
            print("sent the message")
        # else:
        #     print("It isn't my turn")

        # print("")


# call: python RandomGuy.py [ipaddress] [player_number]
# ipaddress is the ipaddress on the computer the server was launched on.
# Enter "localhost" if it is on the same computer
# player_number is 1 (for the black player) and 2 (for the white player)
if __name__ == "__main__":

    if len(sys.argv) < 3:
        print('Arguments: python RandomGuy.py ipaddress player_number [ai_choice] [maxdepth]')
        print('Enter "localhost" in place of ipaddress if it is on the same computer')
        print('player_number is 1 (for the black player) and 2 (for the white player)')
        exit(0)

    maxdepth = 6
    if len(sys.argv) > 4:
        maxdepth = int(sys.argv[4])

    AIs = {
        'random': RandomAI(),
        'greedy': GreedyAI(),
        'greedyprune': GreedyPruneAI(),
        'minimax': MinimaxAI(maxdepth)
    }
    ai = AIs['random']
    if len(sys.argv) < 4:
        print('Doing random')
    else:
        ai_key = sys.argv[3]
        if ai_key in AIs:
            ai = AIs[ai_key]
            print('Doing {}'.format(ai_key))
        else:
            print('{} is not a valid ai'.format(ai_key))
            print('Valid AIs: {}'.format(AIs.keys()))
            exit(0)

    playGame(int(sys.argv[2]), sys.argv[1], ai)
