import numpy as np
import file_io as fio
import algo_util as alg
from sklearn.cluster import SpectralBiclustering

day_num = 25
input_type = 1 # 0 = test, 1 = input

def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---

    comp_dict = {}

    for line in file_contents:
        tmp = line.split(':')
        source = tmp[0]
        dests = tmp[1].split()
        
        if source not in comp_dict:
            comp_dict[source] = set()
        for dest in dests:
            if dest not in comp_dict:
                comp_dict[dest] = set()
            comp_dict[source].add(dest)
            comp_dict[dest].add(source)
        
    # print(comp_dict)

    idx_dict = {}
    for idx, key in enumerate(comp_dict):
        idx_dict[key] = idx


    n = len(idx_dict)
    
    connect_matrix = np.zeros((n,n))

    for key in comp_dict:
        src = comp_dict[key]
        idx = idx_dict[key]
        for dest in src:
            idx2 = idx_dict[dest]
            connect_matrix[idx, idx2] = 1
            
    # print(connect_matrix)
    # biclustering creates two sets
    # we know they split easily because there are only three cuts
    # don't need to find the actual cuts because we know the size of the groups
    
    model = SpectralBiclustering(n_clusters=2, random_state=0)
    model.fit(connect_matrix)

    reordered_rows = connect_matrix[np.argsort(model.row_labels_)]
    reordered_data = reordered_rows[:, np.argsort(model.column_labels_)]

    print(reordered_data)
    
    k = sum(model.row_labels_)
    print(k,n-k)

    # ----------------------
    
    part1 = (n-k)*k
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
