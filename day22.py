import numpy as np
import file_io as fio
import algo_util as alg

day_num = 22
input_type = 1 # 0 = test, 1 = input

class Brick():
    def __init__(self, name, endpoints):
        self.name = name
        self.endpoints = endpoints
        
        # doubly-linked lists
        self.supported_by = set() # set of bricks
        self.supports = set() # set of bricks
        
        return

class HeightGrid():
    def __init__(self, max_x, max_y, bricktionary):
        self.heights = [[0 for _ in range(max_y+1)] for __ in range(max_x+1)]
        self.topbrick = [[None for _ in range(max_y+1)] for __ in range(max_x+1)]
        self.bricktionary = bricktionary
        return
    
    def print_grid(self):
        print('Height:')
        for line in self.heights:
            print(line)
        print()
        print('Top Brick')
        for line in self.topbrick:
            print(line)
        print()
        return
    
    def update_grid(self, brick):
        a = brick.endpoints[0]
        b = brick.endpoints[1]
        # print(a,b)
        
        # scan the xy surface of this brick to find the existing max height
        # hopefully our bricks didn't get crossed up
        min_height = 0
        for x in range(a[0],b[0]+1):
            for y in range(a[1],b[1]+1):
                # print(x,y)
                # print('Tracker:', self.heights[x][y], self.topbrick[x][y])
                min_height = max(self.heights[x][y],min_height)
        
        # at this point we don't care what the starting z value was
        # only need to increment the tracker by the height of this brick
        
        # all bricks are either flat (delta_z = 1 brick high)
        # OR it is a long tall brick (delta_z = many bricks high, but only 1 block around)
            # then for each bottom face find the min height to get the blocking one
        delta_z = b[2]-a[2] + 1
        
        height_check = min_height # we need this to know if a brick is supporting us
        new_height = min_height + delta_z
        # print('new min height', min_height)
        
        # do the same scan again, setting the new minimum height
        # if the block is "sitting" on another block, update the linked lists
        for x in range(a[0],b[0]+1):
            for y in range(a[1],b[1]+1):
                # check if a block is exactly 1 less than the min height
                if self.heights[x][y] == height_check:
                    if self.topbrick[x][y]: # bypass if None
                        brick.supported_by.add(self.topbrick[x][y])
                        self.bricktionary[self.topbrick[x][y]].supports.add(brick.name)
                self.heights[x][y] = new_height
                self.topbrick[x][y] = brick.name
        
        return


def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---

    brick_list = []
    bricktionary = {}

    for idx, brick in enumerate(file_contents):
        tmp = brick.split('~')
        # left = tmp[0].split(',')
        a = np.asarray([int(i) for i in tmp[0].split(',')])
        b = np.asarray([int(i) for i in tmp[1].split(',')])
        key = chr(idx+65) # this is mostly to make the example readable
        # key = idx+1 # otherwise, start numbering at 1; fixes some errors
        new_brick = Brick(key, (a,b))
        brick_list.append(new_brick)
        bricktionary[key] = new_brick

    # sort the brick list by their lower z value
    # this way bricks are processed in order from the ground up
    brick_list = sorted(brick_list,key=lambda brick: brick.endpoints[0][2])

    # DATA VALIDATION:    
    # second endpoint is ALWAYS greater than or equal to first endpoint
    # there is only 1 coord that changes between endpoints
    # there are no negative coords

    # # data validation checks
    # for brick in brick_list:
    #     a = brick.endpoints[0]
    #     b = brick.endpoints[1]
    #     line = b-a
    #     if np.min(line) < 0:
    #         print(a, b, b-a)
    #         print('warning: 2nd endpoint lower')
    #     if np.sum(line) != np.max(line):
    #         print(a, b, b-a)
    #         print('warning: more than 1 delta')
    #     if np.min(a) < 0 or np.min(b) < 0:
    #         print(a, b, b-a)
    #         print('warning: neg coords')

    max_x = 0
    max_y = 0        

    # get grid size
    for brick in brick_list:
        a = brick.endpoints[0]
        max_x = max(max_x, a[0])
        max_y = max(max_y, a[0])
        
    tracker = HeightGrid(max_x, max_y, bricktionary)
    # tracker.print_grid()


    # create the "stable" tower by processing all blocks
    for new_brick in brick_list:
        tracker.update_grid(new_brick)
    # tracker.print_grid()
    
    safe_count = 0
    
    # part 1 -- check if the brick is "safe to remove"
    for brick in brick_list:
        # print('Brick',brick.name)
        # print('- supported by:',brick.supported_by)
        # print('- supports:',brick.supports)
        safe = True
        for supported_brick in brick.supports:
            if len(bricktionary[supported_brick].supported_by) == 1:
                safe = False
                break
        if safe:
            safe_count += 1
        # print('-- safe to remove?',safe)
     
    # part 2
    
    net_fall_counter = 0
    # brick = brick_list[0]
    for brick in brick_list:
        missing_bricks = set()
        missing_bricks.add(brick.name)
    
        # print(brick.name)
        # print(brick.supports)
        
        fall_queue = [brick.name]
        
        while len(fall_queue) > 0:
            new_brick = bricktionary[fall_queue.pop(0)]
            
            # first pass -> check if any fall -- can insert this up top
            for supported_brick in new_brick.supports:
                if supported_brick in missing_bricks: # already falling, ignore
                    continue
                needs = bricktionary[supported_brick].supported_by
                if needs.issubset(missing_bricks): # all supports are missing, the brick falls!
                    fall_queue.append(supported_brick)
                    missing_bricks.add(supported_brick)
    
        # print(missing_bricks)
        # print(fall_queue)
    
        fallen = len(missing_bricks)-1
        # print('Removing Brick', brick.name, 'causes',fallen,'to fall.')
        net_fall_counter += fallen
           

    # ----------------------
    
    part1 = safe_count
    part2 = net_fall_counter


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
