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
        elif op == '*':
            total = total * num_list[idx+1]
        elif op == '||':
            total = int(str(total) + str(num_list[idx+1]))
        else:
            assert False, 'Invalid operation'
            
    return total

def target_possible(target, num_list, operations):
    l = len(num_list) - 1

    for op_list in itertools.product(operations, repeat=l):
        if eval_ops(num_list, op_list) == target:
            return True
    return False


def test_target_possible():
    operations = ['+', '*']
    assert target_possible(3267, [81, 40, 27], operations) == True
    assert target_possible(292, [11, 6, 16, 20], operations) == True
    assert target_possible(156, [15, 6], operations) == False


def total_of_possible_targets(filename, operations):
    input_data = read_file(filename)
    total = 0
    for target, num_list in input_data:
        if target_possible(target, num_list, operations):
            #print('Target:', target, 'is possible with', num_list)
            total += target
    return total
        


if __name__ == '__main__':
    #test_read_file()
    #test_target_possible()
    p1_operations = ['+', '*']
    print('Part1 - Sample ', total_of_possible_targets("day7_sample.txt", p1_operations))
    print('Part1 - Input  ', total_of_possible_targets("day7_input.txt", p1_operations))

    p2_operations = ['+', '*', '||']
    print('Part1 - Sample ', total_of_possible_targets("day7_sample.txt", p2_operations))
    print('Part1 - Input  ', total_of_possible_targets("day7_input.txt", p2_operations))