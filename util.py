from os.path import exists


def read_input(day_num,in_type):

    if in_type == 0:
        test_str = "test"
    else:
        test_str = "input"

    file_name = "D:/Data/AOC23/day" + str(day_num) + "_" + test_str + ".txt"

    file_exists = exists(file_name)

    file_contents = []
    if file_exists:
        file_container = open(file_name)
        file_contents = file_container.read()
        file_container.close()
    else:
        print("File not found!")

    return file_contents
