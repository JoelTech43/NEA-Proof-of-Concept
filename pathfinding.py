import time
maze_layout = [
    [(True,True,False,True), (False,True,False,True), (False,True,True,False), (True,True,False,True), (False,True,True,False)], #each list is a row, each tuple is a cell.
    [(True,True,False,False), (False,True,True,False), (True,False,False,True), (False,True,False,True), (False,False,True,False)], #True = wall, False = gap. 1st value = left, 2nd value = top, 3rd value = right, 4th value = down.
    [(True,False,True,True), (True,False,False,False), (False,True,False,True), (False,True,False,False), (False,False,True,False)], #Need the whole right and bottom of grid.
    [(True,True,False,False), (False,False,True,True), (True,True,False,True), (False,False,True,True), (True,False,True,False)],
    [(True,False,False,True), (False,True,False,True), (False,True,True,True), (True,True,False,True), (False,False,True,True)]
]

class Cell:
    def __init__(self, parent, walls, maze_pos):
        self.parent = parent
        self.walls = walls
        self.maze_pos = maze_pos

        self.prev_cell = None
        self.start_dist = 10000
        self.heuristic_estimate = 10000
        self.overall_dist_estimate = 20000
    
    def update_estimate(self, start_dist, heuristic_estimate):
        new_total = start_dist+heuristic_estimate
        if new_total < self.overall_dist_estimate:
            self.start_dist = start_dist
            self.heuristic_estimate = heuristic_estimate
            self.overall_dist_estimate = new_total
            return True
        return False
    
    def set_prev_cell(self, cell) -> None:
        self.prev_cell = cell
    
    def get_prev_cell(self):
        return self.prev_cell
    
    def get_walls(self):
        return self.walls
    
    def get_start_dist(self):
        return self.start_dist
    
    def get_heuristic_estimate(self):
        return self.heuristic_estimate
    
    def get_overall_estimate(self):
        return self.overall_dist_estimate
    
    def get_maze_pos(self):
        return self.maze_pos
    
    def reset_estimates(self):
        self.prev_cell = None
        self.start_dist = 10000
        self.heuristic_estimate = 10000
        self.overall_dist_estimate = 20000

class Maze:
    def __init__(self, parent, cell_wall_array, maze_dimenstions, cell_height):
        self.parent = parent
        self.cells = [[Cell(self,cell_wall_array[j][i],(i,j)) for i in range(len(cell_wall_array[j]))] for j in range(len(cell_wall_array))]
        self.maze_dimensions = maze_dimenstions
        self.cell_height = cell_height

    def get_cell(self, maze_pos): #maze_pos is tuple, x,y, from top left
        return self.cells[maze_pos[1]][maze_pos[0]]
    
    def get_cells(self):
        return self.cells
    
    def get_cell_height(self):
        return self.cell_height

class Entity:
    def __init__(self, parent, move_dist, maze_pos) -> None:
        self.parent = parent
        self.move_dist = move_dist
        self.maze_pos = maze_pos

class Enemy(Entity):
    def __init__(self, parent, move_dist, maze_pos):
        super().__init__(parent, move_dist, maze_pos)
    
    def get_entity_positions(self):
        return self.parent.get_enemies()
    
    def find_shortest_route(self, dest_coord):
        cells = self.parent.maze.get_cells()
        visited = []
        potential = []

        visiting_cell_coord = self.maze_pos
        
        visiting_cell = cells[visiting_cell_coord[1]][visiting_cell_coord[0]]

        visiting_cell.update_estimate(0, 10000)

        while visiting_cell_coord != dest_coord:
            print(visiting_cell_coord)
            visited.append(visiting_cell_coord)
            
            walls = visiting_cell.get_walls()

            considering_cell_coords = []

            if walls[0] is False:
                considering_coord = (visiting_cell_coord[0]-1, visiting_cell_coord[1])
                considering_cell_coords.append(considering_coord)
            
            if walls[1] is False:
                considering_coord = (visiting_cell_coord[0], visiting_cell_coord[1]-1)
                considering_cell_coords.append(considering_coord)
            
            if walls[2] is False:
                considering_coord = (visiting_cell_coord[0]+1, visiting_cell_coord[1])
                considering_cell_coords.append(considering_coord)
            
            if walls[3] is False:
                considering_coord = (visiting_cell_coord[0], visiting_cell_coord[1]+1)
                considering_cell_coords.append(considering_coord)
            
            for considering_coord in considering_cell_coords:
                if considering_coord not in visited: #don't attempt to update visited cells as they already have shortest route
                    potential.append(considering_coord)
                    considering_cell = cells[considering_coord[1]][considering_coord[0]]

                    start_dist = visiting_cell.get_start_dist() + 1
                    heuristic_estimate = abs(dest_coord[0]-considering_coord[0])+abs(dest_coord[1]-considering_coord[1])

                    updated = considering_cell.update_estimate(start_dist, heuristic_estimate)

                    if updated:
                        considering_cell.set_prev_cell(visiting_cell)

            #potential = list(set(potential)-set(visited))
            potential = list(set(potential))

            potential.sort(key=lambda coord: (cells[coord[1]][coord[0]].get_overall_estimate(), cells[coord[1]][coord[0]].get_heuristic_estimate())) #sort primarily by total estimate, then by heuristic estimate.

            visiting_cell_coord = potential[0]
            del potential[0]

            visiting_cell = cells[visiting_cell_coord[1]][visiting_cell_coord[0]]
        
        #out of loop so visiting_cell is destination
        route = [] #list to hold all coords along shortest route

        while visiting_cell.get_prev_cell() != None: #while haven't got back to start
            route.append(visiting_cell.get_maze_pos()) #add current cell to route
            visiting_cell = visiting_cell.get_prev_cell() #move to previous cell
        
        #route list now starts with destination and ends with start
        route.reverse() #now starts at start and ends at end. DOESN'T INCLUDE START CELL.
        return route

class LevelHandler:
    def __init__(self, maze, enemies) -> None:
        self.maze = maze
        self.enemies = enemies
    
    def get_enemies(self):
        return self.enemies
    
    def create_enemy(self):
        enemy = Enemy(self, 1, (2,0))
        self.enemies.append(enemy)
    
    def create_maze(self):
        maze = Maze(self, maze_layout, (5,5), 100)
        self.maze = maze

level_handler = LevelHandler("placeholder", [])
level_handler.create_enemy()
level_handler.create_maze()

start = time.time()
print(level_handler.get_enemies()[0].find_shortest_route((2,4)))
print(time.time()-start)