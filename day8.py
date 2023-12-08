# import numpy as np
import file_io as fio
# import algo_util as alg

day_num = 8
input_type = 1 # 0 = test, 1 = input

def make_node_dict(node_map):
    
    node_dict = {}
    for line in node_map:
        tmp = line.split('=')
        this_node = tmp[0].split()[0]
        dest = tmp[1].split(',')
        destL = dest[0].split()[0][1:]
        destR = dest[1].split()[0][:-1]
        node_dict[this_node] = {'L':destL, 'R':destR}
    
    return node_dict

def get_finish_steps(start, node_dict, directions, part = 1):
    len_dir = len(directions)
    whereami = start
    steps = 0
    finished = 0
    while not finished:
        steps +=1
        next_turn = directions[(steps % len_dir)-1]
        whereami = node_dict[whereami][next_turn]
        if part == 1 and whereami == 'ZZZ':
            finished = 1
        elif part == 2 and whereami[-1] == 'Z':
            finished = 1
    
    return steps


def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---

    directions = file_contents[0]
    len_dir = len(directions)
    # print(len_dir)
    
    node_map = file_contents[2:]
    # print(node_map)

    node_dict = make_node_dict(node_map)
    # print(node_dict)
    
    # part 1
    steps = get_finish_steps('AAA', node_dict, directions, part = 1)
    
    # part 2
    steps_list = []
    for node in node_dict:
        if node[-1] == 'A':
            steps_list.append(get_finish_steps(node, node_dict, directions, part = 2))
        
    # all step counts have a prime factor of length of directions
    # (this is a convienence to how the problem was set up)
    lcm = len_dir
    for step_count in steps_list:
        lcm *= int((step_count/len_dir))

    # ----------------------
    
    part1 = steps
    part2 = lcm


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
