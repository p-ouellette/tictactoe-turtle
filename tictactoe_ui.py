#!/usr/bin/env python
#
# tictactoe_ui.py

"""TicTacToeUI class to handle all parts of the user interface."""

from __future__ import print_function

import turtle


class TicTacToeUI:
    """Handle the screen and turtles for drawing and writing text."""
    def __init__(self):
        self.wn = turtle.Screen()
        self.wn.title("Welcome to Tic Tac Toe!")
        # Turtles
        self.t_grid = turtle.Turtle()
        self.t_marks = turtle.Turtle()
        self.t_top_text = turtle.Turtle()
        self.t_stats = turtle.Turtle()
        # Hide all turtles and set to max speed
        for t in self.wn.turtles():
            t.ht()
            t.speed(0)
        self.t_grid.pensize(2)
        self.t_marks.pensize(4)
        # Middle coordinates of the 9 grid sections
        self.mid_cors = [(-150, 150), (0, 150), (150, 150), (-150, 0), (0, 0),
                         (150, 0), (-150, -150), (0, -150), (150, -150)]
        self.text_args = (False, 'center', ('Arial', 20, 'normal'))
        # Move text writing turtles to their positions
        self.move(self.t_top_text, 0, 275)
        self.move(self.t_stats, 0, -295)

    def move(self, turtle, x, y):
        """Move turtle to the given coordinates without leaving a trail."""
        turtle.pu()
        turtle.goto(x, y)
        turtle.pd()

    def draw_grid(self):
        """Draw the playing grid."""
        for cor in [75, -75]:
            self.move(self.t_grid, -225, cor)
            self.t_grid.setx(225)
            self.move(self.t_grid, cor, 225)
            self.t_grid.sety(-225)

    def draw_x(self, position):
        """Draw an X at the given board position."""
        self.t_marks.pencolor('blue')
        mid_cor = self.mid_cors[position]
        self.move(self.t_marks, mid_cor[0] + 50, mid_cor[1] + 50)
        self.t_marks.goto(self.t_marks.xcor() - 100, self.t_marks.ycor() - 100)
        self.move(self.t_marks, self.t_marks.xcor(), self.t_marks.ycor() + 100)
        self.t_marks.goto(self.t_marks.xcor() + 100, self.t_marks.ycor() - 100)

    def draw_o(self, position):
        """Draw an O at the given board position."""
        self.t_marks.pencolor('red')
        mid_cor = self.mid_cors[position]
        self.move(self.t_marks, mid_cor[0], mid_cor[1] - 50)
        self.t_marks.circle(50)

    def print_stats(self, usr_wins, ties, bot_wins):
        """Display the games won/tied/lost text."""
        self.t_stats.clear()
        stats = "PLAYER: {}   TIES: {}   BOT: {}".format(usr_wins, ties,
                                                         bot_wins)
        self.t_stats.write(stats, *self.text_args)

    def print_top_text(self, text, color):
        """Display the given text near the top of the screen."""
        self.t_top_text.clear()
        self.t_top_text.pencolor(color)
        self.t_top_text.write(text, *self.text_args)

    def print_game_over_text(self, winner):
        """Display game over text based on the winner ('x', 'o', or
        'tie').
        """
        usr_won = winner == 'x'
        bot_won = winner == 'o'
        txt_color = 'blue' if usr_won else 'red' if bot_won else 'black'
        msg = "YOU WIN!" if usr_won else "BOT WINS!" if bot_won else "TIE GAME"
        self.print_top_text(msg, txt_color)
        print(msg, "\n")
