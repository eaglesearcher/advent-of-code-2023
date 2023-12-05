import numpy as np
import file_io as fio
import algo_util as alg

day_num = 5
input_type = 0 # 0 = test, 1 = input

def parse_line(old_value, almanac_line):
    ans = None
    dest, src, span = [int(i) for i in almanac_line.split()]
    
    # print(src, old_value, src+span)
    if src <= old_value < src+span:
        # print('found map')
        ans = dest + old_value - src
    
    # print(ans)
    return ans

def main():
    file_contents = fio.read_input(day_num, input_type)  
    if not file_contents:
        return
    
    # --- add code here! ---
    almanac = file_contents
    almanac_len = len(almanac)
    
    chapters = []
    for page in range(almanac_len):
        if almanac[page] == '':
            chapters.append(page+2) # mapping starts 2 lines after \n
    
    # part 1
    seed_list_p1 = almanac[0].split()[1:]
    # print(seed_list_p1)

    min_location_p1 = 100000000000000000
    for seed in seed_list_p1:
        mapping = [int(seed)]
        for idx, chapter_idx in enumerate(chapters):
            old_value = mapping[-1]
            page = chapter_idx
            new_value = None
            while(not new_value):
                # break out if end -- the mapping is 1:1
                if page == almanac_len-1 or almanac[page] == '':
                    new_value = old_value
                else:
                    new_value = parse_line(old_value, almanac[page])
                page = page + 1
                if new_value:
                    mapping.append(new_value)
                    break
        # print(mapping)
        if mapping[-1] < min_location_p1:
            min_location_p1 = mapping[-1]
          
    # part 2
    
    # parse the file
    catalog = {}
    
    for chapter_idx, chapter_start in enumerate(chapters):
        catalog[chapter_idx] = {}
        page_idx = chapter_start
        page = almanac[page_idx]
        while page:
            dest, src, span = [int(i) for i in page.split()]
            catalog[chapter_idx][src] = (dest, span)
            page_idx += 1
            if page_idx == almanac_len - 1:
                break
            page = almanac[page_idx]
    
    # print(catalog)
    
    catalog_sorted = {}
    for chapter_idx in catalog:
        start_list = sorted(list(catalog[chapter_idx].keys()))
        print(start_list)
        catalog_sorted[chapter_idx] = []
        if start_list[0] > 0:
            catalog[chapter_idx]
        
        for idx, value in enumerate(start_list):
            catalog_sorted[chapter_idx].append(value)
            if not idx == len(start_list)-1:
                span = catalog[chapter_idx][value][1]
                next_range = value + span
                if next_range < start_list[idx+1]:
                    new_span = start_list[idx+1] - next_range
                    catalog_sorted[chapter_idx].append(next_range)
                    catalog[chapter_idx][next_range] = (next_range, new_span)
                # pass
            
    print(catalog_sorted)
            
        
    
    
    
    # build dirty hash table
    
    
    
    
    
    seed_range = [int(i) for i  in almanac[0].split()[1:]]
    seed_start = seed_range[0::2]
    seed_span = seed_range[1::2]
    # print(seed_span)
    min_location_p2 = 100000000000000000
    for seed_idx, first_seed in enumerate(seed_start):
        # print('first', first_seed)
        last_seed = first_seed + seed_span[seed_idx]
        skip_span = 0
        
        seed = first_seed
        
        
        
        # for inc_seed in range(seed_span[seed_idx]):
        #     seed = first_seed+inc_seed
        # print(seed)
        mapping = [seed]
        for idx, chapter_idx in enumerate(chapters):
            old_value = mapping[-1]
            page = chapter_idx
            new_value = None
            while(not new_value):
                # break out if end -- the mapping is 1:1
                if page == almanac_len-1 or almanac[page] == '':
                    new_value = old_value
                else:
                    new_value = parse_line(old_value, almanac[page])
                page = page + 1
                if new_value:
                    mapping.append(new_value)
                    break
        # print(mapping)
        if mapping[-1] < min_location_p2:
            min_location_p2 = mapping[-1]
            
    
    
    # print(seed_range[0::2])
    # print(seed_range[1::2])
    # seed_start = seed_range
    
    # seed_list_p2 = almanac[0].split()[1:]




    # ----------------------
    
    part1 = min_location_p1
    part2 = min_location_p2


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
