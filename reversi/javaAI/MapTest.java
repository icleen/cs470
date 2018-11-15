import java.awt.*;
import java.util.*;
import java.awt.event.*;
import java.lang.*;
import java.io.*;
import java.net.*;
import javax.swing.*;
import java.math.*;
import java.text.*;

// import javaAI.GenericAI;

class MapTest {

    int round = 8;

    int MaxVal = 100;
    int MinVal = -100;

    int cornerWeight = 5;
    int edgeWeight = 3;

    int maxDepth = 5;

    int me;

    public MapTest(int _me) {
        me = _me;
    }

    protected void printState(int state[][]) {
        for(int i = 0; i < state.length; ++i) {
            for(int j = 0; j < state[i].length; ++j) {
                if(state[i][j] >= 0) {
                    System.out.print(" ");
                }
                System.out.print(state[i][j] + " ");
            }
            System.out.print("\n");
        }
    }

    private int search(int[][] state, int depth, int me) {
        System.out.println("depth: " + depth + ", me: " + me);
        printState(state);
        if(depth == (this.maxDepth)) {
            return getValue(state);
        }
        int val, i, mymove;
        ArrayList<Integer> validMoves = getValidMoves(round, state, me);
        if(validMoves.size() == 0) {
            System.out.println("no validMoves");
            return getValue(state);
        }
        int[][] newstate = updateBoard(state,
                validMoves.get(0)/8, validMoves.get(0)%8, me);
        System.out.println("newstate: ");
        printState(newstate);
        System.out.println("");
        return search( newstate,
                depth+1, me*-1 );
    }


    private int[][] updateBoard(int[][] state, int row, int col, int me) {
        int incx, incy, i;
        int[][] newstate = new int[state.length][];
        for(i = 0; i < state.length; i++)
            newstate[i] = state[i].clone();
        for (incx = -1; incx < 2; incx++) {
            for (incy = -1; incy < 2; incy++) {
                // don't check the 0,0 direction
                if ((incx == 0) && (incy == 0))
                    continue;

                // check sides and diagnols
                newstate = updateDirection(newstate, row, col, incx, incy, me);
            }
        }
        newstate[row][col] = me;
        return newstate;
    }

    private int[][] updateDirection(int state[][], int row, int col,
                                    int incx, int incy, int me) {
        int i, r, c, count = 0;
        boolean isDirection = false;
        for (i = 1; i < 8; i++) {
            r = row+incy*i;
            c = col+incx*i;

            if ((r < 0) || (r > 7) || (c < 0) || (c > 7))
                break;

            if (state[r][c] == -1*me) {
                count++;
            }else {
                if ((state[r][c] == me) && (count > 0))
                    isDirection = true;
                break;
            }
        }
        if(isDirection) {
            System.out.println("checking direction: " + incx + "," + incy);
            for (i = 1; i <= count; i++) {
                r = row+incy*i;
                c = col+incx*i;
                state[r][c] = me;
            }
        }
        return state;
    }


    // generates the set of valid moves for the player; returns a list of valid moves (validMoves)
    protected ArrayList<Integer> getValidMoves(int round, int state[][], int me) {
        int i, j;

        ArrayList<Integer> validMoves = new ArrayList<Integer>();
        if (round < 4) {
            if (state[3][3] == 0) {
                validMoves.add(3*8 + 3);
            }
            if (state[3][4] == 0) {
                validMoves.add(3*8 + 4);
            }
            if (state[4][3] == 0) {
                validMoves.add(4*8 + 3);
            }
            if (state[4][4] == 0) {
                validMoves.add(4*8 + 4);
            }
            // System.out.println("Valid Moves (" + validMoves.size() + "):");
            // for (i = 0; i < numValidMoves; i++) {
            //     System.out.println(validMoves.get(i) / 8 + ", " + validMoves.get(i) % 8);
            // }
        }
        else {
            for (i = 0; i < 8; i++) {
                for (j = 0; j < 8; j++) {
                    if (state[i][j] == 0) {
                        if (couldBe(state, i, j, me)) {
                            validMoves.add(i*8 + j);
                        }
                    }
                }
            }
        }

        return validMoves;
    }

    private boolean couldBe(int state[][], int row, int col, int me) {
        int incx, incy;

        for (incx = -1; incx < 2; incx++) {
            for (incy = -1; incy < 2; incy++) {
                if ((incx == 0) && (incy == 0))
                    continue;

                if (checkDirection(state, row, col, incx, incy, me))
                    return true;
            }
        }

        return false;
    }

    private boolean checkDirection(int state[][], int row, int col, int incx, int incy, int me) {
        int i, r, c, count = 0;

        for (i = 1; i < 8; i++) {
            r = row+incy*i;
            c = col+incx*i;

            if ((r < 0) || (r > 7) || (c < 0) || (c > 7))
                break;

            if (state[r][c] == -1*me)
                count++;
            else {
                if ((state[r][c] == me) && (count > 0))
                    return true;
                break;
            }
        }
        return false;
    }


    private int getValue(int state[][]) {
        int val = 0;
        for(int i = 0; i < state.length; ++i) {
            for(int j = 0; j < state[i].length; ++j) {
                val += state[i][j];
                // give an extra +1 for the edges
                if(i == 0 || i == state.length-1 || j == 0
                          || j == state[i].length-1) {
                    val += state[i][j] * this.edgeWeight;
                }
            }
        }
        // give an extra +1 for the corners
        val += (state[0][0] + state[state.length-1][state.length-1]) * this.cornerWeight;
        val += (state[state.length-1][0] + state[0][state.length-1]) * this.cornerWeight;
        // add the number of possible moves
        ArrayList<Integer> validMoves = getValidMoves(round, state, me);
        val += validMoves.size();
        return val;
    }

    // compile on your machine: javac *.java
    // call: java MiniMaxMonteCarloAI [ipaddress] [player_number]
    //   ipaddress is the ipaddress on the computer the server was launched on.
    // Enter "localhost" if it is on the same computer
    //   player_number is 1 (for the black player) and 2 (for the white player)
    public static void main(String args[]) {
        int[][] state = new int[8][8];
        state[0][2] = 1;
        state[1][2] = 1;
        state[1][3] = 1;
        state[2][1] = -1;
        state[2][2] = -1;
        state[2][3] = -1;
        state[3][3] = 1;
        state[3][4] = 1;
        state[4][3] = -1;
        state[4][4] = -1;
        state[4][5] = -1;

        int depth = 1, me = 1;
        MapTest tester = new MapTest(me);
        int val = tester.search(state, depth, me);
        System.out.println("val: " + val);
    }

}
