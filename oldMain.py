import pygame
from random import choice
import time

pygame.init()

WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)
BLUE = (0,0,255)

WINDOW_SIZE = (500,500)
gridSize = (5,5)
if WINDOW_SIZE[0] // gridSize[0] < WINDOW_SIZE[1] // gridSize[1]:
    tileSize = WINDOW_SIZE[0]//gridSize[0]
else:
    tileSize = WINDOW_SIZE[1]//gridSize[1]

player_screen_pos = [1,1]
player_grid_pos = [0,0]
enemy_screen_pos = [WINDOW_SIZE[0]-tileSize+1, WINDOW_SIZE[1]-tileSize+1]
enemy_grid_pos = [4,4]

maze = [
    [(1,1,0,1), (0,1,0,1), (0,0,1,0), (1,1,0,1), (0,1,1,0)], #each list is a row, each tuple is a cell.
    [(1,1,0,0), (0,1,1,0), (1,0,0,1), (0,1,0,1), (0,0,1,0)], #1 = wall, 0 = gap. 1st value = left, 2nd value = top, 3rd value = right, 4th value = down.
    [(1,0,1,1), (1,0,0,0), (0,1,0,1), (0,1,0,0), (0,0,1,0)], #Need the whole right and bottom of grid.
    [(1,1,0,0), (0,0,1,1), (1,1,0,1), (0,0,1,1), (1,0,1,0)],
    [(1,0,0,1), (0,1,0,1), (0,1,1,0), (1,1,0,1), (0,0,1,1)]
]

class Entity:
    def __init__(self, colour:tuple, screen_pos:list, grid_pos:list, move_distance:int=1) -> None:
        self.colour = colour
        self.screen_pos = screen_pos
        self.grid_pos = grid_pos
        self.current_cell = maze[grid_pos[1]][grid_pos[0]]
        self.move_distance = move_distance
    
    def get_render_info(self) -> tuple:
        return (self.colour, self.screen_pos)
    
    def check_valid_move(self, move:str) -> bool:
        match move:
            case "left":
                if self.current_cell[0] == 0 and self.grid_pos[0] > 0:
                    return True
                else:
                    return False
            case "up":
                if self.current_cell[1] == 0 and self.grid_pos[1] > 0:
                    return True
                else:
                    return False
            case "right":
                if self.current_cell[2] == 0 and self.grid_pos[0] < gridSize[0]-1:
                    return True
                else:
                    return False
            case "down":
                if self.current_cell[3] == 0 and self.grid_pos[1] < gridSize[1]-1:
                    return True
                else:
                    return False
            case _:
                return False
                
    def move_entity(self, move:str) -> bool:
        if not self.check_valid_move(move):
            return False
        match move:
            case "left":
                self.screen_pos[0] -= tileSize
                self.grid_pos[0] -= 1
                self.current_cell = maze[self.grid_pos[1]][self.grid_pos[0]]
            case "up":
                self.screen_pos[1] -= tileSize
                self.grid_pos[1] -= 1
                self.current_cell = maze[self.grid_pos[1]][self.grid_pos[0]]
            case "right":
                self.screen_pos[0] += tileSize
                self.grid_pos[0] += 1
                self.current_cell = maze[self.grid_pos[1]][self.grid_pos[0]]
            case "down":
                self.screen_pos[1] += tileSize
                self.grid_pos[1] += 1
                self.current_cell = maze[self.grid_pos[1]][self.grid_pos[0]]
        return True

class Player(Entity):
    ...

class Enemy(Entity):
    def gen_random_move(self):
        moves = ["left", "up", "right", "down"]
        success = False
        while not success:
            move = choice(moves)
            moves.remove(move)
            success = self.move_entity(move)

canvas = pygame.display.set_mode(WINDOW_SIZE)#, pygame.FULLSCREEN)

pygame.display.set_caption("NEA TEST")

def rectWithOutlineArguments(x,y,width,height,borderWidth,borderColour,innerColour):
    return (borderColour, (x,y,width,height)),(innerColour,(x+borderWidth,y+borderWidth,width-(borderWidth*2),height-(borderWidth*2)))

def cellWalls(x,y,width,height,borderWidth,borderColour, wallsTuple):
    walls = []
    if wallsTuple[0] == 1:
        wall = (borderColour, (x,y,borderWidth,height))
        walls.append(wall)
    if wallsTuple[1] == 1:
        wall = (borderColour, (x,y,width,borderWidth))
        walls.append(wall)
    if wallsTuple[2] == 1:
        wall = (borderColour, (x+(width-borderWidth),y,borderWidth,height))
        walls.append(wall)
    if wallsTuple[3] == 1:
        wall = (borderColour, (x,y+(height-borderWidth),height,borderWidth))
        walls.append(wall)
    return walls

def nextEnemyPos(current_pos):
    direction = ['up','down','left','right']
    if current_pos[0] < tileSize+1:
        direction.remove('left')
    elif current_pos[0] > 500-tileSize:
        direction.remove('right')
    
    if current_pos[1] < tileSize+1:
        direction.remove('up')
    elif current_pos[1] > 500-tileSize:
        direction.remove('down')
    
    match choice(direction):
        case 'up':
            current_pos[1] -= tileSize
        case 'down':
            current_pos[1] += tileSize
        case 'left':
            current_pos[0] -= tileSize
        case 'right':
            current_pos[0] += tileSize
    
    return current_pos


count = 0
last_frame = time.time()
frame_times = [60.0 for i in range(5)]

player = Player(BLUE, player_screen_pos, player_grid_pos, 1)
enemies = [Enemy(RED, enemy_screen_pos, enemy_grid_pos, 1)]

exit = False
while not exit:

    current = time.time()
    difference = current - last_frame
    last_frame = current
    frame_times.append(difference)
    del frame_times[0]
    #print(1//(sum(frame_times)/5))

    canvas.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if player.move_entity("left"):
                    for enemy in enemies:
                        enemy.gen_random_move()
            elif event.key == pygame.K_RIGHT:
                if player.move_entity("right"):
                    for enemy in enemies:
                        enemy.gen_random_move()
            elif event.key == pygame.K_UP:
                if player.move_entity("up"):
                    for enemy in enemies:
                        enemy.gen_random_move()
            elif event.key == pygame.K_DOWN:
                if player.move_entity("down"):
                    for enemy in enemies:
                        enemy.gen_random_move()
    
    # for i in range(0,500,tileSize):
    #     for j in range(0,500,tileSize):
    #         outline, inner = rectWithOutlineArguments(j,i,tileSize,tileSize,1,WHITE,BLACK)
    #         pygame.draw.rect(canvas, outline[0], pygame.Rect(outline[1]))
    #         pygame.draw.rect(canvas, inner[0], pygame.Rect(inner[1]))

    for rowInd in range(len(maze)):
        row = maze[rowInd]
        for cellInd in range(len(row)):
            cell = row[cellInd]
            walls = cellWalls(100*cellInd, 100*rowInd, tileSize, tileSize, 1, WHITE, cell)
            for wall in walls:
                pygame.draw.rect(canvas, wall[0], wall[1])

    player_render_info = player.get_render_info()
    pygame.draw.rect(canvas, player_render_info[0], (player_render_info[1][0],player_render_info[1][1],tileSize-2,tileSize-2))
    for enemy in enemies:
        render_info = enemy.get_render_info()
        pygame.draw.rect(canvas, render_info[0], (render_info[1][0], render_info[1][1],tileSize-2,tileSize-2))
    if enemy_grid_pos == player_grid_pos:
        exit = True
    pygame.display.update()