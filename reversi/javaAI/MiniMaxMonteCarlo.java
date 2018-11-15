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

class MiniMaxMonteCarloAI extends GenericAI {

    double MaxVal = 100000.0;
    double MinVal = -100000.0;

    double cornerWeight = 5.0;
    double edgeWeight = 3.0;

    int maxDepth = 6;
    int monteDepth = 6;
    int monteBranch = 2;


    public MiniMaxMonteCarloAI(int _me, String host
                                // , int _maxDepth, int _monteDepth, int _monteBranch
                                ) {
        super(_me, host);
        // maxDepth = _maxDepth;
        // monteDepth = _monteDepth;
        // monteBranch = _monteBranch;
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
    // validMoves is a list of valid locations that you could place your
    // "stone" on this turn
    // Note that "state" is a global variable 2D list that shows the
    // state of the game
    private int move(int[][] state) {
        double topval, botval, bestval, val;
        int bestvm, depth, i, me = 1;
        ArrayList<Integer> validMoves = getValidMoves(round, state, me);
        // if(round < 4) {
        //     return validMoves.get(generator.nextInt(validMoves.size()));
        // }
        printState(state);
        depth = 0;
        topval = MinVal;
        botval = MaxVal;
        bestval = MinVal;
        val = 0.0;
        bestvm = 0;
        for(i = 0; i < validMoves.size(); i++) {
            val = minSearch(
                    updateBoard(state, validMoves.get(i)/8,
                    validMoves.get(i)%8, me),
                    topval, botval, depth+1
                    );
            if(val > bestval) {
                bestval = val;
                bestvm = i;
                topval = Math.max(topval, val);
            }
        }
        return validMoves.get(bestvm);
    }


    private double maxSearch(int[][] state, double topval, double botval, int depth) {
        // System.out.println("depth: " + depth);
        double val;
        int i, me = 1;
        if(depth == this.maxDepth) {
            return carloDeepSearch(state, depth, me);
        }
        ArrayList<Integer> validMoves = getValidMoves(this.round+depth, state, me);
        if(validMoves.size() < 1) {
            // System.out.println("no moves");
            return getValue(state, this.round+depth);
        }
        // System.out.println("; moves: " + validMoves.size());
        val = MinVal;
        for(i = 0; i < validMoves.size(); i++) {
            val = Math.max( val,
                    minSearch(
                    updateBoard(state, validMoves.get(i)/8,
                                       validMoves.get(i)%8, me),
                    topval, botval, depth+1
                    )
                    );
            if(val >= botval) {
                // System.out.println("; pruning");
                return val;
            }
            topval = Math.max(topval, val);
        }
        // System.out.println("; no pruning");
        return val;
    }


    private double minSearch(int[][] state, double topval, double botval, int depth) {
        // System.out.println("depth: " + depth);
        double val;
        int i, me = -1;
        if(depth == this.maxDepth) {
            return carloDeepSearch(state, depth, me);
        }
        ArrayList<Integer> validMoves = getValidMoves(this.round+depth, state, me);
        if(validMoves.size() < 1) {
            // System.out.println("no moves");
            return getValue(state, this.round+depth);
        }
        // System.out.println("; moves: " + validMoves.size());
        val = MaxVal;
        for(i = 0; i < validMoves.size(); i++) {
            val = Math.min( val,
                    maxSearch(
                    updateBoard(state, validMoves.get(i)/8,
                                       validMoves.get(i)%8, me),
                    topval, botval, depth+1
                    )
                    );
            if(val <= topval) {
                // System.out.println("; pruning");
                return val;
            }
            botval = Math.min(botval, val);
        }
        // System.out.println("; no pruning");
        return val;
    }

    private double carloDeepSearch(int[][] state, int depth, int me) {
        if(depth == (this.maxDepth + this.monteDepth)) {
            return getValue(state, this.round+depth);
        }
        // System.out.println("carlo depth: " + depth);
        double val = 0.0;
        int i, mymove;
        ArrayList<Integer> validMoves = getValidMoves(this.round+depth, state, me);
        if(validMoves.size() == 0) {
            // System.out.println("No valid moves");
            // printState(state);
            return getValue(state, this.round+depth);
        }else if(validMoves.size() <= this.monteBranch) {
            for(i = 0; i < validMoves.size(); i++) {
                val += carloDeepSearch( updateBoard(state,
                        validMoves.get(i)/8, validMoves.get(i)%8, me),
                        depth+1, me*-1 );
            }
            return val/validMoves.size();
        }
        for(i = 0; i < this.monteBranch; i++) {
            mymove = generator.nextInt(validMoves.size());
            val += carloDeepSearch( updateBoard(state,
                    validMoves.get(mymove)/8, validMoves.get(mymove)%8, me),
                    depth+1, me*-1 );
        }
        return val/this.monteBranch;
    }


    private double getValue(int state[][], int round) {
        double val = 0;
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
        // int maxdepth = 2, monteDepth = 10, monteBranch = ;
        // if(args.length > 2) {
        //     maxdepth = Integer.parseInt(args[2]);
        //     System.out.println("MaxDepth: " + args[2]);
        // }
        new MiniMaxMonteCarloAI(Integer.parseInt(args[1]), args[0]).play();
    }

}
