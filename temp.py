import sys
import pygame as pg
import math
import numpy as np
import random
import os
from settings import *

# Constants and global variables

# Board
board = np.zeros((3, 3))
print(board)

# Player - X or O
player = 1

# Functions
def draw_lines():
    # Lines for columns
    for i in range(NUMOFCUBES-1):
        pg.draw.line(screen, LINECOLOR, [(i + 1) * 200, 0], [(i + 1) * 200, 600], LINESIZE)
    # Lines for rows
    for i in range(NUMOFCUBES-1):
        pg.draw.line(screen, LINECOLOR, [0, (i + 1) * 200], [600, (i + 1) * 200], LINESIZE)

def draw_x(x, y):
    x = int(x*200 + 100)
    y = int(y*200 + 100)

    pg.draw.line(screen, LIGHTBLUE, [x-75, y-75], [x+75, y+75], SIZEX)
    pg.draw.line(screen, LIGHTBLUE, [x+75, y-75], [x-75, y+75], SIZEX)

def draw_circle(x, y):
    x = int(x * 200 + 100)
    y = int(y * 200 + 100)

    pg.draw.circle(screen, LIGHTBLUE, (x, y), CIRCLERADIUS, CIRCLESIZE)

# Draw shapes according to the board
def draw_shapes():
    for r in range(NUMOFCUBES):
        for c in range(NUMOFCUBES):
            if board[c][r] == 1:
                draw_x(r, c)
            elif board[c][r] == -1:
                draw_circle(r, c)

# Draw all the objects
def draw():
    draw_lines()
    draw_shapes()
    pg.display.update()

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    for r in range(NUMOFCUBES):
        for c in range(NUMOFCUBES):
            if board[r][c] == 0:
                return False

    return True
def mark_square(row, col, player):
    board[row][col] = player


# Main lines
pg.init()
# Set screen variables
screen = pg.display.set_mode((WIDTH, HEIGHT))
screen.fill(BACKGROUND)
pg.display.set_caption("TIC TAC TOE")
# Set loop for the game
playing = True
while playing:
    # Event loop, checks keyboard and mouse input
    for event in pg.event.get():
        if event.type == pg.K_ESCAPE or event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            row = int(mouseY // 200)
            column = int(mouseX // 200)

            if available_square(row, column):
                mark_square(row, column, player)

                player *= -1

            print(board)
    draw()
