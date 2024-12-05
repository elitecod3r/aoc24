from collections import Counter
import sys

# read until end of file
def read_file(filename):
    reading_order_rules = True 
    update_list = []
    order_dict = {}
    
    # open filename in read mode
    with open(filename, 'r') as f:
        # read one line at a time 
        for line in f:
            if line == '\n':
                reading_order_rules = False
                continue
            if reading_order_rules:
                order = [int(i) for i in line.strip().split("|")]
                a, b = order
                if a in order_dict:
                    order_dict[a].append(b)
                else:
                    order_dict[a] = [b]

            else:
                update = [int(i) for i in line.strip().split(",")]
                update_list.append(update)
    return order_dict, update_list

def test_read_file():
    order_dict, update_list = read_file("day5_sample.txt")
    assert len(order_dict) == 6
    assert len(update_list) == 6
    assert order_dict[29] == [13]
    assert update_list[2] == [75, 29, 13]

# Run this test to make sure the test data matches my assumptions
def test_sanity():
    order_dict, update_list = read_file("day5_input.txt")
    print(len(order_dict))
    print(len(update_list))
    for l in update_list:
        assert len(l) % 2 == 1, "Found entry with even number of elements"
        s = set(l)
        assert len(s) == len(l), "Found duplicate in the update list"
    print("Sanity Check Passed")


def check_update(order_dict, update):
    # return (flag, mid_value)
    # if update matches the order, return True, mid_value 
    # else return False, mid_value after fixing the update list
    #
    update_dict = {}
    for idx, val in enumerate(update):
        update_dict[val] = idx

    correct_order = True

    for a, b_list in order_dict.items():
        if a not in update_dict:
            continue 
        
        min_b_index = sys.maxsize
        for b in b_list:
            if b in update_dict:
                min_b_index = min(min_b_index, update_dict[b])

        if min_b_index == sys.maxsize: # no b in the update list
            continue
        
        a_index = update_dict[a]
        if a_index > min_b_index:
            correct_order = False
            # fix the update list
            update = update[:min_b_index] + [a] + update[min_b_index:a_index] + update[a_index+1:]
            #print("inside this loop", correct_order, update)
            break
        
    mid_index = len(update) // 2
    mid_value = update[mid_index]
    # Recursively try to fix the issue again
    if not correct_order:
        flag, mid_value = check_update(order_dict, update)

    mid_index = len(update) // 2
    return correct_order, mid_value


def test_check_update():
    order_dict, update_list = read_file("day5_sample.txt")
    assert check_update(order_dict, update_list[0]) == (True, 61)
    assert check_update(order_dict, update_list[1]) == (True, 53)
    assert check_update(order_dict, update_list[2]) == (True, 29)
    assert check_update(order_dict, update_list[3]) == (False, 47)
    assert check_update(order_dict, update_list[4]) == (False, 29)
    assert check_update(order_dict, update_list[5]) == (False, 47)


def find_answer(filename):
    order_dict, update_list = read_file(filename)
    part1_total = 0
    part2_total = 0
    for update in update_list:
        status, mid_value = check_update(order_dict, update)
        if status:
            part1_total += mid_value
        else:
            part2_total += mid_value

    return part1_total, part2_total 

def test_find_answer():
    assert find_answer("day5_sample.txt") == (143, 123)
    assert find_answer("day5_input.txt") == (5452, 4598)


if __name__ == '__main__':
    test_check_update()
    print("Part1, Part2 = ", find_answer("day5_input.txt"))
