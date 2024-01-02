import numpy as np
import file_io as fio
import algo_util as alg

day_num = 24
input_type = 1 # 0 = test, 1 = input

class Hailstone():
    def __init__(self, key, input_line):
        tmp = input_line.split(' @ ')
        position = [int(i) for i in tmp[0].split(', ')]
        velocity = [int(i) for i in tmp[1].split(', ')]
        self.name = key
        self.px = position[0]
        self.py = position[1]
        self.pz = position[2]
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.vz = velocity[2]
        
        self.ti = 1
        return

class Stone():
    def __init__(self, params):
        # same as Hailstone class, but defined explicitly
        self.px = params[0]
        self.py = params[1]
        self.pz = params[2]
        self.vx = params[3]
        self.vy = params[4]
        self.vz = params[5]
        return
    
    def copy(self):
        params = [self.px, self.py, self.pz, self.vx, self.vy, self.vz]
        return Stone(params)



def get_intersection_2d(a,b):
    # a and b are hailstone objects
    if a.vx/b.vx == a.vy/b.vy: # parallel case
        # parallel case never intersects    
        # by definition they are heading the same direction
        # so even if they are the same line,
        # ... the intersection happens in the past for one of them
        # only failure case would be 2 stones starting at the same position
        return None, None, None, None

    ta = (b.py - a.py + (b.vy/b.vx)*(a.px - b.px))/(a.vy - (b.vy/b.vx)*a.vx)
    x = a.px + a.vx*ta
    y = a.py + a.vy*ta
    tb = (x-b.px)/b.vx
    
    return x,y,ta,tb

def get_z(stone, t):
    return stone.pz+stone.vz*t

def get_t(stone, hail):
    
    t = 0
    
    alpha = -(stone.px + stone.py + stone.pz)
    beta = (hail.px + hail.py + hail.pz)
    
    gamma = (stone.vx + stone.vy + stone.vz)
    delta = -(hail.vx + hail.vy + hail.vz)
    
    t = (alpha + beta) / (gamma + delta)
    
    if hail.vx != stone.vx:
        tx = (hail.px - stone.px)/(stone.vx-hail.vx)
    else:
        tx = None
    if hail.vy != stone.vy:
        ty = (hail.py - stone.py)/(stone.vy-hail.vy)
    else:
        ty = None
    if hail.vz != stone.vz:
        tz = (hail.pz - stone.pz)/(stone.vz-hail.vz)
    else:
        tz = None
    tsub = (tx,ty,tz)
    return t, tsub

def linear_fit_z(t,z):
    
    vz = (z[1]-z[0])/(t[1]-t[0])
    pz = z[0] - vz*t[0]    
    return pz, vz


def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---

    hail_list = []
    hail_dict = {}

    for idx, line in enumerate(file_contents):
        new_hail = Hailstone(idx+1, line)
        hail_list.append(new_hail)
        hail_dict[idx+1] = new_hail
        
    success_counter = 0
    # part 1 -- "natural" collisions
    count = len(hail_list)

    if input_type == 0:
        test_min = 7
        test_max = 27
    else:
        test_min = 200000000000000
        test_max = 400000000000000

    success_counter = 0

    for idx_a in range(count):
        hail_a = hail_list[idx_a]
        for idx_b in range(idx_a+1,count):
            hail_b = hail_list[idx_b]
            # print(f'{idx_a} & {idx_b}')
            x,y,ta,tb = get_intersection_2d(hail_a,hail_b)
            # if x == None:
            #     print(f'{idx_a} & {idx_b}, Parallel, no intersection')    
            # elif ta < 0 or tb < 0:
            #     print(f'{idx_a} & {idx_b}, Intersection in the past for A or B')    
            # else:
            #     print(f'{idx_a} & {idx_b}, At ta={ta:.2f}, tb={tb:.2f}, x={x:.2f}, y={y:.2f}')
            #     if test_min <= x <= test_max and test_min <= y <= test_max:
            #         print('cross inside')
            #         success_counter += 1
            #     else:
            #         print('cross outside')
            if x != None and ta >= 0  and tb >= 0 and test_min <= x <= test_max and test_min <= y <= test_max:
                success_counter += 1

    # part 2 - throw a rock

    # n = len(hail_list)    

    A = []
    b = []
    
    # full linear system
    i = 1
    for hail in hail_list[i:5+1]:
        A0 = hail.vy
        A1 = -hail.py
        A2 = -hail.vx
        A3 = hail.px
        A4 = 1
        row = [A0, A1, A2, A3, A4]
        A.append(row)
        b.append(hail.px*hail.vy - hail.py*hail.vx)
        

        
    A = np.asarray(A)
    b = np.asarray(b)
    b = np.reshape(b,(len(b),1))
    
    # print(np.shape(A))
    # print(np.shape(b))
    
    # x = np.asarray([24,-3,13,1,-63])
    # x = np.reshape(x,(len(x),1))
    
    # print(A)
    # print(x)
    # # print(b)
    # # print(np.shape(A), np.shape(b))
    # print(np.sum(A*np.transpose(x),1))
    # print(b)


    # print(A)
    # print(b)
    result = np.sum(np.linalg.inv(A)*np.transpose(b),1)
    # print(result)
    
    # for element in result:
    #     print(round(element))

    params = [round(result[0]),round(result[2]), 0, round(result[1]),round(result[3]),0]
    print(params)
    rock = Stone(params)

    # params = [24,13,10,-3,1,2]
    # rock = Stone(params)


    

    
    # -------------------------------------------------------------------------
    # getting Z
    ts = []
    zs = []

    for hail in hail_list[i:5+1]:
        # print(f'Hailstone: {hail.px} {hail.py} {hail.pz}, {hail.vx}, {hail.vy}, {hail.vz}')
        # print(f'Rock: {rock.px} {rock.py} {rock.pz}, {rock.vx}, {rock.vy}, {rock.vz}')
        x,y,ta,tb = get_intersection_2d(rock, hail)
        # print(f'At ta={ta:.2f}, tb={tb:.2f}, x={x:.2f}, y={y:.2f}')
        # za = get_z(rock,ta)
        zb = get_z(hail,tb)
        # print(za,zb)
        ts.append(tb)
        zs.append(zb)
        hail.ti = ts
        
    print(ts)
    print(zs)

    pz,vz = linear_fit_z(ts,zs)
    rock.pz = pz
    rock.vz = vz

    p2_result = rock.px+rock.py+rock.pz

    # ----------------------
    
    part1 = success_counter
    part2 = p2_result


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
