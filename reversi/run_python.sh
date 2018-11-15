cd ReversiServer
pwd
echo "java Reversi 10 &> error.log &"
java Reversi 10 &> error.log &

cd ../ai
source ~/torch_env/bin/activate

sleep 1
echo "python game_setup.py localhost 1 random &>1 &"
python game_setup.py localhost 1 random &>1 &

sleep 1
if [ "$1" != "" ]; then
    echo "python game_setup.py localhost 2 minimax" $1 "&>ai.log &"
    python game_setup.py localhost 2 minimax $1 &>ai.log &
else
    echo "python game_setup.py localhost 2 minimax 6 &>ai.log &"
    python game_setup.py localhost 2 minimax 6 &>ai.log &
fi
