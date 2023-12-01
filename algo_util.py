from queue import PriorityQueue





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
    

def word_to_num(token):
    value = token
    if token == 'zero':
        value = 0
    elif token == 'one':
        value = 1
    elif token == 'two':
        value = 2
    elif token == 'three':
        value = 3
    elif token == 'four':
        value = 4
    elif token == 'five':
        value = 5
    elif token == 'six':
        value = 6
    elif token == 'seven':
        value = 7
    elif token == 'eight':
        value = 8
    elif token == 'nine':
        value = 9
    # if no match, passes the input back
    return value

def num_to_word(value):
    token = str(value)
    if value == 0:
        token = 'zero'
    elif value == 1:
        token = 'one'
    elif value == 2:
        token = 'two'
    elif value == 3:
        token = 'three'
    elif value == 4:
        token = 'four'
    elif value == 5:
        token = 'five'
    elif value == 6:
        token = 'six'
    elif value == 7:
        token = 'seven'
    elif value == 8:
        token = 'eight'
    elif value == 9:
        token = 'nine'
    # if no match, passes the input back as a string
    return token





