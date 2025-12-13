import re
from math import gcd

def read_file(filename):
    robot_set = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip() == '':
                continue
            match = re.search(r'p\=(-?\d+),(-?\d+) v\=(-?\d+),(-?\d+)', line)
            assert match, 'Unexpected line input'
            position = (int(match.group(1)), int(match.group(2)))
            velocity = (int(match.group(3)), int(match.group(4)))
            robot_set.append((position, velocity))
    return robot_set

def test_read_file():
    robot_set = read_file('day14_sample.txt')
    assert len(robot_set) == 12
    assert robot_set[4] == ((0, 0), (1, 3))
    assert robot_set[11] == ((9, 5), (-3, -3))

def move_robots(robot_set, num_moves, rows, cols):
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for position, velocity in robot_set:
        pos_x, pos_y = position
        vel_x, vel_y = velocity
        pos_x = (pos_x + vel_x * num_moves) % cols
        pos_y = (pos_y + vel_y * num_moves) % rows
        grid[pos_y][pos_x] += 1
    return grid

def move_robot_and_update(grid, robot_set):
    rows = len(grid)
    cols = len(grid[0])
    
    for robot_index, robot_val in enumerate(robot_set):
        position, velocity = robot_val
        pos_x, pos_y = position
        vel_x, vel_y = velocity

        grid[pos_y][pos_x] -= 1
        pos_x = (pos_x + vel_x) % cols 
        pos_y = (pos_y + vel_y) % rows 
        grid[pos_y][pos_x] += 1
        robot_set[robot_index] = ((pos_x, pos_y), (vel_x, vel_y))


def find_line(grid):
    for row in grid:
        count = 0 
        for cell in row:
            if cell > 0:
                count += 1
            else:
                count = 0
            if count > 8:
                return True
    return False


def move_robots2(robot_set, num_moves, rows, cols):
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for position, velocity in robot_set:
        pos_x, pos_y = position
        grid[pos_y][pos_x] += 1
    for move_num in range(1,num_moves+1):
        move_robot_and_update(grid, robot_set)
        if find_line(grid):
            print('\nMove:', move_num)
            print_grid(grid)
    return grid


def print_grid(grid):
    for row in grid:
        for cell in row:
            if cell == 0:
                print('.', end='')
            else:
                print(cell, end='')
        print()

def safety_factor(grid):
    mid_row = len(grid) // 2
    mid_col = len(grid[0]) // 2

    top_left_quad = [[cell for cell in row[:mid_col]] for row in grid[:mid_row]]
    #print_grid(top_left_quad)
    top_left_score = sum(sum(row) for row in top_left_quad)

    top_right_quad = [[cell for cell in row[mid_col+1:]] for row in grid[:mid_row]]
    top_right_score = sum(sum(row) for row in top_right_quad)

    bot_left_quad = [[cell for cell in row[:mid_col]] for row in grid[mid_row+1:]]
    bot_left_score = sum(sum(row) for row in bot_left_quad)

    bot_right_quad = [[cell for cell in row[mid_col+1:]] for row in grid[mid_row+1:]]
    bot_right_score = sum(sum(row) for row in bot_right_quad)   

    return top_left_score * top_right_score * bot_left_score * bot_right_score

def test_safety_factor():
    # This will test the whole program
    grid = move_robots(read_file('day14_sample.txt'), 100, 7, 11)
    assert safety_factor(grid) == 12


if __name__ == '__main__':
    print('Part 1')

    grid = move_robots(read_file('day14_sample.txt'), 100, 7, 11)
    print('Sample :', safety_factor(grid))

    grid = move_robots(read_file('day14_input.txt'), 100, 103 , 101)
    print('Input  :', safety_factor(grid))
    # 223432704 is too low.. First gues.. 

    move_robots2(read_file('day14_input.txt'), 10000, 103 , 101)