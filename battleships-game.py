""" Battleships solo game using tkinter module

Requirements:
    Python and tkinter

Output:
    a graphical tkinter window with a battleships grid

Usage:
    ./battleships.py

"""

import re
import sys
import turtle
from random import sample
from itertools import product

# max grid coordinate (0-based)
LIMIT = 15

turtle.setup(width=1000, height=1000)
t = turtle.getturtle()
s = turtle.getscreen()
# width & height of canvas in user coord units
s.screensize(LIMIT + 3, LIMIT + 3)
# allow offset for axes and border space
s.setworldcoordinates(-1, -1, LIMIT + 1, LIMIT + 1)
t.speed(0)

charset = set([str(n) for n in range(LIMIT + 1)])

def drawgrid():
    """ Draw and label a cartesian plane
    """

    for y in range(LIMIT + 1):
        t.pu()
        t.goto(0, y)
        t.pd()
        t.goto(LIMIT, y)

    for x in range(LIMIT + 1):
        t.pu()
        t.goto(x, 0)
        t.pd()
        t.goto(x, LIMIT)

    t.pu()

    for i in range(LIMIT + 1):
        t.goto(-0.5, i)
        # use your system's fonts below
        t.write(str(i), font=('Courier', 12, 'normal'))
    t.goto(0, 0)

    for i in range(LIMIT + 1):
        t.goto(i, -0.5)
        # use your system's fonts below
        t.write(str(i), font=('Courier', 12, 'normal'))
    t.goto(0, 0)

    return None


def draw_green_dot(tpl):
    # miss
    t.pu()
    t.goto(tpl)
    t.dot(20, "green")

def draw_orange_dot(tpl):
    # close
    t.pu()
    t.goto(tpl)
    t.dot(20, "orange")

def draw_red_dot(tpl):
    # direct hit (successful guess)
    t.pu()
    t.goto(tpl)
    t.dot(20, "red")


def make_ships():
    """ Make 3 random battleships coords

    Creates a list of all possible coords using cartesian product.
    Randomly selects 3 of these.

    Output:
        return a list of 3 tuples which are the ships' coords

    """

    coords = list(product(range(LIMIT + 1), range(LIMIT + 1)))
    ships = sample(coords, 3)
    return ships


def check_for_hit(guess, ships):
    """ Checks if a coord guess is a hit, close or miss

    Input:
        a guessed coord (x, y) and
        the list of 3 battleship coords

    Output:
        Draws a red, orange, or green dot at guess coord,
        depending if guess is a hit, close or miss.
        Close means guess coord is adjacent to ship (1 unit away)

    """

    if guess in ships:
        # direct hit
        draw_red_dot(guess)
        t.home()
        print('!!!!!!!!!!!!!  direct hit  !!!!!!!!!!!!!!')
        # remove destroyed ship from list of battleships
        ships.remove(guess)
    else:
        t.pu()
        t.goto(guess)
        # distances of sqrt(2) are rounded down to unity
        distances_to_guess = [round(t.distance(ship)) for ship in ships]
        if 1 in distances_to_guess:
            # we have a close miss
            draw_orange_dot(guess)
            print('************* close *************')
        else:
            # we have a miss
            draw_green_dot(guess)
            print('------------- miss ------------')
        t.home()
    return None


def get_guess():
    """ Get inputs X and Y from player

    Processes X and Y inputs separately

    Output:
        returns (x,y) a tuple of two ints

    """

    while True:
        x = input('Enter X coordinate (or q to quit)\n > ')
        if x == 'q':
            sys.exit()
        if x in charset:
            break

    while True:
        y = input('Enter Y coordinate (or q to quit)\n > ')
        if y == 'q':
            sys.exit()
        if y in charset:
            break

    return int(x), int(y)


def get_guess_re():
    """ Get input guess coord tuple x,y from player

    Processes input as a tuple, sanitizing against a regex

    Output:
        returns (x,y) a tuple of two ints

    """

    po = re.compile(r'^(\d{1,2}),(\d{1,2})$')

    while True:
        s = input('Enter X,Y (or q to quit)\n (e.g. 2,3): ')

        if s == 'q':
            sys.exit()

        m = po.match(s)
        if m is not None:
            x = m[1]
            y = m[2]
            break

    return int(x), int(y)


def main():

    guess_counter = 0 # count of tries
    drawgrid()
    battleships = make_ships()
    t.home()

    while len(battleships) > 0:
        guess = get_guess_re()
        guess_counter += 1
        check_for_hit(guess, battleships)
    else:
        print('*' * 50)
        print(f'You took {guess_counter} guesses to win')
        print('*' * 50)
        input('Enter q to quit> ')
        # s.exitonclick()



if __name__ == "__main__":
    main()

