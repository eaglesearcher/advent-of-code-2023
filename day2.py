import numpy as np
import file_io as fio
import algo_util as alg

day_num = 2
input_type = 1 # 0 = test, 1 = input

def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---
        
    # part 1 / part 2
    max_color = {'blue':14, 'green':13,'red':12} # part 1 given
    
    sum_ids = 0 # part 1 answer tracker
    sum_powers = 0 # part 2 answer tracker
    for game in file_contents:
        x = game.split(':') # split game id from draws
        this_id = x[0].split(' ')[1] # split number from 'Game'
        all_draws = x[1].split(';') #  separate each set of draws
        
        impossible = 0 # part 1 comparison tracker
        min_color = {'blue':0, 'green':0, 'red':0} # part 2 comparison tracker
        
        for this_draw in all_draws:
            drawn = this_draw[1:].split(', ')
            # splits apart each draw within a single game
            # [1:] eliminates leading space
        
            for each_drawn in drawn:
                tmp = each_drawn.split(' ') # splits color from value
                value = int(tmp[0])
                color = tmp[1]
                
                if value > max_color[color]: # part1 -- is game possible
                    impossible = 1
                
                if value > min_color[color]: # part2 -- find min viable cubes
                    min_color[color] = value
                    
        if not impossible:
            sum_ids += int(this_id)
            
        game_power = 1
        for key in min_color:
            game_power *= min_color[key]
        sum_powers += game_power
            
    # ----------------------
    
    part1 = sum_ids
    part2 = sum_powers


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
