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
    







