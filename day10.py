# import numpy as np
import file_io as fio
import algo_util as alg

day_num = 10
input_type = 1 # 0 = test, 1 = input

def next_loc(this_loc, last_step, grid):
    
    symbol = get_symbol(this_loc, grid)
    
    # naive assumption that puzzle was built correctly (1 path in -> 1 path out)
    if symbol == '|':
        if last_step == 'U':
            direction = 'U'
        elif last_step == 'D':
            direction = 'D'
    
    elif symbol == '-':
        if last_step == 'L':
            direction = 'L'
        elif last_step == 'R':
            direction = 'R'
    
    elif symbol == 'L':
        if last_step == 'D':
            direction = 'R'
        elif last_step == 'L':
            direction = 'U'
    
    elif symbol == 'J':
        if last_step == 'D':
            direction = 'L'
        elif last_step == 'R':
            direction = 'U'
    
    elif symbol == '7':
        if last_step == 'U':
            direction = 'L'
        elif last_step == 'R':
            direction = 'D'
    
    elif symbol == 'F':
        if last_step == 'U':
            direction = 'R'
        elif last_step == 'L':
            direction = 'D'
    
    elif symbol == 'S': # hard-coded start
        direction = 'D'
    
    shift = (0,0)
    if direction == 'U':
        shift = (-1,0)
    elif direction == 'D':
        shift = (1,0)
    elif direction == 'L':
        shift = (0,-1)
    elif direction == 'R':
        shift = (0,1)
    
    new_loc = (this_loc[0]+shift[0], this_loc[1]+shift[1])
    
    return new_loc, direction


def get_symbol(loc, grid):
    return grid[loc[0]][loc[1]]

def set_symbol(loc, grid, new_value):
    grid[loc[0]][loc[1]] = new_value
    return 


def set_outside(loc, grid, recursion_depth = 0):
    max_recursion = 500 # python limits to 1000; needs at least 280 to be correct for puzzle input
    
    # set this location as outside
    set_symbol(loc, grid, '0')
    
    # get neighbors and set .'s to outside
    opts_sym, opts_ref = alg.get_adj_cells_2d(grid, loc[0],loc[1])
    valid_dir = ['U','R','D','L']
    for direction in valid_dir:
        if recursion_depth < max_recursion and opts_sym[direction] == '.':
            set_outside(opts_ref[direction],grid, recursion_depth+1)
        
    return
    

def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---
    grid = file_contents
    # get start loc
    for line_idx, line in enumerate(grid):
        for sym_idx, symbol in enumerate(line):
            if symbol == 'S':
                start = (line_idx, sym_idx)

    num_lines = len(grid)
    num_cols = len(grid[0])
    # print(num_lines, num_cols)
    
    map_grid = [['.' for i in range(num_cols)] for i in range(num_lines)]
        
    # sym, ref = alg.get_adj_cells_2d(grid, start[0], start[1])
    # valid_dir = ['U','R','D','L']
    # for direction in valid_dir:
        # print(direction, ref[direction], sym[direction])
    
    # pick starting direction -- down -- works with full input + p2 test
    step = 0
    new_loc = start
    new_dir = 'D'
    
    # take a step
    for _ in range(1000000):
        step += 1
        new_loc, new_dir = next_loc(new_loc, new_dir, grid)
        new_sym = get_symbol(new_loc, grid)
        map_grid[new_loc[0]][new_loc[1]] = new_sym
        if new_sym == 'S':
            map_grid[new_loc[0]][new_loc[1]] = 'S'
            # print('arrived at S, finished at step', step)
            break
    
    
    # build an oversampled grid to capture "squeezing between pipes"
    super_grid = [['.' for i in range(num_cols*2)] for i in range(num_lines*2)]
    
    for line_idx, line in enumerate(map_grid):
        for sym_idx, sym in enumerate(line):
            super_grid[line_idx*2][sym_idx*2] = sym
            if sym in {'F','-','L'}:
                super_grid[line_idx*2][sym_idx*2+1] = '-'
            if sym in {'F','|','7','S'}:
                super_grid[line_idx*2+1][sym_idx*2] = '|'
                
    # for i in super_grid:
    #     print(''.join(i))
    
    # now do search from edges with super grid
    valid_dirs = ['U','L','D','R']
    
    # work from top-bottom, left-right
    for line_idx, line in enumerate(super_grid):
        for sym_idx, sym in enumerate(line):
            loc = (line_idx, sym_idx)
            if sym == '.':
                opts_sym, opts_ref = alg.get_adj_cells_2d(super_grid, loc[0],loc[1])
                # print(opts_ref)
                for direction in valid_dirs:
                    # if any dirs don't exist, we're at an edge
                    # otherwise check if any neighbors are outside
                    if not opts_ref[direction] or opts_sym[direction] == '0': 
                        # spread recursively
                        set_outside(loc,super_grid)
                        break
 
    # finally collapse back to regular grid   
    collapse_grid =   [['.' for i in range(num_cols)] for i in range(num_lines)] 
 
    count_inside = 0
    for line_idx, line in enumerate(super_grid[::2]):
        for sym_idx, sym in enumerate(line[::2]):
            collapse_grid[line_idx][sym_idx] = super_grid[line_idx*2][sym_idx*2]
            if collapse_grid[line_idx][sym_idx] == '.':
                count_inside += 1
    
    print(count_inside)
    
    # print('final grid')
    # for i in collapse_grid:
    #     print(''.join(i))
    
    
    # ----------------------
    
    part1 = int(step/2)
    part2 = count_inside


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
