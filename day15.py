# import numpy as np
import file_io as fio
# import algo_util as alg

day_num = 15
input_type = 1 # 0 = test, 1 = input

def hash_fun(input_str):
    current_value = 0
    for c in input_str:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256
    
    return current_value


def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---

    input_list = file_contents[0].split(',')
    
    # part 1
    hashed_list = [hash_fun(group) for group in input_list]
    p1_sum = sum(hashed_list)

    # part 2
    
    boxes = {}
    boxes_f = {}
    
    for group in input_list:
        if '=' in group:
            label = group[:-2]
            box = hash_fun(label)
            focal_length = group[-1]
            # print('add label:', label, 'to box:', box, 'with f:', focal_length)
            if box not in boxes:
                boxes[box] = []
                boxes_f[box] = {}
                
            if label not in boxes[box]:
                boxes[box].append(label)
            boxes_f[box][label] = int(focal_length)
            
        elif '-' in group:
            label = group[:-1]
            box = hash_fun(label)
            # print('remove label:', label, 'from box:', box)
            if box in boxes and label in boxes[box]:
                boxes[box].remove(label)
                pass
    
    total_power = 0  
    for box in boxes:
        for idx, lens in enumerate(boxes[box]):
            power = (1+box)*(1+idx)*boxes_f[box][lens]
            total_power += power

    # ----------------------
    
    part1 = p1_sum
    part2 = total_power


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
