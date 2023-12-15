import numpy as np
import file_io as fio
import algo_util as alg

day_num = 14
input_type = 1 # 0 = test, 1 = input

def convert_array(dish):
    # turn lists into numpy matrix for easy indexing
    dish_array = []
    for row in dish:
        new_row = []
        for element in row:
            if element == '.':
                new_row.append(0)
            elif element == 'O':
                new_row.append(1)
            elif element == '#':
                new_row.append(-1)
        dish_array.append(new_row)
    return np.asarray(dish_array)

def print_array(dish_array):
    # pretty print the numeric array
    for row in dish_array:
        print_row = ''
        for element in row:
            if element == 1:
                print_row += 'O'
            if element == -1:
                print_row += '#'
            if element == 0:
                print_row += '.'
        print(print_row)
    return

def calc_load(dish_array):
    # calc load of numeric array
    max_load = len(dish_array)
    total_load = 0
    for row_idx, row in enumerate(dish_array):
        for element in row:
            if element == 1:
                total_load += (max_load - row_idx)
    return total_load

def tilt(dish_array):
    # always tilts north, because I know it works that way
    num_rows = len(dish_array)
    num_cols = len(dish_array[0])

    for c in range(num_cols):
        next_open = 0
        for r in range(num_rows):
            if dish_array[r,c] == 0: # blank space, nothing to see here
                continue
            elif dish_array[r,c] == -1: # stopper, set next_open to idx+1
                next_open = r+1
            elif dish_array[r,c] == 1: # round
                if next_open == r: # don't move anything, increment next
                    next_open += 1
                else:
                    dish_array[next_open,c] = 1
                    dish_array[r,c] = 0
                    next_open += 1
    return dish_array

def spin_cycle(dish_array):
    # assume compass is normal at start "pointing north"
    dish_array = tilt(dish_array)
    # west
    dish_array = np.rot90(dish_array,k=-1)
    dish_array = tilt(dish_array)
    
    # south
    dish_array = np.rot90(dish_array,k=-1)
    dish_array = tilt(dish_array)
    
    # east
    dish_array = np.rot90(dish_array,k=-1)
    dish_array = tilt(dish_array)
    
    # return to north
    dish_array = np.rot90(dish_array,k=-1)
    
    return dish_array

def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---

    dish = file_contents

    # part 1 cheesy solution that doesn't move anything
    max_load = len(dish)
    num_cols = len(dish[0])
    next_load = [max_load for i in range(num_cols)]
    total_load = 0
    for row_idx, row in enumerate(dish):
        for idx, element in enumerate(row):
            if element == 'O':
                total_load += next_load[idx]
                next_load[idx] -= 1
            elif element == '#':
                next_load[idx] = max_load - row_idx - 1
                
    # part 2
    dish_array = convert_array(dish)
    # print_array(dish_array)

    # shake n bake for awhile to build up load list
    load_list = []
    for i in range(200): 
        dish_array = spin_cycle(dish_array)
        x = calc_load(dish_array)
        load_list.append(x)

    # print_array(dish_array)
    
    cycle_list, cycle_indices = alg.cycle_detect(load_list, n=20, print_samples=4)
    
    final = 0
    goal_number = 1000000000
    if cycle_list != None:
        final = alg.extract_cycle_value(cycle_list, cycle_indices, goal_number)
    
    # ----------------------
    
    part1 = total_load
    part2 = final


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
