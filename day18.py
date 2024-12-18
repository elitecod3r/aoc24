import re
# Values for the grid 

WALL  = -1
MAX_VAL = 1000000000

def read_file(num_lines, rows, cols, filename):
    grid = [[MAX_VAL for _ in range(cols)] for _ in range(rows)]  
    lines_read = 0

    with open(filename, 'r') as f:
        for line in f:
            if line == '\n':
                continue
            match = re.search(r'(\d+),(\d+)', line)
            assert match, 'Unexpected line input'
            col, row  = int(match.group(1)), int(match.group(2))
            grid[row][col] = WALL
            lines_read += 1
            if lines_read == num_lines:
                break
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
    grid = read_file(12, 7, 7, 'day18_sample.txt')
    #print_grid(grid)
    assert len(grid) == 7
    assert len(grid[0]) == 7
    assert grid[0][0] == MAX_VAL
    assert grid[0][3] == WALL
    assert grid[1][5] == WALL
    assert grid[2][1] == MAX_VAL

    find_path(grid)


def find_path(in_grid):
    rows, cols = len(in_grid), len(in_grid[0])
    #print_grid(in_grid)

    grid = []
    # make a copy of the grid and add walls to the edge
    for row_idx in range(rows+2):
        row = []
        if row_idx == 0 or row_idx == rows+1:
            row = [WALL for _ in range(cols+2)]
        else:
            for col_idx in range(cols+2):
                if col_idx == 0 or col_idx == cols+1:
                    row.append(WALL)
                    continue
                row.append(in_grid[row_idx-1][col_idx-1])
        grid.append(row)
    #grid[1][1] = 0
    
    #print_grid(grid)
    counter = 0 

    start_row, start_col = 1, 1
    end_row, end_col = rows, cols
    cell_stack = [(start_row, start_col, 0)]
    while cell_stack:
        counter += 1
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


if __name__ == '__main__':
    print('Part 1')
    #print(find_path(read_file('day16_sample.txt')))
    #print(find_path(read_file(12, 7, 7, 'day18_sample.txt')))
    print(find_path(read_file(1024, 71, 71, 'day18_input.txt')))
    #print(find_path(read_file('day16_input.txt')))
    # Got answer 133588 by incrasing recursion limit but the answer is too big. 
