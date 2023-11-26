import time
import util
import day1

if __name__ == '__main__':
    t0 = time.time()
    x = day1.main()
    t1 = time.time()

    # x  = util.read_input(1,0)


    dt = (t1-t0)*1000
    print()
    # print('Results', x)
    print('Runtime = ', int(dt), 'msec')
    # print('Runtime = ', int(dt)/1000, 'sec')
    # print('Runtime = ', int(dt)/1000000, 'msec')

