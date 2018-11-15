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

class MiniMaxAI extends GenericAI {

    int MaxVal = 100;
    int MinVal = -100;

    int cornerWeight = 5;
    int edgeWeight = 3;

    int maxDepth;

    public MiniMaxAI(int _me, String host, int _maxDepth) {
        super(_me, host);
        maxDepth = _maxDepth;
    }

    private void play() {
        int myMove, count = 0;
        long totalTime = 0, time, endTime;

        while (true) {
            System.out.println("Read");
            readMessage();

            if (turn == me) {
                System.out.println("Move");
                int[][] state = changeState(this.state.clone());

                count++;
                time = System.nanoTime();
                myMove = move(state);
                endTime = System.nanoTime();
                time = (endTime - time);
                totalTime += time;
                System.out.println("Time to run: " + time);
                System.out.println("Avg time to run: " + totalTime/count);

                String sel = myMove / 8 + "\n" + myMove % 8;
                sout.println(sel);
            }
        }
    }

    // You should modify this function
    // validMoves is a list of valid locations that you could place your "stone" on this turn
    // Note that "state" is a global variable 2D list that shows the state of the game
    private int move(int[][] state) {
        int topval, botval, bestval, bestvm, depth, val, i, me = 1;
        ArrayList<Integer> validMoves = getValidMoves(round, state, me);
        // if(round < 4) {
        //     return validMoves.get(generator.nextInt(validMoves.size()));
        // }
        printState(state);

        depth = 0;
        topval = MinVal;
        botval = MaxVal;
        bestval = MinVal;
        val = 0;
        bestvm = 0;
        int[][] newstate;
        for(i = 0; i < validMoves.size(); i++) {
            newstate = updateBoard(state, validMoves.get(i)/8,
                                          validMoves.get(i)%8, me);
            System.out.println("newstate: ");
            printState(newstate);
            val = minSearch(newstate, topval, botval, depth+1);
            if(val > bestval) {
                bestval = val;
                bestvm = i;
                topval = Math.max(topval, val);
            }
        }
        return validMoves.get(bestvm);
    }


    private int maxSearch(int[][] state, int topval, int botval, int depth) {
        System.out.print("depth: " + depth);
        if(depth == this.maxDepth) {
            return getValue(state);
        }else {
            int val, i, me = 1;
            ArrayList<Integer> validMoves = getValidMoves(round+depth, state, me);
            if(validMoves.size() < 1) {
                return getValue(state);
            }
            val = MinVal;
            for(i = 0; i < validMoves.size(); i++) {
                val = Math.max( val,
                        minSearch(
                        updateBoard(state, validMoves.get(i)/8, validMoves.get(i)%8, me),
                        topval, botval, depth+1)
                        );
                if(val >= botval) {
                    return val;
                }
                topval = Math.max(topval, val);
            }
            return val;
        }
    }


    private int minSearch(int[][] state, int topval, int botval, int depth) {
        System.out.print("depth: " + depth);
        if(depth == this.maxDepth) {
            return getValue(state);
        }else {
            int val, i, me = -1;
            ArrayList<Integer> validMoves = getValidMoves(round+depth, state, me);
            if(validMoves.size() < 1) {
                return getValue(state);
            }
            val = MaxVal;
            for(i = 0; i < validMoves.size(); i++) {
                val = Math.min( val,
                        maxSearch(
                        updateBoard(state, validMoves.get(i)/8, validMoves.get(i)%8, me),
                        topval, botval, depth+1)
                        );
                if(val <= topval) {
                    return val;
                }
                botval = Math.min(botval, val);
            }
            return val;
        }
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
    // call: java MiniMaxAI [ipaddress] [player_number]
    //   ipaddress is the ipaddress on the computer the server was launched on.
    // Enter "localhost" if it is on the same computer
    //   player_number is 1 (for the black player) and 2 (for the white player)
    public static void main(String args[]) {
        int maxdepth = 2;
        if(args.length > 2) {
            maxdepth = Integer.parseInt(args[2]);
            System.out.println("MaxDepth: " + args[2]);
        }
        new MiniMaxAI(Integer.parseInt(args[1]), args[0], maxdepth).play();
    }

}
