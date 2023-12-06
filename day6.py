import numpy as np
import file_io as fio
import algo_util as alg

day_num = 6
input_type = 1 # 0 = test, 1 = input

def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---

    # part 1

    times = [int(i) for i in file_contents[0].split(':')[1].split()]
    dist = [int(i) for i in file_contents[1].split(':')[1].split()]

    margin = []
    product_p1 = 1
    for race_idx in range(len(times)):
        T = times[race_idx]
        d = dist[race_idx]
        min_th = np.floor((T-np.sqrt(T**2-4*d))/2 + 1)
        max_th = np.ceil((T+np.sqrt(T**2-4*d))/2 - 1)
        new_margin = max_th - min_th + 1
        margin.append(new_margin)
        # print(min_th, max_th, new_margin)
        product_p1 *= new_margin
    
    
    # part 2
    
    T = int(''.join(file_contents[0].split(':')[1].split()))
    d = int(''.join(file_contents[1].split(':')[1].split()))

    # print(T, d)
    
    min_th = np.floor((T-np.sqrt(T**2-4*d))/2 + 1)
    max_th = np.ceil((T+np.sqrt(T**2-4*d))/2 - 1)
    new_margin = max_th - min_th + 1
    
    

    # ----------------------
    
    part1 = product_p1
    part2 = new_margin


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
