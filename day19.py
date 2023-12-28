import numpy as np
import file_io as fio
import algo_util as alg

day_num = 19
input_type = 1 # 0 = test, 1 = input


class Widget():
    def __init__(self, xmas):
        self.value = {}
        xmas = xmas[1:-1].split(',')
        self.sum = 0
        for item in xmas:
            key = item.split('=')[0]
            value = int(item.split('=')[1])
            self.value[key] = value
            self.sum += value
        return


class RangeWidget():
    def __init__(self, x, m, a, s):
        self.value = {}
        self.value['x'] = x
        self.value['m'] = m
        self.value['a'] = a
        self.value['s'] = s
        return
    
    def copy(self):
        x = self.value['x']
        m = self.value['m']
        a = self.value['a']
        s = self.value['s']
        new_widget = RangeWidget(x,m,a,s)
        return new_widget

    def get_combos(self):
        xl,xh = self.value['x']
        ml,mh = self.value['m']
        al,ah = self.value['a']
        sl,sh = self.value['s']
        return (xh-xl+1)*(mh-ml+1)*(ah-al+1)*(sh-sl+1)
        

class Workflow():
    def __init__(self, line):
        # magic parsing
        self.name = line.split('{')[0]
        step_list = line[:-1].split('{')[1].split(',')
        
        self.tests = []
        self.targets = []
        for step in step_list:
            # print(step)
            if ':' in step:
                expression = step.split(':')[0]
                goto = step.split(':')[1]
                self.tests.append(expression)
                self.targets.append(goto)
            else:
                self.tests.append('True')
                self.targets.append(step)
        
        self.num_steps = len(self.tests)
        return
    
    def exec(self, widget):
        x = widget.value['x']
        m = widget.value['m']
        a = widget.value['a']
        s = widget.value['s']
        
        for idx in range(self.num_steps):
            test = eval(self.tests[idx]) 
            if test == True:
                return self.targets[idx]
        print('Something went wrong! -- Workflow.exec')
        return None

    def widget_splitter(self, widget):
        # this_target
        # strategy: when we find a knee in the middle of the range
        # we will split the widget
        # passing range gets the new target
        # failing range is returned with this same widget as a target
        for idx in range(self.num_steps):
            this_test = self.tests[idx]
            this_target = self.targets[idx]
            
            if '<' in this_test:
                key = this_test.split('<')[0]
                knee = int(this_test.split('<')[1])
                vl,vh = widget.value[key]
                # print(key, '<', knee, vl, vh)
                # the knee sits in the middle of the range
                # otherwise we just go on to the next case
                if vl < knee < vh:
                    # print('knee detected')
                    new_widget_l = widget.copy()
                    new_widget_l.value[key] = (vl, knee-1)
                    new_widget_h = widget.copy()
                    new_widget_h.value[key] = (knee, vh)
                    
                    new_target_l = this_target
                    new_target_h = self.name
                    
                    state_l = WidgetState(new_widget_l, new_target_l)
                    state_h = WidgetState(new_widget_h, new_target_h)
                    
                    return [state_l, state_h]
                if vh < knee:
                    # all pass, so pass this widget to the next target
                    return [WidgetState(widget, this_target)]
                
            elif '>' in this_test:
                key = this_test.split('>')[0]
                knee = int(this_test.split('>')[1])
                vl,vh = widget.value[key]
                # print(key, '>', knee, vl, vh)
                # the knee sits in the middle of the range
                # otherwise we just go on to the next case
                if vl < knee < vh:
                    # print('knee detected')
                    new_widget_l = widget.copy()
                    new_widget_l.value[key] = (vl, knee)
                    new_widget_h = widget.copy()
                    new_widget_h.value[key] = (knee+1, vh)
                    
                    new_target_l = self.name
                    new_target_h = this_target
                    
                    state_l = WidgetState(new_widget_l, new_target_l)
                    state_h = WidgetState(new_widget_h, new_target_h)
                    
                    return [state_l, state_h]     
                if vl > knee:
                    # all pass, so pass this widget to the next target
                    return [WidgetState(widget, this_target)]
                
            elif this_test == 'True': # only other valid case
                # no splitting here, just pass the widget to a new target
                return [WidgetState(widget, this_target)]
        
        print('Something went wrong! -- Workflow.widget_splitter')
        return []
        
            
class WidgetState():
    def __init__(self, widget, target):
        self.widget = widget
        self.target = target
        return


def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---

    workflows = {}
    gears = []

    # parse file
    for line in file_contents:
        # print(line)
        if len(line) > 0 and line[0] != '{': # new workflow
            x = Workflow(line)    
            workflows[x.name] = x
        # key = line.split('{')[0]
            # tmp = line[:-1].split('{')[1].split(',') # list of steps
            # workflows[key] = Workflow(tmp)
        if len(line) > 0 and line[0] == '{': # new widget
            gears.append(Widget(line))
    
    # part 1 --> process the parts
    net_sum = 0
    for part in gears:
        target = 'in'
        while (target != 'R' and target != 'A'):
            target = workflows[target].exec(part)
        if target == 'A':
            net_sum += part.sum


    # part 2 --> combos
    
    # xmas can be between 1-4000
    x = (1,4000)
    m = (1,4000)
    a = (1,4000)
    s = (1,4000)
    
    part = RangeWidget(x, m, a, s)
    target = 'in'
    state = WidgetState(part, target)
    
    acceptable_widgets = []

    widget_queue = []
    widget_queue.append(state)    
    
    for _ in range(5000):
        if len(widget_queue) == 0:
            print('all widgets processed')
            break
        
        this_state = widget_queue.pop()
        next_widget = this_state.widget
        next_target = this_state.target
    
        # print(next_target, next_widget.value)
        new_states = workflows[next_target].widget_splitter(next_widget)
        if new_states:
            for state in new_states:
                if state.target == 'A':
                    acceptable_widgets.append(state.widget)
                elif state.target != 'R':
                    widget_queue.append(state)

    print('widgets found',len(acceptable_widgets))
    
    total_combos = 0
    for part in acceptable_widgets:
        total_combos += part.get_combos()
    
    
    
    # ----------------------
    
    part1 = net_sum
    part2 = total_combos


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
