import numpy as np
import file_io as fio
import algo_util as alg

day_num = 23
input_type = 1 # 0 = test, 1 = input


# node rules for p1 --> include slopes in neighbor considerations
class Node1():
    def __init__(self, name, coords, grid):
        self.name = name
        self.coords = coords    
        self.grid = grid

        self.value = grid[coords[0]][coords[1]]

        self.children = self.get_all_children()
        self.parents = []
        
        return

    def get_all_children(self):
        # node linking in the forward direction
        
        slopes = ['^','v','<','>']
        r = self.coords[0]
        c = self.coords[1]
        
        valid_dirs = check_slope(self.coords, self.grid)
        
        self.is_slope = False
        if self.value in slopes:
            self.is_slope = True
        
        adj_dict, adj_ref = alg.get_adj_cells_2d(self.grid, r,c)
        
        outbound = []
        
        neighbor_slope = False
        
        for d in valid_dirs:
            # print(d, adj_dict[d], adj_ref[d])
            if adj_dict[d] and adj_dict[d] != '#': # next step is .|<|>|^|v
                if adj_dict[d] in slopes:
                    neighbor_slope = True
                if not is_uphill(d,adj_dict[d]): # not going uphill (p1)
                    option = (adj_ref[d],1)
                    outbound.append(option)
        
        is_simple = False
        if not neighbor_slope and len(outbound) == 2:
            is_simple = True
    
        self.is_simple = is_simple
        
        return outbound
    
class Node2():
    def __init__(self, coords, grid):
        # self.name = name
        self.coords = coords    
        self.value = grid[coords[0]][coords[1]]

        self.children = self.get_all_children(grid)
        self.parents = []
        
        self.is_end = False
        self.bonus_len = 0
        
        start, end = get_start_end(grid)
        if self.coords == end:
            self.is_end = True
        
        
        return

    def get_all_children(self, grid):
        # node linking in the forward direction
        r = self.coords[0]
        c = self.coords[1]
        
        valid_dirs = ['U','D','L','R']
        
        # self.is_slope = False
        
        adj_dict, adj_ref = alg.get_adj_cells_2d(grid, r,c)
        
        outbound = []
        
        for d in valid_dirs:
            if adj_dict[d] and adj_dict[d] != '#': # next step is .|<|>|^|v
                option = (adj_ref[d],1)
                outbound.append(option)
        
        self.is_simple = (len(outbound) == 2)
        
        return outbound



def get_start_end(grid):
    line = grid[0]
    for idx, item in enumerate(line):
        if item == '.':
            start_c = idx
            break
    start_pos = (0, start_c)
    
    end_r = len(grid)-1
    line = grid[-1]
    for idx, item in enumerate(line):
        if item == '.':
            end_c = idx
            break
    end_pos = (end_r, end_c)
    
    return start_pos, end_pos

def check_slope(position, grid):
    valid_dirs = ['U','D','L','R']
    slopes = ['^','v','<','>']
    r = position[0]
    c = position[1]
    here = grid[r][c]
    if here in slopes:
        valid_dirs = [valid_dirs[slopes.index(here)]]
    return valid_dirs

def is_uphill(direction, target):
    valid_dirs = ['D','U','R','L']
    slopes = ['^','v','<','>']
    return target == slopes[valid_dirs.index(direction)]

def prune_simple(node, node_dict):
    
    if node.is_simple: # exactly 2 neighboring dots and no slopes
        # print('is simple')
        a = node.children[0]
        b = node.children[1]
        a_coords = a[0]
        a_steps = a[1]
        b_coords = b[0]
        b_steps = b[1]
        
        # goto a, replace *this* node with b
        # print(a, b)
        x = node_dict[a_coords]
        find = (node.coords, a_steps)
        replace = (b_coords, a_steps+b_steps)
        if find in x.children:
            x.children.remove(find)
            x.children.append(replace)
        x = node_dict[b_coords]
        find = (node.coords, b_steps)
        replace = (a_coords, a_steps+b_steps)
        if find in x.children:
            x.children.remove(find)
            x.children.append(replace)
    return

def match_parents(node, node_dict):
    # node linking in the reverse direction
    for child_coords, child_steps  in node.children:
        child_node = node_dict[child_coords]
        parent_state = (node.coords, child_steps)
        child_node.parents.append(parent_state)
    return
    
def prune_slope(node, node_dict):
    
    if node.is_slope: # uni-directional node
        # need to find parent
        
        print(node.coords, node.value)

        # print(node.parents) # only has 1 parent
        # print(node.children) # only has 1 child
        
        parent_link = node.parents[0]
        parent_coords = parent_link[0]
        parent_steps = parent_link[1]
        parent_node = node_dict[parent_coords]
        
        child_link = node.children[0]
        child_coords = child_link[0]
        child_steps = child_link[1]
        child_node = node_dict[child_coords]
        
        # remove the slope as a parent node to child and add slope's parent
        new_parent_link = (parent_coords, parent_steps+child_steps)
        old_parent_link = (node.coords, child_steps)
        
        if old_parent_link in child_node.parents:
            child_node.parents.remove(old_parent_link)
        else:
            print('warning: unrecognized parent!')
        
        child_node.parents.append(new_parent_link)
        
        # remove the slope as a child node to parent and add slope's child
        new_child_link = (child_coords, parent_steps+child_steps)
        
        
        return
    
    
    
def prune_end(node, node_dict):
    
    if node.is_end:
        parent_coords, parent_steps = node.parents[0] # end only has 1 parent
        parent_node = node_dict[parent_coords]
        parent_node.is_end = True
        parent_node.bonus_len = parent_steps
    
    return
    
    
def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---

    the_map = file_contents
    start_pos, end_pos = get_start_end(the_map)
    
    node_list = []
    node_dict = {}

    node_idx = 1
    # parse the map into nodes to do graph reduction
    # don't grab 1st or last line -- (start/end)
    for r, line in enumerate(the_map):
        for c, place in enumerate(line):
            coords = (r,c)
            if the_map[r][c] != '#':
                new_node = Node2(coords, the_map)
                node_list.append(new_node)
                node_dict[coords] = new_node
                node_idx += 1

    # fill out doubly-linked list
    for node in node_list:
        match_parents(node, node_dict)
    
    # simple pruning
    for node in node_list:
        prune_simple(node, node_dict)

    prune_end(node_dict[end_pos], node_dict)


    start_history = [start_pos]
    start_steps = 0

    max_trail = 0
    trail_queue = []
    
    # need to maintain position history per state to prevent backtracking
    # last item in position_history is the current position
    # len(position_history)-1 == length of trail
    start_state = [start_history, start_steps]
    
    trail_queue.append(start_state)

    loop_counter = 0
    while len(trail_queue) > 0:
        loop_counter += 1
        if loop_counter > 60000000: # full input p1 converges @ 5360
            print('danger, inf loop')
            break
        
        state = trail_queue.pop(-1)
        
        history = state[0]
        steps = state[1]
        current_coords = history[-1]
        current_node = node_dict[current_coords]
        
        # check if we've reached the end
        if current_node.is_end:
            # stop walking
            if steps > max_trail:
                max_trail = steps + current_node.bonus_len
                continue
        
        children = current_node.children
        
        for option, step_len in children: # children are all coords
            if option not in history: # never been here before
                new_history = history.copy()
                new_history.append(option)
                new_state = (new_history, steps+step_len)
                trail_queue.append(new_state)

    print(max_trail,'@', loop_counter)


    # ----------------------
    
    part1 = max_trail
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
