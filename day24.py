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
        
        self.p = {}
        self.p['x'] = self.px
        self.p['y'] = self.py
        self.p['z'] = self.pz
        
        self.v = {}
        self.v['x'] = self.vx
        self.v['y'] = self.vy
        self.v['z'] = self.vz
        
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
        
        self.p = {}
        self.p['x'] = self.px
        self.p['y'] = self.py
        self.p['z'] = self.pz
        
        self.v = {}
        self.v['x'] = self.vx
        self.v['y'] = self.vy
        self.v['z'] = self.vz
        
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

def get_z(stone, x,y,t):
    return stone.pz+stone.vz*t


def get_error(stone, hail):
    x,y,ta,tb = get_intersection_2d(stone, hail)
    if x != None:
        # print(hail.name, x,y,ta,tb)
        return (ta-tb)**2
    else:
        print('did not intersect')
        return None
    # if stone.vy != hail.vy:
        # error = stone.px - hail.px + (hail.py - stone.py)*(stone.vx - hail.vx)/(stone.vy - hail.vy)
    # else:
    # error = 0
    # return error**2

def get_params(stone, hail):
    # only gets called if there was an intersection
    
    x,y,ta,tb = get_intersection_2d(stone, hail)
    
    ta = (ta+tb)/2
    
    a = hail.px + ta*(hail.vx - stone.vx)
    b = hail.vx + (hail.px - stone.px)/ta
    c = hail.py + ta*(hail.vy - stone.vy)
    d = hail.vy + (hail.py - stone.py)/ta
    e = hail.pz + ta*(hail.vz - stone.vz)
    f = hail.vz + (hail.pz - stone.pz)/ta
    
    return [a, b, c, d, e, f]

# def get_ts(stone,hail0,hail1, dim):
#     if dim == 'x':
#         if stone.vx == hail0.vx or stone.vx == hail1.vx:
#             return None, None
#         t0 = (hail0.px - stone.px)/(stone.vx-hail0.vx)
#         t1 = (hail1.px - stone.px)/(stone.vx-hail1.vx)
#     elif dim == 'y':
#         if stone.vy == hail0.vy or stone.vy == hail1.vy:
#             return None, None
        
#         t0 = (hail0.py - stone.py)/(stone.vy-hail0.vy)
#         t1 = (hail1.py - stone.py)/(stone.vy-hail1.vy)
#     elif dim == 'z':
#         if stone.vz == hail0.vz or stone.vz == hail1.vz:
#             return None, None
#         t0 = (hail0.pz - stone.pz)/(stone.vz-hail0.vz)
#         t1 = (hail1.pz - stone.pz)/(stone.vz-hail1.vz)
        
#     return t0,t1

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



# def set_next_dims(stone, hail0, hail1, dim):
#     t0, t1 = get_ts(stone, hail0, hail1, dim)
#     # print(t0,t1)
#     if t0 == None:
#         return stone
#     # if t0 == t1:
#         # return stone
#     if dim == 'x':
#         stone.vy = (hail1.py - hail0.py + hail1.vy*t1 - hail0.vy*t0) / (t1-t0)
#         stone.py = hail0.py - t0*(stone.vy - hail0.vy)
#         # if t0 < 0 or t1 < 0:
#             # stone.vy = -stone.vy
#             # stone.vy = 1
#     if dim == 'y':
#         stone.vz = (hail1.pz - hail0.pz + hail1.vz*t1 - hail0.vz*t0) / (t1-t0)
#         stone.pz = hail0.pz - t0*(stone.vz - hail0.vz)
#         # if t0 < 0 or t1 < 0:
#             # stone.vz = -stone.vz
#             # stone.vz = 1
#     if dim == 'z':
#         stone.vx = (hail1.px - hail0.px + hail1.vx*t1 - hail0.vx*t0) / (t1-t0)
#         stone.px = hail0.px - t0*(stone.vx - hail0.vx)
#         # if t0 < 0 or t1 < 0:
#             # stone.vx = -stone.vx
#             # stone.vx = 1

#     return stone


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
    # # part 1 -- "natural" collisions
    # count = len(hail_list)

    # if input_type == 0:
    #     test_min = 7
    #     test_max = 27
    # else:
    #     test_min = 200000000000000
    #     test_max = 400000000000000

    # success_counter = 0

    # for idx_a in range(count):
    #     hail_a = hail_list[idx_a]
    #     for idx_b in range(idx_a+1,count):
    #         hail_b = hail_list[idx_b]
    #         # print(f'{idx_a} & {idx_b}')
    #         x,y,ta,tb = get_intersection_2d(hail_a,hail_b)
    #         # if x == None:
    #         #     print(f'{idx_a} & {idx_b}, Parallel, no intersection')    
    #         # elif ta < 0 or tb < 0:
    #         #     print(f'{idx_a} & {idx_b}, Intersection in the past for A or B')    
    #         # else:
    #         #     print(f'{idx_a} & {idx_b}, At ta={ta:.2f}, tb={tb:.2f}, x={x:.2f}, y={y:.2f}')
    #         #     if test_min <= x <= test_max and test_min <= y <= test_max:
    #         #         print('cross inside')
    #         #         success_counter += 1
    #         #     else:
    #         #         print('cross outside')
    #         if x != None and ta >= 0  and tb >= 0 and test_min <= x <= test_max and test_min <= y <= test_max:
    #             success_counter += 1

    # part 2 - throw a rock

    # params = [24,13,10,-3,1,2]
    # rock = Stone(params)
    
    # for hail in hail_list:
    #     print(f'Hailstone: {hail.px} {hail.py} {hail.pz}, {hail.vx}, {hail.vy}, {hail.vz}')
    #     x,y,ta,tb = get_intersection_2d(rock, hail)
    #     print(f'At ta={ta:.2f}, tb={tb:.2f}, x={x:.2f}, y={y:.2f}')
    #     za = get_z(rock,x,y,ta)
    #     zb = get_z(hail,x,y,tb)
    #     print(za,zb)


    n = len(hail_list)    

    # params = [0,0,0,-1,1,1]
    # params = [20,31,34,1,1,1]
    params = [24,13,10,-3,1,2]
    rock = Stone(params)
    
    dims = ['x','y','z']
    dim_idx = 0

    A = []
    b = []
    
    # full linear system

    for hail in hail_list[:5]:
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
    
    print(np.shape(A))
    print(np.shape(b))
    
    # x = np.asarray([24,-3,13,1,-63])
    # x = np.reshape(x,(len(x),1))
    
    # print(A)
    # print(x)
    # # print(b)
    # # print(np.shape(A), np.shape(b))
    # print(np.sum(A*np.transpose(x),1))
    # print(b)


    print(A)
    print(b)
    result = np.sum(np.linalg.inv(A)*np.transpose(b),1)
    print(result)
    
    for element in result:
        print(element)


    # summation over linear system
    
    # test = [sum_vy, -sum_py, -sum_vx, sum_px, n]
    
    # i_mat = np.identity(5)*test
    # print(i_mat)
    # print(x)
    # print(np.sum(i_mat*x))
    
    # print(np.sum(np.linalg.inv(i_mat)*np.transpose(b),1))
    





    # -------------------------------------------------------------------------
    # # minimization one dimension at a time
    # # choose a,b -> find ti -> calculate c,d -> find new ti, etc
    
    # for __ in range(10):
    #     t_sum = 0
    #     data_sum = 0
        
    #     dim = dims[dim_idx]
    #     next_dim = dims[(dim_idx+1)%3]
        
    #     pr = rock.p[dim]
    #     vr = rock.v[dim]
        
    #     # find ti for current dimension
    #     for hail in hail_list:
    #         ph = hail.p[dim]
    #         vh = hail.v[dim]
    #         ph2 = hail.p[next_dim]
    #         vh2 = hail.v[next_dim]
            
    #         if vr != vh:
    #             hail.ti = (ph - pr) / (vr - vh)

    #         t_sum += hail.ti
            
    #         hail.nextdata = ph2 + vh2*hail.ti
    #         data_sum += hail.nextdata
            
    #         # print(hail.ti, hail.nextdata)
        
    #     new_p = 0
    #     new_v = 0
    #     # print('tsum', t_sum)
        
    #     # set next dimension
    #     for hail in hail_list:
    #         new_p += (hail.ti*data_sum - t_sum*hail.nextdata)/(n*hail.ti - t_sum)
    #         new_v += (n*hail.nextdata - data_sum)/(n*hail.ti - t_sum)
        
    #     deltap = rock.p[next_dim] - new_p/n
    #     deltav = rock.v[next_dim] - new_v/n
        
    #     rock.p[next_dim] -= deltap*0.1
    #     rock.v[next_dim] -= deltav*0.1
    #     dim_idx = (dim_idx+1)%3
    
    # print(rock.p)
    
    # -------------------------------------------------------------------------
    # attempt at minimizing the loss function - messy
    
    # t_list = []
        
    # t_sum = 0
    # data_sum_x = 0
    # data_sum_y = 0
    # data_sum_z = 0
    
    # for _ in range(1):
    
    #     a_sum = 0
    #     b_sum = 0
    #     c_sum = 0
    #     d_sum = 0
    #     e_sum = 0
    #     f_sum = 0
        
    #     # hail = hail_list[0]
    #     for hail in hail_list:
    #         t0, tsub = get_t(rock, hail)
            
    #         t_loss = 0
    #         for ti in tsub:
    #             if ti != None:
    #                 t_loss += (t0-ti)**2
            
    #         # print(t0, tsub, t_loss/3)
    #         print(t_loss)
            
    #         a = rock.px
    #         b = rock.vx
    #         c = rock.py
    #         d = rock.vy
    #         e = rock.pz
    #         f = rock.vz
            
    #         sumpi = hail.px+hail.py+hail.pz
    #         sumvi = hail.vx+hail.vy+hail.vz
    #         denom = b+d+f - sumvi
    #         numer = sumpi - (a+c+e)
            
    #         a = hail.px*denom+(c+e)*(b-hail.vx) - sumpi*(b-hail.vx)
    #         a = a/(denom - (b-hail.vx))
            
    #         c = hail.py*denom+(a+e)*(d-hail.vy) - sumpi*(d-hail.vy)
    #         c = c/(denom - (d-hail.vy))
            
    #         print(denom, f, hail.vz)
    #         e = hail.pz*denom + (a+c)*(f-hail.vz) - sumpi*(f-hail.vz)
    #         e = e/(denom - (f-hail.vz))
            
    #         b = hail.vx*numer + (d+f)*(hail.px-a) - sumvi*(hail.px-a)
    #         b = b/(numer - (hail.px-a))
            
    #         d = hail.vy*numer + (b+f)*(hail.py-c) - sumvi*(hail.py-c)
    #         d = d/(numer - (hail.py-c))
            
    #         f = hail.vz*numer + (b+d)*(hail.pz-e) - sumvi*(hail.pz-e)
    #         f = f/(numer - (hail.pz-e))
            
    #         a_sum += a/n
    #         b_sum += b/n
    #         c_sum += c/n
    #         d_sum += d/n
    #         e_sum += e/n
    #         f_sum += f/n
            
    #     params = [a_sum, c_sum, e_sum, b_sum, d_sum, f_sum]
    #     rock = Stone(params)
    
    # print(params)
    
    
    # -------------------------------------------------------------------------
    # attempt bulk minimization
    # set abcdef -> calculate ti -> set new abcdef
    
    
    # for __ in range(100):
    
    #     t_list = []
            
    #     t_sum = 0
    #     data_sum_x = 0
    #     data_sum_y = 0
    #     data_sum_z = 0
    #     for hail in hail_list:
            
    #         t0, tsub = get_t(rock, hail)
    #         # t0 = max(t0,-t0)
            
    #         t_loss = 0
    #         for ti in tsub:
    #             if ti != None:
    #                 t_loss += (t0-ti)**2
            
    #         # print('loss',t0, tsub, t_loss/3)
    #         # print(t_loss)
    #         hail.ti = t0
    #         if tsub[0] != None:
    #             hail.tx = tsub[0]
    #             # hail.tx = max(tsub[0],-tsub[0])
    #         else:
    #             hail.tx = t0
    #         if tsub[1] != None:
    #             hail.ty = tsub[1]
    #             # hail.ty = max(tsub[1],-tsub[1])
    #         else:
    #             hail.ty = t0
    #         if tsub[2] != None:
    #             hail.tz = tsub[2]
    #             # hail.tz = max(tsub[2],-tsub[2])
    #         else:
    #             hail.tz = t0
    #         # hail.ty = tsub[1]
    #         # hail.tz = tsub[2]
            
    #         t_list.append(t_loss)
    #         t_sum += t0
            
            
    #         hail.data_x = hail.px + hail.vx * hail.tx
    #         hail.data_y = hail.py + hail.vy * hail.ty
    #         hail.data_z = hail.pz + hail.vz * hail.tz
            
    #         data_sum_x += (hail.data_x)
    #         data_sum_y += (hail.data_y)
    #         data_sum_z += (hail.data_z)
        
    #     a_sum = 0
    #     b_sum = 0
    #     c_sum = 0
    #     d_sum = 0
    #     e_sum = 0
    #     f_sum = 0
        
    #     for idx, hail in enumerate(hail_list):
    #         t0 = hail.ti
    #         # print(t0)
    #         data_x = hail.data_x
    #         data_y = hail.data_y
    #         data_z = hail.data_z
            
    #         b = (n*(data_x) - data_sum_x) / (n*hail.tx - t_sum)
    #         d = (n*(data_y) - data_sum_y) / (n*hail.ty - t_sum)
    #         f = (n*(data_z) - data_sum_z) / (n*hail.tz - t_sum)
            
    #         a = (hail.tx*data_sum_x - t_sum*data_x) / (n*hail.tx - t_sum)
    #         c = (hail.ty*data_sum_y - t_sum*data_y) / (n*hail.ty - t_sum)
    #         e = (hail.tz*data_sum_z - t_sum*data_z) / (n*hail.tz - t_sum)
            
    #         if hail.px > a:
    #             b = max(hail.vx,b)
    #         elif hail.px < a:
    #             b = min(hail.vx,b)
    #         elif hail.px == a:
    #             b = hail.vx
            
    #         if hail.py > c:
    #             d = max(hail.vy,d)
    #         elif hail.py < c:
    #             d = min(hail.vy,d)
    #         elif hail.py == c:
    #             d = hail.vy
            
    #         if hail.pz > e:
    #             f = max(hail.vz,f)
    #         elif hail.pz < e:
    #             f = min(hail.vz,f)
    #         elif hail.pz == e:
    #             f = hail.vz
            
            
    #         a_sum += a/n
    #         c_sum += c/n
    #         e_sum += e/n
            
    #         b_sum += b/n
    #         d_sum += d/n
    #         f_sum += f/n
        
        
    #     new_px = rock.px - 0.1*(rock.px-a_sum)
    #     new_py = rock.py - 0.1*(rock.py-c_sum)
    #     new_pz = rock.pz - 0.1*(rock.pz-e_sum)
        
    #     new_vx = rock.vx - 0.1*(rock.vx-b_sum)
    #     new_vy = rock.vy - 0.1*(rock.vy-d_sum)
    #     new_vz = rock.vz - 0.1*(rock.vz-f_sum)
        
    #     params = [new_px,new_py,new_pz,new_vx,new_vy,new_vz]
    #     rock = Stone(params)

    #     # print(sum(t_list)/n)
    # # print(a_sum,c_sum,e_sum)
    # # print(b_sum,d_sum,f_sum)
    
    # print(rock.px,rock.py,rock.pz)
    
    # -------------------------------------------------------------------------
    # checking the answer

    # for hail in hail_list:
    #     print(f'Hailstone: {hail.px} {hail.py} {hail.pz}, {hail.vx}, {hail.vy}, {hail.vz}')
    #     x,y,ta,tb = get_intersection_2d(rock, hail)
    #     print(f'At ta={ta:.2f}, tb={tb:.2f}, x={x:.2f}, y={y:.2f}')
    #     za = get_z(rock,x,y,ta)
    #     zb = get_z(hail,x,y,tb)
    #     # print(za,zb)




    # ----------------------
    
    part1 = success_counter
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
