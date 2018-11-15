import java.awt.*;
import java.util.*;
import java.awt.event.*;
import java.lang.*;
import java.io.*;
import java.net.*;
import javax.swing.*;
import java.math.*;
import java.text.*;

class GenericAI {

    public Socket s;
	public BufferedReader sin;
	public PrintWriter sout;
    Random generator = new Random();

    double t1, t2;
    int me;
    int boardState;
    int state[][] = new int[8][8]; // state[0][0] is the bottom left corner of the board (on the GUI)
    int turn = -1;
    int round;

    int validMoves[] = new int[64];
    int numValidMoves;


    // main function that (1) establishes a connection with the server, and then plays whenever it is this player's turn
    public GenericAI(int _me, String host) {
        me = _me;
        initClient(host);
        //while (turn == me) {
        //    System.out.println("My turn");

            //readMessage();
        //}
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

                System.out.println("Selection: " + myMove / 8 + ", " + myMove % 8);

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

    protected int[][] changeState(int state[][]) {
        for(int i = 0; i < state.length; ++i) {
            for(int j = 0; j < state[i].length; ++j) {
                if(state[i][j] == this.me) {
                    state[i][j] = 1;
                }else if(state[i][j] != 0) {
                    state[i][j] = -1;
                }
            }
        }
        return state;
    }

    protected void printState(int state[][]) {
        for(int i = 0; i < state.length; ++i) {
            for(int j = 0; j < state[i].length; ++j) {
                System.out.print(state[i][j] + " ");
            }
            System.out.print("\n");
        }
    }

    protected int[][] updateBoard(int[][] state, int row, int col, int me) {
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

    protected int[][] updateDirection(int state[][], int row, int col,
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

    public void readMessage() {
        int i, j;
        String status;
        try {
            //System.out.println("Ready to read again");
            turn = Integer.parseInt(sin.readLine());

            if (turn == -999) {
                try {
                    Thread.sleep(200);
                } catch (InterruptedException e) {
                    System.out.println(e);
                }

                System.exit(1);
            }

            //System.out.println("Turn: " + turn);
            round = Integer.parseInt(sin.readLine());
            t1 = Double.parseDouble(sin.readLine());
            System.out.println(t1);
            t2 = Double.parseDouble(sin.readLine());
            System.out.println(t2);
            for (i = 0; i < 8; i++) {
                for (j = 0; j < 8; j++) {
                    state[i][j] = Integer.parseInt(sin.readLine());
                }
            }
            sin.readLine();
        } catch (IOException e) {
            System.err.println("Caught IOException: " + e.getMessage());
        }

        // System.out.println("Turn: " + turn);
        System.out.println("Round: " + round);
        // for (i = 7; i >= 0; i--) {
        //     for (j = 0; j < 8; j++) {
        //         System.out.print(state[i][j]);
        //     }
        //     System.out.println();
        // }
        // System.out.println();
    }

    public void initClient(String host) {
        int portNumber = 3333+me;

        try {
			s = new Socket(host, portNumber);
            sout = new PrintWriter(s.getOutputStream(), true);
			sin = new BufferedReader(new InputStreamReader(s.getInputStream()));

            String info = sin.readLine();
            System.out.println(info);
        } catch (IOException e) {
            System.err.println("Caught IOException: " + e.getMessage());
        }
    }


    // compile on your machine: javac *.java
    // call: java GenericAI [ipaddress] [player_number]
    //   ipaddress is the ipaddress on the computer the server was launched on.  Enter "localhost" if it is on the same computer
    //   player_number is 1 (for the black player) and 2 (for the white player)
    public static void main(String args[]) {
        new GenericAI(Integer.parseInt(args[1]), args[0]).play();
    }

}
