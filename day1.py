import numpy as np
import file_io as fio
import algo_util as alg
import re # regex

day_num = 1
input_type = 1 # 0 = test, 1 = input

def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---
    
    text = file_contents
    
    value1 = 0
    value2 = 0
    for each_line in text:
        # part 1
        # regex to grab any numbers, take first/last from list
        x1 = re.findall('[0-9]',each_line)
        value1 += int(x1[0] + x1[-1])
        
        # part 2
        # separate searches for first & last
        token = '[0-9]|one|two|three|four|five|six|seven|eight|nine'
        x2 = re.search(token,each_line)
        char1 = str(alg.word_to_num(x2[0]))

        # flip the string to find the last occurance
        # cheap trick to flip the tokens
        # reuse word_to_num by re-flipping the token
        token = '[0-9]|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin'
        x2 = re.search(token,each_line[::-1])
        char2 = str(alg.word_to_num(x2[0][::-1]))

        value2 += int(char1+char2)
    
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
