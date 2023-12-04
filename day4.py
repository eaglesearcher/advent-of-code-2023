# import numpy as np
import file_io as fio
# import algo_util as alg

day_num = 4
input_type = 1 # 0 = test, 1 = input

def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---
    num_cards = len(file_contents)
    count_cards = [1 for i in range(num_cards)]
    
    winnings = 0
    for idx, card in enumerate(file_contents):
        tmp = card.split(':')[1].split('|')
        winning_nums = set(tmp[0].split(' '))
        winning_nums.remove('')
        card_nums = set(tmp[1].split(' '))
        card_nums.remove('')
        
        count_wins = 0
        for num in winning_nums:
            if num in card_nums:
                count_wins += 1
                # print(num)
        if count_wins > 0:
            winnings += 2**(count_wins - 1)
            for inc in range(count_wins):
                new_card_idx = idx + inc + 1
                if new_card_idx < num_cards:
                    count_cards[new_card_idx] += count_cards[idx]
    
        
    # ----------------------
    
    part1 = winnings
    part2 = sum(count_cards)


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
