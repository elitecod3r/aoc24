import re
# Values for the grid 

WALL  = -1
MAX_VAL = 1000000000

def read_bytes(filename):
    byte_array = []
    with open(filename, 'r') as f:
        for line in f:
            if line == '\n':
                continue
            match = re.search(r'(\d+),(\d+)', line)
            assert match, 'Unexpected line input'
            col, row  = int(match.group(1)), int(match.group(2))
            byte_array.append((row, col))
    return byte_array


def create_grid_with_border(num_lines, rows, cols, byte_array):
    # create a grid with border of wall added 
    grid = [[MAX_VAL for _ in range(cols+2)] for _ in range(rows+2)]  
    for row_idx in range(rows+2):
        for col_idx in range(cols+2):
            if row_idx == 0 or row_idx == rows+1:
                grid[row_idx][col_idx] = WALL
            if col_idx == 0 or col_idx == cols+1:
                grid[row_idx][col_idx] = WALL

    # add walls from the byte array
    for i in range(num_lines):
        row, col = byte_array[i]
        grid[row+1][col+1] = WALL
    return grid
        

def print_grid(grid):
    print()
    for row in grid:
        for cell in row:
            if cell == WALL:
                print('# ', end='')
            elif cell == MAX_VAL:
                print('. ', end='')
            else:
                print(cell, end='')
        print('')
    

def test_read_file():
    byte_array = read_bytes('day18_sample.txt')
    grid = create_grid_with_border(12, 7, 7, byte_array)
    assert len(grid) == 9
    assert len(grid[0]) == 9
    assert grid[1][1] == MAX_VAL
    assert grid[1][4] == WALL
    assert grid[2][6] == WALL
    assert grid[3][2] == MAX_VAL

def find_path3(rows, cols, filename, start_index):
    byte_array = read_bytes(filename)
    for idx in range(start_index, len(byte_array)):
        grid = create_grid_with_border(idx, rows, cols, byte_array)
        shortest_path = find_path(grid)
        print(f'Shortest path for {idx} = {shortest_path}')
        if shortest_path == MAX_VAL:
            return byte_array[idx-1]
    return byte_array[-1]

def find_path2(rows, cols, filename):
    byte_array = read_bytes(filename)
    upper = len(byte_array) -1
    lower = 0

    while upper >= lower: 
        mid = (upper + lower) // 2
        grid = create_grid_with_border(mid, rows, cols, byte_array)
        shortest_path = find_path(grid)
        #print(f'Shortest path for {mid} = {shortest_path}')
        if shortest_path == MAX_VAL:
            upper = mid - 1
        else:
            lower = mid + 1

    return byte_array[upper]

def find_path(grid):
    rows, cols = len(grid), len(grid[0])

    start_row, start_col = 1, 1
    end_row, end_col = rows-2, cols-2

    cell_stack = [(start_row, start_col, 0)]
    while cell_stack:
        row, col, score = cell_stack.pop()
        if grid[row][col] == WALL:
            continue
        if grid[row][col] <= score:
            continue
        assert grid[row][col] > score , 'Unexpected wall'
        grid[row][col] = score
    
        cell_stack.append((row, col+1, score + 1))
        cell_stack.append((row, col-1, score + 1))
        cell_stack.append((row+1, col, score + 1))
        cell_stack.append((row-1, col, score + 1))

    return grid[end_row][end_col]

def test_find_path():
    byte_array = read_bytes('day18_sample.txt')
    grid = create_grid_with_border(12, 7, 7, byte_array)
    assert find_path(grid) == 22

    assert find_path2(7, 7, 'day18_sample.txt') == (1,6)


if __name__ == '__main__':
    byte_array = read_bytes('day18_input.txt')
    grid = create_grid_with_border(1024, 71, 71, byte_array)
    print('Part 1 =', find_path(grid))

    row, col = find_path2(71, 71, 'day18_input.txt')
    print(f'Part 2 = {col},{row}') 
    #print(find_path3(71, 71, 'day18_input.txt', 2950))
