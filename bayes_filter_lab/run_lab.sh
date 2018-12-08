cd /home/iclee141/workspace/cs470/bayes_filter_lab

cd Server
# if [ $# -gt 0 ]; then
#     echo "java BayesWorld mundo_15_15.txt" $1 $2 "unknown &> error.log &"
#     java BayesWorld mundo_15_15.txt $1 $2 unknown &> error.log &
# else
#     echo "java BayesWorld mundo_15_15.txt 0.9 0.9 unknown &> error.log &"
#     java BayesWorld mundo_15_15.txt 0.9 0.9 unknown &> error.log &
# fi

if [ $# -gt 0 ]; then
    echo "java BayesWorld mundo_maze.txt" $1 $2 "unknown &> error.log &"
    java BayesWorld mundo_maze.txt $1 $2 unknown &> error.log &
else
    echo "java BayesWorld mundo_maze.txt 1.0 1.0 known &> error.log &"
    java BayesWorld mundo_maze.txt 1.0 1.0 known &> error.log &
fi

cd ../Robot
javac *.java
# sleep 1
echo "java TheRobot automatic 300 &> error.log &"
java TheRobot automatic 300 &> error.log &
# echo "java TheRobot manual 0 &> error.log &"
# java TheRobot manual 0 &> error.log &
