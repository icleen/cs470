
import javax.swing.*;
import java.awt.event.*;
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.lang.*;
import javax.swing.JComponent;
import javax.swing.JFrame;
import java.io.*;
import java.util.Random;
import java.util.Scanner;
import java.net.*;
import java.lang.Math;

// This is the main class that you will add to in order to complete the lab
public class TheRobot extends JFrame {
    // Mapping of actions to integers
    public static final int NORTH = 0;
    public static final int SOUTH = 1;
    public static final int EAST = 2;
    public static final int WEST = 3;
    public static final int STAY = 4;

    Color bkgroundColor = new Color(230,230,230);

    static mySmartMap myMaps; // instance of the class that draw everything to the GUI
    String mundoName;

    World mundo; // mundo contains all the information about the world.  See World.java
    double moveProb, sensorAccuracy;  // stores probabilies that the robot moves in the intended direction
                                      // and the probability that a sonar reading is correct, respectively

    // variables to communicate with the Server via sockets
    public Socket s;
	public BufferedReader sin;
	public PrintWriter sout;

    // variables to store information entered through the command-line about the current scenario
    boolean isManual = false; // determines whether you (manual) or the AI (automatic) controls the robots movements
    boolean knownPosition = false;
    int startX = -1, startY = -1;
    int decisionDelay = 250;

    // store your probability map (for position of the robot in this array
    double[][] probs;

    // store your computed value of being in each state (x, y)
    double[][] values;
    double gamma = 0.99;
    int actionNum;

    public TheRobot(String _manual, int _decisionDelay) {
        // initialize variables as specified from the command-line
        if (_manual.equals("automatic"))
            isManual = false;
        else
            isManual = true;
        decisionDelay = _decisionDelay;

    // get a connection to the server and get initial information about the world
        initClient();

        // Read in the world
        mundo = new World(mundoName);

        // set up the GUI that displays the information you compute
        int width = 500;
        int height = 500;
        int bar = 20;
        setSize(width,height+bar);
        getContentPane().setBackground(bkgroundColor);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setBounds(0, 0, width, height+bar);
        myMaps = new mySmartMap(width, height, mundo);
        getContentPane().add(myMaps);

        setVisible(true);
        setTitle("Probability and Value Maps");
// Function to have the robot move about its world
// until it gets to its goal or falls in a stairwell
        doStuff();
    }

    // this function establishes a connection with the server and learns
    //   1 -- which world it is in
    //   2 -- it's transition model (specified by moveProb)
    //   3 -- it's sensor model (specified by sensorAccuracy)
    //   4 -- whether it's initial position is known.
    //         if known, its position is stored in (startX, startY)
    public void initClient() {
        int portNumber = 3333;
        String host = "localhost";

        try {
			s = new Socket(host, portNumber);
            sout = new PrintWriter(s.getOutputStream(), true);
			sin = new BufferedReader(new InputStreamReader(s.getInputStream()));

            mundoName = sin.readLine();
            moveProb = Double.parseDouble(sin.readLine());
            sensorAccuracy = Double.parseDouble(sin.readLine());
            System.out.println("Need to open the mundo: " + mundoName);
            System.out.println("moveProb: " + moveProb);
            System.out.println("sensorAccuracy: " + sensorAccuracy);

            // find out of the robots position is know
            String _known = sin.readLine();
            if (_known.equals("known")) {
                knownPosition = true;
                startX = Integer.parseInt(sin.readLine());
                startY = Integer.parseInt(sin.readLine());
                System.out.println("Robot's initial position is known: " +
                        startX + ", " + startY);
            }
            else {
                System.out.println("Robot's initial position is unknown");
            }
        } catch (IOException e) {
            System.err.println("Caught IOException: " + e.getMessage());
        }
    }

    // function that gets human-specified actions
    // 'i' specifies the movement up
    // ',' specifies the movement down
    // 'l' specifies the movement right
    // 'j' specifies the movement left
    // 'k' specifies the movement stay
    int getHumanAction() {
        System.out.println("Reading the action selected by the user");
        while (myMaps.currentKey < 0) {
            try {
                Thread.sleep(50);
            }
            catch(InterruptedException ex) {
                Thread.currentThread().interrupt();
            }
        }
        int a = myMaps.currentKey;
        myMaps.currentKey = -1;

        System.out.println("Action: " + a);

        return a;
    }

    // initializes the probabilities of where the AI is
    void initializeProbabilities() {
        probs = new double[mundo.width][mundo.height];
        // if the robot's initial position is known, reflect that in the probability map
        if (knownPosition) {
            probs[startX][startY] = 1.0;
        }
        else {  // otherwise, set up a uniform prior over all the positions in the world that are open spaces
            int x, y, count = 0;

            for (y = 0; y < mundo.height; y++) {
                for (x = 0; x < mundo.width; x++) {
                    if (mundo.grid[x][y] == 0)
                        count++;
                }
            }
            double iprob = 1.0 / count;
            for (y = 0; y < mundo.height; y++) {
                for (x = 0; x < mundo.width; x++) {
                    if (mundo.grid[x][y] == 0) {
                        probs[x][y] = iprob;
                    }
                }
            }
        }

        myMaps.updateProbs(probs);
    }

    double s_given_prev(int x, int y, int action, double[][] priors) {
        double prob = 0.0, failProb = (1 - moveProb);

        switch (action) {
        case 0:
            prob += moveProb * priors[x][y+1];
            prob += failProb * priors[x][y-1];
            prob += failProb * priors[x-1][y];
            prob += failProb * priors[x+1][y];
            prob += failProb * priors[x][y];
            if(mundo.grid[x][y-1] == 1) {
                prob += moveProb * priors[x][y];
            }
            break;
        case 1:
            prob += failProb * priors[x][y+1];
            prob += moveProb * priors[x][y-1];
            prob += failProb * priors[x-1][y];
            prob += failProb * priors[x+1][y];
            prob += failProb * priors[x][y];
            if(mundo.grid[x][y+1] == 1) {
                prob += moveProb * priors[x][y];
            }
            break;
        case 2:
            prob += failProb * priors[x][y+1];
            prob += failProb * priors[x][y-1];
            prob += moveProb * priors[x-1][y];
            prob += failProb * priors[x+1][y];
            prob += failProb * priors[x][y];
            if(mundo.grid[x+1][y] == 1) {
                prob += moveProb * priors[x][y];
            }
            break;
        case 3:
            prob += failProb * priors[x][y+1];
            prob += failProb * priors[x][y-1];
            prob += failProb * priors[x-1][y];
            prob += moveProb * priors[x+1][y];
            prob += failProb * priors[x][y];
            if(mundo.grid[x-1][y] == 1) {
                prob += moveProb * priors[x][y];
            }
            break;
        case 4:
            prob += failProb * priors[x][y+1];
            prob += failProb * priors[x][y-1];
            prob += failProb * priors[x-1][y];
            prob += failProb * priors[x+1][y];
            prob += moveProb * priors[x][y];
            break;
        }
        // System.out.println("s_given_prev: " + prob);
        return prob;
    }

    double z_given_s(String z, int x, int y, World state) {
        double prob = 1.0, sensorFail = 1 - sensorAccuracy;
        int c = 0;

        c = z.charAt(0);
        if(c == '1' && state.grid[x][y-1] == 1) {
            prob *= sensorAccuracy;
        }else if(c == '0' && state.grid[x][y-1] != 1) {
            prob *= sensorAccuracy;
        }else {
            prob *= sensorFail;
        }

        c = z.charAt(1);
        if(c == '1' && state.grid[x][y+1] == 1) {
            prob *= sensorAccuracy;
        }else if(c == '0' && state.grid[x][y+1] != 1) {
            prob *= sensorAccuracy;
        }else {
            prob *= sensorFail;
        }

        c = z.charAt(2);
        if(c == '1' && state.grid[x+1][y] == 1) {
            prob *= sensorAccuracy;
        }else if(c == '0' && state.grid[x+1][y] != 1) {
            prob *= sensorAccuracy;
        }else {
            prob *= sensorFail;
        }

        c = z.charAt(3);
        if(c == '1' && state.grid[x-1][y] == 1) {
            prob *= sensorAccuracy;
        }else if(c == '0' && state.grid[x-1][y] != 1) {
            prob *= sensorAccuracy;
        }else {
            prob *= sensorFail;
        }
        // System.out.println("z_given_s: " + prob);
        return prob;
    }

    // TODO: update the probabilities of where the AI thinks it is based on
    // the action selected and the new sonar readings
    //       To do this, you should update the 2D-array "probs"
    // Note: sonars is a bit string with four characters, specifying the sonar
    // reading in the direction of North, South, East, and West
    //       For example, the sonar string 1001, specifies that the sonars
    // found a wall in the North and West directions, but not in the South and East directions
    void updateProbabilities(int action, String sonars) {
        System.out.println("action: " + action);
        int x, y;
        double zp = 0.0, sump = 0.0, eta = 0.0;
        double[][] bel = new double[mundo.width][mundo.height];

        // For all xt do:
        for (y = 0; y < mundo.height; y++) {
            for (x = 0; x < mundo.width; x++) {
                if (mundo.grid[x][y] == 0) {
                    // bel_(xt) = SUM( p(xt | ut, xt-1) * bel(xt-1) )
                    sump = s_given_prev(x, y, action, probs);
                    // bel(xt) = lr * p(zt | xt) * bel_(xt)
                    zp = z_given_s(sonars, x, y, mundo);
                    if(sump > 0.0 || zp > 0.0) {
                        // System.out.print(", sump: " + sump + ", zp: " + zp);
                    }
                    bel[x][y] = zp * sump;
                    eta += bel[x][y];
                }
            }
        }
        // System.out.println("\neta: " + eta);
        eta = 1.0 / (eta + 0.000000001);

        probs = new double[mundo.width][mundo.height];
        for (y = 0; y < mundo.height; y++) {
            for (x = 0; x < mundo.width; x++) {
                if (mundo.grid[x][y] == 0) {
                    probs[x][y] = bel[x][y] * eta;
                }
            }
        }

        myMaps.updateProbs(probs);
// call this function after updating your probabilities so that the
//  new probabilities will show up in the probability map on the GUI
    }

    void valueIteration() {
        values = new double[mundo.width][mundo.height];
        int x, y;
        for (y = 0; y < mundo.height; y++) {
            for (x = 0; x < mundo.width; x++) {
                if(mundo.grid[x][y] == 2) {
                    values[x][y] = -10;
                }else if(mundo.grid[x][y] == 3) {
                    values[x][y] = 10;
                    System.out.println("value, x, y: " + values[x][y] + ", " + x + ", " + y);
                }
            }
        }
        boolean unstable = true;
        double u = 0.0, maxU, failProb = (1.0 - moveProb)/3, dif = 0, limit = 1.0;
        // if(moveProb < 1.0) {
        //     limit = mundo.height * mundo.width * 0.1;
        // }
        // System.out.println("move, fail, limit: " + moveProb + ", " + failProb + ", " + limit);
        // System.out.println("goal: " + values[13][1]);
        // while values continue to change
        while(unstable) {
            dif = 0.0;
            // for each state
            for (y = 0; y < mundo.height; y++) {
                for (x = 0; x < mundo.width; x++) {
                    if(mundo.grid[x][y] == 0) {

                        // u = values[x][y] * moveProb;
                        // u += values[x][y-1] * failProb;
                        // u += values[x][y+1] * failProb;
                        // u += values[x-1][y] * failProb;
                        // u += values[x+1][y] * failProb;
                        // maxU = u;
                        // u = values[x][y] * failProb;
                        u = 0.0;
                        u += values[x][y-1] * moveProb;
                        u += values[x][y+1] * failProb;
                        u += values[x-1][y] * failProb;
                        u += values[x+1][y] * failProb;
                        // if(mundo.grid[x][y-1] == 1) {
                        //     u += values[x][y] * moveProb;
                        // }
                        maxU = u;
                        // u = values[x][y] * failProb;
                        u = 0.0;
                        u += values[x][y-1] * failProb;
                        u += values[x][y+1] * moveProb;
                        u += values[x-1][y] * failProb;
                        u += values[x+1][y] * failProb;
                        // if(mundo.grid[x][y+1] == 1) {
                        //     u += values[x][y] * moveProb;
                        // }
                        if(u > maxU) {
                            maxU = u;
                        }
                        // u = values[x][y] * failProb;
                        u = 0.0;
                        u += values[x][y-1] * failProb;
                        u += values[x][y+1] * failProb;
                        u += values[x-1][y] * moveProb;
                        u += values[x+1][y] * failProb;
                        // if(mundo.grid[x-1][y] == 1) {
                        //     u += values[x][y] * moveProb;
                        // }
                        if(u > maxU) {
                            maxU = u;
                        }
                        // u = values[x][y] * failProb;
                        u = 0.0;
                        u += values[x][y-1] * failProb;
                        u += values[x][y+1] * failProb;
                        u += values[x-1][y] * failProb;
                        u += values[x+1][y] * moveProb;
                        // if(mundo.grid[x+1][y] == 1) {
                        //     u += values[x][y] * moveProb;
                        // }
                        if(u > maxU) {
                            maxU = u;
                        }
                        // if(x == 12 && y == 1) {
                        //     System.out.println("info: " + maxU + ", " + u + ", "  + values[x+1][y]);
                        //     System.out.println("above: " + values[x][y-1] + ", " + (values[x][y-1] * moveProb));
                        // }
                        u = gamma * maxU;
                        dif += Math.abs(values[x][y] - u);
                        // if(Double.isNaN(dif)) {
                        //     System.out.println("Nan: maxU - " + maxU);
                        //     return;
                        // }
                        // if(x == 12 && y == 1) {
                        //     System.out.println("info: " + maxU + ", " + u + ", "  + dif + ", "  + values[x][y]);
                        // }
                        values[x][y] = u;
                    }
                }
            } // end loop over states
            if(dif < limit) {
                unstable = false;
            }else {
                System.out.println("Dif: " + dif);
            }
        }// end while
        myMaps.updateValues(values);
        return;
    }

    int algorithm2() {
        ++actionNum;
        if(actionNum < 10) {
            return STAY;
        }

        double maxP = 0, maxV = 0;
        int x, y, maxx = 1, maxy = 1;
        for (y = 0; y < mundo.height; y++) {
            for (x = 0; x < mundo.width; x++) {
                if (mundo.grid[x][y] == 0) {
                    if(probs[x][y] > maxP) {
                        maxP = probs[x][y];
                        maxx = x;
                        maxy = y;
                    }
                }
            }
        }
        int action = STAY;
        if(values[maxx][maxy-1] > maxV) {
            maxV = values[maxx][maxy-1];
            action = NORTH;
        }if(values[maxx][maxy+1] > maxV) {
            maxV = values[maxx][maxy+1];
            action = SOUTH;
        }if(values[maxx-1][maxy] > maxV) {
            maxV = values[maxx-1][maxy];
            action = WEST;
        }if(values[maxx+1][maxy] > maxV) {
            maxV = values[maxx+1][maxy];
            action = EAST;
        }
        return action;
    }

    // This is the function you'd need to write to make the robot move using your AI;
    int automaticAction() {
        if(false) {
            return algorithm2();
        }
        int ax = 0, ay = -1, x, y;
        // for each state find the utility of the action
        for (y = 0; y < mundo.height; y++) {
            for (x = 0; x < mundo.width; x++) {
                if (mundo.grid[x][y] == 0) {

                }
            }
        }

        return STAY;
    }

    void doStuff() {
        int action;
        initializeProbabilities();  // Initializes the location (probability) map
        System.out.println("finding values");
        valueIteration();
        actionNum = 0;
        System.out.println("finished values");

        while (true) {
            try {
                if (isManual)
                    action = getHumanAction();
                    // get the action selected by the user (from the keyboard)
                else
                    action = automaticAction();
                    // get the action selected by your AI;

                sout.println(action); // send the action to the Server

                // get sonar readings after the robot moves
                String sonars = sin.readLine();
                // System.out.println("Sonars: " + sonars);

                // check to see if the robot has reached its goal or fallen down stairs
                if (sonars.length() > 4) {
                    if (sonars.charAt(4) == 'w') {
                        System.out.println("I won!");
                        myMaps.setWin();
                        break;
                    }
                    else if (sonars.charAt(4) == 'l') {
                        System.out.println("I lost!");
                        myMaps.setLoss();
                        break;
                    }
                }
                else {
                    // here, you'll want to update the position probabilities
                    // since you know that the result of the move indicates the robot
                    // is not at the goal or in a stairwell
                    updateProbabilities(action, sonars);
                }
                Thread.sleep(decisionDelay);
// delay that is useful to see what is happening when the AI selects actions
// decisionDelay is specified by the send command-line argument,
// which is given in milliseconds
            }
            catch (IOException e) {
                System.out.println(e);
            }
            catch(InterruptedException ex) {
                Thread.currentThread().interrupt();
            }
        }
    }

    // java TheRobot [manual/automatic] [delay]
    public static void main(String[] args) {
        TheRobot robot = new TheRobot(args[0], Integer.parseInt(args[1]));
        // starts up the robot
    }
}
