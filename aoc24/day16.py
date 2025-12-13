# Values for the grid 
START = 'S'
END = 'E'
WALL = '#'
EMPTY = '.'

def read_file(filename):
    grid = []
    with open(filename, 'r') as f:
        for line in f:
            if line == '\n':
                continue
            grid.append(list(line.strip()))
    return grid

def print_grid(grid):
    for row in grid:
        for cell in row:
            print(cell, end='')
    print()

def find_path(grid):
    # make a deep copy of the grid
    grid = [row[:] for row in grid]

    # Prepare the grid 
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell == WALL:
                continue
            if cell == START:
                start_row, start_col = row_index, col_index
                grid[row_index][col_index] = {'N': 0, 'S': 0, 'E': 0, 'W': 0}
                continue
            if cell == END:
                end_row, end_col = row_index, col_index
            grid[row_index][col_index] = {'N':1000000000000, 'S':1000000000000, 'E':1000000000000, 'W':1000000000000}

    cell_stack = [(start_row, start_col, 'E', 0)]
    while cell_stack:
        row, col, direction, score = cell_stack.pop()
        if grid[row][col] == WALL:
            continue
        if grid[row][col][direction] < score:
            continue
        grid[row][col][direction] = score
        if direction in ['N', 'S']:
            cell_stack.append((row, col+1, 'E', score + 1001))
            cell_stack.append((row, col-1, 'W', score + 1001))
            if direction == 'N':
                cell_stack.append((row-1, col, 'N', score + 1))
            else:
                cell_stack.append((row+1, col, 'S', score + 1))
        if direction in ['E', 'W']:
            cell_stack.append((row+1, col, 'S', score + 1001))
            cell_stack.append((row-1, col, 'N', score + 1001))
            if direction == 'E':
                cell_stack.append((row, col+1, 'E', score + 1))
            else:
                cell_stack.append((row, col-1, 'W', score + 1))

    return min(grid[end_row][end_col].values())

def test_find_path():
    assert find_path(read_file('day16_sample1.txt')) == 7036
    assert find_path(read_file('day16_sample2.txt')) == 11048

if __name__ == '__main__':
    print('Part 1')
    print(find_path(read_file('day16_input.txt')))
    # Got answer 133588 by incrasing recursion limit but the answer is too big. 
