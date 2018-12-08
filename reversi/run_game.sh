cd ReversiServer
pwd
echo "java Reversi 10 &> error.log &"
java Reversi 10 &> error.log &

cd ../javaAI/
javac *.java

sleep 1
if [ "$1" != "" ]; then
    echo "java MiniMaxAI localhost 1" $1 "&>ai.log &"
    java MiniMaxAI localhost 1 $1 &>ai.log &
else
    echo "java MiniMaxMonteCarloAI localhost 1 6 &>ai.log &"
    java MiniMaxMonteCarloAI localhost 1 6 &>ai.log &
fi

sleep 1

# echo "java RandomAI localhost 2 10 &>1 &"
# java RandomAI localhost 2 10 &>1 &
# echo "java MiniMaxMonteCarloAI localhost 2 6 &>1 &"
# java MiniMaxMonteCarloAI localhost 2 6 &>1 &

cd ../
java -jar MCTS.jar localhost 2
1
