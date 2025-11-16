import pygame

class Maze:
    def __init__(self, screen_dimensions: tuple, maze_dimensions: tuple, cell_height: int, wall_thickness: int, wall_colour: tuple, maze_array: list, player: Player, enemies: list) -> None:
        self.maze_dimensions = maze_dimensions
        self.rows = maze_dimensions[0]
        self.cols = maze_dimensions[1]

        self.cell_height = cell_height
        self.wall_thickness = wall_thickness
        self.wall_colour = wall_colour

        self.maze_array = maze_array
        self.player = player
        self.enemies = enemies

        #basically determines the start coordinate of the centred maze.
        self.left_pad = (screen_dimensions[1]-(self.cols*self.cell_height))//2
        self.top_pad = (screen_dimensions[0]-(self.rows*self.cell_height))//2
    
    def get_info(self) -> dict:
        return {
            "dimensions": self.maze_dimensions,
            "cell_height": self.cell_height,
            "wall_thickness": self.wall_thickness,
            "top_padding": self.top_pad,
            "left_padding": self.left_pad
        }

    def get_cell(self, maze_pos) -> tuple:
        return self.maze_array[maze_pos[0]][maze_pos[1]]

    def draw_cell_walls(self, canvas, cell_pos: tuple, wall_thickness: int, wall_colour: tuple, walls: tuple) -> None:
        cell_x = cell_pos[0]
        cell_y = cell_pos[1]

        if walls[0] == 1:
            pygame.draw.rect(canvas, wall_colour, pygame.Rect(cell_x,cell_y,wall_thickness,self.cell_height))
        if walls[1] == 1:
            pygame.draw.rect(canvas, wall_colour, pygame.Rect(cell_x,cell_y,self.cell_height,wall_thickness))
        if walls[2] == 1:
            pygame.draw.rect(canvas, wall_colour, pygame.Rect(cell_x+(self.cell_height-wall_thickness),cell_y,wall_thickness,self.cell_height))
        if walls[3] == 1:
            pygame.draw.rect(canvas, wall_colour, pygame.Rect(cell_x,cell_y+(self.cell_height-wall_thickness),self.cell_height,wall_thickness))
        pygame.display.update()

    def draw_maze(self, canvas) -> None:
        for rowInd in range(self.rows):
            for collInd in range(self.cols):
                cell_walls = self.maze_array[rowInd][collInd]
                current_cell_screen_pos = (self.left_pad+(self.cell_height*(collInd+1)), self.top_pad+(self.cell_height*(rowInd+1)))
                self.draw_cell_walls(canvas, current_cell_screen_pos, self.wall_thickness, self.wall_colour, cell_walls)

        self.player.draw()

class Entity:
    def __init__(self, maze_pos: tuple, colour: tuple, maze: Maze) -> None:
        self.maze_pos = maze_pos
        self.colour = colour

        maze_info = maze.get_info()
        self.screen_pos = (maze_info["left_padding"]+(maze_info["cell_height"]*self.maze_pos[0])+maze_info["wall_thickness"], maze_info["top_padding"]+(maze_info["cell_height"]*self.maze_pos[1])+maze_info["wall_thickness"])

        self.current_cell = maze.get_cell(maze_pos)

        self.sprite_height = maze_info["cell_height"]-(2*maze_info["wall_thickness"])

    def update_attributes(self, maze: Maze) -> None: #Updates screen_pos and current_cell attributes based on self.maze_pos so don't have to recalculate every frame.
        maze_info = maze.get_info()
        self.screen_pos = (maze_info["left_padding"]+(maze_info["cell_height"]*self.maze_pos[0])+maze_info["wall_thickness"], maze_info["top_padding"]+(maze_info["cell_height"]*self.maze_pos[1])+maze_info["wall_thickness"])

        self.current_cell = maze.get_cell(self.maze_pos)

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.colour, pygame.Rect(self.screen_pos[0], self.screen_pos[1], self.sprite_height, self.sprite_height))
        pygame.display.update()

class Player(Entity):
    def __init__(self, maze_pos: tuple, colour: tuple, maze: Maze) -> None:
        super().__init__(maze_pos, colour, maze)

class Enemy(Entity):
    def __init__(self, maze_pos: tuple, colour: tuple, maze: Maze) -> None:
        super().__init__(maze_pos, colour, maze)