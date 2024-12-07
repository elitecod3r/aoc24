import copy

# read until end of file
def read_file(filename):

    player_row = -1
    player_col = -1
    player_direction = ""
    grid = []
    direction_map = {
        '^': 'up',
        'v': 'down',
        '<': 'left',
        '>': 'right'
    }

    with open(filename, 'r') as f:
        # read one line at a time 
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            
            temp_row = []
            for c in line:
                if c == '.':
                    temp_row.append(0)
                elif c == '#':
                    temp_row.append(1)
                elif c in direction_map:
                    temp_row.append(0)
                    player_row = len(grid)
                    player_col = len(temp_row) - 1
                    player_direction = direction_map[c]

            grid.append(temp_row)
        return grid, player_row, player_col, player_direction       
                
        
def test_read_file():
    grid, prow, pcol, pdir = read_file("day6_sample.txt")
    assert len(grid) == 10
    assert len(grid[0]) == 10
    assert grid[0][0] == 0
    assert grid[0][4] == 1
    assert prow == 6
    assert pcol == 4
    assert grid[prow][pcol] == 0    
    assert pdir == 'up'

    grid, prow, pcol, pdir = read_file("day6_input.txt")
    assert len(grid) == 130
    assert len(grid[0]) == 130
    assert prow == 71
    assert pcol == 48
    assert grid[prow][pcol] == 0    
    assert pdir == 'up'

def print_grid(grid):
    print('   ', end='')
    for col_idx in range(len(grid[0])):
        print(f'{col_idx: >2}', end='')
    print('')

    for row_idx, row in enumerate(grid):
        string = ''.join([f"{num: >2}" for num in row])
        print(f'{row_idx:>2} {string}')

def move_player(grid, prow, pcol, pdir, obstacle_added=0):
    # Returns (number_of_cells_visited, )
    # Returns distinct_positions, obstacle_count, loop_detected 
    #  distinct_positions: number of cells visited by the player until they 
    #       walk off the grid. 
    #  obstacle_count: number of obstacles we can place on the route to 
    #       place the user on the loop.
    #  loop_detected: if there is a loop without adding an obstacle. This is 
    #       used to compute obstacle count since initial grid is not expected
    #       have loop

    if obstacle_added > 1:
        # We can only place one obstacle. Return if we have alredy placed 
        #  2 or more obstacles. 
        return 0, 0, False     

    # bit mask for steps in different direction
    dir_map = { "up": 2, "down": 4, "left": 8, "right": 16 }
    # right_turn gives the next direciton if player takes a right turn
    right_turn = {"up": "right", "right": "down", "down": "left", "left": "up"}
    # next_setp gives the increments for row and col if player takes one more step
    next_step = {"up": (-1, 0), "down": (+1, 0), "right": (0, +1), "left": (0, -1)}
    
    obstacle_count = 0    
    distinct_positions = 1   # initial position is counted as already visited
    grid[prow][pcol] = grid[prow][pcol] | dir_map[pdir]
    loop_detected = False 

    while not loop_detected:
        if False and obstacle_added == 0:  # don't print in recursive calls
            print('\n')
            print(f'== Player is at {prow}, {pcol} facing {pdir} ==')
            print_grid(grid)

        # next_row, next_col are where we will move to next if there is no obstacle in front
        # next_dir is where we will turn if there is an obstacle in front
        row_incr, col_incr = next_step[pdir]
        next_row = prow + row_incr
        next_col = pcol + col_incr  
        next_dir = right_turn[pdir]

        # We are done if the player steps off the grid. 
        if next_row < 0 or next_row >= len(grid) or next_col < 0 or next_col >= len(grid[0]):
            break

        # if we have an obstacle in front, we will take a turn and continue on our path
        if grid[next_row][next_col] == 1:  
            # When we take a turn, we stay in current location but change direction
            pdir = next_dir
            if grid[prow][pcol] & dir_map[pdir]:
                loop_detected = True
            else:
                grid[prow][pcol] = grid[prow][pcol] | dir_map[pdir] 
            continue 

        # At this stage, the cell in front is empty. We will first check 
        # if we get a loop if we place an obstacle on the next step. 
        if True:
            new_grid = copy.deepcopy(grid)
            new_grid[next_row][next_col] = 1
            dp, oc, new_loop_detected = move_player(new_grid, prow, pcol, pdir, obstacle_added + 1)
            if new_loop_detected:
                obstacle_count += 1
                #print(f'** found loop at {next_row}, {next_col} **')
        
        # We will now move to the next cell. Advance row/col but pdir stays the same
        prow = next_row
        pcol = next_col

        if grid[prow][pcol] == 0:
            distinct_positions += 1
            print(distinct_positions)

        if grid[prow][pcol] & dir_map[pdir]:
            loop_detected = True
        else:
            grid[prow][pcol] = grid[prow][pcol] | dir_map[pdir] 

    return distinct_positions, obstacle_count, loop_detected

def test_move_player():
    distinct_positions, obstacle_count, loop_detected = move_player(*read_file("day6_sample.txt"))
    assert distinct_positions == 41
    assert obstacle_count == 6
    assert loop_detected == False

    distinct_positions, obstacle_count, loop_detected = move_player(*read_file("day6_input.txt"))
    assert distinct_positions == 858
    assert obstacle_count == 0
    assert loop_detected == False


if __name__ == '__main__':
    print(move_player(*read_file("day6_sample.txt")))
    print(move_player(*read_file("day6_input.txt")))



