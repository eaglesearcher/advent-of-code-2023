import numpy as np
import file_io as fio
# import algo_util as alg

day_num = 11
input_type = 1 # 0 = test, 1 = input

class galaxy():
    def __init__(self, pos, gal_id):
        self.id = gal_id
        self.pos = pos

def get_man_dist(pos1, pos2):
    dy = np.abs(pos2[1]-pos1[1])
    dx = np.abs(pos2[0]-pos1[0])
    return dx + dy
    
def get_galaxy_dist(gal_a, gal_b, blank_rows, blank_cols, expand_factor):
    y1, x1 = gal_a.pos
    y2, x2 = gal_b.pos
        
    y_dist = np.abs(y2-y1)
    x_dist = np.abs(x2-x1)
        
    for dark_space in blank_rows:
        if dark_space in set(range(min(y2,y1),max(y2,y1))):
            y_dist += (expand_factor-1)
    for dark_space in blank_cols:
        if dark_space in set(range(min(x2,x1),max(x2,x1))):
            x_dist += (expand_factor-1)        
    
    
    return x_dist + y_dist

def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---
    universe = file_contents
    
    num_lines = len(universe)
    num_obs = len(universe[0])
    
    # make a binary universe for easy analysis
    bin_univ = np.zeros((num_obs, num_lines), int)
    
    for line_idx, line in enumerate(universe):
        for obs_idx, observation in enumerate(line):
            if observation == '#':
                bin_univ[line_idx][obs_idx] = 1
                
    # for i in bin_univ:
    #     print(i)
        
    #check for blank rows/cols
    blank_rows = []
    blank_cols = []
    for row_idx, line in enumerate(bin_univ):
        if max(line) == 0:
            blank_rows.append(row_idx)
    for col_idx, col in enumerate(np.transpose(bin_univ)):
        if max(col) == 0:
            blank_cols.append(col_idx)
        
    # # expand the universe # naive p1
    # for idx in blank_cols[::-1]:
    #     bin_univ = np.insert(bin_univ, idx, 0, axis = 1)
    # for idx in blank_rows[::-1]:
    #     bin_univ = np.insert(bin_univ, idx, 0, axis = 0)
    
    # for i in bin_univ:
    #     print(i)

    # catalog galaxies
    galaxy_list = []
    this_id = 1
    for line_idx, line in enumerate(bin_univ):
        for obs_idx, obs in enumerate(line):
            if obs == 1:
                pos = (line_idx, obs_idx)
                galaxy_list.append(galaxy(pos, this_id))
                this_id += 1

    total_dist_p1 = 0 # int overflows
    total_dist_p2 = 0.0 # int overflows
    for a_idx, galaxy_a in enumerate(galaxy_list[:-1]):
        for b_idx, galaxy_b in enumerate(galaxy_list[a_idx+1:]):
            dist1 = get_galaxy_dist(galaxy_a, galaxy_b, blank_rows, blank_cols, 2)
            dist2 = get_galaxy_dist(galaxy_a, galaxy_b, blank_rows, blank_cols, 1000000)
            # print(f'{galaxy_a.id}->{galaxy_b.id}, d:{dist}')
            total_dist_p1 += dist1
            total_dist_p2 += dist2

    # ----------------------
    
    part1 = total_dist_p1
    part2 = total_dist_p2


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
