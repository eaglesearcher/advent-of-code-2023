import numpy as np
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

    def is_symbol(char):
        ans = True
        if char.isalpha():
            ans = False
        elif char.isdigit():
            ans = False
        elif char == '.':
            ans = False
        return ans


    def check_for_symbol(input_file, line_idx, start_idx, end_idx):
        max_lines = len(input_file)
        line_len = len(input_file[line_idx])

        # print(input_file[line_idx][end_idx])

        if start_idx > 0:
            l_check = input_file[line_idx][start_idx - 1]
            if is_symbol(l_check):
                return True
        else:
            start_idx += 1

        if end_idx < line_len-1:
            r_check = input_file[line_idx][end_idx]
            if is_symbol(r_check):
                return True
        else:
            end_idx -= 1
            
        # "above"
        if line_idx > 1:
            up_check = input_file[line_idx-1][start_idx-1:end_idx+1]
            for char in up_check:
                if is_symbol(char):
                    return True
        # "below"
        if line_idx < max_lines-1:
            dn_check = input_file[line_idx+1][start_idx-1:end_idx+1]
            for char in dn_check:
                if is_symbol(char):
                    return True
        
        return False
        

    sum_nums = 0
    
    for line_idx, line in enumerate(file_contents):
        num_chars = len(line)
        
        idx = 0
        
        while(idx is not num_chars):
            new_char = line[idx]
            if new_char.isdigit():
                tmp = line[idx:]
                num_str = ''
                for char in tmp:
                    if char.isdigit():
                        num_str += char
                    else:
                        break
                # print(num_str)
                valid = check_for_symbol(file_contents, line_idx, idx, idx+len(num_str))
                # print(tmp, valid)
                
                idx += len(num_str)
                if valid:
                    # print(num_str)
                    sum_nums += int(num_str)
            else:
                idx += 1


    # part 2

    def get_number(chars):
        builder = ''
        for c in chars:
            if c.isdigit():
                builder += c
            else:
                return builder
        return builder
        

    def check_for_number(input_file, line_idx, char_idx):
        max_lines = len(input_file)
        line_len = len(input_file[line_idx])
        
        nums = []
        # left stuff
        if char_idx > 0:
            if input_file[line_idx][char_idx-1].isdigit():
                check = input_file[line_idx][:char_idx]
                check = check[::-1]
                nums.append(int(get_number(check)[::-1]))
        
        # right stuff
        if char_idx < line_len - 1:
            if input_file[line_idx][char_idx+1].isdigit():
                check = input_file[line_idx][char_idx+1:]
                nums.append(int(get_number(check)))

        # up stuff
        if line_idx > 0:
            # as long as the middle is a digit, there can only be one adj
            if input_file[line_idx-1][char_idx].isdigit():
                check = input_file[line_idx-1][:char_idx+1]
                check = check[::-1]
                check2 = input_file[line_idx-1][char_idx:]
                nums.append(int(get_number(check)[1:][::-1] + get_number(check2)))
                
            else:
                # must check both upper left & upper right
                if char_idx > 0 and input_file[line_idx-1][char_idx-1].isdigit():
                    check = input_file[line_idx-1][:char_idx]
                    check = check[::-1]
                    nums.append(int(get_number(check)[::-1]))
                if char_idx < line_len-1 and input_file[line_idx-1][char_idx+1].isdigit():
                    check = input_file[line_idx-1][char_idx+1:]
                    nums.append(int(get_number(check)))
                    
        # dn stuff
        if line_idx < max_lines - 1:
            # as long as the middle is a digit, there can only be one adj
            if input_file[line_idx+1][char_idx].isdigit():
                check = input_file[line_idx+1][:char_idx+1]
                check = check[::-1]
                
                check2 = input_file[line_idx+1][char_idx:]
                nums.append(int(get_number(check)[1:][::-1] + get_number(check2)))   
                
            else:
                # must check both lower left & lower right
                if char_idx > 0 and input_file[line_idx+1][char_idx-1].isdigit():
                    check = input_file[line_idx+1][:char_idx]
                    check = check[::-1]
                    nums.append(int(get_number(check)[::-1]))
                if char_idx < line_len-1 and input_file[line_idx+1][char_idx+1].isdigit():
                    check = input_file[line_idx+1][char_idx+1:]
                    nums.append(int(get_number(check)))
                
        return nums        
        

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
