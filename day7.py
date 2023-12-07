import numpy as np
import file_io as fio
import algo_util as alg

day_num = 7
input_type = 0 # 0 = test, 1 = input

def get_hand_type(hand):
    
    # 5K:7, 4K:6, FH:5, 3K:4, 2P:3, 1P:2, High:1
    cards = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
    card_dict = {}
    for card in cards:
        card_dict[card] = 0
        
    for card in hand:
        card_dict[card] += 1
        
    pair_3 = 0
    pair_2 = 0
    
    for card in card_dict:
        if card_dict[card] == 5:
            hand_type = 7 # 5 of a kind
            break
        if card_dict[card] == 4:
            hand_type = 6 # 4 of a kind
            break
        if card_dict[card] == 3:
            pair_3 = 1
        if card_dict[card] == 2:
            pair_2+= 1
    if pair_3 == 1:
        if pair_2 == 1:
            hand_type = 5 # full house
        else:
            hand_type = 4 # three of a kind
    elif pair_2 == 2:
        hand_type = 3 # two pair
    elif pair_2 == 1: # one pair
        hand_type = 2
    else:
        hand_type = 1
    
    return hand_type



# def compare_hands(hand_1, hand_2):
    
    
    
    
    
    





def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---
    hands = [i.split()[0] for i in file_contents]
    bids = [i.split()[1] for i in file_contents]
    
    card_dict = {}
    for idx, bid in enumerate(bids):
        card_dict[hands[idx]] = int(bid)
    
    print(card_dict)
    # print(bids)


    # ----------------------
    
    part1 = 0
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
