# tictactoe-turtle

A tic tac toe game with an unbeatable AI that uses the Python turtle module for
the user interface. The AI player uses the
[minimax](https://en.wikipedia.org/wiki/Minimax) algorithm.

There are two files:

* [ttt_util.py](ttt_util.py) contains the TicTacToeUI class that handles the
user interface using the [turtle](https://docs.python.org/3/library/turtle.html)
module and the human and bot player classes.
* [tictactoe.py](tictactoe.py) handles the overall control of the game and the
bot AI.

To start a game (after moving into the project directory):

    python tictactoe.py

On Windows you may have to use the full path to the Python executable. It works
with both Python 2 and 3.
