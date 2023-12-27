import numpy as np
import file_io as fio
import algo_util as alg

day_num = 18
input_type = 1 # 0 = test, 1 = input


def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---
    plan = file_contents
    
    
    # redux == shoelace
        
    # part 1 -- using direction / color from the line
    pt_list = []
    start_position = (0,0)
    pt_list.append(start_position)
    last_position = start_position
    
    width_dig = 0
    
    for line in plan:
        r = last_position[0]
        c = last_position[1]
    
        direction, count, color = line.split()
        count = int(count)
        color = alg.hex2dec(color[2:-1])
        if direction == 'R':
            new_pt = (r, c+count)
        elif direction == 'L':
            new_pt = (r,c-count)
        elif direction == 'U':
            new_pt = (r-count,c)
        elif direction == 'D':
            new_pt = (r+count,c)
        pt_list.append(new_pt)
        last_position = new_pt
        # adds the bonus width of the trench (not including end points)
        width_dig += 0.5*(count - 1)
        
    # this is a special case (square/manhattan digging)
    # square trench with width = 1
    # there are 4 unique "outer" blocks w/ 3/4 bonus area
    # every other "outer" must be paired with an "inner" for a total area of 1
    num_pts = len(pt_list)-1
    corner_dig = 4*3/4 + (num_pts-4)/2
        
    shoelace_area = alg.shoelace(pt_list)
            
    dig_area = shoelace_area + corner_dig + width_dig
    

    
    # part 2 -- extract direction & count from color
    pt_list = []
    start_position = (0,0)
    pt_list.append(start_position)
    last_position = start_position
    
    width_dig = 0
    
    for line in plan:
        r = last_position[0]
        c = last_position[1]
    
        direction, count, color = line.split()
        count = alg.hex2dec(color[2:-2])
        direction = color[-2]
        print(count, direction)
        # color = alg.hex2dec(color[2:-1])
        if direction == '0': # R
            new_pt = (r, c+count)
        elif direction == '2': # L
            new_pt = (r,c-count)
        elif direction == '3': # U
            new_pt = (r-count,c)
        elif direction == '1': # D
            new_pt = (r+count,c)
        pt_list.append(new_pt)
        last_position = new_pt
        # adds the bonus width of the trench (not including end points)
        width_dig += 0.5*(count - 1)
        
    # this is a special case (square/manhattan digging)
    # square trench with width = 1
    # there are 4 unique "outer" blocks w/ 3/4 bonus area
    # every other "outer" must be paired with an "inner" for a total area of 1
    num_pts = len(pt_list)-1
    corner_dig = 4*3/4 + (num_pts-4)/2

    shoelace_area = alg.shoelace(pt_list)

    dig_area_p2 = shoelace_area + corner_dig + width_dig


        
    # # ---- OG solution -- do a flood / counting approach ----
    # # create a brute force list of points
    # pt_list = []
    
    # last_position = (0,0)
    # pt_list.append(last_position)
    
    # for line in plan:
    #     r = last_position[0]
    #     c = last_position[1]
        
    #     direction, count, color = line.split()
    #     count = int(count)
    #     if direction == 'R':
    #         new_elements = [(r,c+i+1) for i in range(count)]
    #     elif direction == 'L':
    #         new_elements = [(r,c-i-1) for i in range(count)]
    #     elif direction == 'U':
    #         new_elements = [(r-i-1,c) for i in range(count)]
    #     elif direction == 'D':
    #         new_elements = [(r+i+1,c) for i in range(count)]
    #     # print(new_elements)
    #     pt_list.extend(new_elements)
    #     last_position = new_elements[-1]

    # # find the bounds of the box
    # max_r = 0
    # min_r = 1
    # max_c = 0
    # min_c = 1

    # for pt in pt_list:
    #     r = pt[0]
    #     c = pt[1]
    #     max_r = max(max_r, r)
    #     min_r = min(min_r, r)
    #     max_c = max(max_c, c)
    #     min_c = min(min_c, c)
    
    # # print(min_r, max_r, min_c, max_c)
    # grid = [['.' for _ in range(max_c-min_c+1)] for _ in range(max_r - min_r+1)]
    # new_grid = [['.' for _ in range(max_c-min_c+1)] for _ in range(max_r - min_r+1)]
    
    # # normalize the bounds to positive ints (now they are matrix indices)
    # dig_count = 0
    # pt_list_norm = []
    # for pt in pt_list:
    #     r = pt[0] - min_r
    #     c = pt[1] - min_c
    #     pt_list_norm.append((r,c))
    #     grid[r][c] = '#'
        
    # dig_count = len(set(pt_list))
    # print(dig_count)

    # # from visual inspection, the square 1 R and 1 U from start is inside
    # # for both example and input
    # # then flood the interior using a queue (avoid recursion depth)
    # start_pos = (-min_r+1, -min_c+2)
    
    # inside_set = set()
    # seed_set = set()
    
    # seed_set.add(start_pos)

    # ref = ['L','R','U','D']

    # counter = 0
    # while(len(seed_set) > 0):
    #     counter += 1
    #     if counter > 10000000:
    #         # while loop running forever
    #         break
    #     # print(seed_set)
    #     new_seed = seed_set.pop()
    #     inside_set.add(new_seed)
    #     r = new_seed[0]
    #     c = new_seed[1]
    #     adj_dict, adj_ref = alg.get_adj_cells_2d(grid, r, c)
        
    #     for direction in ref:
    #         value = adj_dict[direction]
    #         coord = adj_ref[direction]
    #         if value == '.' and coord not in inside_set:
    #             inside_set.add(coord)
    #             seed_set.add(coord)
    
    # dig_count += len(inside_set)
    
    
    
    
    
    
    # --- visualization ---
        
    # with open('d18_viz.txt','w') as f:
    #     for line in grid:
    #         f.write(''.join(line)+'\n')
        

    # ----------------------
    
    part1 = dig_area
    part2 = dig_area_p2


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
