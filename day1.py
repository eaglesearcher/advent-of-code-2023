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
    file_contents = file_contents.split('\n')
    file_contents = file_contents[0:-1] # trim the ending newline
    # --- add code here! ---
    
    text = file_contents
    
    def translate_char(chars):
        if chars == 'one' or chars == 'eno':
            return '1'
        if chars == 'two' or chars == 'owt':
            return '2'
        if chars == 'three' or chars == 'eerht':
            return '3'
        if chars == 'four' or chars == 'ruof':
            return '4'
        if chars == 'five' or chars == 'evif':
            return '5'
        if chars == 'six' or chars == 'xis':
            return '6'
        if chars == 'seven' or chars == 'neves':
            return '7'
        if chars == 'eight' or chars == 'thgie':
            return '8'
        if chars == 'nine' or chars == 'enin':
            return '9'
        else:
            return chars

    value1 = 0
    value2 = 0
    for each_line in text:
        # print(each_line)
        x1 = re.findall('[0-9]',each_line)
        value1 += int(x1[0] + x1[-1])
        x2 = re.search('[0-9]|one|two|three|four|five|six|seven|eight|nine',each_line)
        char1 = translate_char(x2[0])
        x2 = re.search('[0-9]|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin',each_line[::-1])
        char2 = translate_char(x2[0])
        # print(char1, char2)
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
    print(x[0])
    print(f'Part 1: {x[1]}')
    print(f'Part 2: {x[2]}')
