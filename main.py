import pygame
from random import choice
import time
import config #used this form as means that when I run set_constants() function in config.py, the updated versions will be imported.
from classes import Maze, Player, Enemy

pygame.init()
config.set_constants()

maze_layout = [
    [(1,1,0,1), (0,1,0,1), (0,0,1,0), (1,1,0,1), (0,1,1,0)], #each list is a row, each tuple is a cell.
    [(1,1,0,0), (0,1,1,0), (1,0,0,1), (0,1,0,1), (0,0,1,0)], #1 = wall, 0 = gap. 1st value = left, 2nd value = top, 3rd value = right, 4th value = down.
    [(1,0,1,1), (1,0,0,0), (0,1,0,1), (0,1,0,0), (0,0,1,0)], #Need the whole right and bottom of grid.
    [(1,1,0,0), (0,0,1,1), (1,1,0,1), (0,0,1,1), (1,0,1,0)],
    [(1,0,0,1), (0,1,0,1), (0,1,1,0), (1,1,0,1), (0,0,1,1)]
]

player = Player((0,0), config.RED, )

maze = Maze(config.WINDOW_SIZE, config.MAZE_SIZE, config.CELL_HEIGHT, config.WALL_THICKNESS, config.WHITE, maze_layout, )
