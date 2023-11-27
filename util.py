from os.path import exists
from queue import PriorityQueue


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


class a_star():
    # the priorityQueue object is a tuple of (heuristic, ID, state)
    # unique IDs allow debugging and tie-breaks
    # see Day16 2022
    def __init__(self):
        self.prospects = PriorityQueue()
        self.next_id = 0
        return
    
    def add_child(self, heuristic, state):
        # assumes "smaller" is better (distance)
        # PQ gets the highest value, so add heuristic as negative
        self.prospects.put((-heuristic, self.next_id, state))
        self.next_id += 1
        return
    
    def get_best(self):
        return self.prospects.get()
    
    def get_children(self, state, child_func):
        return child_func(state)
    
    def is_end(self, state, end_func):
        return end_func(state)
    
    def pseudocode(self):
        pass
        # astar init
        # put init state / start
        # loop
        #   pop the queue (get_best)
        #   check if winner (is_end)
        #   generate new state (get_children)
        #       add each to queue (add_child)
        # if no winner, print debug (top 2 remaining in queue)
    







