from os.path import exists
import requests

AOC_YEAR = 2023

def read_input(day,in_type = 1):

    # switch between input (1) & test case (0)
    if in_type == 0:
        test_str = "test"
    else:
        test_str = "input"

    file_name = f'.\input\day{day}_{test_str}.txt'
    file_contents = basic_read(file_name)
    
    # if a file exists, it may be the placeholder --> attempt to re-pull
    # if there is no file, this should skip
    if is_placeholder_text(file_contents):
        print('Old placeholder, attempting new pull')
        pull_input(day)
        file_contents = basic_read(file_name)
    
    # if there is no file, attempt to pull a new one
    if file_contents is None:
        print('File not found, pulling input data')
        pull_input(day)
        file_contents = basic_read(file_name)
        
    # at this point a file *should* exist and
    # if we get the placeholder, we KNOW it was a fresh pull
    # if we get the placeholder, send None so that the caller exits properly
    if is_placeholder_text(file_contents):
        file_contents = None
    
    if file_contents:
        # files are always a series of lines
        # there is always a blank line at the end
        file_contents = file_contents.split('\n')
        file_contents = file_contents[0:-1] # trim the ending newline
    
    return file_contents


def basic_read(file_name):
    file_contents = None
    if exists(file_name):
        with open(file_name) as file_container:
            file_contents = file_container.read()
    return file_contents


def is_placeholder_text(file_text):
    if file_text == None:
        return False
    test = file_text.split(' ')
    if test[0] == "Please":
        if test[1] == "don't":
            if test[2] == 'repeatedly':
                return True
    return False


def pull_input(day = 1, year = AOC_YEAR):
    
    # get your session auth cookie and put it in a file
    # file is not pushed to git for security!
    with open('.\input\cookie.txt', 'r') as file_container:
        session = file_container.read()

    # build http request
    cookies = {'session': session}
    response = requests.get(
        f'https://adventofcode.com/{year}/day/{day}/input',
        cookies=cookies)
    # print(response.text)

    # dump the response into a file
    with open(f'.\input\day{day}_input.txt', 'w') as file_container:
        file_container.write(response.text)
    
    # convenience: create dumping spot for test input
    # don't overwrite if it exists!
    if not exists(f'.\input\day{day}_test.txt'):
        print('Creating blank test file')
        with open(f'.\input\day{day}_test.txt', 'w') as file_container:
            file_container.write('')
    
    return


def new_day(day):
    # don't clone if the day exists!
    if exists(f'day{day}.py'):
        print('Day already exists!')
        return

    
    if not exists('dayX.py'):
        print('dayX template missing!')
        return
    
    # open the template
    with open('dayX.py', 'r') as file_container:
        contents = file_container.read()

    # update the day number in the template
    new_contents = contents.split('\n')
    new_contents[4] = f'day_num = {day}'
    
    # rejoin the template and write to file
    with open(f'day{day}.py', 'w') as file_container:
        file_container.write('\n'.join(new_contents))
 
    return
    




