# import numpy as np
import file_io as fio
# import algo_util as alg
import re

day_num = 12
input_type = 1 # 0 = test, 1 = input

cheater_dict = {}


def get_combos(spring, num):
    # assume that only one sequence considered for this chunk
    # assume the sequence is preceded by .
    # the input spring should never have a . in it, only # or ?
    
    # go through a few shortcuts to avoid actual counting
    
    if len(spring) == num or num == 0:
        # only one possibility (valid due to [#?] assumption
        # also if num = 0, they must all be [.]
        return 1

    if '#' not in spring:
        # all wildcards -> maximum number of combos
        return len(spring)-num+1

    x =  re.search('#'*num, spring)
    if x:
        # hard match, there can be only 1
        return 1
    
    # do the slide, starting num spots back from the first #
    x = re.search('#', spring)
    first_idx = max(x.start() - num + 1,0)
    
    count = 0
    for i in range(first_idx, len(spring)):
        pre = spring[:i]
        match = spring[i:i+num]
        post = spring[i+num:]
        # print(i, num, 'first', spring[:i], 'match', spring[i:i+num],'post', spring[i+num:])
        
        if not '#' in pre and not '#' in post and len(match) == num:
            # all wildcard case already resolved, so there is at least 1 #
            # if that # shows up in preceding or post, that won't work            
            count += 1
    if count > 0:
        return count

    # I don't know how you got here
    # print('PROBLEMS')
    return 0



def pattern_match(spring, check):
    # assume that spring[0] is # --> it automatically starts the next check sequence
    # assume that the index before spring[0] is either begining of string or [.]
    # check[0] -> [N #][1 .]
    
    # not enough chars left to even fit check!
    if len(spring) < (sum(check)+len(check)-1):
        print('check 1')
        return False
    
    # not enough chars left after check[0] to fit either
    print(len(check))
    print((spring[check[0]+2:]))
    print((sum(check[1:])+len(check)-2))
    if len(check) > 1 and len(spring[check[0]+2:]) < (sum(check[1:])+len(check)-2):
        print('check 2')
        return False
    
    # if there is a [.] in the first N chars, this string doesn't match check[0]
    for c in spring[:(check[0]+1)]:
        if c == '.':
            print('check 3')
            return False
    
    # if string keeps going, and next char is a #, then this isn't a valid start string
    if len(spring) > check[0] and spring[check[0]+1] == '#':
        print('check 4')
        return False
    
    return True
    
def contains_pattern(spring, checknum):
    test_str = spring.replace('?','.').split('.')
    test = [len(i) for i in test_str]
    return checknum in test

def hashcheck(spring):
    # assume all ? are #
    x = [len(i) for i in spring.split('.')]
    while 0 in x:
        x.remove(0)
    return x

def hashcount(spring):
    exact = sum([c=='#' for c in spring])
    wildcards = sum([c=='?' for c in spring])
    lb = exact
    ub = exact+wildcards
    return lb, ub

def hash_scan(spring):
    check = []
    counter = 0
    for c in spring:
        if c == '.':
            check.append(counter)
            counter = 0
        elif c == '#':
            counter += 1
        elif c == '?':
            check.append(counter)
            break
    while 0 in check:
        check.remove(0)
    return check

def haswildcard(spring):
    return '?' in spring

def replace_next_q(spring):
    idx = spring.index('?')
    option1 = spring[:idx]+'.'+spring[idx+1:]
    option2 = spring[:idx]+'#'+spring[idx+1:]
    return [option1, option2]

# recursive approach - faster
def parse_spring(spring, check, valid=[]):
    checksum = sum(check)
    if haswildcard(spring):
        lb,ub = hashcount(spring)
        if lb <= checksum <= ub:
            test_check = hash_scan(spring)
            for idx, sub_check in enumerate(test_check):
                if idx < len(check) and sub_check > check[idx]:
                    return valid
            options = replace_next_q(spring)
            for test in options:
                valid = parse_spring(test,check, valid)
    elif hashcheck(spring)==check:
        valid.append(spring)
    
    return valid

def first_dot(spring):
    x = re.search('[.]', spring)
    if x:
        return x.start()
    return None

def first_hash(spring):
    x = re.search('[#]', spring)
    if x:
        return x.start()
    return None


def trim_leading_dots(spring):
    x = re.search('[?|#]', spring)
    if x:
        return spring[x.start():]
    return spring


def check_len_verify(spring, check):
    # must be at least enough chars left for check with joining [.]
    current_check_minlen = sum(check) + len(check) - 1
    check_len = current_check_minlen <= len(spring)
    
    # count the #? in the string
    current_lb, current_ub = hashcount(spring)            
    
    # sum(check) must also be less than the max possible hashes
    check_ub = sum(check) <= current_ub
    
    # count hashes, sum(check) must be at least greater than the min. hashes
    check_lb = sum(check) >= current_lb

    return check_len, check_lb, check_ub


def spring_search(spring, check):
    # print('New search', spring, check)
    
    if len(check) == 0:
        if '#' in spring: # this case never triggers? -- good?
            return 0
        else: # this one does -> empty check with (non-#) string remaining
            return 1
    
    # dict hash short-circuit
    cheater_key = (spring, str(check))
    if cheater_key in cheater_dict:
        count = cheater_dict[cheater_key]
        return count

    if '.' in spring: # dots exist in input, so we can break it up easily
        # iterate through what checks fit in the first segment
        max_len = first_dot(spring)    
        spring_part = spring[:max_len]
        remaining = spring[max_len+1:] # skip the dot
        
        sum_valid = 0
        for i in range(len(check)+1):
            current_check = check[:i]
            future_check = check[i:]
            
            # minor efficiency short-circuit
            if future_check == [] and '#' in remaining:
                break
            
            # do short-circuit length checks on current/future check
            check_len_current, check_lb_current, check_ub_current = check_len_verify(spring_part, current_check)
            
            # if not check_len_current or not check_lb_current or not check_ub_current:
            #     continue
            
            # current_check is getting larger relative to current spring
            if not check_len_current or not check_ub_current:
                break
            if not check_lb_current:
                continue
            
            check_len_future, check_lb_future, check_ub_future = check_len_verify(remaining, future_check)
            
            # if not check_len or not check_lb or not check_ub:
            #     continue
            
            # future_check is getting smaller relative to remaining
            if not check_lb_future:
                break
            if not check_len_future or not check_ub_future:
                continue

            # find the number of combos for the current sequence
            cheater_key = (spring_part, str(current_check))
            if cheater_key in cheater_dict:
                num_combos = cheater_dict[cheater_key]
            else:
                num_combos = spring_search(spring_part, current_check)
                cheater_dict[cheater_key] = num_combos
            
            if future_check == []:
                sum_valid += num_combos*1
                continue
            else:
                new_spring = trim_leading_dots(remaining)
                cheater_key = (new_spring, str(future_check))
                if cheater_key in cheater_dict:
                    recursed_combos = cheater_dict[cheater_key]
                else:
                    recursed_combos = spring_search(new_spring, future_check)
                    cheater_dict[cheater_key] = recursed_combos
                
                sum_valid += num_combos*recursed_combos
                continue
                
    else: # no dots in the string!
        # iterate through segments that work for the first check
        
        # can use a very quick method for len(check) = 1
        if len(check) == 1:
            sum_valid = get_combos(spring, check[0])
            cheater_key = (spring, str(check))
            cheater_dict[cheater_key] = sum_valid
            return sum_valid
        
        # # leading check trim trick
        # new_spring = ''
        # while new_spring != spring:
        #     new_spring, check = leading_check_trick(spring, check)
        #     spring = new_spring
        #     if check == []: # it's possible we trimmed off all the checks
        #         # doesn't seem to ever occur
        #         # print('overtrimmed??')
        #         return 1 
        
        # we can't break the input into smaller parts, so we need to get smarter
        # start by doing standard checks
        check_len, check_lb, check_ub = check_len_verify(spring, check)
        
        # short-circuit no valid combos
        if not check_len or not check_lb or not check_ub:
            return 0

        # it's possible we trimmed off all but 1 check
        # in this case, we're better off recursing to avoid the slog below
        # it actually just takes us a few lines up in the "no dot" case
        if len(check) == 1:
            sum_valid = spring_search(spring, check)
            return sum_valid

        current_check = check[0]
        future_check = check[1:]
        
        # this is really just an expanded case of get_combos()
        sum_valid = 0
        for i in range(len(spring)):
            pre = spring[:i]
            match = spring[i:i+current_check]
            remaining = spring[i+current_check:]
            
            # if we've passed a # or the current string isn't long enough
            # then we're done here            
            if '#' in pre or len(match) < current_check:
                break
            
            # if the next char is a #, guarenteed not to be a valid solution
            # check only matters if not end of string
            if len(remaining) > 0 and remaining[0] == '#':
                continue

            # "current" spring is automatically (no dots)
            # exactly 1 possibility for each step in this loop
            # but remaining still multiplies up as usual
            
            if len(remaining) > 1:
                remaining = remaining[1:]

                check_len, check_lb, check_ub = check_len_verify(remaining, future_check)

                # if not check_len or not check_lb or not check_ub:
                #     continue
                
                # remaining is getting smaller relative to future check
                if not check_lb:
                    continue
                if not check_len or not check_ub:
                    break
                
                cheater_key = (remaining, str(future_check))
                if cheater_key in cheater_dict:
                    count = cheater_dict[cheater_key]
                else:
                    count = spring_search(remaining, future_check)
                    cheater_dict[cheater_key] = count
                sum_valid += 1*count
                
            else:
                # only 1 item left in remaining and it must be a dot
                break
            
    # print('>Combos this level', sum_valid)
    # print()
    return sum_valid


def strip_biggest(spring, check):

    new_spring = spring
    check_dict = {}
    for value in check:
        if value in check_dict:
            check_dict[value] += 1
        else:
            check_dict[value] = 1
    # if there are N exact matches to the largest key
    # replace those matches with X's
    # otherwise, break, because we can't guarentee anything but the biggest
    for key in sorted(check_dict.keys(), reverse=True):
        match_str = '#{'+f'{key}'+'}'
        x = re.findall(match_str,new_spring)
        if x != None and len(x) == check_dict[key]:
            x = re.sub(match_str, 'X'*key, new_spring, check_dict[key])
            new_spring = x
        else:
            break
    # print(new_spring)
    # if we did any replacement, check if we can add [.]
    if 'X' in new_spring:
        new_spring2 = ''
        for idx,c in enumerate(new_spring):
            if c == '?':
                if (idx-1) >= 0 and new_spring[idx-1] == 'X':
                    new_spring2 += '.'
                elif idx+1 < len(new_spring) and new_spring[idx+1] == 'X':
                    new_spring2 += '.'
                else:
                    new_spring2 += '?'
            else:
                new_spring2 += c
        x = re.sub('X','#',new_spring2)
        new_spring = x

    return new_spring

def leading_check_trick(spring, check):
    # leading check trick
    # if first check appears entirely within the first check*2 chars
    # then all other [?] must be [.]
    # because you can't fit any other checks in there
    # there's only one solution in this case
    # so we return the simplified spring and check as equivalent
    # and if there's no match, then spring and check flow back out
    # works great for single # problems
    
    # this breaks if for "incorrect" scenarios
    # check that the next spot is a ? or . to be sure
    first_check = check[0]
    spring_lead = spring[:first_check*2]
    match_str = '#{'+f'{first_check}'+'}'
    
    x = re.search(match_str, spring_lead)
    # print(spring_lead, x.start(), x.end())
    if x != None and x.end() < len(spring) and spring[x.end()] != '#':
        spring = spring[x.end()+1:]
        check = check[1:]
    # print(new_spring, new_check)
    return spring, check


def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---
    
    all_springs = [line.split()[0] for line in file_contents]
    all_hashes = [[int(i) for i in line.split()[1].split(',')] for line in file_contents]
    # all_sum = [sum(i) for i in all_hashes]

    # original part 1 solution (with comparison to updated parsing)
    valid_sum_p1 = 0
    for idx, spring in enumerate(all_springs):
        check = all_hashes[idx]

        # valid = parse_spring_queue(spring, check)
        # valid_sum += len(valid)
        # print(len(valid))

        valid2 = spring_search(spring, check)
        valid_sum_p1 += valid2
        
        # # comparison / sanity check
        # valid = parse_spring(spring, check, [])
        # # valid_sum_p1 += len(valid)
        # if max(len(valid),valid2) - min(len(valid), valid2) > 0:
        #     print(idx, len(valid), valid2)
        
    
    # print(len(all_springs))
    valid_sum = 0
    # full input 3 is the nasty one ??????#????????
    for idx in range(len(all_springs)):
    # for idx in range(10,20):
    # for idx in range(210,220):
    # idx = 218
    # idx = 3
    # idx = 97
        # print(idx)
        spring = all_springs[idx]
        check = all_hashes[idx]
    
        # print(spring, check)
    
        new_spring = ''
        new_check = []
        
        count = 5
        for i in range(count):
            new_spring += '?' + spring
            new_check += check
    
        spring = new_spring[1:] # trim the leading ? (artifact of lazy join method)
        check = new_check
        
        spring = strip_biggest(spring, check)
        spring = trim_leading_dots(spring)
        
        valid_sum += spring_search(spring, check)
    
    # x = parse_spring(spring, check,[])
    # print('sanity', len(x))
    
    print('num keys', len(cheater_dict))



    # print('TESTING')
    
    # # spring = '???????????.???#????'
    # # check = [1, 1, 2, 3, 3]
    # spring = '???????????.???#???????????????.???#????'
    # check = [1, 1, 2, 3, 3, 1, 1, 2, 3, 3]
    # # spring = '???????????'
    # # check = [1]
    
    # print('input', spring, check)
    # x = spring_search(spring, check)
    # print(x)
    
    
    
    
    # ----------------------
    
    part1 = valid_sum_p1
    part2 = valid_sum


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
