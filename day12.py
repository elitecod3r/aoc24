import copy
import time
import itertools

def print_grid(grid):
    for row in grid:
        string = ''.join(row)
        print(string)
        

def read_file(filename):
    grid = []
    with open(filename, 'r') as f:
        # read one line at a time 
        for line in f:
            line = line.strip()
            if line == '':
                continue
            l = list(line)
            grid.append(l)
    return grid

def create_visited_grid(grid):
    visited = []
    for row in grid:
        visited.append([False] * len(row))
    return visited  

def test_read_file():
    grid = read_file('day12_sample1.txt')
    assert len(grid) == 4 
    assert len(grid[0]) == 4 
    assert grid[0][0] == 'A'
    assert grid[3][3] == 'C'

def get_cell(grid, row, col):
    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
        return ''
    return grid[row][col]

def compute_island(grid, visited, row, col):
    # Do a spread fill starting from the row, col and mark the cells as visited 
    #   returns the area and perimeter
    if visited[row][col]:
        return (0,0)
    val = get_cell(grid, row, col)
    visited[row][col] = True
    
    area = 1
    perimeter = 0
    for row_delta, col_delta in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        n_row = row + row_delta
        n_col = col + col_delta
        if get_cell(grid, n_row, n_col) == val:
            a, p = compute_island(grid, visited, n_row, n_col)
            area += a
            perimeter += p
        else:
            perimeter += 1

    return area, perimeter

def test_compute_island():
    grid = read_file('day12_sample1.txt')
    visited = create_visited_grid(grid)
    assert compute_island(grid, visited, 0, 0) == (4, 10)
    assert compute_island(grid, visited, 0, 0) == (0, 0)
    assert compute_island(grid, visited, 1, 0) == (4, 8)
    assert compute_island(grid, visited, 3, 1) == (3, 8)
    assert compute_island(grid, visited, 2, 2) == (4, 10)

    grid = read_file('day12_sample2.txt')
    visited = create_visited_grid(grid)
    assert compute_island(grid, visited, 1, 0) == (21, 36)
    assert compute_island(grid, visited, 1, 1) == (1, 4)
    assert compute_island(grid, visited, 3, 3) == (1, 4)



def compute_score(grid):
    visited = create_visited_grid(grid)
    score = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if not visited[row][col]:
                area, perimeter = compute_island(grid, visited, row, col)
                score += area * perimeter
    return score

def test_compute_score():
    grid = read_file('day12_sample1.txt')
    assert compute_score(grid) == 140
    grid = read_file('day12_sample2.txt')
    assert compute_score(grid) == 772
    grid = read_file('day12_sample3.txt')
    assert compute_score(grid) == 1930


if __name__ == '__main__':
    print(compute_score(read_file('day12_input.txt')))