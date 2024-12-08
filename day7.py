import copy
import time
import itertools

# read until end of file
def read_file(filename):

    input_data = []

    with open(filename, 'r') as f:
        # read one line at a time 
        for line in f:
            line = line.strip()
            target, num_list = line.split(':')
            target = int(target)
            num_list = [int(num) for num in num_list.split()]
            input_data.append((target, num_list))
            
    return input_data

def test_read_file():
    input_data = read_file("day7_sample.txt")
    assert input_data[0] == (190, [10,19])
    assert input_data[8] == (292, [11, 6,16,20])

def eval_ops(num_list, op_list):
    total = num_list[0]
    for idx, op in enumerate(op_list):
        if op == '+':
            total = total + num_list[idx+1]
        else:
            total = total * num_list[idx+1]
    return total

def target_possible(target, num_list):
    l = len(num_list) - 1

    operations = ['+', '*']
    for op_list in itertools.product(operations, repeat=l):
        if eval_ops(num_list, op_list) == target:
            return True
    return False

    if len(num_list) == 1:
        return target == num

    # Check if we can use a plus sign 
    if target >= num:
        if target_possible(target - num, num_list[1:]):
            return True

    # if we are here plus sign didn't work out. Let's try product sign 
    print('   trying out products', target, num)
    new_target = target // num
    if new_target * num != target:
        return False
    print('   not fractional ')
    
    return target_possible(new_target, num_list[1:])

def test_target_possible():
    assert target_possible(3267, [81, 40, 27]) == True
    assert target_possible(292, [11, 6, 16, 20]) == True
    assert target_possible(156, [15, 6]) == False


def total_of_possible_targets(filename):
    input_data = read_file(filename)
    total = 0
    for target, num_list in input_data:
        if target_possible(target, num_list):
            #print('Target:', target, 'is possible with', num_list)
            total += target
    return total
        


if __name__ == '__main__':
    test_read_file()
    test_target_possible()
    print(total_of_possible_targets("day7_sample.txt"))
    print(total_of_possible_targets("day7_input.txt"))