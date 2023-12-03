# import numpy as np
import file_io as fio
import algo_util as alg

day_num = 3
input_type = 1 # 0 = test, 1 = input

def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---

    # part 1

    def get_number(chars):
        builder = ''
        for c in chars:
            if c.isdigit():
                builder += c
            else:
                return builder
        return builder

    def is_symbol(char):
        ans = True
        if not char:
            ans = False
        elif char == '.':
            ans = False
        elif char.isalpha():
            ans = False
        elif char.isdigit():
            ans = False
        return ans

    def check_for_symbol(input_file, line_idx, start_idx, end_idx):
        # loop through each char of number
        for col_idx in range(start_idx, end_idx+1):
            # get adj cells for each char
            adj_dict, __ = alg.get_adj_cells_2d(input_file, line_idx, col_idx)
            for key in adj_dict:
                if is_symbol(adj_dict[key]):
                    return True
        return False
        
    # main loop, part 1
    sum_nums = 0
    
    for line_idx, line in enumerate(file_contents):
        num_chars = len(line)
        
        idx = 0
        while(idx is not num_chars):
            new_char = line[idx]
            if new_char.isdigit():
                tmp = line[idx:]
                num_str = get_number(tmp)
                valid = check_for_symbol(file_contents, line_idx, idx, idx+len(num_str)-1)
                idx += len(num_str)
                if valid:
                    sum_nums += int(num_str)
            else:
                idx += 1

    # ------------------------------------------------
    # part 2

    def check_for_number(input_file, line_idx, char_idx):
        nums = []
        
        adj_dict, __ = alg.get_adj_cells_2d(input_file, line_idx, char_idx)
        
        # left stuff
        if adj_dict['L'] and adj_dict['L'].isdigit():
            check = input_file[line_idx][:char_idx]
            check = check[::-1]
            nums.append(int(get_number(check)[::-1]))

        # right stuff
        if adj_dict['R'] and adj_dict['R'].isdigit():
            if input_file[line_idx][char_idx+1].isdigit():
                check = input_file[line_idx][char_idx+1:]
                nums.append(int(get_number(check)))
                
        # up stuff
        if adj_dict['U'] and adj_dict['U'].isdigit():
            # as long as the middle is a digit, there can only be one adj
            check = input_file[line_idx-1][:char_idx+1]
            check = check[::-1]
            check2 = input_file[line_idx-1][char_idx:]
            nums.append(int(get_number(check)[1:][::-1] + get_number(check2)))
        else:
            # must check both upper left & upper right
            if adj_dict['UL'] and adj_dict['UL'].isdigit():
                check = input_file[line_idx-1][:char_idx]
                check = check[::-1]
                nums.append(int(get_number(check)[::-1]))
            if adj_dict['UR'] and adj_dict['UR'].isdigit():
                check = input_file[line_idx-1][char_idx+1:]
                nums.append(int(get_number(check)))
            
        # dn stuff
        if adj_dict['D'] and adj_dict['D'].isdigit():
            # as long as the middle is a digit, there can only be one adj
            check = input_file[line_idx+1][:char_idx+1]
            check = check[::-1]
            check2 = input_file[line_idx+1][char_idx:]
            nums.append(int(get_number(check)[1:][::-1] + get_number(check2)))   
        else:
            # must check both lower left & lower right
            if adj_dict['DL'] and adj_dict['DL'].isdigit():
                check = input_file[line_idx+1][:char_idx]
                check = check[::-1]
                nums.append(int(get_number(check)[::-1]))
            if adj_dict['DR'] and adj_dict['DR'].isdigit():
                check = input_file[line_idx+1][char_idx+1:]
                nums.append(int(get_number(check)))
   
        return nums        
        
    # main loop, part 2
    gears = 0
    for line_idx, line in enumerate(file_contents):
        # print(line)
        for char_idx, char in enumerate(line):
            if char == '*':
                nums = check_for_number(file_contents, line_idx, char_idx)
                if len(nums) == 2:
                    gears += nums[0]*nums[1]
           
    
    # ----------------------
    
    part1 = sum_nums
    part2 = gears


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
