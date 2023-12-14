# import numpy as np
import file_io as fio
# import algo_util as alg
import re

day_num = 12
input_type = 1 # 0 = test, 1 = input

def get_combos(spring, num):
    # assume that only one sequence considered for this chunk
    # assume the sequence is preceded by .
    # the input spring should never have a . in it, only # or ?
    
    # go through a few shortcuts to avoid actual counting
    
    if len(spring) == num:
        # only one possibility (valid due to [#?] assumption
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
    print('PROBLEMS')
    return None



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
    # if not haswildcard(spring): # exact hash
    x = [len(i) for i in spring.split('.')]
    while 0 in x:
        x.remove(0)
    # else:
    #     teststr = ''
    #     for c in spring:
    #         if c == '?':
    #             teststr += '.'
    #         else:
    #             teststr += c
    #     x = [len(i) for i in teststr.split('.')]
    #     while 0 in x:
    #         x.remove(0)
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
    option1 = spring[:idx]+'#'+spring[idx+1:]
    option2 = spring[:idx]+'.'+spring[idx+1:]
    return [option1, option2]

# recursive approach - faster
def parse_spring(spring, check, valid=[]):
    # print(spring, hashcheck(spring)[0], check[0], hash_scan(spring))
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

# # queue approach - a bit slower?
def parse_spring_queue(spring, check):
    valid = []
    checksum = sum(check)
    to_be_evaluated = [spring]
    while(len(to_be_evaluated) > 0):
        next_branch = to_be_evaluated.pop()
        options = replace_next_q(next_branch)
        for test in options:
            lb,ub = hashcount(test)
            if haswildcard(test) and lb <= checksum and ub >= checksum:
                to_be_evaluated.append(test)
            if not haswildcard(test) and hashcheck(test) == check:
                valid.append(test)
    return valid


def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---
    
    all_springs = [line.split()[0] for line in file_contents]
    all_hashes = [[int(i) for i in line.split()[1].split(',')] for line in file_contents]
    all_sum = [sum(i) for i in all_hashes]


    # full input 3 is the nasty one ??????#????????
    idx = 3
    spring = all_springs[idx]
    check = all_hashes[idx]
    
    # long_spring = ''
    # long_check = []
    # for i in range(5):
    #     long_spring += ('?' + spring)
    #     for j in check:
    #         long_check.append(j)
    
    
    # spring = long_spring[1:]
    # check = long_check
    
    valid = parse_spring(spring, check, [])

    print(spring)
    print(check)
    # print(valid)
    print('# valid', len(valid))
    
    test_check = check
    
    # print(sorted(test_check, reverse=True))
    spring = spring+spring
    check = [7,2,7,2]
    test_check = check[0]
    for i in range(len(spring)):
        # since we are exactly matching the test sequence
        # ASSUMES immediate prior and after are .
        preceding = spring[:i]
        match = spring[i:i+test_check+1]
        post = spring[i+test_check+1:]
        
        if '#' in preceding:
            # this sequence can't after another
            break
        if len(match) < test_check:
            # rolling over the ends of the string
            break
        if len(post) < sum(check[1:])+len(check[1:]):
            # remaining string not long enough to accomodate remaining sequences
            break
        # print(preceding, match, post)
    
    
    test_spring = '????#???'
    checknum = 3
    x = get_combos(test_spring, checknum)
    print(test_spring, x)
    
    
    
    
    # new_spring = spring
    # test_spring = new_spring
    # for value in sorted(test_check, reverse=True):
    #     x = re.search('[.?]'+'#'*value+'[.?]',test_spring)
    #     if x:
    #         a = x.span()[0]
    #         b = x.span()[1]
            
    #         if x.group()[0] == '?':
    #             new_spring = new_spring[:a] + '.'+ new_spring[a+1:]
            
    #         if x.group()[-1] == '?':
    #             new_spring = new_spring[:b-1] + '.'+ new_spring[b:]
        
    #         test_spring = test_spring[:a] + '.'*(b-a) + test_spring[b:]
    #     else:
    #         break
    
    # print(new_spring)
    # print(test_spring)
        
    
    
    # # test = max(test_check)
    # # x = contains_pattern(spring, test)
    # test = 4
    # spring2 = spring
    
    # x = re.search('[.?]'+'#'*test+'[.?]',spring)
    # if x:
    #     # print(x.start(), x.span())
    #     x1 = x.span()[0]
    #     x2 = x.span()[1]
    #     print(spring[x1:x2])
    #     print(x.group())
        
    #     if x.group()[0] == '?':
    #         spring2 = spring2[:x1] + '.'+ spring2[x1+1:]
        
    #     if x.group()[-1] == '?':
    #         spring2 = spring2[:x2-1] + '.'+ spring2[x2:]
        
    #     print(spring2)
    
    
    
    
    
    # to_be_eval = [(spring,check,spring)]
    
    # next_eval = to_be_eval.pop()
    # current_spring = next_eval[0]
    # current_check = next_eval[1]
    
    # # x = pattern_match(spring, check)
    # # print(x)
    
    # for start_idx in range(len(spring)):
    #     x = pattern_match(spring[start_idx:], check)
    #     print(spring[start_idx],x)
    
    
    # x = pattern_match(spring[1:], check)
    # print(x)
    
    
    

    # new strategy --> divide spring into tokens
    # subproblem search over tokens to build combos
    # total = sum (branches)
    # total_branch = product of subtokens
    #
    # avoids counting every subtoken

    # # # tokenize spring *as is* -> these are "hard" boundaries
    # x = spring.split('.')
    # while '' in x:
    #     x.remove('')
    
    # print(x, len(x))

    # # 1:1 assignment of tokens
    # if len(x) == len(check):
    #     y = 1    
    #     for idx, token in enumerate(x):
    #         print(token, check[idx])
    #         valid_list = parse_spring(token, [check[idx]],[])
    #         print(valid_list)
    #         y *= len(valid_list)
    #     print('short', y)
    # # token matching
    # else:
    #     pass


    
    



    valid_sum = 0
    # for idx, spring in enumerate(all_springs):
    #     check = all_hashes[idx]

    #     # valid = parse_spring_queue(spring, check)
    #     # valid_sum += len(valid)
    #     # print(len(valid))

    #     valid = parse_spring(spring, check, [])
    #     # print(valid)
    #     valid_sum += len(valid)
    #     # print(len(valid))
    
    
    # ----------------------
    
    part1 = valid_sum
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
