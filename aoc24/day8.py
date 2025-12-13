import copy
import time
import itertools

def print_grid(grid):
    print('  ', end='')
    for col_idx in range(len(grid[0])):
        print(f'{col_idx%10}', end='')
    print('')

    for row_idx, row in enumerate(grid):
        string = ''.join([f"{num}" for num in row])
        print(f'{row_idx%10} {string}')

# read until end of file
def read_file(filename):
    grid = []

    with open(filename, 'r') as f:
        # read one line at a time 
        for line in f:
            line = line.strip()
            l = list(line)
            grid.append(l)
    return grid

def is_node_in_grid(node, grid):
    row, col = node
    if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[0]):
        return False
    return True

def find_antidotes_p1(node1, node2, grid):
    row1, col1 = node1
    row2, col2 = node2
    delta_row = row2 - row1
    delta_col = col2 - col1
    row0 = row1 - delta_row
    col0 = col1 - delta_col
    row3 = row2 + delta_row
    col3 = col2 + delta_col
    node_list = []
    if is_node_in_grid((row0, col0), grid):
        node_list.append((row0, col0))
    if is_node_in_grid((row3, col3), grid):
        node_list.append((row3, col3))
    return node_list
        
def find_antidotes_p2(node1, node2, grid):
    row1, col1 = node1
    row2, col2 = node2
    delta_row = row2 - row1
    delta_col = col2 - col1

    node_list = []
    while is_node_in_grid((row1, col1), grid):
        node_list.append((row1, col1))
        row1 -= delta_row
        col1 -= delta_col
    while is_node_in_grid((row2, col2), grid):
        node_list.append((row2, col2)) 
        row2 += delta_row
        col2 += delta_col
    return node_list


def test_find_antidotes():
    grid = read_file('day8_sample.txt')
    n1 = (4,5)
    n2 = (6,8)

    n0, n3 = find_antidotes_p1(n2, n1, grid)
    assert n3 == (2, 2)
    assert n0 == (8, 11)

    n0, n3 = find_antidotes_p1(n1, n2, grid)
    assert n0 == (2, 2)
    assert n3 == (8, 11)

    node_list = find_antidotes_p2(n1, n2, grid)
    #print(node_list)
    assert node_list == [n1, n0, n2, n3]

def total_antidotes(input_grid):
    freq_map = {}
    for row_idx, row in enumerate(input_grid):
        for col_idx, col in enumerate(row):
            if col == '.':
                continue
            if col not in freq_map:
                freq_map[col] = []
            freq_map[col].append((row_idx, col_idx))
    
    grid1 = copy.deepcopy(input_grid)
    count1 = 0
    for freq, node_list in freq_map.items():
        for n1, n2 in itertools.product(node_list,repeat=2):
            if n1 == n2:
                continue
            node_list = find_antidotes_p1(n1, n2, grid1)
            for row, col in node_list:
                if grid1[row][col] != '#':
                    grid1[row][col] = '#'
                    count1 += 1

    grid2 = copy.deepcopy(input_grid)
    count2 = 0
    for freq, node_list in freq_map.items():
        for n1, n2 in itertools.product(node_list,repeat=2):
            if n1 == n2:
                continue
            node_list = find_antidotes_p2(n1, n2, grid2)
            for row, col in node_list:
                if grid2[row][col] != '#':
                    grid2[row][col] = '#'
                    count2 += 1

    
    return count1, count2

def test_total_antidotes():
    grid = read_file('day8_sample.txt')
    #print_grid(grid)
    assert total_antidotes(grid) == (14, 34)
    #print_grid(grid)


if __name__ == '__main__':
    #test_target_possible()
    print('Sample - Part1, Part2 = ', total_antidotes(read_file('day8_sample.txt')))
    print('Input  - Part1, Part2 = ', total_antidotes(read_file('day8_input.txt')))