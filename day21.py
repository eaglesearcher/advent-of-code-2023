import numpy as np
import file_io as fio
import algo_util as alg
from queue import PriorityQueue

day_num = 21
input_type = 1 # 0 = test, 1 = input

class Grid():
    def __init__(self, puzzle_input):
        self.og = puzzle_input
        self.start = self.find_start()
        self.n_rows = len(puzzle_input)
        self.n_cols = len(puzzle_input[0])
        self.history = []
        self.history.append(self.first_grid())
        return

    def find_start(self):
        position = None
        for r, row in enumerate(self.og):
            for c, item in enumerate(row):
                if item == 'S':
                    position = (r, c)
        if position == None:
            print('Start position not found!')
        return position
    
    def clean_grid(self):
        new_grid = [['.' for __ in range(self.n_cols)] for __ in range(self.n_rows)]
        for r, row in enumerate(self.og):
            for c, item in enumerate(row):
                if item == '#':
                    new_grid[r][c] = '#'
        return new_grid
        
    def first_grid(self):
        new_grid = self.clean_grid()
        r = self.start[0]
        c = self.start[1]
        new_grid[r][c] = 'O'
        return new_grid

    def step_grid(self):
        old_grid = self.history[-1]
        new_grid = self.clean_grid()
        valid_dirs = ['U','L','D','R']
        for r,row in enumerate(old_grid):
            for c, item in enumerate(row):
                if item == 'O':
                    adj_dict, adj_ref = alg.get_adj_cells_2d(old_grid, r, c)
                    for d in valid_dirs:
                        if adj_dict[d] == 'O':
                            # elf could be on a neighbor, so eligble to step here
                            new_grid[r][c] = 'O'
                        if adj_dict[d] == '.':
                            # valid place to step next
                            new_r, new_c = adj_ref[d]
                            new_grid[new_r][new_c] = 'O'
        self.history.append(new_grid)
        return new_grid

class Grid2():
    def __init__(self, basic_grid, f):
        self.template = basic_grid
        self.expansion = f
        new_grid = self.clean_grid()
        new_start = (basic_grid.start[0] + basic_grid.n_rows*f, basic_grid.start[1] + basic_grid.n_cols*f)
        self.start = new_start
        self.n_rows = len(new_grid)
        self.n_cols = len(new_grid[0])
        self.history = []
        r = new_start[0]
        c = new_start[1]
        new_grid[r][c] = 'O'
        self.history.append(new_grid)
        
    def clean_grid(self):
        f = self.expansion
        new_grid = self.template.clean_grid()
        
        newer_grid = []
        for __ in range(2*f+1):
            for row in new_grid:
                newer_row = []
                for __ in range(2*f+1):
                    for item in row:
                        newer_row.append(item)
                newer_grid.append(newer_row)
    
        return newer_grid     
    
    def step_grid(self):
        old_grid = self.history[-1]
        new_grid = self.clean_grid()
        # print_grid(new_grid)
        valid_dirs = ['U','L','D','R']
        for r, row in enumerate(old_grid):
            for c, item in enumerate(row):
                if item == 'O':
                    adj_dict, adj_ref = alg.get_adj_cells_2d(old_grid, r, c)
                    for d in valid_dirs:
                        if adj_dict[d] == 'O':
                            # elf could be on a neighbor, so eligble to step here
                            new_grid[r][c] = 'O'
                        if adj_dict[d] == '.':
                            # valid place to step next
                            new_r, new_c = adj_ref[d]
                            # print(new_r,new_c)
                            new_grid[new_r][new_c] = 'O'
        self.history.append(new_grid)
        return new_grid
        
def print_grid(grid):
    for line in grid:
        print(''.join(line))
    print()
    return

def count_plots(grid):
    count = 0
    for row in grid:
        for item in row:
            if item == 'O':
                count += 1
    return count

def count_rocks(grid):
    count = 0
    for row in grid:
        for item in row:
            if item == '#':
                count += 1
    return count


def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---
    valid_spots = 0
    valid_spots2 = 0


    # consider stability -> any spot reached previously on an even number
    # ... of steps backwards can be reached again by bouncing back/forth an
    # ... even number number of times
    # this is is strictly a search problem -> how many "new" plots can be
    # reached by a given time
    
    # consider all even times for the toy example
    
    
    odd = 1
    
    
    grid_tracker0 = Grid(file_contents)
    grid_tracker = Grid2(grid_tracker0,100)
    
    grid = grid_tracker.clean_grid()
    start_pos = grid_tracker.start
    # print(start_pos)
    
    new_time = 0
    
    prev_visit = set()
    prev_visit.add(start_pos)
    
    
    pos_queue = PriorityQueue()
    next_id = 0
    
    
    state = (new_time, next_id, start_pos)
    next_id += 1
    
    pos_queue.put(state)
    
    
    if (new_time%2) == odd:
        prev_visit.add(start_pos)
    
    
    # each time record, we will count only new visits
    # still going to grow exponentially
    # only record even visits to align with toy example
    new_visits_record = {}
    new_visits_record[0] = 1
    
    max_time = 2000
        
    while not pos_queue.empty():
        state = pos_queue.get()
        # print(state)
        pos = state[2]
        new_time = state[0]+1
        
        adj_dict, adj_ref = alg.get_adj_cells_2d(grid, pos[0], pos[1])
        valid_dirs = ['U','D','L','R']
        
        for d in valid_dirs:
            if adj_dict[d] == '.'  and adj_ref[d] not in prev_visit:
                
                if new_time < max_time:
                    new_state = (new_time, next_id, adj_ref[d])
                    next_id += 1
                
                pos_queue.put(new_state)
                
                if new_time in new_visits_record:
                    new_visits_record[new_time] += 1
                else:
                    new_visits_record[new_time] = 1
                prev_visit.add(adj_ref[d])
            
            
            
            
    # print(pos_queue)
            
    # print(prev_visit)
    
    # print(new_visits_record)
    
    new_array = []
    
    running_sum = 0
    for key in new_visits_record:
        if key%2 == 1:
            new_array.append(new_visits_record[key])
            running_sum += new_visits_record[key]
    
    print(running_sum)
    
    print(new_array)
    
    
    
    
    
    

    # new_grid = grid_tracker.history[0]
    # # print_grid(new_grid)
    
    # for _ in range(19):
    #     new_grid = grid_tracker.step_grid()
    
    # print_grid(new_grid)

    # valid_spots = count_plots(new_grid)
    



    # grid_tracker2 = Grid2(grid_tracker, 0)
    # new_grid = grid_tracker2.history[0]

    # count_tracker = []
    # count_tracker.append(count_plots(new_grid))

    # for _ in range(10):
    #     new_grid = grid_tracker2.step_grid()
    #     new_count = count_plots(new_grid)
    #     count_tracker.append(new_count)
        
        
    # print_grid(new_grid)
    
    # valid_spots2 = count_plots(new_grid)

    # print(count_tracker)
    # # # print(delta_tracker)

    # num_rocks = count_rocks(new_grid)
    # print('rocks', num_rocks)
    # print(grid_tracker2.n_rows, grid_tracker2.n_cols)

    # ----------------------
    
    part1 = valid_spots
    part2 = valid_spots2


    if input_type == 1:
        in_txt = 'Full Input'
    else:
        in_txt = 'Test Input:'
    return [in_txt, part1, part2]


if __name__ == '__main__':
    x = main()
    if x:
        print(x[0])
        print(f'Part 1: {x[1]}')
        print(f'Part 2: {x[2]}')
