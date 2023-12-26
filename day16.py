import numpy as np
import file_io as fio
import algo_util as alg

day_num = 16
input_type = 1 # 0 = test, 1 = input


class Beam():
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.hash = (position, direction)
        return

def get_new_beams(grid, input_beam):
    r = input_beam.position[0]
    c = input_beam.position[1]
    d = input_beam.direction

    here = grid[r][c]
    new_dirs = []

    if here == '.':
        new_dirs.append(d)
    elif here == '-':
        if d == 'L' or d == 'R':
            new_dirs.append(d)
        elif d == 'U' or d == 'D':
            # two beams L+R, regardless of U vs D    
            new_dirs.append('L')
            new_dirs.append('R')
    elif here == '|':
        if d == 'U' or d == 'D':
            new_dirs.append(d)
        elif d == 'L' or d == 'R':
            # two beams U+D, regardless of L vs R
            new_dirs.append('U')
            new_dirs.append('D')
    elif here == '\\':
        if d == 'U':
            new_dirs.append('L')
        elif d == 'D':
            new_dirs.append('R')
        elif d == 'L':
            new_dirs.append('U')
        elif d == 'R':
            new_dirs.append('D')
    elif here == '/':
        if d == 'U':
            new_dirs.append('R')
        elif d == 'D':
            new_dirs.append('L')
        elif d == 'L':
            new_dirs.append('D')
        elif d == 'R':
            new_dirs.append('U')
            
    adj_dict, adj_ref = alg.get_adj_cells_2d(grid, r, c)

    new_beams = []
    for this_dir in new_dirs:
        if adj_ref[this_dir] != None:
            new_beams.append(Beam(adj_ref[this_dir], this_dir))
    
    
    return new_beams
    
   
def set_lit(grid, beam):
    r = beam.position[0]
    c = beam.position[1]
    grid[r][c] = 1
    return grid

def reset_lit(grid):
    lit_grid = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    return lit_grid

def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---

    grid = file_contents
    
    # for line in grid:
    #     print(line)

    # lit_grid = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    lit_grid = reset_lit(grid)

    beam_hash = {}
    beam_list = []

    # part 1

    # starting beam
    pos = (0,0)
    direction = 'R'
    beam_list.append(Beam(pos, direction))

    while len(beam_list) > 0:
    # for _ in range(100):
        old_beam = beam_list.pop()
        if old_beam in beam_hash:
            continue
        lit_grid = set_lit(lit_grid, old_beam)
        beam_hash[old_beam.hash] = 1
        
        new_beams = get_new_beams(grid, old_beam)

        for each_beam in new_beams:
            if each_beam.hash not in beam_hash and each_beam not in beam_list:
                beam_list.append(each_beam)
    
    # for line in lit_grid:
        # print(line)

    energized_p1 = np.sum(lit_grid)
    

    # part 2 (exhaustive)

    max_energy = 0

    # top row looking down
    for i in range(len(grid[0])): # len of line:
        pos = (0,i)
        direction = 'D'
    
        beam_hash = {}
        beam_list = []
        lit_grid = reset_lit(grid)
    
        beam_list.append(Beam(pos, direction))
    
        while len(beam_list) > 0:
        # for _ in range(2):
            old_beam = beam_list.pop()
            if old_beam in beam_hash:
                continue
            lit_grid = set_lit(lit_grid, old_beam)
            beam_hash[old_beam.hash] = 1
            new_beams = get_new_beams(grid, old_beam)
            for each_beam in new_beams:
                if each_beam.hash not in beam_hash and each_beam not in beam_list:
                    beam_list.append(each_beam)
        
        # for line in lit_grid:
        #     print(line)
    
        energized = np.sum(lit_grid)
        max_energy = max(energized, max_energy)
        
    # bottom row looking up
    for i in range(len(grid[0])): # len of line:
        pos = (len(grid)-1,i)
        direction = 'U'
    
        beam_hash = {}
        beam_list = []
        lit_grid = reset_lit(grid)
    
        beam_list.append(Beam(pos, direction))
    
        while len(beam_list) > 0:
        # for _ in range(2):
            old_beam = beam_list.pop()
            if old_beam in beam_hash:
                continue
            lit_grid = set_lit(lit_grid, old_beam)
            beam_hash[old_beam.hash] = 1
            new_beams = get_new_beams(grid, old_beam)
            for each_beam in new_beams:
                if each_beam.hash not in beam_hash and each_beam not in beam_list:
                    beam_list.append(each_beam)
        
        # for line in lit_grid:
        #     print(line)
    
        energized = np.sum(lit_grid)
        max_energy = max(energized, max_energy)

    # left col looking right
    for i in range(len(grid)): # len of line:
        pos = (i,0)
        direction = 'R'
    
        beam_hash = {}
        beam_list = []
        lit_grid = reset_lit(grid)
    
        beam_list.append(Beam(pos, direction))
    
        while len(beam_list) > 0:
        # for _ in range(2):
            old_beam = beam_list.pop()
            if old_beam in beam_hash:
                continue
            lit_grid = set_lit(lit_grid, old_beam)
            beam_hash[old_beam.hash] = 1
            new_beams = get_new_beams(grid, old_beam)
            for each_beam in new_beams:
                if each_beam.hash not in beam_hash and each_beam not in beam_list:
                    beam_list.append(each_beam)
        
        # for line in lit_grid:
        #     print(line)
    
        energized = np.sum(lit_grid)
        max_energy = max(energized, max_energy)

    # right col looking left
    for i in range(len(grid)): # len of line:
        pos = (i,len(grid)-1)
        direction = 'L'
    
        beam_hash = {}
        beam_list = []
        lit_grid = reset_lit(grid)
    
        beam_list.append(Beam(pos, direction))
    
        while len(beam_list) > 0:
        # for _ in range(2):
            old_beam = beam_list.pop()
            if old_beam in beam_hash:
                continue
            lit_grid = set_lit(lit_grid, old_beam)
            beam_hash[old_beam.hash] = 1
            new_beams = get_new_beams(grid, old_beam)
            for each_beam in new_beams:
                if each_beam.hash not in beam_hash and each_beam not in beam_list:
                    beam_list.append(each_beam)
        
        # for line in lit_grid:
        #     print(line)
    
        energized = np.sum(lit_grid)
        max_energy = max(energized, max_energy)

    # ----------------------
    
    part1 = energized_p1
    part2 = max_energy


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
