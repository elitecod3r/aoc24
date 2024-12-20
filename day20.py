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

MAX_PATH = 1000000000000
def find_path(in_grid):
    # make a deep copy of the grid
    grid = [row[:] for row in in_grid]

    # Prepare the grid 
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell == WALL:
                continue

            grid[row_index][col_index] = {}
            if cell == START:
                start_row, start_col = row_index, col_index
                grid[row_index][col_index]['start'] = 0 
                grid[row_index][col_index]['end'] = MAX_PATH
                continue
            elif cell == END:
                end_row, end_col = row_index, col_index
                grid[row_index][col_index]['start'] = MAX_PATH
                grid[row_index][col_index]['end'] = 0
            else:
                assert cell == EMPTY
                grid[row_index][col_index]['start'] = MAX_PATH
                grid[row_index][col_index]['end'] = MAX_PATH

    cell_stack = []
    cell_stack.append((end_row, end_col, 'end', 0))
    cell_stack.append((start_row, start_col, 'start', 0))
    # stack contains the score with which we can enter a cell 
    while cell_stack:
        row, col, dir, score = cell_stack.pop()
        if grid[row][col] == WALL:
            continue
        if grid[row][col][dir] < score:
            continue
        grid[row][col][dir] = score
        cell_stack.append((row, col+1, dir, score + 1))
        cell_stack.append((row, col-1, dir, score + 1))
        cell_stack.append((row+1, col, dir, score + 1))
        cell_stack.append((row-1, col, dir, score + 1))
    
    #print('start cell :', grid[start_row][start_col])
    #print('end cell   :', grid[end_row][end_col])

    return grid, start_row, start_col, end_row, end_col

def find_new_path(grid, curr_row, curr_col, delta_row, delta_col):
    row = curr_row + delta_row
    col = curr_col + delta_col
    if row < 0 or col < 0:
        return MAX_PATH
    if row >= len(grid) or col >= len(grid[0]):
        return MAX_PATH
    if grid[row][col] == WALL:
        return MAX_PATH
    return grid[curr_row][curr_col]['start'] + grid[row][col]['end'] + 2 

def find_cheats(in_grid, min_saving):
    grid, start_row, start_col, end_row, end_col  = find_path(in_grid)
    min_path = grid[start_row][start_col]['end']
    paths = 0
    
    # Grid below shows how cheat can help go from a cell to 8 new locations.
    #    +/- 2*row, +/- 2*col, (+/-1 row and +/-1 col)
    ###.###
    ##.#.##
    #.#*#.#
    ##.#.##
    ###.###
    cheat_deltas = [(2, 0), (-2, 0), (0, 2), (0, -2), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell == WALL:
                continue
            for cheat_row, cheat_col in cheat_deltas:
                new_path = find_new_path(grid, row_index, col_index, cheat_row, cheat_col)
                if new_path <= min_path - min_saving:
                    #print(f'-new path: ({row_index},{col_index}) -> ({row_index+cheat_row}, {col_index+cheat_col}) = {new_path}')
                    paths += 1
    return paths



def test_find_cheats():
    grid = read_file('day20_sample.txt')
    #print_grid(grid)
    path_grid = find_path(grid)
    assert find_cheats(grid, 60) == 1
    assert find_cheats(grid, 1) == 44

if __name__ == '__main__':
    print('Part 1')
    grid = read_file('day20_input.txt')
    path_grid = find_path(grid)
    print('cheats :', find_cheats(grid, 100))
