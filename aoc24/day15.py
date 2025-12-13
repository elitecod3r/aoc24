import re
from math import gcd

# Values for the grid 
ROBOT = '@'
BOX = 'O'
WALL = '#'
EMPTY = '.'


def read_file(filename):
    grid = []
    moves = ''
    reading_grid = True

    with open(filename, 'r') as f:
        for line in f:
            if reading_grid:
                if line == '\n':
                    reading_grid = False
                    continue
                grid.append(list(line.strip()))
            else:
                moves += line.strip()

    return grid, moves

def find_robot(grid):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == ROBOT:
                return i, j
    return None

def test_read_file():
    grid, moves = read_file('day15_sample1.txt')
    assert len(grid) == 8
    assert len(grid[0]) == 8
    assert grid[2][2] == '@'
    assert find_robot(grid) == (2, 2)

    assert len(moves) == 15 
    assert moves[14] == '<'
    
def print_grid(grid):
    for row in grid:
        print(''.join(row))


def move_robot(grid, row, col, direction):
    assert grid[row][col] == ROBOT, f'Invalid robot position {row}, {col}' 

    d_row, d_col = 0, 0 
    if direction == '^':
        d_row = -1
    elif direction == 'v':
        d_row = 1
    elif direction == '<':
        d_col = -1
    elif direction == '>':
        d_col = 1
    else:
        raise ValueError(f'Invalid direction {direction}')

    f_row, f_col = row, col 
    while True:
        if grid[f_row][f_col] in [WALL, EMPTY]:
            break
        f_row += d_row
        f_col += d_col

    if grid[f_row][f_col] == EMPTY:
        while f_row != row or f_col != col:
            grid[f_row][f_col] = grid[f_row-d_row][f_col-d_col]
            f_row -= d_row
            f_col -= d_col
        assert f_row == row and f_col == col
        grid[row][col] = EMPTY
        return row + d_row, col + d_col

    elif grid[f_row][f_col] == WALL:
        return row, col
    else:
        raise ValueError(f'Unexpected grid value {grid[f_row][f_col]}')

def make_all_moves(grid, moves):
    row, col = find_robot(grid)
    for move in moves:
        row, col = move_robot(grid, row, col, move)
    return grid


def calculate_gps_sum(grid):
    score = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == BOX:
                score += 100*r + c 
    return score 


if __name__ == '__main__':
    print('Part 1')

    grid, moves = read_file('day15_sample1.txt')
    grid = make_all_moves(grid, moves)
    print_grid(grid)
    print('Sample1 : score =', calculate_gps_sum(grid))

    grid, moves = read_file('day15_sample2.txt')
    print('Sample2 : score =', calculate_gps_sum(make_all_moves(grid, moves)))

    grid, moves = read_file('day15_input.txt')
    print('Input   : score =', calculate_gps_sum(make_all_moves(grid, moves)))

