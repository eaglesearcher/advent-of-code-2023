import numpy as np
import file_io as fio
import algo_util as alg

day_num = 20
input_type = 1 # 0 = test, 1 = input

class Flipflop():
    def __init__(self,name, dest_list):
        self.name = name
        self.type = 'ff'
        self.dest_list = dest_list
        self.state = 0
        return
    
    def send_pulse(self, in_pulse):
        # FF ignores high pulses (active low)
        if in_pulse.value == 1:
            return []
        # on low pulse, invert the state
        self.state = 1-self.state
        pulse_train = []
        # send the new state to all dest
        for target in self.dest_list:
            pulse_train.append(Pulse(self.state,target,self.name))
        return pulse_train
    
class Conj():
    def __init__(self, name, dest_list):
        self.name = name
        self.type = 'conj'
        self.dest_list = dest_list
        self.memory = {}
        return
    
    def send_pulse(self, in_pulse):
        # update the value in memory for this sender
        self.memory[in_pulse.sender] = in_pulse.value
        
        # if all memory is 1, send 1; else send 0
        out_value = 0
        for key in self.memory:
            if self.memory[key] == 0:
                out_value = 1
                break
        pulse_train = []
        # send the value to all dest
        for target in self.dest_list:
            pulse_train.append(Pulse(out_value,target,self.name))
        return pulse_train
    
class Broadcaster():
    def __init__(self, name, dest_list):
        self.name = name
        self.type = 'tx'
        self.dest_list = dest_list
        return
    
    def send_pulse(self, in_pulse):
        pulse_train = []
        # broadcast sends whatever it rx to all dest
        for target in self.dest_list:
            pulse_train.append(Pulse(in_pulse.value,target,self.name))
        return pulse_train
        
class Button():
    def __init__(self):
        self.name = 'button'
        self.type = 'button'
        self.dest_list = ['broadcaster']
        return
    
    def push(self):
        pulse_train = []
        # button sends a low signal to the broadcaster
        for target in self.dest_list:
            pulse_train.append(Pulse(0,target,self.name))
        return pulse_train

class Tester():
    # mostly in case of shenanigans (e.g. ex # 2 with "output" not defined)
    def __init__(self, name):
        self.name = name
        self.dest_list = []
        
    def send_pulse(self, in_pulse):
        return []
            
class Pulse():
    def __init__(self, value, target, sender):
        self.value = value
        self.target = target
        self.sender = sender
        return        

def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---

    module_dict = {}

    module_dict['button'] = Button()

    # parse the file to create all the modules
    for line in file_contents:
        name = line.split(' -> ')[0]
        connected_list = line.split(' -> ')[1].split(', ')
        module_type = name[0]
        module_name = name[1:]
        # print(name, connected_list)
        if module_type == '%':
            module_dict[module_name] = Flipflop(module_name, connected_list)
        elif module_type == '&':
            module_dict[module_name] = Conj(module_name, connected_list)
        elif module_type == 'b':
            module_dict[name] = Broadcaster(name, connected_list)
            
    # spin through all the modules again to create AND gate memory
    # also creates empties, if required
    # we can't modify module_dict inside the loop, so create a bucket and dump later
    new_modules = {}
    for key in module_dict:
        destinations = module_dict[key].dest_list
        for this_dest in destinations:
            if this_dest in module_dict:
                module = module_dict[this_dest]
                if module.type == 'conj':
                    module.memory[key] = 0
            else:
                new_modules[this_dest] = Tester(this_dest)
    for key in new_modules:
        module_dict[key] = new_modules[key]
        
    # set up trackers for analysis after the loop
    low_tracker = []
    high_tracker = []
    gf_tracker = {}
    gf_tracker['kr'] = []
    gf_tracker['zs'] = []
    gf_tracker['kf'] = []
    gf_tracker['qk'] = []
    
    cycle_tracker = []
    pulse_queue = []
    
    n = 20000
    # many button presses
    for idx in range(n):
        # press the button!
        # print(f'Pressing the button! (#{idx+1})')
        new_pulses = module_dict['button'].push()
        pulse_queue.extend(new_pulses)
        
        low_count = 0
        high_count = 0
        
        # for _ in range(10000):
        while len(pulse_queue) != 0:
            # if len(pulse_queue) == 0:
                # print('All pulses resolved')
                # break
            pulse = pulse_queue.pop(0)
            # print(pulse.sender,'@', pulse.value, '->', pulse.target)
            # if pulse.target == 'rx' and pulse.value == 0:
                # print('solved @', idx+1)
                # break
            
            # part 2 --> looking for pulses sent to 'gf'
            # on receive, poll memory and report the button press idx if high
            if pulse.target == 'gf':
                success = 0
                for key in module_dict['gf'].memory:
                    if module_dict['gf'].memory[key] == 1:
                        if (idx+1) not in gf_tracker[key]:
                            gf_tracker[key].append(idx+1)

            # part 1 -> counting high and low pulses sent
            low_count += 1-pulse.value
            high_count += pulse.value
            
            new_pulses = module_dict[pulse.target].send_pulse(pulse)
            pulse_queue.extend(new_pulses)
    
        # print('Low', low_count, 'High', high_count)
        # print()
        # gf_tracker.append(module_dict['gf'].memory)
        
        if idx < 1000:
            low_tracker.append(low_count)
            high_tracker.append(high_count)
        cycle_tracker.append((low_count, high_count))
    

    # part 1 -- exhaustive 1000 cycles for power detection
    exhaustive_p1 = sum(low_tracker)*sum(high_tracker)

    
    # part 1 -- cycle detection on low/high pulse count
    cycle_list, cycle_parameters = alg.cycle_detect(cycle_tracker, 300)
    if cycle_parameters:
        x0, delta = cycle_parameters
        # print(cycle_list)
        # print(cycle_parameters)
        
        # full cycles --> multiply up
        low_count = 0
        high_count = 0
        for item in cycle_list:
            low_count += item[0]
            high_count += item[1]
    
        n = 1000
        k = len(cycle_list)
        print('cycle length', k)
        low_total = low_count*np.floor(n/k)
        high_total = high_count*np.floor(n/k)
    
        # transient --> before the cycle starts
        transient = cycle_tracker[:x0]
        low_count = 0
        high_count = 0
        for item in transient:
            low_count += item[0]
            high_count += item[1]
        
        low_total += low_count
        high_total += high_count    
        
        # partial_cycle
        partial_cycle = cycle_list[:(n%k)]
        low_count = 0
        high_count = 0
        for item in partial_cycle:
            low_count += item[0]
            high_count += item[1]
        
        low_total += low_count
        high_total += high_count    
    
        power = int(low_total * high_total)
    
        print('exhaustive p1', exhaustive_p1)
        print('cycle detect p1', power)
        # true_ans = 739960225
    else:
        power = 0

    print()

    # part 2 -- visual inspection of gf memory cycles
    for key in gf_tracker:
        print(key, gf_tracker[key])
    
    # they are all primes, and the cycle starts at 0
    # so lcm is the product
    lcm = 1
    for key in gf_tracker:
        lcm *= gf_tracker[key][0]

    print()

    # ----------------------
    
    part1 = power
    part2 = lcm


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
