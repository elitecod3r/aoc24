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
    # If update matches the order list, return (True, middle_value), 
    # else return (False, 0)
    update_dict = {}
    for idx, val in enumerate(update):
        update_dict[val] = idx

    for a, b_list in order_dict.items():
        for b in b_list:
            if a in update_dict and b in update_dict and update_dict[a] > update_dict[b]:
                return False, 0

    mid_index = len(update) // 2
    return True, update[mid_index]


def test_check_update():
    order_dict, update_list = read_file("day5_sample.txt")
    assert check_update(order_dict, update_list[0]) == (True, 61)
    assert check_update(order_dict, update_list[1]) == (True, 53)
    assert check_update(order_dict, update_list[2]) == (True, 29)
    assert check_update(order_dict, update_list[3]) == (False , 0)
    assert check_update(order_dict, update_list[4]) == (False, 0)
    assert check_update(order_dict, update_list[5]) == (False, 0)


def part1(filename):
    order_dict, update_list = read_file(filename)
    total = 0
    for update in update_list:
        status, mid_value = check_update(order_dict, update)
        if status:
            total += mid_value
    return total

def test_part1():
    assert part1("day5_sample.txt") == 143
    assert part1("day5_input.txt") == 5452


if __name__ == '__main__':
    test_read_file()
    print("Part1 = ", part1("day5_input.txt"))
