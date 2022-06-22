#!/usr/bin/env python3

from math import sqrt, floor

def jump_search(sorted_list: list[int], target: int) -> int:
    
    start = 0
    index = 0
    interval = floor(sqrt(len(sorted_list)))
    
    while index < len(sorted_list):
        if sorted_list[index] < target:
            start = index
        elif sorted_list[index] == target:
            return index
        elif sorted_list[index] > target:
            break

        index += interval

    index = start
    while index < len(sorted_list):
        if sorted_list[index] == target:
            return index
        index += 1
    
    return -1


sorted_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 256, 450]
res = jump_search(sorted_list, 256)
print(res)