import numpy as np
import file_io as fio
import algo_util as alg
from operator import itemgetter

day_num = 7
input_type = 1 # 0 = test, 1 = input

def get_hand_type(hand, part = 1):
    
    # 5K:7, 4K:6, FH:5, 3K:4, 2P:3, 1P:2, High:1
    hand_counts = {}
        
    # count each type of card in hand
    for card in hand:
        if card in hand_counts:
            hand_counts[card] += 1
        else:
            hand_counts[card] = 1
    
    counts = sorted(hand_counts.values(), reverse = True)
    
    if part == 2 and 'J' in hand_counts:
        # remove jokers, check edge case, resort and add to best
        jokers = hand_counts.pop('J')
        
        if jokers == 5: # covers the JJJJJ case (no other cards)
            hand_type = 7
        else:
            counts = sorted(hand_counts.values(), reverse = True)
            counts[0] += jokers # jokers always modify the best 

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

def init_card_values(part = 1):
    if part == 2: # J = jokers worth less
        cards = 'AKQT98765432J'
    else: # default to part 1 (J is jack)
        cards = 'AKQJT98765432'
    card_value = {}
    for idx, card in enumerate(cards):
        card_value[card] = 13-idx
    return card_value

def tokenize(hand, card_values, part = 1):
    values = [get_hand_type(hand, part)]
    for card in hand:
        values.append(card_values[card])
    return values


def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---
    card_values = init_card_values(part = 1)
    card_values2 = init_card_values(part = 2)
    
    hands_raw = [i.split()[0] for i in file_contents]
    bids_raw = [i.split()[1] for i in file_contents]
    
    # sorting pattern: decorate, sort, undecorate
    # separate trackers for p1 and p2
    bids = {}
    decorated = []
    decorated2 = []
    for idx, hand in enumerate(hands_raw):
        bids[hand] = int(bids_raw[idx])
        decorated.append((tokenize(hand, card_values, part = 1), hand))
        decorated2.append((tokenize(hand, card_values2, part = 2), hand))
    
    decorated.sort()
    decorated2.sort()
    
    sorted_hands = [i[1] for i in decorated]
    sorted_hands2 = [i[1] for i in decorated2]
    
    value = [bids[i]*(idx+1) for idx,i in enumerate(sorted_hands)]
    sum_value_p1 = sum(value)

    value2 = [bids[i]*(idx+1) for idx,i in enumerate(sorted_hands2)]
    sum_value_p2 = sum(value2)
    
    # sum_value = 0
    # for idx, hand in enumerate(sorted_hands):
    #     # print(hand, card_dict[hand])
    #     sum_value += bids[hand]*(idx+1)
    
    # ----------------------
    
    part1 = sum_value_p1
    part2 = sum_value_p2


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
