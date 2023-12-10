# import numpy as np
import file_io as fio
import algo_util as alg

day_num = 10
input_type = 0 # 0 = test, 1 = input

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
                # print(line_idx, sym_idx)

    # print(start, get_symbol(start, grid))

    num_lines = len(grid)
    num_cols = len(grid[0])
    print(num_lines, num_cols)
    
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
        # if new_sym in {'F','J','L','7'}:
        #     map_grid[new_loc[0]][new_loc[1]] = '+'
        # elif new_sym == '|':
        #     map_grid[new_loc[0]][new_loc[1]] = '|'
        # elif new_sym == '-':
        #     map_grid[new_loc[0]][new_loc[1]] = '-'
        # print('Take a step -', new_dir, '- arrive at', new_loc, 'with symbol', new_sym)
        if new_sym == 'S':
            map_grid[new_loc[0]][new_loc[1]] = 'S'
            # print('arrived at S, finished at step', step)
            break
    
    # print('next step - U')
    
    for i in map_grid:
        print(''.join(i))
    
    super_grid = [['.' for i in range(num_cols*2)] for i in range(num_lines*2)]
    
    # super_grid[start[0]*2+1][start[1]] = '|'
    
    for line_idx, line in enumerate(map_grid):
        for sym_idx, sym in enumerate(line):
            super_grid[line_idx*2][sym_idx*2] = sym
            if sym in {'F','-','L'}:
                super_grid[line_idx*2][sym_idx*2+1] = '-'
            if sym in {'F','|','7','S'}:
                super_grid[line_idx*2+1][sym_idx*2] = '|'
                
    
    
    for i in super_grid:
        print(''.join(i))
    
    # now do search on edges with super grid
    # finally collapse back to regular grid
    
    
    
    
    
    
    # ----------------------
    
    part1 = int(step/2)
    part2 = 0


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
