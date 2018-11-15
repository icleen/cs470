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

class RandomAI extends GenericAI {

    public RandomAI(int _me, String host) {
        super(_me, host);
    }

    private void play() {
        int myMove;

        while (true) {
            System.out.println("Read");
            readMessage();

            if (turn == me) {
                System.out.println("Move");
                state = changeState(state);

                myMove = move();

                String sel = myMove / 8 + "\n" + myMove % 8;

                // System.out.println("Selection: " + validMoves[myMove] / 8 + ", " + validMoves[myMove] % 8);

                sout.println(sel);
            }
        }
    }

    // You should modify this function
    // validMoves is a list of valid locations that you could place your "stone" on this turn
    // Note that "state" is a global variable 2D list that shows the state of the game
    private int move() {
        ArrayList<Integer> validMoves = getValidMoves(round, state, 1);
        // just move randomly for now
        int myMove = generator.nextInt(validMoves.size());
        int x, y;
        x = validMoves.get(myMove) / 8;
        y = validMoves.get(myMove) % 8;

        return validMoves.get(myMove);
    }

    private int getValue(int state[][]) {
        int val = 0;
        for(int i = 0; i < state.length; ++i) {
            for(int j = 0; j < state[i].length; ++j) {
                val += state[i][j];
            }
        }
        return val;
    }

    // compile on your machine: javac *.java
    // call: java RandomAI [ipaddress] [player_number]
    //   ipaddress is the ipaddress on the computer the server was launched on.  Enter "localhost" if it is on the same computer
    //   player_number is 1 (for the black player) and 2 (for the white player)
    public static void main(String args[]) {
        new RandomAI(Integer.parseInt(args[1]), args[0]).play();
    }

}
