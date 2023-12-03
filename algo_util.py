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
    
    adj_cells = [[None,None,None],[None,None,None],[None,None,None]]
    adj_dict = {'L':None, 'C': None, 'R':None,
                'UL':None, 'U':None, 'UR':None,
                'DL':None,'D':None,'DR':None}
    adj_ref = {'L':None, 'C': None, 'R':None,
                'UL':None, 'U':None, 'UR':None,
                'DL':None,'D':None,'DR':None}
    # above left, above, above right
    # left, This, right
    # below left, below, below right
    
    # checks if the calling cell is on an edge
    # adj_dict & adj_ref returns None for out-of-bounds cells

    max_rows = len(grid)
    max_cols = len(grid[row_idx])
    
    if col_idx > 0:
        adj_cells[1][0] = grid[row_idx][col_idx - 1]
        adj_dict['L'] = grid[row_idx][col_idx - 1]
        adj_ref['L'] = (row_idx, col_idx - 1)
    
    if col_idx < max_rows - 1:
        adj_cells[1][2] = grid[row_idx][col_idx + 1]
        adj_dict['R'] = grid[row_idx][col_idx + 1]
        adj_ref['R'] = (row_idx, col_idx + 1)
    
    if row_idx > 0: # not on the first row
        adj_cells[0][1] = grid[row_idx - 1][col_idx]
        adj_dict['U'] = grid[row_idx - 1][col_idx]
        adj_ref['U'] = (row_idx - 1, col_idx)
        
        if col_idx > 0: # not on the first col
            adj_cells[0][0] = grid[row_idx - 1][col_idx - 1]
            adj_dict['UL'] = grid[row_idx - 1][col_idx - 1]
            adj_ref['UL'] = (row_idx - 1, col_idx - 1)
        
        if col_idx < max_cols - 1:
            adj_cells[0][2] = grid[row_idx - 1][col_idx + 1]
            adj_dict['UR'] = grid[row_idx - 1][col_idx + 1]
            adj_ref['UR'] = (row_idx - 1, col_idx + 1)

    if row_idx < max_rows - 1: # not on the last row
        adj_cells[2][1] = grid[row_idx + 1][col_idx]
        adj_dict['D'] =  grid[row_idx + 1][col_idx]
        adj_ref['D'] = (row_idx + 1, col_idx)
        
        if col_idx > 0: # not on the first col
            adj_cells[2][0] = grid[row_idx + 1][col_idx - 1]
            adj_dict['DL'] = grid[row_idx + 1][col_idx - 1]
            adj_ref['DL'] = (row_idx + 1, col_idx - 1)
        
        if col_idx < max_cols - 1:
            adj_cells[2][2] = grid[row_idx + 1][col_idx + 1]
            adj_dict['DR'] = grid[row_idx + 1][col_idx + 1]
            adj_ref['DR'] = (row_idx + 1, col_idx + 1)
    
    return adj_dict, adj_ref



