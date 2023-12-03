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
    word_dict = {
        'zero' : 0,
        'one' : 1,
        'two' : 2,
        'three' : 3,
        'four' : 4,
        'five' : 5,
        'six' : 6,
        'seven' : 7,
        'eight' : 8,
        'nine' : 9
        }
    if token in word_dict:
        value = word_dict[token]
    else:
        # if no match return token
        value = token
    return value
    
def num_to_word(value):
    num_dict = {
        0 : 'zero',
        1 : 'one',
        2 : 'two',
        3 : 'three',
        4 : 'four',
        5 : 'five',
        6 : 'six',
        7 : 'seven',
        8 : 'eight',
        9 : 'nine'
        }
    if value in num_dict:
        token = num_dict[value]
    else:
        # if no match, passes the input back as a string
        token = str(value)
    return token

def get_adj_cells_2d(grid, row_idx, col_idx):
    # checks if the calling cell is on an edge
    # adj_dict & adj_ref returns None for out-of-bounds cells
    
    adj_cells = [[None,None,None],[None,None,None],[None,None,None]]
    # above left, above, above right
    # left, This, right
    # below left, below, below right

    max_rows = len(grid)
    max_cols = len(grid[row_idx])
    
    # loop through neighbors
    shift = [-1, 0, 1]
    for row_shift in shift:
        new_row = row_idx + row_shift
        if new_row >= 0 and new_row <= max_rows-1:
            for col_shift in shift:
                new_col = col_idx + col_shift
                if new_col >= 0 and new_col <= max_cols-1:
                    adj_cells[row_shift+1][col_shift+1] = grid[new_row][new_col]

    # convert to easy dicts
    adj_dict = {
                'UL':adj_cells[0][0], 'U':adj_cells[0][1], 'UR':adj_cells[0][2],
                'L':adj_cells[1][0], 'C': adj_cells[1][1], 'R':adj_cells[1][2],
                'DL':adj_cells[2][0], 'D':adj_cells[2][1], 'DR':adj_cells[2][2]
                }
    
    adj_ref = {
                'UL':(row_idx - 1, col_idx - 1),
                'U':(row_idx - 1, col_idx),
                'UR':(row_idx - 1, col_idx + 1),
                'L':(row_idx, col_idx - 1),
                'C':(row_idx, col_idx),
                'R':(row_idx, col_idx + 1),
                'DL':(row_idx + 1, col_idx - 1),
                'D':(row_idx + 1, col_idx),
                'DR':(row_idx + 1, col_idx + 1),
                }
    
    # remove out of bounds by comparing ot adj_dict
    key_list = ['UL', 'U', 'UR', 'L', 'C', 'R', 'DL', 'D', 'DR']
    for key in key_list:
        if not adj_dict[key]:
            adj_ref[key] = None
    
    
    return adj_dict, adj_ref



