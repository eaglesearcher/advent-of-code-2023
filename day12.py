# import numpy as np
import file_io as fio
# import algo_util as alg

day_num = 12
input_type = 1 # 0 = test, 1 = input

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

def haswildcard(spring):
    return '?' in spring

def replace_next_q(spring):
    idx = spring.index('?')
    option1 = spring[:idx]+'#'+spring[idx+1:]
    option2 = spring[:idx]+'.'+spring[idx+1:]
    return [option1, option2]

# recursive approach - faster
def parse_spring(spring, check, valid=[]):
    # print(spring, hashcheck(spring)[0], check[0])
    checksum = sum(check)
    if haswildcard(spring):
        lb,ub = hashcount(spring)
        if lb <= checksum <= ub:
            # test_check = hashcheck(spring)
            # if test_check[0] <= check[0]:
            options = replace_next_q(spring)
            for test in options:
                valid = parse_spring(test,check, valid)
    elif hashcheck(spring)==check:
        valid.append(spring)
    
    return valid

# # queue approach - a bit slower?
# def parse_spring_queue(spring, check):
#     valid = []
#     checksum = sum(check)
#     to_be_evaluated = [spring]
#     while(len(to_be_evaluated) > 0):
#         next_branch = to_be_evaluated.pop()
#         options = replace_next_q(next_branch)
#         for test in options:
#             lb,ub = hashcount(test)
#             if haswildcard(test) and lb <= checksum and ub >= checksum:
#                 to_be_evaluated.append(test)
#             if not haswildcard(test) and hashcheck(test) == check:
#                 valid.append(test)
#     return valid


def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---
    
    all_springs = [line.split()[0] for line in file_contents]
    all_hashes = [[int(i) for i in line.split()[1].split(',')] for line in file_contents]
    all_sum = [sum(i) for i in all_hashes]

    idx = 11
    spring = all_springs[idx]
    check = all_hashes[idx]
    
    valid = parse_spring(spring, check, [])

    print(spring)
    print(valid)
    print('# valid', len(valid))

    # new strategy --> divide spring into tokens
    # subproblem search over tokens to build combos
    # total = sum (branches)
    # total_branch = product of subtokens
    #
    # avoids counting every subtoken

    # tokenize spring *as is* -> these are "hard" boundaries
    x = spring.split('.')
    while '' in x:
        x.remove('')
    
    print(x, len(x))


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
