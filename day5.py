import numpy as np
import file_io as fio
import algo_util as alg
from bisect import bisect

day_num = 5
input_type = 1 # 0 = test, 1 = input

def parse_line(old_value, almanac_line):
    ans = None
    dest, src, span = [int(i) for i in almanac_line.split()]
    
    # print(src, old_value, src+span)
    if src <= old_value < src+span:
        # print('found map')
        ans = dest + old_value - src
    
    # print(ans)
    return ans

def get_hash(old_value, catalog_chapter):
    
    n = bisect(catalog_chapter,old_value)
    ref_seed = catalog_chapter[n-1]

    return ref_seed

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
    
    # parse the file, build a dirty hash table
    # initial parse of file
    catalog = {}
    for chapter_idx, chapter_start in enumerate(chapters):
        catalog[chapter_idx] = {}
        page_idx = chapter_start
        page = almanac[page_idx]
        while page:
            dest, src, span = [int(i) for i in page.split()]
            delta = dest-src
            catalog[chapter_idx][src] = (dest, span, delta)
            page_idx += 1
            if page_idx == almanac_len - 1:
                break
            page = almanac[page_idx]

    # sort each page per chapter, then insert additional spaces
    # never need to check spans inline, always just grab the right index
    catalog_sorted = {}
    for chapter_idx in catalog:
        start_list = sorted(list(catalog[chapter_idx].keys()))
        catalog_sorted[chapter_idx] = [-1]
        catalog[chapter_idx][-1] = (-1, start_list[0]+1, 0)
        for idx, value in enumerate(start_list):
            catalog_sorted[chapter_idx].append(value)
            if not idx == len(start_list)-1:
                span = catalog[chapter_idx][value][1]
                next_start = value + span
                if next_start < start_list[idx+1]:
                    new_span = start_list[idx+1] - next_start
                    delta = 0
                    catalog_sorted[chapter_idx].append(next_start)
                    catalog[chapter_idx][next_start] = (next_start, new_span, delta)
        last_start = start_list[-1]+catalog[chapter_idx][start_list[-1]][1]
        catalog[chapter_idx][last_start] = (last_start, None, 0)
        catalog_sorted[chapter_idx].append(last_start)
            
    # print(catalog)
    # print(catalog_sorted)
    
    
    # part 1
    seed_list_p1 = [int(i) for i in almanac[0].split()[1:]]
    # print(seed_list_p1)

    min_location_p1 = 100000000000000000
    for seed in seed_list_p1:
        mapping = [seed]
        # print('---- First Seed', seed)
        for idx, chapter_idx in enumerate(chapters):
            old_value = mapping[-1]

            ref_seed = get_hash(old_value, catalog_sorted[idx])
            delta = catalog[idx][ref_seed][2]
            new_value = old_value+delta
            mapping.append(new_value)
            
            # print('Chapter', idx)
            # print(ref_seed, catalog[idx][ref_seed])
            # print('new seed = ',old_value+delta)
            
            # while(not new_value):
            #     # break out if end -- the mapping is 1:1
            #     if page == almanac_len-1 or almanac[page] == '':
            #         new_value = old_value
            #     else:
            #         new_value = parse_line(old_value, almanac[page])
            #     page = page + 1
            #     if new_value:
            #         mapping.append(new_value)
            #         break
        # print(mapping)
        if mapping[-1] < min_location_p1:
            min_location_p1 = mapping[-1]
          
    # part 2
    
    seed_range = [int(i) for i  in almanac[0].split()[1:]]
    seed_start = seed_range[0::2]
    seed_span = seed_range[1::2]
    
    # seed_start = seed_start[0:1]

    # print(seed_span)
    min_location_p2 = 100000000000000000
    for seed_idx, first_seed in enumerate(seed_start):
        # print('first', first_seed)
        last_seed = first_seed + seed_span[seed_idx]
        skip_span = seed_span[seed_idx]
        
        seed = first_seed
        
        while(seed < last_seed):
            skip_span = seed_span[seed_idx] - (seed - first_seed)
            # print('--- Starting seed',seed)
            # print('skip @ start', skip_span)
            # print('--- next seed', seed+skip_span)
            
            
            # for inc_seed in range(seed_span[seed_idx]):
            #     seed = first_seed+inc_seed
            # print('seed', seed)
            mapping = [seed]
            for idx, chapter_start in enumerate(chapters):
                old_value = mapping[-1]
    
                ref_seed = get_hash(old_value, catalog_sorted[idx])
                
                
                delta = catalog[idx][ref_seed][2]
                
                if catalog[idx][ref_seed][1]:
                    ref_span = catalog[idx][ref_seed][1]
                    # print('ref span', ref_span, 'old value', old_value, 'ref_seed', ref_seed)
                    valid_span = ref_span - (old_value - ref_seed)
                    # print('valid_span', valid_span)
                    if valid_span < skip_span:
                        skip_span = valid_span
                
                new_value = old_value+delta
                mapping.append(new_value)
                
                
                # print('Chapter', idx)
                # print(ref_seed, catalog[idx][ref_seed])
                # print('new seed = ',old_value+delta)
                # print('span remaining',skip_span)
                
                
            # print(mapping)
            if mapping[-1] < min_location_p2:
                min_location_p2 = mapping[-1]
                
            # print('skip @ end', skip_span)
            seed = seed + skip_span
            
    
    
    # # print(seed_range[0::2])
    # # print(seed_range[1::2])
    # # seed_start = seed_range
    
    # # seed_list_p2 = almanac[0].split()[1:]


    # min_location_p2 = 0

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
