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
        
    # part 1
    max_per_color = {'blue':14, 'green':13,'red':12}
    
   
    sum_ids = 0
    for game in file_contents:
        x = game.split(':')
        this_id = x[0].split(' ')[1]
        all_draws = x[1].split(';')
        failed = 0
        for this_draw in all_draws:
            drawn = this_draw[1:].split(', ')
            for each_drawn in drawn:
                tmp = each_drawn.split(' ')
                value = int(tmp[0])
                color = tmp[1]
                if value > max_per_color[color]:
                    failed = 1
                    break
            if failed:
                break
        if failed:
            continue
        sum_ids += int(this_id)
            
    # part 2
    sum_powers = 0
    for game in file_contents:
        x = game.split(':')
        this_id = x[0].split(' ')[1]
        all_draws = x[1].split(';')
        min_color = {'blue':0, 'green':0, 'red':0}

        for this_draw in all_draws:
            drawn = this_draw[1:].split(', ')
            for each_drawn in drawn:
                tmp = each_drawn.split(' ')
                value = int(tmp[0])
                color = tmp[1]
                if value > min_color[color]:
                    min_color[color] = value
                    
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
