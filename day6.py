from collections import Counter
import sys


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
    for row in grid:
        string = ''.join(map(str, row))
        print(string)

def move_player(grid, prow, pcol, pdir):
    count = 1 
    grid[prow][pcol] = 2

    while True:
        if pdir == 'up':
            prow -= 1
        elif pdir == 'down':
            prow += 1  
        elif pdir == 'left':
            pcol -= 1
        elif pdir == 'right':   
            pcol += 1

        
        if prow < 0 or prow >= len(grid) or pcol < 0 or pcol >= len(grid[0]):
            break

        if grid[prow][pcol] == 1:  
            # we hit a wall. First back off the move operation and then turn right
            if pdir == 'up':
                prow += 1
                pdir = 'right'
            elif pdir == 'down':
                prow -= 1  
                pdir = 'left'
            elif pdir == 'left':
                pcol += 1
                pdir = 'up'
            elif pdir == 'right':   
                pcol -= 1
                pdir = 'down'
            #print(f'Turned {pdir} at {prow},{pcol}  count = {count}')
            #print_grid(grid)

        if grid[prow][pcol] == 0:
            grid[prow][pcol] = 2
            count += 1

    return count
    

if __name__ == '__main__':
    count = move_player(*read_file("day6_sample.txt"))
    print(count)

    count = move_player(*read_file("day6_input.txt"))
    print(count)


