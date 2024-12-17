import re
from math import gcd
import sys
import resource

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

def recurse_path(grid, row, col, direction, score):
    # Entering the 'curr' cell with direction 'direction' and score 'score'
    #print(row, col, direction, score, grid[row][col], end='')
    if grid[row][col] == WALL:
        #print(' hit a wall')
        return
    if grid[row][col] < score:   # new path is longer. return
        #print(' lower score ')
        return
    #print(' processing ')
    grid[row][col] = score

    if direction in ['N', 'S']:
        if direction == 'N':
            recurse_path(grid, row-1, col, 'N', score + 1)
        else:
            recurse_path(grid, row+1, col, 'S', score + 1)
        recurse_path(grid, row, col+1, 'E', score + 1001)
        recurse_path(grid, row, col-1, 'W', score + 1001)
    if direction in ['E', 'W']:
        if direction == 'E':
            recurse_path(grid, row, col+1, 'E', score + 1)
        else:
            recurse_path(grid, row, col-1, 'W', score + 1)
        recurse_path(grid, row+1, col, 'S', score + 1001)
        recurse_path(grid, row-1, col, 'N', score + 1001)

    return

def find_path(grid):
    # make a deep copy of the grid
    grid = [row[:] for row in grid]

    # Prepare the grid 
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell == START:
                start_row, start_col = row_index, col_index
                grid[row_index][col_index] = 0
            elif cell == END:
                end_row, end_col = row_index, col_index
                grid[row_index][col_index] = 1000000000000
            elif cell == EMPTY:
                grid[row_index][col_index] = 1000000000000

    recurse_path(grid, start_row, start_col, 'E', 0)
    return grid[end_row][end_col]



if __name__ == '__main__':
    #resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
    sys.setrecursionlimit(10**6)

    print('Part 1')
    print(find_path(read_file('day16_sample1.txt')))
    print(find_path(read_file('day16_sample2.txt')))
    print(find_path(read_file('day16_input.txt')))
    # Got answer 133588 by incrasing recursion limit but the answer is too big. 
