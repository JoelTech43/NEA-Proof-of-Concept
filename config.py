import pygame

#Colour constants
WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)
BLUE = (0,0,255)

#Height and width of grid squares in px
MAZE_SIZE = (5,5)
WINDOW_SIZE = None #set to None until set by set_constants
CELL_HEIGHT = None

WALL_THICKNESS = 1

def set_constants(): #done in fundction as pygame function can't be used until pygame initialised in main.py
    #get_desktop_sizes() returns list of tuples, one for each desktop. I keep first which is main one.
    main_desktop_size = pygame.display.get_desktop_sizes()[0]
    WINDOW_SIZE = main_desktop_size
    #Currently want maze to fill screen (in at least 1 dimension) so need to determine height of each cell (px) by dividing smallest screen dimension by number of cells in maze.
    CELL_HEIGHT = min((WINDOW_SIZE[0]//MAZE_SIZE[1], WINDOW_SIZE[1]//MAZE_SIZE[0]))

