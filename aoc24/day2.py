
# 

from collections import Counter
from io import StringIO
import sys


# Return 1 if the list is safe, 0 otherwise
def is_safe(l):
    if len(l) <= 1:
        return 1

    positive = -1
    if l[0] < l[1]:
        positive = 1

    for i in range(1, len(l)):
        diff = (l[i] - l[i-1]) * positive
        if diff < 1 or diff > 3:
            return 0
    return 1

def is_safe_with_removal(l):
    if is_safe(l):
        return 1
    
    for i in range(0, len(l)):
        # remove element i from list
        new_l = l[:i] + l[i+1:]
        #print(f'safe = {is_safe(new_l)} new_l = {new_l}')
        if is_safe(new_l):
            return 1   
    return 0

assert(is_safe_with_removal([65,68,71,72,71]) == 1)   # can be made safe by removing last 71 

def test_is_safe():
    assert(is_safe([7,6,3,2,1]) == 1)   # safe
    assert(is_safe([1,3,6,7,9]) == 1)   # safe
    assert(is_safe([1,3,6,5,3]) == 0)   # up and down 
    assert(is_safe([1,2,6,8,9]) == 0)   # not safe coz diff of 4
    assert(is_safe([9,7,6,2,1]) == 0)   # not safe coz diff of 4
    assert(is_safe([8,6,4,4,1]) == 0)   # not safe coz diff of 0
    assert(is_safe([1,3,2,4,5]) == 0)   # can be made safe by removing 4 

def test_is_safe_with_removal():
    assert(is_safe_with_removal([7,6,3,2,1]) == 1)   # safe
    assert(is_safe_with_removal([1,3,6,7,9]) == 1)   # safe
    assert(is_safe_with_removal([1,3,6,5,3]) == 0)   # up and down 
    assert(is_safe_with_removal([1,2,6,8,9]) == 0)   # not safe coz diff of 4
    assert(is_safe_with_removal([9,7,6,2,1]) == 0)   # not safe coz diff of 4
    assert(is_safe_with_removal([8,6,4,4,1]) == 1)   # can be made safe by removing 4 
    assert(is_safe_with_removal([1,3,2,4,5]) == 1)   # can be made safe by removing 3 
    assert(is_safe_with_removal([65,68,71,72,71]) == 1)   # can be made safe by removing last 71 
    assert(is_safe_with_removal([65, 65,68,71,72,71]) == 0)   # not safe 
    assert(is_safe_with_removal([65, 65,68,71,72]) == 1)   # can be made safe by removing frist 65 


def count_safe(input_lists):
    safe_count = 0 
    for l in input_lists:
        safe_count += is_safe(l)
    return safe_count  

def count_safe_with_removal(input_lists):
    safe_count = 0 
    for l in input_lists:
        safe_count += is_safe_with_removal(l)
        #print(f'safe = {is_safe_with_removal(l)} -> {l}')
    return safe_count  

# read until end of file
def read_input(file_object):
    input_list = []
    while True:
        try:
            line = file_object.readline()
            if not line:
                break
            l = [int(a) for a in line.split()]
            input_list.append(l)
        except EOFError:
            break
    return input_list

# test case 
def sample_test():
    test_input = """\
        7 6 4 2 1
        1 2 7 8 9
        9 7 6 2 1
        1 3 2 4 5
        8 6 4 4 1
        1 3 6 7 9"""
    l = read_input(StringIO(test_input))
    assert(count_safe(l) == 2)
    assert(count_safe_with_removal(l) == 4)


test_is_safe()
test_is_safe_with_removal()
sample_test()


l = read_input(sys.stdin)
print(f'safe count = {count_safe(l)}')
print(f'safe count with removal = {count_safe_with_removal(l)}')
# Got 306 in first try but the answer was wrong -- too low. I wasn't testing by removing the first and the last element. That's a reminder to think more carefully about the boundary cases and also add more test cases. 