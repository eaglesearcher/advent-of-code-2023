import numpy as np
import file_io as fio
import algo_util as alg

day_num = 9
input_type = 1 # 0 = test, 1 = input

def get_next_order_derivative(sequence):
    return sequence[1:] - sequence[:-1]


def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---

    all_seq = []
    for line in file_contents:
        new_list = np.asarray([int(i) for i in line.split()])
        all_seq.append(new_list)
    
    sum_p1 = 0
    sum_p2 = 0
    for line in all_seq:
        first_derivative = [line[0]]
        last_derivative = [line[-1]]
        idx = 1
        while not (np.max(line)==0 and np.min(line)==0):
            line = get_next_order_derivative(line)
            print(line)
            last_derivative.append(line[-1])
            first_derivative.append(line[0]*(-1)**idx)
            idx += 1
        # print(last_derivative)
        next_value = np.sum(last_derivative)
        prev_value = np.sum(first_derivative)
        sum_p1 += next_value
        sum_p2 += prev_value
        print(prev_value)
    



    # ----------------------
    
    part1 = sum_p1
    part2 = sum_p2


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
