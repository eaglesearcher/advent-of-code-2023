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
    max_cards = len(file_contents)
    
    # part 1: sum all winnings
    total_winnings = 0
    
    # part 2: count all the cards
    # starts with 1 of every card
    count_cards = [1 for i in range(max_cards)]
    
    # loop through every game
    for idx, card in enumerate(file_contents):
        tmp = card.split(':')[1].split('|')
        winning_nums = set(tmp[0].split(' '))
        winning_nums.remove('') # remove double-space clutter
        card_nums = set(tmp[1].split(' '))
        card_nums.remove('')
        
        # count wins on the card
        count_wins = 0
        for num in winning_nums:
            # compare winning nums to card
            if num in card_nums:
                count_wins += 1
                
        # score processing
        if count_wins > 0: # only score if wins > 0
            # part 1: each win doubles the value of the card
            total_winnings += 2**(count_wins - 1)
            
            # part 2: each win sequentially awards the next card
            for inc in range(count_wins):
                new_card_idx = idx + inc + 1
                if new_card_idx < max_cards:
                    # we may have multiple copies of this card
                    # (won from previous cards)
                    # this awards multiple copies of following cards
                    count_cards[new_card_idx] += count_cards[idx]
    
    # ----------------------
    
    part1 = total_winnings
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
