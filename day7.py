import numpy as np
import file_io as fio
import algo_util as alg
from operator import itemgetter

day_num = 7
input_type = 1 # 0 = test, 1 = input

def get_hand_type(hand):
    
    # 5K:7, 4K:6, FH:5, 3K:4, 2P:3, 1P:2, High:1
    card_dict = {}
        
    for card in hand:
        if card in card_dict:
            card_dict[card] += 1
        else:
            card_dict[card] = 1
            
    counts = sorted(card_dict.values(), reverse = True)
    
    if counts[0] == 5: # five of a kind
        hand_type = 7
    elif counts[0] == 4: # four of a kind
        hand_type = 6
    elif counts[0] == 3 and counts[1] == 2: # full house
        hand_type = 5
    elif counts[0] == 3: # three of a kind
        hand_type = 4
    elif counts[0] == 2 and counts[1] == 2: # two pair
        hand_type = 3
    elif counts[0] == 2: # one pair
        hand_type = 2
    else:
        hand_type = 1
    
    return hand_type

def init_card_values():
    cards = 'AKQJT98765432'
    card_value = {}
    for idx, card in enumerate(cards):
        card_value[card] = 13-idx
    return card_value

def tokenize(hand, card_values):
    values = [get_hand_type(hand)]
    for card in hand:
        values.append(card_values[card])
    return values


def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---
    card_values = init_card_values()
    
    
    hands = [i.split()[0] for i in file_contents]
    bids = [i.split()[1] for i in file_contents]
    
    card_dict = {}
    for idx, hand in enumerate(hands):
        card_dict[hand] = int(bids[idx])
    
    # pattern: decorate, sort, undecorate
    # print(card_dict)
    decorated = [(tokenize(hand, card_values), hand) for hand in card_dict.keys()]
    decorated.sort()
    sorted_hands = [i[1] for i in decorated]
    
    sum_value = 0
    for idx, hand in enumerate(sorted_hands):
        # print(hand, card_dict[hand])
        sum_value += card_dict[hand]*(idx+1)
    
    # value = [card_dict[i]*(idx+1) for idx,i in enumerate(sorted_hands)]
    # sum_value = sum(value)


    

    # ----------------------
    
    part1 = sum_value
    part2 = 0


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
