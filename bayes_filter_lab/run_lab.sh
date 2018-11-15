cd /home/iclee141/workspace/cs470/bayes_filter_lab

cd Server
if [ $# -gt 0 ]; then
    echo "java BayesWorld mundo_maze.txt" $1 $2 "unknown &> error.log &"
    java BayesWorld mundo_maze.txt $1 $2 unknown &> error.log &
else
    echo "java BayesWorld mundo_maze.txt 0.9 0.9 unknown &> error.log &"
    java BayesWorld mundo_maze.txt 0.9 0.9 unknown &> error.log &
fi

cd ../Robot
sleep 1
echo "java theRobot manual 0 &> error.log &"
java theRobot manual 0 &> error.log &
