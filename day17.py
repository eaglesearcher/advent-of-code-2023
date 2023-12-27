import numpy as np
import file_io as fio
import algo_util as alg

day_num = 17
input_type = 1 # 0 = test, 1 = input


class State():
    def __init__(self, position, direction, streak, heat):
        self.position = position
        self.direction = direction
        self.streak = streak
        self.heat = heat
        return

def is_end(state, end_position):
    return state.position == end_position

def get_heuristic(state, end_position):
    man_dist = alg.manhat(state.position, end_position)
    current_heat = state.heat
    return current_heat + man_dist


def get_new_states(state, grid):
    r, c = state.position
    current_direction = state.direction
    current_streak = state.streak
    current_heat = state.heat
    adj_dict, adj_ref = alg.get_adj_cells_2d(grid, r, c)

    new_states = []
    # add a special case for start 'S'
    if current_direction == 'S':
        # start in the upper left corner, so options are R and D
        # no need for special case checking, these are always valid
        test_cases = ['D','R']
        for new_direction in test_cases:
            new_position = adj_ref[new_direction]
            new_heat = current_heat + int(adj_dict[new_direction])
            new_streak = 1
            new_states.append(State(new_position, new_direction, new_streak, new_heat))
        return new_states
    
    # go straight, check the current streak
    new_direction = current_direction
    if current_streak < 3 and adj_ref[new_direction] != None:
        new_position = adj_ref[new_direction]
        new_heat = current_heat + int(adj_dict[new_direction])
        new_streak = current_streak + 1
        new_states.append(State(new_position, new_direction, new_streak, new_heat))
    
    # check left/right turns
    turns = [turn_left(current_direction), turn_right(current_direction)]
    for new_direction in turns:
        if adj_ref[new_direction] != None:
            new_position = adj_ref[new_direction]
            new_heat = current_heat + int(adj_dict[new_direction])
            new_streak = 1
            new_states.append(State(new_position, new_direction, new_streak, new_heat))
    
    return new_states

def get_new_states_p2(state, grid):
    r, c = state.position
    current_direction = state.direction
    current_streak = state.streak
    current_heat = state.heat
    adj_dict, adj_ref = alg.get_adj_cells_2d(grid, r, c)

    new_states = []
    # add a special case for start 'S'
    if current_direction == 'S':
        # start in the upper left corner, so options are R and D
        # no need for special case checking, these are always valid
        test_cases = ['D','R']
        for new_direction in test_cases:
            new_position = adj_ref[new_direction]
            new_heat = current_heat + int(adj_dict[new_direction])
            new_streak = 1
            new_states.append(State(new_position, new_direction, new_streak, new_heat))
        return new_states
    
    # go straight, check the current streak
    new_direction = current_direction
    if current_streak < 10 and adj_ref[new_direction] != None:
        new_position = adj_ref[new_direction]
        new_heat = current_heat + int(adj_dict[new_direction])
        new_streak = current_streak + 1
        new_states.append(State(new_position, new_direction, new_streak, new_heat))
    
    # check left/right turns (only turn if streak at least 4)
    turns = [turn_left(current_direction), turn_right(current_direction)]
    if current_streak >= 4:
        for new_direction in turns:
            if adj_ref[new_direction] != None:
                new_position = adj_ref[new_direction]
                new_heat = current_heat + int(adj_dict[new_direction])
                new_streak = 1
                new_states.append(State(new_position, new_direction, new_streak, new_heat))
    
    return new_states

def turn_left(direction):
    ref = ['L','D','R','U']
    return ref[(ref.index(direction)+1)%4]

def turn_right(direction):
    ref = ['L','D','R','U']
    return ref[(ref.index(direction)-1)%4]


def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---

    city = file_contents

    solver = alg.a_star()    
    end_pos = (len(city)-1, len(city[0])-1)

    # init state
    position = (0,0) # [0]
    direction = 'S' # [1]
    streak = 0 # [2]
    heat = 0 # [3]
    
    prev_hash = {}
    future_hash = {}
    
    state = State(position, direction, streak, heat)
    heur = get_heuristic(state, end_pos)
    solver.add_child(heur, state)

    solution = False
    for i in range(1000000):
        new_step = solver.get_best()
        state = new_step[2]
        key = (state.position, state.direction, state.streak)
        if key in prev_hash:
            if prev_hash[key] <= state.heat:
                # print('hello')
                continue
        else:
            prev_hash[key] = state.heat

        # print('this state', new_step[0], state.position, state.direction, state.streak, state.heat)
        if is_end(state,end_pos):
            print('solution found')
            solution = True
            break
        child_states = get_new_states_p2(state, city)
        for child in child_states:
            heur = get_heuristic(child, end_pos)
            key = (child.position, child.direction, child.streak)
            if key in prev_hash:
                if prev_hash[key] <= child.heat:
                    continue
            if key in future_hash:
                if future_hash[key] <= child.heat:
                    continue
            # print('child', heur, child.position, child.direction, child.streak, child.heat)
            solver.add_child(heur, child)
            future_hash[key] = child.heat
    
    
    if solution:
        print(state.position, state.direction, state.streak, state.heat)
        print(i)
    
    
    
    print('q size', solver.prospects.qsize())
    
    for _ in range(10):
        new_step = solver.get_best()
        state = new_step[2]
        print(new_step[0], new_step[1], state.position, state.direction, state.streak, state.heat)
        if solver.prospects.empty():
            break
    
    # for key in prev_hash:
    #     print(key, prev_hash[key])
    
    print(len(prev_hash))
    


    # ----------------------
    
    part1 = state.heat
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
