

def read_file(filename):
    grid = []
    # open filename in read mode
    with open(filename, 'r') as f:
        # read one line at a time 
        for line in f:
            line = line.strip()
            if len(line) > 0:
                row = [int(i) for i in line]
                grid.append(row)
    return grid

def next_step(grid, cell_dict, num):
    new_cell_dict = {}
    for cell, trail_set in cell_dict.items():
        row, col = cell
        for i in range(-1, 2):
            for j in range(-1, 2):
                if abs(i) == abs(j):
                    continue
                new_row = row + i
                new_col = col + j
                if new_row < 0 or new_row >= len(grid):
                    continue
                if new_col < 0 or new_col >= len(grid[0]):
                    continue
                if grid[new_row][new_col] == num:
                    new_cell = (new_row, new_col)
                    if new_cell not in new_cell_dict:
                        new_cell_dict[new_cell] = set()
                    new_cell_dict[new_cell] = new_cell_dict[new_cell].union(trail_set)
    return new_cell_dict

def compute_score(grid):
    cell_dict = {}
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell == 9:
                key = (row_idx, col_idx)
                cell_dict[key] = set([key])

    for next_num in range(8, -1, -1):
        #print(cell_dict)
        next_dict = next_step(grid, cell_dict, next_num)
        cell_dict = next_dict
    
    #print(cell_dict)
    score = 0
    for key, trail_set in cell_dict.items():
        score += len(trail_set)
    return score

def next_step_part2(grid, cell_dict, num):
    new_cell_dict = {}
    for cell, count in cell_dict.items():
        row, col = cell
        for i in range(-1, 2):
            for j in range(-1, 2):
                if abs(i) == abs(j):
                    continue
                new_row = row + i
                new_col = col + j
                if new_row < 0 or new_row >= len(grid):
                    continue
                if new_col < 0 or new_col >= len(grid[0]):
                    continue
                if grid[new_row][new_col] == num:
                    new_cell = (new_row, new_col)
                    if new_cell not in new_cell_dict:
                        new_cell_dict[new_cell] = 0
                    new_cell_dict[new_cell] += count
    return new_cell_dict

def compute_score_part2(grid):
    cell_dict = {}
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell == 9:
                cell_key = (row_idx, col_idx)
                cell_dict[cell_key] = 1

    for next_num in range(8, -1, -1):
        #print(cell_dict)
        next_dict = next_step_part2(grid, cell_dict, next_num)
        cell_dict = next_dict
    
    #print(cell_dict)
    score = 0
    for _, count in cell_dict.items():
        score += count
    return score


def test_read_file():
    grid = read_file('day10_sample.txt')
    assert len(grid) == 8
    assert len(grid[0]) == 8
    assert grid[0][0] == 8
    assert grid[1][2] == 1

def test_compute_score():
    assert compute_score(read_file('day10_sample.txt')) == 36
    assert compute_score_part2(read_file('day10_sample.txt')) == 81


if __name__ == '__main__':
    print("Part1")
    print('  Sample :', compute_score(read_file('day10_sample.txt')))
    print('  input  :', compute_score(read_file('day10_input.txt')))
    print('')
    print("Part2")
    print('  Sample :', compute_score_part2(read_file('day10_sample.txt')))
    print('  input  :', compute_score_part2(read_file('day10_input.txt')))