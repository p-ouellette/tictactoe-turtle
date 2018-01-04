#!/usr/bin/env python3
#
# tictactoe.py

"""A tic tac toe game with an unbeatable AI that uses the Python turtle
module. The AI player chooses it's move using the minimax algorithm.

How the minimax function works:
1. Identify all the empty positions on the given board.
2. Play in each empty position on a copy of the board.
3. Score the board for the current player: 1 for a win, -1 for a loss,
0 for a tie.
4. If the board is not at a terminal state (game not over), recursively
run the function on the new board for the opponent until a terminal
state is reached. The score is negated so that it represents the
favorability of the move from the perspective of the maximizing player.
5. Choose the maximum score and return it along with the position that
resulted in that score.

If the bot goes first, the minimax function gets executed over 50,000
times before a move is chosen, which is why it takes a couple seconds.
"""

from tictactoe_ui import TicTacToeUI
from random import shuffle


class TicTacToe:
    def __init__(self):
        self.UI = TicTacToeUI()
        # Board and win variables
        self.board = [None] * 9
        self.usr_wins = 0
        self.bot_wins = 0
        self.ties = 0
        # All combinations of board positions that result in a win
        self.win_lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        self.who_first = 'x'
        # Draw the grid and write the stats text
        self.UI.draw_grid()
        self.UI.print_stats(self.usr_wins, self.ties, self.bot_wins)
        # Start the game
        if self.who_first == 'o':
            self.bot_take_turn()
        self.UI.print_turn('user')
        self.UI.wn.onclick(self.play_round)
        self.UI.wn.mainloop()

    def play_round(self, x, y):
        """Play a round of tic tac toe starting with a user move in the
        grid section containing the click coordinates.
        """
        # Remove event binding so play_round can't be called a second
        # time before it's done
        self.UI.wn.onclick(None)

        # Get the board section of the clicked point
        usr_pos = self.get_position(x, y)
        # Exit if click is outside the grid or the grid section isn't empty
        if usr_pos is None or self.board[usr_pos]:
            self.UI.wn.onclick(self.play_round)
            return

        self.usr_take_turn(usr_pos)
        if self.check_if_won(self.board, 'x'):
            self.end_game('usrwin')
            return
        if None not in self.board:
            self.end_game('tie')
            return

        self.bot_take_turn()
        if self.check_if_won(self.board, 'o'):
            self.end_game('botwin')
            return
        if None not in self.board:
            self.end_game('tie')
            return

        # Reactivate event binding
        self.UI.wn.onclick(self.play_round)
        self.UI.print_turn('user')

    def get_position(self, x, y):
        """Return the grid section (0-8) of the given coordinates."""
        if x > -225 and x < -75 and y > 75 and y < 225:
            position = 0
        elif x > -75 and x < 75 and y > 75 and y < 225:
            position = 1
        elif x > 75 and x < 225 and y > 75 and y < 225:
            position = 2
        elif x > -225 and x < -75 and y > -75 and y < 75:
            position = 3
        elif x > -75 and x < 75 and y > -75 and y < 75:
            position = 4
        elif x > 75 and x < 225 and y > -75 and y < 75:
            position = 5
        elif x > -225 and x < -75 and y > -225 and y < -75:
            position = 6
        elif x > -75 and x < 75 and y > -225 and y < -75:
            position = 7
        elif x > 75 and x < 225 and y > -225 and y < -75:
            position = 8
        else:
            position = None
        return position

    def usr_take_turn(self, position):
        """Update the board with the user's move at the given position."""
        self.board[position] = 'x'
        print("User marks section", position)
        self.UI.draw_x(position)

    def bot_take_turn(self):
        """Update the board with a move that the bot chooses."""
        self.UI.print_turn('bot')
        move = self.minimax_choose_pos(self.board, 'o')
        position = move[0]
        score = move[1]
        self.board[position] = 'o'
        print(f"Bot marks section {position} (minimax score {score})")
        self.UI.draw_o(position)

    def minimax_choose_pos(self, board, turn):
        """Return a tuple with the best position for the given player to
        play on the given board and the score associated with that move.
        A score of 1 means the player has a guaranteed win, -1 indicates
        a loss if the opponent plays well, and 0 means the game will end
        in a tie.
        """
        opponent = 'o' if turn == 'x' else 'x'
        empty_pos = [pos for pos in range(9) if not board[pos]]
        shuffle(empty_pos)
        max_score = -10
        for pos in empty_pos:
            # Play on a new board
            new_board = board.copy()
            new_board[pos] = turn
            # Score the board
            if self.check_if_won(new_board, turn):
                score = 1
            elif self.check_if_won(new_board, opponent):
                score = -1
            elif None not in new_board:
                score = 0
            else:
                # Game is not over, recursively check child nodes
                score = -self.minimax_choose_pos(new_board, opponent)[1]
            # Maximize the score
            if score == 1:
                # 1 is the best possible score so we can stop searching
                return (pos, score)
            if score > max_score:
                best_pos = pos
                max_score = score
        return (best_pos, max_score)

    def check_if_won(self, board, player):
        """Return True if the given player ('x' or 'o') has won."""
        # Check if all positions in line are occupied by the given
        # player for any of the lines in win_lines
        return any(all(board[pos] == player for pos in line) for line in
                   self.win_lines)

    def end_game(self, outcome):
        """Show game over text and update the stats based on the outcome
        ('usrwin', 'botwin', or 'tie').
        Bind a screen click event to reset().
        """
        if outcome == 'usrwin':
            self.usr_wins += 1
        elif outcome == 'botwin':
            self.bot_wins += 1
        elif outcome == 'tie':
            self.ties += 1
        self.UI.print_game_over_text(outcome)
        self.UI.print_stats(self.usr_wins, self.ties, self.bot_wins)
        # Reset the board for the next game
        self.UI.wn.onclick(self.reset)

    def reset(self, *_):  # We dont't care where the user clicks
        """Clear game over text, reset board, and start a new game."""
        self.UI.t_top_text.clear()
        self.UI.t_marks.clear()
        self.board = [None] * 9
        # Switch who goes first
        self.who_first = 'x' if self.who_first == 'o' else 'o'
        # Start next game
        if self.who_first == 'o':
            self.bot_take_turn()
        self.UI.print_turn('user')
        self.UI.wn.onclick(self.play_round)


def main():
    """Initialize a game of tic tac toe."""
    ttt = TicTacToe()


if __name__ == '__main__':
    main()
