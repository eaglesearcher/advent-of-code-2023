import numpy as np
import file_io as fio
# import algo_util as alg
import copy

day_num = 13
input_type = 1 # 0 = test, 1 = input

def parse_line(line):
    # print(line)
    line = line.replace('.','0')
    line = line.replace('#','1')
    line = [int(i) for i in line]
    return line

def get_mirror(pattern, old = (-1,-1)):
    # old = idx, axis
    
    r,c = np.shape(pattern)
    mirror_idx = -1
    mirror_axis = -1
    
    for i in range(r-1):
        valid = True
        for j in range(r-1):
            if i+j+1 < r and i-j >= 0:
                if not np.array_equal(pattern[i-j,:], pattern[i+1+j,:]):
                    valid = False
            if not valid:
                break
        if valid and not old == (i+1,0):
            # found the mirror (also isn't the previous mirror found!)
            mirror_idx = i+1 # 1-indexed
            mirror_axis = 0
            break
        else:
            valid = False
    
    # don't search if you found it already
    if not valid:
        for i in range(c-1):
            valid = True
            for j in range(c-1):
                if i+j+1 < c and i-j >= 0:
                    if not np.array_equal(pattern[:,i-j], pattern[:,i+1+j]):
                        valid = False
                if not valid:
                    break
            if valid and not old == (i+1,1):
                # found the mirror (also isn't the previous mirror found!)
                mirror_idx = i+1 # 1-indexed
                mirror_axis = 1
                break
            else:
                valid = False
            
    return mirror_idx, mirror_axis, valid

def invert_bit(pattern, loc):
    old_value = pattern[loc[0],loc[1]]
    new_pattern = copy.deepcopy(pattern)
    new_pattern[loc[0],loc[1]] = 1-old_value
    return new_pattern
    



def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---

    all_patterns = []
    new_pattern = []

    for line in file_contents:
        if line == '':
            all_patterns.append(np.asarray(new_pattern))
            new_pattern = []
        else:
            x = parse_line(line)
            new_pattern.append(x)
    # get the last one too!
    all_patterns.append(np.asarray(new_pattern))


    value1 = 0
    value2 = 0
    for this_pattern in all_patterns:

        # find the original mirror & value
        mirror_idx, mirror_axis, _ = get_mirror(this_pattern,(-1,-1))
        value1 += mirror_idx*((1-mirror_axis)*100+mirror_axis*1)

        old_mirror = (mirror_idx, mirror_axis)

        # print('old mirror', mirror_idx, mirror_axis)

        # start flipping bits until you find a new valid mirror
        r,c = np.shape(this_pattern)
        for i in range(r):
            for j in range(c):
                new_pattern = invert_bit(this_pattern,(i,j))
                mirror_idx, mirror_axis, valid = get_mirror(new_pattern, old_mirror)
                if valid:
                    break
            if valid:
                break
        if not valid:
            print('something went wrong!')
        # print('new mirror', mirror_idx, mirror_axis, valid)
        value2 += mirror_idx*((1-mirror_axis)*100+mirror_axis*1)


    # ----------------------
    
    part1 = value1
    part2 = value2


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
