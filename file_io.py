from os.path import exists
from queue import PriorityQueue
import requests

AOC_YEAR = 2022

def read_input(day,in_type = 1):

    # switch between input (1) & test case (0)
    if in_type == 0:
        test_str = "test"
    else:
        test_str = "input"

    file_name = f'.\input\day{day}_{test_str}.txt'
    file_exists = exists(file_name)

    if file_exists:
        file_container = open(file_name)
        file_contents = file_container.read()
        file_container.close()
    else:
        print('File not found, pulling input')
        pull_input(day)
        file_exists = exists(file_name)
        if file_exists:
            file_container = open(file_name)
            file_contents = file_container.read()
            file_container.close()
        else:
            print('Unable to pull file')
            file_contents = None

    return file_contents

def pull_input(day = 1, year = AOC_YEAR):
    
    # get your session auth cookie and put it in a file
    # file is not pushed to git for security!
    file_container = open('.\input\cookie.txt', 'r')
    session = file_container.read()
    file_container.close()

    # build http request
    cookies = {'session': session}
    response = requests.get(
        f'https://adventofcode.com/{year}/day/{day}/input',
        cookies=cookies)
    # print(response.text)

    # dump the response into a file
    file_container = open(f'.\input\day{day}_input.txt', 'w')
    file_container.write(response.text)
    file_container.close()
    
    # convenience: create dumping spot for test input
    # don't overwrite if it exists!
    file_exists = exists(f'.\input\day{day}_test.txt')
    if not file_exists:
        print('Creating blank test file')
        file_container = open(f'.\input\day{day}_test.txt', 'w')
        file_container.write('')
        file_container.close()
    
    return

def new_day(day):
    # don't clone if the day exists!
    file_exists = exists(f'day{day}.py')
    if file_exists:
        print('Day already exists!')
        return

    # open the template
    file_container = open('dayX.py', 'r')
    contents = file_container.read()
    file_container.close()

    # update the day number in the template
    new_contents = contents.split('\n')
    new_contents[4] = f'day_num = {day}'
    
    # rejoin the template and write to file
    # print('\n'.join(new_contents))
    file_container = open(f'day{day}.py', 'w')
    file_container.write('\n'.join(new_contents))
    file_container.close()

    return
    




